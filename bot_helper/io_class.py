from abc import ABC, abstractmethod

class IO_Base(ABC):
    @abstractmethod
    def print(self, *args, **kwargs):
        pass

    @abstractmethod
    def input(self,  *args, **kwargs):
        pass

class CLI_IN_OUT(IO_Base):
    def print(self, args):
        print(args)
    
    def input(self, args):
        return input(args)