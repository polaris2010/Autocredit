import flet as ft

def main(page: ft.Page):
    page.title = "Автокредит"
    page.window_width = 1200
    page.window_height = 600
    # t = ft.Text(value="Оформление автокредита", color="green")
    # page.controls.append(t)
    page.update()


    page.add(
        ft.Row(controls=[
            ft.TextField(label="Фамилия"),
            ft.TextField(label="Дата рождения"),
            ft.TextField(label="Паспорт"),
            ft.ElevatedButton(text="Проверить")

        ])
    )

    # # Выпадающие списки для выбора автомобиля
    # brands = ["Toyota"]  # Добавьте свои марки
    # models = ["Camry", "Corolla", "Prado"]  # Добавьте свои модели
    #
    # brand_dropdown = ft.Dropdown(
    #     options=[ft.dropdown.Option(br) for br in brands],
    #     label="Марка",
    #     width=20,
    # )
    # model_dropdown = ft.Dropdown(
    #     options=[ft.dropdown.Option(md) for md in models],
    #     label="Модель",
    #     width=20,
    # )

    page.add(
        ft.Row(controls=[
            ft.Dropdown(
                label="Бренд",
                options=[
                    ft.dropdown.Option("Toyota")
                ]
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
            ft.ElevatedButton(text="Искать")
        ])
    )


    page.add(
        ft.Row(controls=[
            ft.TextField(label="Сумма кредита"),

        ])
    )

    page.add(
        ft.Row(controls=[
            ft.TextField(label="Процент"),
            ft.TextField(label="Срок кредита"),
            ft.TextField(label="К возврату"),
            ft.ElevatedButton(text="Оформить кредит")

        ])
    )


ft.app(target=main)
