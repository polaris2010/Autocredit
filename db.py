import sqlite3

def check_debtors(fio=None, birth_date=None, passport_data=None):
    conn = sqlite3.connect('borrowers.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS debtors
                      (fio TEXT, birth_date TEXT, passport_data TEXT, 
                      brand TEXT, year INTEGER, loan_amount REAL, return_amount REAL)''')

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
    result = cursor.fetchone()

    conn.close()

    return result

def save_loan(fio, birth_date, passport_data, brand, year, loan_amount, return_amount):
    conn = sqlite3.connect('borrowers.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO debtors (fio, birth_date, passport_data, 
                      brand, year, loan_amount, return_amount) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (fio, birth_date, passport_data, brand, year, loan_amount, return_amount))

    conn.commit()
    conn.close()
