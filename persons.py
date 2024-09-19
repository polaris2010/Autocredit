from string import ascii_letters
from datetime import datetime


class Person:
    # Допустимые символы русского алфавита и дефис
    S_RUS = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя-'
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self, full_name, birthdate, passport):
        self.verify_full_name(full_name)  # Проверка ФИО
        self.full_name = full_name
        self.birthdate = birthdate  # Устанавливаем дату рождения
        self.passport = passport

    # Проверка правильности ФИО
    @classmethod
    def verify_full_name(cls, full_name):
        if not isinstance(full_name, str):
            raise TypeError("Full name must be a string")

        name_parts = full_name.split()
        if len(name_parts) != 3:
            raise TypeError("Full name must contain 3 parts (first, last, middle name)")

        allowed_characters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER
        for part in name_parts:
            if len(part) < 1:
                raise TypeError("Each part of the full name must contain at least one character")
            if any(char not in allowed_characters for char in part):
                raise TypeError("Full name must contain only letters")

    # Проверка корректности даты рождения
    @classmethod
    def verify_birthdate(cls, birthdate):
        if not isinstance(birthdate, str):
            raise TypeError("Birthdate must be a string in the format DD.MM.YYYY")
        try:
            datetime.strptime(birthdate, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid birthdate format. Expected format: DD.MM.YYYY")

    # Проверка номера паспорта
    @classmethod
    def verify_passport(cls, passport):
        if not isinstance(passport, str):
            raise TypeError("Passport number must be a string in the format 0000 000000")

        passport_parts = passport.split()
        if len(passport_parts) != 2 or len(passport_parts[0]) != 4 or len(passport_parts[1]) != 6:
            raise TypeError("Invalid passport format. Expected format: 0000 000000")

        if not (passport_parts[0].isdigit() and passport_parts[1].isdigit()):
            raise TypeError("Passport series and number must contain only digits")

    # Метод для вычисления возраста
    def calculate_age(self):
        birthdate = datetime.strptime(self.birthdate, '%d.%m.%Y')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    # Геттер для полного имени
    @property
    def full_name(self):
        return self.__full_name

    # Сеттер для полного имени с проверкой
    @full_name.setter
    def full_name(self, full_name):
        self.verify_full_name(full_name)
        self.__full_name = full_name

    # Геттер для даты рождения
    @property
    def birthdate(self):
        return self.__birthdate

    # Сеттер для даты рождения с проверкой
    @birthdate.setter
    def birthdate(self, birthdate):
        self.verify_birthdate(birthdate)
        self.__birthdate = birthdate

    # Геттер для паспорта
    @property
    def passport(self):
        return self.__passport

    # Сеттер для паспорта с проверкой
    @passport.setter
    def passport(self, passport):
        self.verify_passport(passport)
        self.__passport = passport


# Тестирование
person = Person('Ivanov Ivan Ivanovich', '15.06.1990', '1234 123456')
print(f"ФИО: {person.full_name}")
print(f"Дата рождения: {person.birthdate}")
print(f"Возраст: {person.calculate_age()}")

# Тестирование сеттеров
person.full_name = 'Petrov Petr Petrovich'
person.birthdate = '20.07.1985'
person.passport = '1235 654321'
