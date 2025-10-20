from utils.dbUtil import dbConnection
class LeetMdl:
    def __init__(self, leet_no, leet_func_name):
        self.leet_no = leet_no
        self.leet_func_name = leet_func_name


    def save_leet(self):
        conn = dbConnection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Leet(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        leet_func_name TEXT NOT NULL,
        leet_no  INTEGER NOT NULL)
        ''')
        conn.commit()

        cursor.execute('''
        INSERT INTO Leet(leet_func_name, leet_no)
        VALUES (?, ?)''', (self.leet_func_name, self.leet_no))
        print("Saved")
        conn.commit()
        conn.close()

    def __str__(self):
        print(self.leet_no, self.leet_func_name)