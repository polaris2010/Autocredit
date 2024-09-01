'''
- Выберите тему и распишите функционал и интерфейс (какие будут окна, какие действия умеет делать пользователь),
текст описания и схемы интерфейса прикрепить в README.md

- Подберите нужные библиотеки. Интерфейс можно писать на любой удобной, для функционала можно использовать дополнительные внешние библиотеки.

'''

import flet as ft
import db
import parse

def main(page: ft.Page):
    page.title = "Автокредит"
    page.window.width = 1200
    page.window.height = 600
    page.update()

    def check_debtor_action(e):
        fio = fio_input.value
        birth_date = birth_date_input.value
        passport_data = passport_input.value

        search = db.check_debtors(fio=fio, birth_date=birth_date,
                                  passport_data=passport_data)

        if search:
            page.add(ft.Text("Запись найдена, выдать кредит невозможно", color="green"))
        else:
            page.add(ft.Text("Запись не найдена", color="blue"))

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
            # Не выводим сообщение об ошибке при изменении значений
            pass

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

    def fetch_car_price(e):
        brand = brand_dropdown.value
        model = model_dropdown.value
        year = year_dropdown.value

        # Получаем среднюю цену с помощью функции из модуля parse.py
        avg_price = parse.get_avg_price(brand, model, year)
        if avg_price > 0:
            loan_amount_input.value = str(avg_price)
            loan_amount_input.read_only = True  # Запрещаем изменение суммы кредита, если цена найдена
        else:
            loan_amount_input.value = ""
            loan_amount_input.read_only = False  # Разрешаем ввод суммы кредита вручную
            page.add(ft.Text("Цена не найдена. Введите сумму кредита вручную.", color="red"))
        page.update()

    def reset_form(e):
        # Очищаем все поля формы
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

    fio_input = ft.TextField(label="Фамилия")
    birth_date_input = ft.TextField(label="Дата рождения")
    passport_input = ft.TextField(label="Паспорт")
    check_button = ft.ElevatedButton(text="Проверить", on_click=check_debtor_action)

    brand_dropdown = ft.Dropdown(
        label="Бренд",
        options=[ft.dropdown.Option("Toyota")]
    )
    model_dropdown = ft.Dropdown(
        label="Модель",
        options=[
            ft.dropdown.Option("Corolla"),
            ft.dropdown.Option("Camry"),
            ft.dropdown.Option("Prado"),
            ft.dropdown.Option("L200"),
        ]
    )
    year_dropdown = ft.Dropdown(
        label="Год",
        options=[
            ft.dropdown.Option("2020"),
            ft.dropdown.Option("2021"),
            ft.dropdown.Option("2022"),
            ft.dropdown.Option("2023"),
        ]
    )
    loan_amount_input = ft.TextField(label="Сумма кредита")
    interest_rate_input = ft.TextField(label="Процент", on_change=calculate_loan)
    term_input = ft.TextField(label="Срок кредита", on_change=calculate_loan)
    return_amount_input = ft.TextField(label="К возврату", read_only=True)
    calculate_button = ft.ElevatedButton(text="Оформить кредит", on_click=submit_loan)

    price_button = ft.ElevatedButton(text="Стоимость", on_click=fetch_car_price)  # Кнопка для получения стоимости
    next_client_button = ft.ElevatedButton(text="Следующий клиент", on_click=reset_form)  # Кнопка для сброса формы

    form = ft.Column(
        controls=[
            ft.Row(controls=[fio_input, birth_date_input, passport_input, check_button]),
            ft.Row(controls=[brand_dropdown, model_dropdown, year_dropdown, price_button]),
            # Кнопка для получения стоимости
            ft.Row(controls=[loan_amount_input]),
            ft.Row(controls=[interest_rate_input, term_input, return_amount_input, calculate_button]),
            ft.Row(controls=[next_client_button])  # Добавлена кнопка "Очистить форму"
        ],
        spacing=40
    )

    page.add(form)


ft.app(target=main)
