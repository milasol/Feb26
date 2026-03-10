# Task 1
# Field classesfrom datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value
        
#Name field
class Name(Field):
    pass

# Phone field
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain 10 digits")
        super().__init__(value)
        
# Birthday field
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(birthday_date)
        
# Record classclass Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        bday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Not set"
        return f"{self.name.value}: {phones}, birthday: {bday}"
    
# address book class
class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value.replace(year=today.year)

            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)

            delta = (birthday - today).days

            if delta <= 7:
                congratulation_day = birthday

                if congratulation_day.weekday() >= 5:
                    congratulation_day += timedelta(days=(7 - congratulation_day.weekday()))

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_day.strftime("%d.%m.%Y")
                })

        return upcoming

# Error decoration
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the required arguments."
        except KeyError:
            return "Contact not found."
    return wrapper

# Command handlers
@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_birthday(birthday)
    return "Birthday added."

# Show birthday
@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if record is None or record.birthday is None:
        return "Birthday not found."

    return record.birthday.value.strftime("%d.%m.%Y")

# uocoming birthday
@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No birthdays in the next week."

    result = []
    for item in upcoming:
        result.append(f"{item['name']} - {item['congratulation_date']}")

    return "\n".join(result)

# example usage

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")