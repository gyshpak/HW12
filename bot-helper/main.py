import address_book as book

def input_error(func):
    def inner(my_book, val):
    # def inner(val):
        try:
            return_data = func(my_book, val)
            # return_data = func(val)
        except IndexError:
            return_data = "Give me name and phone please"
        except ValueError:
            return_data = "Wrong number, repeat please"
        except KeyError:
            return_data = "Wrong Name, repeat please"
        except TypeError:
            return_data = "Wrong command, try again"
        return return_data
    return inner


def handler_hello(_):
    return "How can I help you?"

def handler_add(my_book, list_):
# def handler_add(list_):
    # LIST_PHONEBOOK[list_[0]] = int(list_[1])
    record = my_book.find(list_[0].capitalize())
    if record is not None:
       record.add_phone(list_[1])
       my_book.add_record(record)
       print(record)
    else:
        record = book.Record(list_[0].capitalize())
        record.add_phone(list_[1])
        print(record)
        my_book.add_record(record)
    return "Command successfully complete"

def handler_change(my_book, list_):
    # _ = LIST_PHONEBOOK[list_[0]]
    # LIST_PHONEBOOK[list_[0]] = int(list_[1])
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.edit_phone(list_[1], list_[2])
    return "Command successfully complete"
    
def handler_phone(my_book, list_):
    # return LIST_PHONEBOOK[list_[0]]
    list_rec = my_book.finde_records(list_[0])
    if list_rec is not None:
        # for item in list_rec:
        #     print (item)
        print(list_rec)
        dict_rec = {rec_.name.value: rec_ for rec_ in list_rec}
        # print(type(dict_rec))
        copy_book = my_book.copy(dict_rec)
        # print(type(copy_book))
        return copy_book

def handler_show_all(my_book):
# def handler_show_all():
    # return LIST_PHONEBOOK
    return my_book

def handler_exit(my_book, _ = None):
# def handler_exit(_ = None):
    return "Good bye!"


# LIST_PHONEBOOK = {}
NAME_COMMANDS = {
    "hello": handler_hello,
    "add": handler_add,
    "change": handler_change,
    "phone": handler_phone,
    "showall": handler_show_all,
    "goodbye": handler_exit,
    "close": handler_exit,
    "exit": handler_exit
}


def defs_commands(comm):
    return NAME_COMMANDS[comm]


@input_error
def parser_command(my_book, command):
# def parser_command(command):
    list_command = command.split(" ")
    if list_command[0] in NAME_COMMANDS:
        any_command = defs_commands(list_command[0])
        ret_rezault = any_command(my_book, list_command[1:])
        return ret_rezault
    elif len(list_command) > 1 and list_command[0]+list_command[1] in NAME_COMMANDS:
        any_command = defs_commands(list_command[0]+list_command[1])
        ret_rezault = any_command(my_book)
        # ret_rezault = any_command()
        return ret_rezault
    else:
        any_command = defs_commands()
        return ret_rezault


# my_book = None

def main():


    # file_name_p = "bot-helper\\book_pickle.bin"
    file_name_j = "bot-helper\\book_json.json"
    # my_book_p = book.AddressBook()
    my_book_j = book.AddressBook()
    # my_book = my_book_p.load_from_file_pickle(file_name_p) 
    my_book = my_book_j.load_from_file_json(file_name_j)
    while True:
        command = input("please enter command ").lower()
        ret_rezault = parser_command(my_book, command)
        # ret_rezault = parser_command(command)
        if ret_rezault:
            try:
                print(ret_rezault)
            except:
                pass
            if ret_rezault == "Good bye!":
                # my_book.save_to_file_pickle(file_name_p)
                # my_book.save_to_file_json(file_name_j)
                exit()

        
if __name__ == "__main__":
    main()