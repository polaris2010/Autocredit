'''
- Выберите тему и распишите функционал и интерфейс (какие будут окна, какие действия умеет делать пользователь),
текст описания и схемы интерфейса прикрепить в README.md

- Подберите нужные библиотеки. Интерфейс можно писать на любой удобной, для функционала можно использовать дополнительные внешние библиотеки.
'''

import flet as ft
import db
import parse  # Импортируем модуль с функцией парсинга
import re


def main(page: ft.Page):
    page.title = "Автокредит"
    page.window.width = 1200
    page.window.height = 600
    page.update()

    # Обработка и форматирование ФИО
    def format_fio(e):
        fio_input.value = ' '.join(word.capitalize() for word in fio_input.value.split())
        page.update()

    # Валидация даты рождения
    def format_birth_date(e):
        if re.match(r'^\d{2}\.\d{2}\.\d{4}$', birth_date_input.value):
            birth_date_input.error_text = None
        else:
            birth_date_input.error_text = "Формат должен быть дд.мм.гггг"
        page.update()

    # Валидация паспортных данных
    def format_passport_data(e):
        if re.match(r'^\d{2} \d{2} \d{6}$', passport_input.value):
            passport_input.error_text = None
        else:
            passport_input.error_text = "Формат должен быть 00 00 000000"
        page.update()

    # Проверка должника
    def check_debtor_action(e):
        fio = fio_input.value
        birth_date = birth_date_input.value
        passport_data = passport_input.value

        search = db.check_debtors(fio=fio, birth_date=birth_date, passport_data=passport_data)

        if search:
            page.add(ft.Text("Запись найдена, выдать кредит невозможно", color="green"))
        else:
            page.add(ft.Text("Запись не найдена", color="blue"))

    # Расчет кредита
    def calculate_loan(e):
        try:
            loan_amount = float(loan_amount_input.value)
            interest_rate = float(interest_rate_input.value) / 100  # Преобразуем процент в десятичную дробь
            term_months = int(term_input.value)

            # Рассчитываем сумму возврата
            return_amount = loan_amount * (1 + interest_rate * term_months)
            return_amount_input.value = str(return_amount)
            page.update()

        except ValueError:
            pass  # Игнорируем ошибки преобразования значений

    # Оформление кредита
    def submit_loan(e):
        try:
            calculate_loan(e)  # Выполняем расчет суммы возврата перед сохранением

            # Сохраняем данные в базе
            db.save_loan(
                fio=fio_input.value,
                birth_date=birth_date_input.value,
                passport_data=passport_input.value,
                brand=brand_dropdown.value,
                year=int(year_dropdown.value),
                loan_amount=float(loan_amount_input.value),
                return_amount=float(return_amount_input.value)
            )
            page.add(ft.Text("Кредит оформлен успешно!", color="green"))
        except ValueError:
            page.add(ft.Text("Ошибка при оформлении кредита. Проверьте введенные данные.", color="red"))

    # Получение средней цены
    def fetch_car_price(e):
        brand = brand_dropdown.value
        model = model_dropdown.value
        year = year_dropdown.value

        # Проверяем, что все поля заполнены
        if not brand or not model or not year:
            page.add(ft.Text("Пожалуйста, выберите бренд, модель и год автомобиля.", color="red"))
            page.update()
            return  # Выход из функции, если данные не введены

        # Формируем URL для парсинга
        url = f"https://www.avito.ru/samara/avtomobili/{brand}/{model}-ASgBAgICAkTgtg20mSjitg2woig?cd=1&radius=0&searchRadius=0"

        print(f"URL для парсинга: {url}")  # Отладочное сообщение для проверки URL

        # Получаем среднюю цену с помощью функции веб-скрапинга
        avg_price = parse.scrape_item_prices(url)  # Открытие браузера происходит только здесь

        if avg_price > 0:
            loan_amount_input.value = str(avg_price)
            loan_amount_input.read_only = True  # Запрещаем изменение суммы кредита
        else:
            loan_amount_input.value = ""
            loan_amount_input.read_only = False  # Разрешаем ввод суммы кредита вручную
            page.add(ft.Text("Цена не найдена. Введите сумму кредита вручную.", color="red"))

        page.update()

    # Очистка формы
    def reset_form(e):
        fio_input.value = ""
        birth_date_input.value = ""
        passport_input.value = ""
        brand_dropdown.value = None
        model_dropdown.value = None
        year_dropdown.value = None
        loan_amount_input.value = ""
        interest_rate_input.value = ""
        term_input.value = ""
        return_amount_input.value = ""
        loan_amount_input.read_only = False  # Снова делаем поле для суммы кредита редактируемым
        page.update()

    # Создание полей и кнопок
    fio_input = ft.TextField(label="Фамилия", on_change=format_fio)
    birth_date_input = ft.TextField(label="Дата рождения", on_change=format_birth_date)
    passport_input = ft.TextField(label="Паспорт", on_change=format_passport_data)
    check_button = ft.ElevatedButton(text="Проверить", on_click=check_debtor_action)

    brand_dropdown = ft.Dropdown(
        label="Бренд",
        options=[ft.dropdown.Option("Toyota")]
    )
    model_dropdown = ft.Dropdown(
        label="Модель",
        options=[ft.dropdown.Option("Corolla"), ft.dropdown.Option("Camry"),
                 ft.dropdown.Option("Land Cruiser Prado"), ft.dropdown.Option("Land Cruiser")]
    )
    year_dropdown = ft.Dropdown(
        label="Год",
        options=[ft.dropdown.Option("2006"), ft.dropdown.Option("2020")]
    )
    loan_amount_input = ft.TextField(label="Средняя стоимость авто")
    credit_sum = ft.TextField(label="Сумма кредита")
    interest_rate_input = ft.TextField(label="Процент", on_change=calculate_loan)
    term_input = ft.TextField(label="Срок кредита", on_change=calculate_loan)
    return_amount_input = ft.TextField(label="К возврату", read_only=True)
    calculate_button = ft.ElevatedButton(text="Оформить кредит", on_click=submit_loan)

    price_button = ft.ElevatedButton(text="Стоимость", on_click=fetch_car_price)  # Кнопка для получения стоимости
    next_client_button = ft.ElevatedButton(text="Очистить форму", on_click=reset_form)  # Кнопка для сброса формы

    form = ft.Column(
        controls=[ft.Row(controls=[fio_input, birth_date_input, passport_input, check_button]),
                  ft.Row(controls=[brand_dropdown, model_dropdown, year_dropdown, price_button]),
                  ft.Row(controls=[loan_amount_input]),
                  ft.Row(controls=[interest_rate_input, term_input, return_amount_input, calculate_button]),
                  ft.Row(controls=[next_client_button])],
        spacing=40
    )

    page.add(form)


ft.app(target=main)
