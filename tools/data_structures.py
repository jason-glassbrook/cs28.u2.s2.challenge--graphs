############################################################
#   DATA STRUCTURES
############################################################

import collections

############################################################
#   Default Dicts
############################################################


class _DefaultDict(collections.defaultdict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return repr(dict(self))


class DefaultDict(_DefaultDict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return

    @staticmethod
    def OfValue(some_value, *args, **kwargs):
        return DefaultDict(lambda: some_value, *args, **kwargs)


class NestedDefaultDict(_DefaultDict):

    def __init__(self, *args, **kwargs):
        super().__init__(NestedDefaultDict, *args, **kwargs)
        return


############################################################
#   Queue
############################################################


class Queue:

    def __init__(self):

        self.__container = collections.deque()
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

        self.__container = collections.deque()
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
