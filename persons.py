import sqlite3
from string import ascii_letters
from datetime import datetime

class Person:
    # Допустимые символы русского алфавита и дефис
    S_RUS = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя-'
    S_RUS_UPPER = S_RUS.upper()

    def __init__(self, full_name, birthdate, passport, status=None):
        self.verify_full_name(full_name)  # Проверка ФИО
        self.verify_birthdate(birthdate)   # Проверка даты рождения
        self.verify_passport(passport)     # Проверка номера паспорта
        self.__full_name = full_name
        self.__birthdate = birthdate
        self.__passport = passport
        self.__status = status if status is not None else self.calculate_status()  # Вычисляем статус при создании объекта

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

    # Проверка кредитного статуса
    def calculate_status(self):
        age = self.calculate_age()

        # Проверяем возраст
        if not (18 < age < 60):
            return False

        # Проверяем данные в базе "плохих заемщиков"
        if self.is_in_borrowers():
            return False

        return True

    # Функция проверки в базе заемщиков через SQLite
    def is_in_borrowers(self):
        conn = sqlite3.connect('borrowers.db')  # Подключаемся к базе данных
        cursor = conn.cursor()

        query = """
        SELECT 1
        FROM debtors
        WHERE fio = ? AND birth_date = ? AND passport_data = ?
        """
        cursor.execute(query, (self.__full_name, self.__birthdate, self.__passport))
        result = cursor.fetchone()

        conn.close()
        return result is not None

    # Метод для вычисления возраста
    def calculate_age(self):
        birthdate = datetime.strptime(self.__birthdate, '%d.%m.%Y')
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
        # Пересчитываем статус при изменении данных
        self.__status = self.calculate_status()

    # Геттер для даты рождения
    @property
    def birthdate(self):
        return self.__birthdate

    # Сеттер для даты рождения с проверкой
    @birthdate.setter
    def birthdate(self, birthdate):
        self.verify_birthdate(birthdate)
        self.__birthdate = birthdate
        # Пересчитываем статус при изменении данных
        self.__status = self.calculate_status()

    # Геттер для паспорта
    @property
    def passport(self):
        return self.__passport

    # Сеттер для паспорта с проверкой
    @passport.setter
    def passport(self, passport):
        self.verify_passport(passport)
        self.__passport = passport
        # Пересчитываем статус при изменении данных
        self.__status = self.calculate_status()

    # Геттер для статуса
    @property
    def status(self):
        return self.__status

    # Сеттер для статуса с проверкой
    @status.setter
    def status(self, status):
        # Статус изменять напрямую нельзя, пересчитывается автоматически
        raise AttributeError("Кредитный статус нельзя устанавливать напрямую")

# Тестирование
person = Person('Ivanov Ivan Ivanovich', '15.06.1990', '1234 123456')
print(f"ФИО: {person.full_name}")
print(f"Дата рождения: {person.birthdate}")
print(f"Возраст: {person.calculate_age()}")
print(f"Проверка статуса: {person.status}")

# Тестирование сеттеров
person.full_name = 'Petrov Petr Petrovich'
person.birthdate = '20.07.1985'
person.passport = '1235 654321'
print(f"ФИО: {person.full_name}")
print(f"Возраст: {person.calculate_age()}")
print(f"Проверка статуса: {person.status}")
