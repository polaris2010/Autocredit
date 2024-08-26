'''
- Выберите тему и распишите функционал и интерфейс (какие будут окна, какие действия умеет делать пользователь),
текст описания и схемы интерфейса прикрепить в README.md

- Подберите нужные библиотеки. Интерфейс можно писать на любой удобной, для функционала можно использовать дополнительные внешние библиотеки.

'''


import flet as ft

def main(page: ft.Page):
    page.title = "Автокредит"
    page.window.width = 1200
    page.window.height = 600
    page.update()

    def check_debtor_action(e):
        fio = fio_input.value
        birth_date = birth_date_input.value
        passport_data = passport_input.value

        search = check_debtors(fio=fio, birth_date=birth_date, passport_data=passport_data)

        if search:
            page.add(ft.Text("Запись найдена, выдать кредит невозможно", color="green"))
        else:
            page.add(ft.Text("Запись не найдена", color="blue"))

    def check_debtors(fio, birth_date, passport_data):
        debtors = [
            {"fio": "Иван Иванов", "birth_date": "1980-01-01", "passport_data": "123456"},
        ]
        for debtor in debtors:
            if debtor["fio"] == fio and debtor["birth_date"] == birth_date and debtor["passport_data"] == passport_data:
                return True
        return False

    fio_input = ft.TextField(label="Фамилия")
    birth_date_input = ft.TextField(label="Дата рождения")
    passport_input = ft.TextField(label="Паспорт")
    check_button = ft.ElevatedButton(text="Проверить", on_click=check_debtor_action)

    # Оборачиваем строки в Column для управления расстоянием
    form = ft.Column(
        controls=[
            ft.Row(controls=[fio_input, birth_date_input, passport_input, check_button]),
            ft.Row(controls=[
                ft.Dropdown(
                    label="Бренд",
                    options=[ft.dropdown.Option("Toyota")]
                ),
                ft.Dropdown(
                    label="Модель",
                    options=[
                        ft.dropdown.Option("Corolla"),
                        ft.dropdown.Option("Camry"),
                        ft.dropdown.Option("Prado"),
                        ft.dropdown.Option("L200"),
                    ]
                ),
                ft.Dropdown(
                    label="Год",
                    options=[
                        ft.dropdown.Option("2020"),
                        ft.dropdown.Option("2021"),
                        ft.dropdown.Option("2022"),
                        ft.dropdown.Option("2023"),
                    ]
                ),
                ft.ElevatedButton(text="Стоимость")
            ]),
            ft.Row(controls=[ft.TextField(label="Сумма кредита")]),
            ft.Row(controls=[
                ft.TextField(label="Процент"),
                ft.TextField(label="Срок кредита"),
                ft.TextField(label="К возврату"),
                ft.ElevatedButton(text="Оформить кредит")
            ])
        ],
        spacing=40  # Устанавливаем расстояние между строками
    )

    page.add(form)  # Добавляем весь Column на страницу

ft.app(target=main)
