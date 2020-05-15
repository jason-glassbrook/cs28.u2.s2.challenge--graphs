############################################################
#   DATA STRUCTURES
############################################################

from collections import (
    namedtuple as NamedTuple,
    defaultdict as DefaultDict,
    deque as Deck,
)

############################################################
#   Queue
############################################################


class Queue:

    def __init__(self):

        self.__container = Deck()
        return

    def __len__(self):

        return len(self.__container)

    def push(self, value):

        self.__container.append(value)
        return

    def pop(self):

        if len(self) > 0:
            return self.__container.popleft()

        else:
            return None


############################################################
#   Stack
############################################################


class Stack:

    def __init__(self):

        self.__container = Deck()
        return

    def __len__(self):

        return len(self.__container)

    def push(self, value):

        self.__container.appendleft(value)
        return

    def pop(self):

        if len(self) > 0:
            return self.__container.popleft()

        else:
            return None
