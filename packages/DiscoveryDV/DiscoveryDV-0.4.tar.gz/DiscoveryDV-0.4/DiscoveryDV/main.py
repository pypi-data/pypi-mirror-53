# --------------------------------------------------------------------------
# Company:      DecisionVis LLC
# Author:       Jayson Kempinger
# Created:      2019-05-17
# License:      MIT License
# --------------------------------------------------------------------------

import re
import time
from copy import deepcopy
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from argparse import ArgumentParser
from collections.abc import Sequence
from contextlib import AbstractContextManager

from zmq import Context
from zmq import Socket
from zmq import ZMQError
# noinspection PyUnresolvedReferences
from zmq import POLLIN, POLLOUT, REQ, SUB, SUBSCRIBE, NOBLOCK
from msgpack import packb
from msgpack import unpackb


# Types
Path = TypeVar('Path', bound=Tuple[Union[str, int], ...])
Value = TypeVar('Value', bound=Union['State', 'Collection', str, bool, int, float])


# Constants
spacing: str = '  '
hidden_fields: Tuple[str, ...] = ('id', 'fresh', 'internal')


class Collection(Sequence):
    _enumerator = '—'

    __slots__ = ('client', 'path', 'names', '_children')

    def __init__(
            self, children: Iterable[Dict[str, Any]],
            client: 'Connection', path: Path):
        self.client = client
        self.path = path
        self._children = list(children)
        self.names = tuple(c['name'] for c in self._children)
        for index, child in enumerate(children):
            # OrderedLookup and NameLookup may only contain NamedTuples
            if type(child) is dict:
                path = self.path + (index,)
                self._children[index] = State(child, self.client, path)

    def _get_named_item(self, name: str) -> 'State':
        indices = [ii for ii, nn in enumerate(self.names) if nn == name]
        if len(indices) == 1:
            return self._children[indices[0]]
        elif len(indices) == 0:
            raise KeyError(f"'{name}'")
        else:
            class_name = self.__class__.__name__
            raise KeyError(
                f'{class_name} contains multiple items named "{name}".  '
                f'Please choose an index: {indices}')

    def _set_named_item(self, name: str, value: 'State'):
        indices = [ii for ii, nn in enumerate(self.names) if nn == name]
        if len(indices) == 1:
            self._children[indices[0]] = value
        elif len(indices) == 0:
            raise KeyError(f"'{name}'")
        else:
            class_name = self.__class__.__name__
            raise KeyError(
                f'{class_name} contains multiple items named "{name}".  '
                f'Please choose an index: {indices}')

    def __getitem__(self, index: Union[int, str]) -> 'State':
        if type(index) is int:
            return self._children[index]
        else:
            return self._get_named_item(index)

    def __setitem__(self, index: Union[int, str], value: 'State'):
        # TODO: perform an add and "dump" attributes
        raise NotImplementedError('TODO')

    def __delitem__(self, index: Union[int, str]):
        self.client.delete(self.path + (index,))

    def __len__(self) -> int:
        return len(self._children)

    def __repr__(self) -> str:
        if len(self._children) == 0:
            return f'{self._enumerator} []'
        lines = list()
        for child in self._children:
            repr_lines = repr(child).split('\n')
            if len(repr_lines) == 0:
                lines.append('')
            if len(repr_lines) == 1:
                lines.append(f'{self._enumerator} {repr_lines[0]}')
            else:
                repr_text = f'\n{spacing}  '.join(repr_lines)
                lines.append(f'{spacing}{self._enumerator} {repr_text}')
        text = f'\n{spacing}{self._enumerator} '.join(lines)
        return text

    def __str__(self) -> str:
        name = self.__class__.__name__
        path = self.client.command_path(self.path)
        children = ', '.join(f"{i}: '{c.name}'" for i, c in enumerate(self._children))
        return f"{name}('{path}', [{children}])"

    def _get(self, path: Path) -> Optional[Value]:
        loc = len(self.path) + 1
        try:
            sub_path = path[:loc]
            *_, index = sub_path
            child = self[index]
        except (ValueError, IndexError, KeyError):
            return None
        if path == sub_path:
            return child
        else:
            path = child.path + path[loc:]
            # noinspection PyProtectedMember
            return child._get(path)

    def _update(self, path: Path, state: Value):
        loc = len(self.path) + 1
        try:
            sub_path = path[:loc]
            *_, index = sub_path
            child = self[index]
        except (IndexError, ValueError):
            raise KeyError(f'Update to {path} failed') from None
        if path == sub_path:
            if type(index) is int:
                self._children[index] = state
            else:
                self._set_named_item(index, state)
        else:
            path = child.path + path[loc:]
            # noinspection PyProtectedMember
            child._update(path, state)

    def insert(self, index: int, name: str = None) -> 'State':
        return self.client.insert(self.path, index, name)

    def add(self, name: str = None) -> 'State':
        return self.client.insert(self.path, -1, name)

    def help(self) -> str:
        return self.client.help(self.path)

    def setlist(self, *names) -> Iterable['State']:
        return self.client.setlist(self.path, *names)

    def paths(self) -> List[Path]:
        return self.client.paths(self.path)

    def expand(self):
        self.client.expand(self.path)

    def collapse(self):
        self.client.collapse(self.path)


