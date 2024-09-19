import sqlite3

def check_debtors(fio=None, birth_date=None, passport_data=None):
    conn = sqlite3.connect('borrowers.db')
    cursor = conn.cursor()

    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS debtors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fio TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        passport_data TEXT NOT NULL,
        brand TEXT,
        model TEXT,
        year INTEGER,
        loan_amount REAL,
        return_amount REAL
    )''')

    # Начинаем формирование запроса
    query = "SELECT * FROM debtors WHERE 1=1"
    params = []

    if fio:
        query += " AND fio = ?"
        params.append(fio)
    if birth_date:
        query += " AND birth_date = ?"
        params.append(birth_date)
    if passport_data:
        query += " AND passport_data = ?"
        params.append(passport_data)

    # Выполняем запрос
    cursor.execute(query, params)
    result = cursor.fetchone()

    # Закрываем соединение
    conn.close()

    return result

def save_loan(fio, birth_date, passport_data, brand, model, year, loan_amount, return_amount):
    conn = sqlite3.connect('borrowers.db')
    cursor = conn.cursor()

    try:
        # Вставляем данные в таблицу
        cursor.execute('''
        INSERT INTO debtors (fio, birth_date, passport_data, brand, model, year, loan_amount, return_amount) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (fio, birth_date, passport_data, brand, model, year, loan_amount, return_amount))

        # Сохраняем изменения
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Закрываем соединение
        conn.close()
