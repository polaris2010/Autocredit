import sqlite3


def check_debtors(fio=None, birth_date=None, passport_data=None):
    conn = sqlite3.connect('borrowers.db')
    cursor = conn.cursor()

    # Проверяем наличие таблицы
    cursor.execute('''CREATE TABLE IF NOT EXISTS debtors
                      (fio TEXT, birth_date TEXT, passport_data TEXT, 
                      brand TEXT, year INTEGER, loan_amount REAL, return_amount REAL)''')

    # Формируем запрос с учетом переданных параметров
    query = "SELECT * FROM debtors WHERE 1=1"
    params = []

    if fio:
        query += " AND fio=?"
        params.append(fio)
    if birth_date:
        query += " AND birth_date=?"
        params.append(birth_date)
    if passport_data:
        query += " AND passport_data=?"
        params.append(passport_data)

    cursor.execute(query, params)
    result = cursor.fetchone()  # Получаем первую запись, соответствующую условиям

    conn.close()

    return result  # Возвращаем результат (None, если запись не найдена)


# def add_debtor(fio, birth_date, passport_data):
#     conn = sqlite3.connect('borrowers.db')
#     cursor = conn.cursor()
#
#     # Добавляем новую запись
#     cursor.execute('''INSERT INTO debtors (fio, birth_date, passport_data, brand, year, loan_amount, return_amount)
#                       VALUES (?, ?, ?, '', 0, 0.0, 0.0)''', (fio, birth_date, passport_data))
#
#     conn.commit()
#     conn.close()