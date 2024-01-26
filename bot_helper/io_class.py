from abc import ABC, abstractmethod
import json, pickle

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
        return input(args).lower()
    
class JSON_IN_OUT(IO_Base):
    def print(self, file_name, data):
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def input(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data

class PICKLE_IN_OUT(IO_Base):
    def print(self, file_name, book):
        with open(file_name, 'wb') as file:
            pickle.dump(book, file)
        
        # with open(file_name_j, 'w') as file:
        #     pickle.dump(data, file)

    def input(self, file_name):
        with open(file_name, 'rb') as file:
            return pickle.load(file)
        
        # with open(file_name_j, 'r') as file:
        #     data = pickle.load(file)
        # return data