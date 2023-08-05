import socket
import sys
import os
from code import InteractiveConsole
from utils import send_all, receive_all
import rlcompleter
import json


class CompleterWrapper(rlcompleter.Completer):
    def __init__(self, socket_in):
        self._socket = socket_in
        rlcompleter.Completer.__init__(self)
        pass

    def complete(self, text, state):

        json_obj = {"text": text, "state": state}
        # send the command to the server
        send_all(self._socket, json.dumps(json_obj).encode())

        # wait for response from the server
        data = receive_all(self._socket)
        data = json.loads(data)
        # data = None if data == "" else data
        if data["response"] != "exception":
            return data["response"]
        else:
            # raise AttributeError(data["exception"])
            return None

class Client(InteractiveConsole):
    def __init__(self):
        self._socket = None
        try:
            envs = globals()
            envs.update(locals())
            InteractiveConsole.__init__(self, envs)
        except ImportError:
            InteractiveConsole.__init__(self)

    def connect(self, port):
        self._socket = socket.socket()
        self._socket.connect(('localhost', port))

        if sys.platform == 'darwin':
            import readline  # this will work only on mac
        elif sys.platform == 'win32':
            sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
            from lib import readline

        # initialize InteractiveConsole with autocomplete (arrow keys)
        envs = globals()
        envs.update(locals())
        readline.set_completer(CompleterWrapper(self._socket).complete)
        readline.parse_and_bind("tab: complete")

    def push(self, line):
        line.strip()
        if len(line) == 0:
            InteractiveConsole.push(self, line)
            return

        if line == 'exit()':
            InteractiveConsole.push(self, line)
            return

        # send the command to the server
        send_all(self._socket, line.encode())

        # wait for response from the server
        data = receive_all(self._socket)
        if not data:
            return

        # print the command
        data = data.strip()
        if len(data) > 0:
            print(data, end='\n')

    def close(self):
        self._socket.close()


def main(argv):
    if len(argv) != 1:
        print('invalid number of arguments, expecting int argument for port number')
        return -1

    # connect to server
    port = int(argv[0])
    client = Client()
    client.connect(port)

    # start interactive console loop
    banner = ("Python %s\n%s\n" % (sys.version, sys.platform) +
              'Type "help", "copyright", "credits" or "license" '
              'for more information.\n')
    client.interact(banner)

    # exit, close connection
    client.close()


if __name__ == '__main__':
    main(sys.argv[1:])
