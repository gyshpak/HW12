from collections import UserDict
from copy import copy, deepcopy
from datetime import date
from re import match
import pickle
import json


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __repr__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        self.__value = ""
        self.value = value

    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, new_value):
        if self.is_valid_phone(new_value):
            norm_phone = self.normalis_phone(new_value)
            self.__value =  norm_phone
        else:
            raise Exception
 
    def is_valid_phone(self, value):
        if value != "":
            if match(r"^[\+]?3?8?[\s]?\(?0\d{2}?\)?[\s]?\d{3}[\s|-]?\d{2}[\s|-]?\d{2}$", value) != None:
                return True
            else:
                return False

    def normalis_phone(self, value):
        norm_mob = value.replace("+","")\
                        .replace(" ","")\
                        .replace("(","")\
                        .replace(")","")\
                        .replace("-","")
        if len(norm_mob) == 10:
            return "+38" + norm_mob
        if len(norm_mob) == 11:
            return "+3" + norm_mob
        if len(norm_mob) == 12:
            return "+" + norm_mob
        return ""

    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return NotImplemented
    

class Birthday(Field):
    def __init__(self, value):
        self.__value = ""
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if self.is_valid_birthday(new_value):
            norm_birthday = self.normalis_birthday(new_value)
            if norm_birthday != "":
                self.__value = norm_birthday
            else:
                raise Exception

    def is_valid_birthday(self, value):
        if value != "":
            if match(r"^\d{2}['\s'|\-|'.'|:]{1}\d{2}[\s|\-|'.'|:]{1}\d{4}$|^\d{4}['\s'|\-|'.'|:]{1}\d{2}[\s|\-|'.'|:]{1}\d{2}$", value) != None:
                return True
            else:
                return False
            
    def normalis_birthday(self, new_value):
        norm_birthday = new_value.replace(".",",")\
                    .replace(" ",",")\
                    .replace("-",",")\
                    .replace(":",",")
        date_birthday = norm_birthday.split(",")
        if len(date_birthday[0]) == 4:
            return date(int(date_birthday[0]), int(date_birthday[1]), int(date_birthday[2]))
        else:
            return date(int(date_birthday[2]), int(date_birthday[1]), int(date_birthday[0]))
        
    def __sub__(self, other):
        try:
            birthday_month = self.value.month
            birthday_day = self.value.day
            my_birthday = date(other.value.year, birthday_month, birthday_day)
            date_today = other.value
            if my_birthday < date_today:
                my_birthday = my_birthday.replace(year=date_today.year + 1)
            day_to_birthday = my_birthday - date_today
            return day_to_birthday.days
        except AttributeError:
            return None
    
    def __repr__(self):
        return self.value.strftime("%Y %m %d")

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        try:
            self.birthday = Birthday(birthday)
        except:
            pass

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
        except:
            pass
        else:
            if phone_obj not in self.phones:
                    self.phones.append(phone_obj)

    def remove_phone(self, phone):
        try:
            search_phone = Phone(phone)
        except:
            pass
        else:
            for item in self.phones:
                if item == search_phone:
                    self.phones.remove(item)

    def edit_phone(self, phone, new_phone):
        search_phone = Phone(phone)
        chandge_phone = Phone(new_phone)
        for item in self.phones:
            if item == search_phone:
                index = self.phones.index(item)
                self.phones[index] = chandge_phone
    
    def find_phone(self, phone):
        try:
            search_phone = Phone(phone)
        except:
            pass
        else:
            for item in self.phones:
                if item == search_phone:
                    return item
                
    def days_to_birthday(self):
        today = Birthday(date.today().strftime("%Y %m %d"))
        try:
            return self.birthday - today
        except:
            return None


    def __str__(self):
        # return f"Contact name:"
    
        if hasattr(self, "birthday"):
            return f"Contact name: {self.name.value}, phones: {', '.join(p.value for p in self.phones)}, birthday: {date.strftime(self.birthday.value, '%d %m %Y')}"
        else:
            return f"Contact name: {self.name.value}, phones: {', '.join(p.value for p in self.phones)}"
        
    # def __repr__(self):
    #     if hasattr(self, "birthday"):
    #         return f"{'{'}'phones': '{', '.join(p.value for p in self.phones)}'{'}'}, 'birthday': '{date.strftime(self.birthday.value, '%Y %m %d')}'"
    #     else:
    #         return f"{'{'}'phones': '{', '.join(p.value for p in self.phones)}'{'}'}"


