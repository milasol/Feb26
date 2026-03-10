# Tak assistent
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Ім'я — обов'язкове поле, успадковує логіку Field
    pass

class Phone(Field):
    def __init__(self, value):
        # Валідація: номер має складатися рівно з 10 цифр
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        # Додаємо новий об'єкт Phone до списку
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        # Видаляємо телефон, якщо значення збігається
        original_count = len(self.phones)
        self.phones = [p for p in self.phones if p.value != phone_number]
        if len(self.phones) == original_count:
            raise ValueError(f"Phone number {phone_number} not found.")

    def edit_phone(self, old_number, new_number):
        # Знаходимо старий номер і замінюємо його на новий об'єкт Phone (з валідацією)
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                return
        raise ValueError(f"Phone number {old_number} not found.")

    def find_phone(self, phone_number):
        # Шукаємо об'єкт Phone за значенням
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        # Додаємо запис, використовуючи ім'я як ключ
        self.data[record.name.value] = record

    def find(self, name):
        # Повертаємо об'єкт Record або None
        return self.data.get(name)

    def delete(self, name):
        # Видаляємо запис за ключем
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")