class State:
    _enumerator = '•'

    __slots__ = ('client', 'path', 'fields', '_values')

    def __init__(
            self, values: Dict[str, Any],
            client: 'Connection', path: Path):
        self.client = client
        self.path = path
        self.fields = tuple(k for k in values.keys() if k not in hidden_fields)
        self._values = values
        for key, value in self._values.items():
            path = self.path + (key,)
            if type(value) is dict:
                # NamedTuple
                self._values[key] = State(value, self.client, path)
                continue
            elif type(value) is list \
                    and (len(value) == 0 or type(value[0]) is dict):
                # OrderedLookup or NameLookup
                self._values[key] = Collection(value, self.client, path)
            # else: primitive (or potentially a Python list); leave in dict as is

    def __getattr__(self, attribute: str) -> Value:
        try:
            return self._values[attribute]
        except KeyError:
            name = self.__class__.__name__
            raise AttributeError(
                f"'{name}' has no attribute '{attribute}'") from None

    def __setattr__(self, attribute: str, value: Value):
        try:
            super().__setattr__(attribute, value)
        except AttributeError:
            if attribute in self._values:
                self.client.set(self.path + (attribute,), value)
            else:
                raise

    def __delattr__(self, attribute: str):
        try:
            super().__delattr__(attribute)
        except AttributeError:
            if attribute in self._values:
                self.client.delete(self.path + (attribute,))
            else:
                raise

    def __getitem__(self, item: str) -> Value:
        return self._values[item]

    def __setitem__(self, item: str, value: Value):
        # Check if item exists
        _ = self._values[item]
        self.client.set(self.path + (item,), value)

    def __delitem__(self, item: str):
        # Check if item exists
        _ = self._values[item]
        self.client.delete(self.path + (item,))

    def __repr__(self) -> str:
        lines = list()
        for key, value in self._values.items():
            if key in hidden_fields:
                continue
            repr_lines = repr(value).split('\n')
            if len(repr_lines) == 0:
                lines.append(f'{self._enumerator} {key}:')
            if len(repr_lines) == 1:
                lines.append(f'{self._enumerator} {key}: {repr_lines[0]}')
            else:
                repr_text = f'\n{spacing}'.join(repr_lines)
                lines.append(f'{self._enumerator} {key}: \n{spacing}{repr_text}')
        text = ',\n'.join(lines)
        return text
    
    def __str__(self) -> str:
        name = self.__class__.__name__
        path = self.client.command_path(self.path)
        fields = ', '.join(f"'{k}'" for k in self._values.keys()
                           if k not in hidden_fields)
        return f"{name}('{path}', {{{fields}}})"

    def _get(self, path: Path) -> Optional[Value]:
        for key, value in self._values.items():
            child_path = self.path + (key,)
            if path == child_path:
                return self._values[key]
            elif child_path == path[:len(child_path)]:
                # noinspection PyProtectedMember
                return self._values[key]._get(path)
        return None

    def _update(self, path: Path, state: Value):
        for key, value in self._values.items():
            child_path = self.path + (key,)
            if path == child_path:
                self._values[key] = state
                break
            elif child_path == path[:len(child_path)]:
                # noinspection PyProtectedMember
                self._values[key]._update(path, state)
                break
        else:
            raise KeyError(f'Update to {path} failed')

    def delete(self):
        self.client.delete(self.path)

    def help(self) -> str:
        return self.client.help(self.path)

    def setfields(self, **fields):
        self.client.setfields(self.path, **fields)

    def paths(self) -> List[Path]:
        return self.client.paths(self.path)

    def expand(self):
        self.client.expand(self.path)

    def collapse(self):
        self.client.collapse(self.path)

    def takedefault(self):
        self.client.takedefault(self.path)


