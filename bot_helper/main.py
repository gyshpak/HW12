# from pathlib import Path
# import bot_helper.address_book as book
import address_book as book

def input_error(func):
    def inner(my_book, val):
        try:
            return_data = func(my_book, val)
        except IndexError:
            return_data = "Give me name and phone please"
        except TypeError:
            return_data = "Wrong command, try again"
        except KeyError:
            return_data = "Wrong user, repeat please"
        except ValueError:
            return_data = "Wrong number, repeat please"
        except book.WrongBirthday:
            return_data = "Wrong birthday, repeat please"
        except book.ExistsPhone:
            return_data = "Phone is exist"
        return return_data
    return inner


def handler_hello(my_book, _ = None):
    return "How can I help you?"

def handler_add(my_book, list_):
    my_book.exists_phone(list_[1])
    try:
        record = my_book.find(list_[0].capitalize())
    except:
        if len(list_) == 3:
            record = book.Record(list_[0].capitalize(),list_[2])
        else:
            record = book.Record(list_[0].capitalize())
        record.add_phone(list_[1])
        my_book.add_record(record)
    else:
        record.add_phone(list_[1])
        my_book.add_record(record)
    return "Command successfully complete"

def handler_change(my_book, list_):
    my_book.exists_phone(list_[2])
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.edit_phone(list_[1], list_[2])
    return f"Phone {list_[1]} from user {list_[0].capitalize()} successfully chandget to phone {list_[2]}"
    
def handler_show_all(my_book, _ = None):
    return my_book

def handler_exit(my_book, _ = None):
    return "Good bye!"

def handler_find(my_book, list_):
    list_rec = my_book.finde_records(list_[0].capitalize())
    if len(list_rec) != 0:
        ret_book = book.AddressBook()
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return ret_book
    else:
        return "Contact not found"
    
def handler_delete_phone(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    record.remove_phone(list_[1])
    return f"Phone {list_[1]} of user {list_[0].capitalize()} successfully deleted"

def handler_delete_user(my_book, list_):
    print(list_[0].capitalize())
    my_book.delete(list_[0].capitalize())
    return f"User {list_[0].capitalize()} successfully deleted"

def handler_next_birthday(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    days = record.days_to_birthday()
    return f"Next birthday for user {list_[0].capitalize()} after {days} days"


def handler_help(my_book = None, _ = None):
    help_string = '''
                Hellow, you can us next command with format:\n
                help - for help\n
                hello - for hello\n
                add <user_name> <phone(10 or 13 number)> [birthday] - for add user, if user is exist will be added phone to user\n
                change <user_name> <phone_from_chandge> <phone_to_chandge> - for chandge phone\n
                show all - for show all records\n
                good bye | close | exit - for exit\n
                find <some_letters> | <some_nombers> - for find record by name or phone\n
                delete phone <user_name> <phone> - for delete phone from user\n
                delete user <user_name> - for delete user from address book

                variation format for telefon number:
                +38(055)111-22-33
                38(055)111-22-34
                8(055)111-22-35
                (055)111-22-36
                055111-22-37
                and all variant without "-"
                '''
    return help_string

NAME_COMMANDS = {

    "help": handler_help,
    "hello": handler_hello,
    "add": handler_add,
    "change": handler_change,
    "showall": handler_show_all,
    "goodbye": handler_exit,
    "close": handler_exit,
    "exit": handler_exit,
    "find": handler_find,
    "deletephone": handler_delete_phone,
    "deleteuser": handler_delete_user,
    "nextbirthday": handler_next_birthday
}


def defs_commands(comm):
    return NAME_COMMANDS[comm]


@input_error
def parser_command(my_book, command):
    list_command = command.split(" ")
    if list_command[0] in NAME_COMMANDS:
        any_command = defs_commands(list_command[0])
        ret_rezault = any_command(my_book, list_command[1:])
        return ret_rezault
    elif len(list_command) > 1 and list_command[0]+list_command[1] in NAME_COMMANDS:
        any_command = defs_commands(list_command[0]+list_command[1])
        ret_rezault = any_command(my_book, list_command[2:])
        return ret_rezault
    else:
        any_command = defs_commands()
        return ret_rezault


def main():
    print(handler_help())
    # file_name_p = "bot_helper\\book_pickle.bin"
    file_name_j = "bot_helper\\book_json.json"
    # file_name_j = Path("E:\pyton_proj\Go-IT\\bot_helper\\bot_helper\\book_json.json")
    # my_book_p = book.AddressBook()
    my_book_j = book.AddressBook()
    # my_book = my_book_p.load_from_file_pickle(file_name_p) 
    my_book = my_book_j.load_from_file_json(file_name_j)
    while True:
        command = input("please enter command ").lower()
        ret_rezault = parser_command(my_book, command)
        if ret_rezault:
            print(ret_rezault)
            if ret_rezault == "Good bye!":
                # my_book.save_to_file_pickle(file_name_p)
                my_book.save_to_file_json(file_name_j)
                exit()

        
if __name__ == "__main__":
    main()