class AddressBook(UserDict):
    qua_for_iter = 2
    list_for_iter = []

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for key, record in self.data.items():
            if key == name:
                return(record)

    def delete(self, name):
        try:
            self.data.pop(name)
        except:
            None
    
    def finde_records(self,search = None):
        list_rec = []
        for name, records in self.data.items():
            if search.lower() in name.lower():
                # print(records)
                list_rec.append(records)
            else:
                for phones in records.phones:
                    if search in phones.value:
                        # print(records)
                        list_rec.append(records)
                        break
        return list_rec
    
    def __next__(self):
        if len(self.list_for_iter) == len(self.data):
            self.list_for_iter.clear()
            raise StopIteration
        iter = 0
        for_return = []
        for key, value in self.data.items():
            if key in self.list_for_iter:
                pass
            else:
                for_return.append(str(value))
                self.list_for_iter.append(key)
                iter += 1
            if len(for_return) == self.qua_for_iter:
                break
        # return for_return
        return f"{'; '.join(i for i in for_return)} \n"

    def __iter__(self):
        return self
    
    def save_to_file_pickle(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)
    
    def load_from_file_pickle(self, file_name):
        with open(file_name, 'rb') as file:
            return pickle.load(file)
        
    def save_to_file_json(self, file_name):
        data = {}
        dict_phones = {}
        list_phones = []
        for name_i, records_i in self.data.items():
            for i_phone in records_i.phones:
                list_phones.append(i_phone.value)
            dict_phones["phone"] = list_phones
            if hasattr(records_i, "birthday"):
                data[name_i] = [dict_phones, {"birthday": records_i.birthday.value.strftime("%Y %m %d")}]
            else:
                data[name_i] = [dict_phones]
            list_phones = []
            dict_phones = {}
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def load_from_file_json(self, file_name):
        data = None
        with open(file_name, 'r') as file:
            data = json.load(file)
        ret_book = self
        for j_name, j_records in data.items():
            if len(j_records) == 2:
                record = Record(j_name, j_records[1].get("birthday"))
            else:
                record = Record(j_name)
            for j_phone in j_records[0].get("phone"):
                record.add_phone(j_phone)
            ret_book.add_record(record)
        return ret_book
    
    def __copy__(self, **dict_):
        copy_obj = AddressBook(None)
        copy_obj.qua_for_iter = copy(self.qua_for_iter)
        copy_obj.list_for_iter = copy(self.list_for_iter)
        copy_obj.data = dict_
        return copy_obj
    
    def __str__(self):
        for record in self:
            print(record)

            
if __name__ == "__main__":
    ###################################        Blok for verification         #################################

    # # Створення нової адресної книги
    # book = AddressBook()

    # # # Створення запису для John
    # john_record = Record("John", "17 12 1975")
    # john_record.add_phone("023 456 78 90")
    # john_record.add_phone("023 456 78 91")
    # john_record.add_phone("(055)555-55-55")
    # john_record.add_phone("(055) 555-55-")
    # # print(john_record.days_to_birthday())

    # # # # Додавання запису John до адресної книги
    # book.add_record(john_record)

    # # # Створення запису для Jorjy
    # # # Додавання запису Jorjy до адресної книги
    # jorjy_record = Record("Jorjy", "01.01.1980")
    # jorjy_record.add_phone("38 088 888 88 88")
    # book.add_record(jorjy_record)
    # # print(jorjy_record.days_to_birthday())


    # # print(jorjy_record.birthday - john_record.birthday)
    # # print(john_record.birthday - jorjy_record.birthday)

    # jorjy1_record = Record("Jorjy1")
    # jorjy1_record.add_phone("38 088 888 88 88")
    # book.add_record(jorjy1_record)
    # # print(jorjy1_record.days_to_birthday())

    # jorjy2_record = Record("Jorjy2")
    # jorjy2_record.add_phone("38 088 888 88 88")
    # book.add_record(jorjy2_record)

    # jorjy3_record = Record("Jorjy3")
    # jorjy3_record.add_phone("38 088 888 88 88")
    # book.add_record(jorjy3_record)

    # jorjy4_record = Record("Jorjy4")
    # jorjy4_record.add_phone("38 088 888 88 88")
    # book.add_record(jorjy4_record)

    # # # # Створення та додавання нового запису для Jane
    # jane_record = Record("Jane")
    # jane_record.add_phone("987")
    # book.add_record(jane_record)

    ###################################################
    # print(jane_record.days_to_birthday())
    # jane = book.find("Jane")
    # print(jane)
    # jane = book.find("Jannne")
    # print(jane)

    # Виведення всіх записів у книзі
    # for name, record in bok.data.items():
    #     print(record)

    # # # Знаходження та редагування телефону для John
    # john = book.find("John")
    # # print(john)
    # john.edit_phone("023 456 78 90", "011 222 33 33")
    # # print(john)
    # try:
    #     john.edit_phone("123", "(011)2223333")
    # except:
    #     print("Wrong nomber, request rejected")
    # try:
    #     john.edit_phone("(011)2223333", "111")
    # except:
    #     print("Wrong nomber for chandging")
    # print(john)
    # john.remove_phone("011 222 33 3")
    # print(john)
    # john.remove_phone("011 222 33 33")
    # print(john)
    # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # # # # Пошук конкретного телефону у записі John
    # found_phone = john.find_phone("023 456 78 91")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
    # found_phone = john.find_phone("+38 055 555 55 55")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
    # found_phone = john.find_phone("+385(5)")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # # # Видалення запису Jorjy4
    # book.delete("Jorjy4")

    # Jorjy4 = book.find("Jorjy4")
    # print(Jorjy4)

    # for record in book:
    #     print(record)
    # print("")
    # for record in book:
    #     print(record)

    ########################  for  12  HW   #####################################


    file_name_pickle = "bot-helper\\book_pickle.bin"
    # book.save_to_file_pickle(file_name_pickle)

    book_from_pickle = AddressBook()
    book = book_from_pickle.load_from_file_pickle(file_name_pickle)

    # print("\nFrom pickle: \n")
    try:
        print(book)
    except:
        pass
    
    # for record in book:
    #     print(record)


    # file_name_json = "bot-helper\\book_json.json"
    # # book.save_to_file_json(file_name_json)

    # book_from_json = AddressBook()
    # book_from_json = book_from_json.load_from_file_json(file_name_json)

    # # print("\nFrom json: \n")
    # for record in book_from_pickle:
    #     print(record)


    # john = book_from_json.find("Jjjjohn")
    # print(john)

    # book_from_pickle.finde_records("80")
        

    # record = book_from_pickle.find("John")
    # record.add_phone("0674626244")
    # book_from_pickle.add_record(record)
    # print(record)