class Connection(AbstractContextManager):
    @staticmethod
    def command_path(path: Path) -> str:
        if len(path) == 0:
            return ''
        parts = '/'.join(str(p) for p in path)
        return f'/{parts}/'

    @staticmethod
    def escaped(value: Any) -> str:
        text = str(value)
        text = text.replace("\\", "\\\\").replace("\n", "\\\\n").replace('"', '\\"')
        return f'"{text}"'

    def __init__(self, address: str = '127.0.0.1', req_port: int = 33929,
                 sub_port: int = 33930, timeout: int = 10_000):
        self.address: str = address
        self.req_port: int = req_port
        self.sub_port: int = sub_port
        self.timeout: int = timeout
        self.time_format = '%H:%M:%S'
        # Uncomment to show full date & time
        # self.time_format = '%Y-%d-%m %H:%M:%S %Z (%z)'

        self._req_socket: Optional[Socket] = None
        self._sub_socket: Optional[Socket] = None
        self._path: Path = tuple()
        self._state: Optional[State] = None
        self._history: List[Tuple[float, str, dict]] = list()
        self._messages: List[Tuple[float, dict]] = list()
        self._connected: Optional[float] = None
        self._updated: Optional[float] = None
        self.commands: Tuple[str, ...] = tuple()  # Populated on `connect`

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __str__(self) -> str:
        name = self.__class__.__name__
        if self._connected is not None:
            connected = time.strftime(
                self.time_format, time.localtime(self._connected))
        else:
            connected = 'None'
        if self._updated is not None:
            updated = time.strftime(
                self.time_format, time.localtime(self._updated))
        else:
            updated = 'None'
        return f"{name}(" \
            f"tcp://{self.address}:({self.req_port}, {self.sub_port}), " \
            f"timeout={self.timeout} ms, " \
            f"connected={connected}, " \
            f"state={updated})"

    @property
    def state(self) -> State:
        if self._state is None:
            state = self.get(self._path)
            self._state = State(state, self, self._path)
            self._updated = time.time()
        return self._state

    @property
    def history(self) -> List[Tuple[str, str]]:
        return [(time.strftime(self.time_format, time.localtime(t)), c)
                for t, c, _ in self._history]

    @property
    def messages(self) -> List[Tuple[str, dict]]:
        try:
            self.listen(0)
        except ValueError:
            pass
        return [(time.strftime(self.time_format, time.localtime(t)), deepcopy(r))
                for t, r in self._messages]

    def connect(self, address: str = None, req_port: int = None,
                sub_port: int = None, timeout: int = None):
        if address is not None:
            self.address = address
        if req_port is not None:
            self.req_port = req_port
        if req_port is not None:
            self.req_port = req_port
        if sub_port is not None:
            self.sub_port = sub_port
        if timeout is not None:
            self.timeout = timeout
        if self._req_socket is not None or self._sub_socket is not None:
            # If already connected, close and reconnect
            self.close()
        self._req_socket = Context.instance().socket(REQ)
        self._req_socket.connect(f"tcp://{self.address}:{self.req_port}")
        self._sub_socket = Context.instance().socket(SUB)
        # Subscribe to all updates
        self._sub_socket.setsockopt(SUBSCRIBE, bytes())
        self._sub_socket.connect(f"tcp://{self.address}:{self.sub_port}")
        self.commands = self._commands()
        self._connected = time.time()
        self._state = None
        self._updated = None

    def close(self):
        if self._req_socket is not None:
            self._req_socket.close()
            self._req_socket = None
        if self._sub_socket is not None:
            self._sub_socket.close()
            self._sub_socket = None
        self._connected = None
        self._state = None
        self._updated = None

    def reload(self):
        self._state = None

    def _update(self, path: Path) -> Value:
        value = self.get(path)
        if type(value) is dict:
            updated = State(value, self, path)
        elif type(value) is list \
                and (len(value) == 0 or type(value[0]) is dict):
            updated = Collection(value, self, path)
        else:
            updated = value
        # noinspection PyProtectedMember
        self.state._update(path, updated)
        self._updated = time.time()
        return updated

    def _commands(self) -> List[str]:
        response = self.send('commands')
        if response['type'] != 'INFO' or 'commands' not in response:
            raise ValueError('Invalid response from DiscoveryDV')
        return list(response['commands'])

    def _verify(self, command: str):
        responses = self.listen()
        for response in responses:
            if response['text'] != command:
                continue
            type_ = response['type']
            if type_ == 'SUCCESS' and response['changes'] > 0:
                return
            elif type_ == 'SUCCESS' and response['changes'] == 0:
                raise ValueError('Command produced no changes')
            elif type_ == 'ERROR':
                raise ValueError(response['message'])
        raise ValueError('No response from DiscoveryDV')

    def listen(self, timeout: int = None) -> List[dict]:
        if timeout is None:
            timeout = self.timeout
        if self._sub_socket is None:
            name = self.__class__.__name__
            raise ValueError(f'{name} is not connected')
        if self._sub_socket.poll(timeout, POLLIN):
            messages = list()
            while True:
                try:
                    received = self._sub_socket.recv(flags=NOBLOCK)
                except ZMQError:
                    break
                else:
                    response = unpackb(received, encoding='utf-8')
                    messages.append(response)
                    self._messages.append((time.time(), response))
            return messages
        raise ValueError('No messages from DiscoveryDV')

    def send(self, command: str, timeout: int = None) -> dict:
        if timeout is None:
            timeout = self.timeout
        if self._req_socket is None:
            name = self.__class__.__name__
            raise ValueError(f'{name} is not connected')
        if self._req_socket.poll(timeout, POLLOUT):
            self._req_socket.send(packb(command, use_bin_type=True))
        if self._req_socket.poll(timeout, POLLIN):
            response = unpackb(self._req_socket.recv(), encoding='utf-8')
            self._history.append((time.time(), command, response))
            return response
        raise ValueError('No response from DiscoveryDV')

    def paths(self, path: Path = tuple()) -> List[Path]:
        if len(path) == 0:
            response = self.send('paths -t')
        else:
            command_path = self.command_path(path)
            response = self.send(f'paths -t {command_path}')
        if response['type'] != 'INFO' or 'paths' not in response:
            raise ValueError('Invalid response from DiscoveryDV')
        paths = response['paths']
        return [tuple(path['path']) for path in paths]

    def get(self, path: Path = tuple()) -> Value:
        if len(path) == 0:
            response = self.send('pack')
        else:
            command_path = self.command_path(path)
            response = self.send(f'pack {command_path}')
            if response['type'] == 'SUCCESS' \
                    and response['warning'].startswith('No matches for '):
                at = re.match(
                    r'^No matches for \(.*\) at (.*)$',
                    response['warning']).group(1)
                try:
                    first, *rest = [ii for ii, pp in enumerate(path)
                                    if str(pp) == at]
                except ValueError:
                    sub_path = path
                else:
                    sub_path = path[:first + 1]
                command_path = self.command_path(sub_path)
                if len(sub_path) == len(path):
                    raise KeyError(f'Path, {command_path}, was not found.')
                else:
                    raise KeyError(f'Sub-path, {command_path}, was not found.')
        if response['type'] != 'INFO' or 'packed' not in response:
            raise ValueError('Invalid response from DiscoveryDV')
        return response['packed']

    def help(self, path: Union[Path, str] = tuple()) -> str:
        if type(path) is str:
            # Can query help directly on a command
            response = self.send(f'help {path}')
            if response['type'] != 'INFO' or 'help' not in response:
                raise ValueError(f'Could not query help for "{path}"')
            help_text = response['help'].split('\n')
        elif len(path) == 0:
            response = self.send('help')
            if response['type'] != 'INFO' or 'help' not in response:
                raise ValueError(f'Could not query help for DiscoveryDV')
            help_text = response['help'].split('\n')
        else:
            # Make sure path exists
            obj = self.get(path)
            command_path = self.command_path(path)
            response = self.send(f'help {command_path}')
            if response['type'] != 'INFO' or 'help' not in response:
                raise ValueError(f'Could not query help for {command_path}')
            help_text = response['help'].split('\n')
            if type(obj) is dict:
                type_name = 'NameTuple'
            elif type(obj) is list:
                type_name = 'OrderedLookup | NameLookup'
            else:
                type_name = f'{str(obj)}: {type(obj).__name__}'
            help_text[0] = f'Path {command_path} ({type_name})'
        return '\n |  '.join(help_text)

    def insert(self, path: Path, index: int = -1, name: str = None) -> State:
        parent = self.get(path)
        command_path = self.command_path(path)
        if type(parent) is not list:
            raise ValueError(f'Cannot add: {command_path} is not a collection')
        command = f'insert {command_path} {index}'
        if name is not None:
            command += f' {self.escaped(name)}'
        response = self.send(command)
        if response['type'] != 'SUCCESS':
            raise ValueError(f'Could not insert at {command_path}')
        # Verify that command was processed and update the state
        self._verify(command)
        new = self._update(path)
        return new[index]

    def setlist(self, path: Path, *names) -> Iterable[State]:
        parent = self.get(path)
        command_path = self.command_path(path)
        if type(parent) is not list:
            raise ValueError(
                f'Cannot set list: {command_path} is not a collection')
        names_text = ' '.join(self.escaped(name) for name in names)
        command = f'setlist {command_path} {names_text}'
        response = self.send(command)
        if response['type'] != 'SUCCESS':
            raise ValueError(f'Could not set list at {command_path}')
        # Verify that command was processed and update the state
        self._verify(command)
        new = self._update(path)
        return iter(new)

    def delete(self, path: Path):
        if len(path) == 0:
            raise KeyError("Cannot delete root")
        # Make sure path exists
        _ = self.get(path)
        parent_path = path[:-1]
        parent = self.get(parent_path)
        reset = type(parent) is dict
        command_path = self.command_path(path)
        command = f'delete {command_path}'
        response = self.send(command)
        if response['type'] != 'SUCCESS':
            verb = 'reset' if reset else 'delete'
            raise ValueError(f'Could not {verb} {command_path}')
        # Verify that command was processed and update the state
        self._verify(command)
        if reset:
            _ = self._update(path)
        else:
            _ = self._update(parent_path)

    def set(self, path: Path, value: Union[str, bool, int, float]):
        current = self.get(path)
        command_path = self.command_path(path)
        if type(current) in (list, dict):
            raise ValueError(
                f'Can only set a terminal field, not {command_path}')
        if value == current:
            # Nothing to do
            return
        command = f'set {command_path} {self.escaped(value)}'
        response = self.send(command)
        if response['type'] == 'ERROR' and response['listen'].startswith('Bad arguments'):
            raise ValueError(
                f'Invalid type or value out of range for '
                f'{command_path}: {value}')
        if response['type'] != 'SUCCESS':
            raise ValueError(f'Could not set {command_path} to "{value}"')
        # Verify that command was processed and update the state
        self._verify(command)
        _ = self._update(path)

    def setfields(self, path: Path, **fields):
        current = self.get(path)
        command_path = self.command_path(path)
        if type(current) is not dict:
            raise ValueError(f'No fields available to set at {command_path}')
        fields_text = ' '.join(f'{k}={self.escaped(v)}' for k, v in fields.items())
        command = f'setfields {command_path} {fields_text}'
        response = self.send(command)
        if response['type'] == 'ERROR' and response['listen'].startswith('Bad arguments'):
            raise ValueError(
                f'Invalid type or value out of range for setting fields of '
                f'{command_path}')
        if response['type'] != 'SUCCESS':
            raise ValueError(f'Could not set fields for {command_path}')
        # Verify that command was processed and update the state
        self._verify(command)
        _ = self._update(path)

    def new(self, name: str = None) -> State:
        if name is None:
            command = 'new'
        else:
            command = f'new {self.escaped(name)}'
        response = self.send(command)
        if response['type'] != 'SUCCESS':
            raise ValueError(f'Could not create a new document')
        # Verify that command was processed and update the state
        self._verify(command)
        self.reload()
        return self.state

    def undo(self):
        response = self.send('undo')
        if response['type'] != 'SUCCESS':
            raise ValueError(f'Could not undo')
        self.reload()

    def redo(self):
        response = self.send('redo')
        if response['type'] != 'SUCCESS':
            raise ValueError(f'Could not redo')
        self.reload()

    def expand(self, path: Path):
        # Make sure path exists
        _ = self.get(path)
        command_path = self.command_path(path)
        response = self.send(f'expand {command_path}')
        if response['type'] != 'SUCCESS':
            raise ValueError(
                f'Could not expand {command_path} in the Storyboard')

    def collapse(self, path: Path):
        # Make sure path exists
        _ = self.get(path)
        command_path = self.command_path(path)
        response = self.send(f'collapse {command_path}')
        if response['type'] != 'SUCCESS':
            raise ValueError(
                f'Could not collapse {command_path} in the Storyboard')

    def _pref_path(self, path: Path) -> Path:
        if len(path) == 0 or path[0] != 'page':
            raise ValueError('Preferences path must be in a page')
        pref_path = ['preferences']
        state = self.state
        for element in path:
            if isinstance(state, Collection):
                pref_path.append(0)
            else:
                pref_path.append(element)
            # noinspection PyProtectedMember
            state = state._get(state.path + (element,))
        return tuple(pref_path)

    def takedefault(self, path: Path) -> State:
        pref_path = self._pref_path(path)
        # Make sure path exists and is not a Collection
        state = self.get(path)
        command_path = self.command_path(path)
        if type(state) is list:
            raise ValueError(
                f'Could not take defaults from a collection: {command_path}')
        command = f'takedefault {command_path}'
        response = self.send(command)
        if response['type'] != 'SUCCESS':
            raise ValueError(
                f'Could not take defaults from {command_path}')
        # Verify that command was processed and update the state
        self._verify(command)
        new_prefs = self._update(pref_path)
        return new_prefs


# TODO:
#  * Implement:
#    - copy
#    - move
#    - snapshot
#    - powerpoint
#    - soap
#    - vice
#    - activate
#    - refresh
#  * Write unit tests
#  * Develop a full demo for __main__
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--address", type=str, help="IP address",
        default='127.0.0.1')
    parser.add_argument(
        "--req_port", type=int, help="port number for sending commands",
        default=33929)
    parser.add_argument(
        "--sub_port", type=int, help="port number for subscribing to messages",
        default=33930)
    args = parser.parse_args()

    with Connection(args.address, args.req_port, args.sub_port) as connection:
        print(connection.commands)
        connection.new('Python Connection')
        new_page = connection.insert(('page',), -1, 'New Page')
        # client.delete(('page', -1))
        connection.set(('page', -1, 'paused'), True)
        print(connection.get(('page', -1, 'paused')))
        print(connection.help(('page', -1, 'paused')))
        connection.state.page[0].setfields(**{'paused': False, 'cwd': '/'})
        connection.state.page[0].comment.setlist('one', 'two', 'three')
        connection.state.page[0].comment.setlist('one', 'two')
        connection.state.page[0].pcplot.add()
        print(connection.state.page[0].comment[0].paths())
