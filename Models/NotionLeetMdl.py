from utils.dbUtil import  dbConnection

class SavedLeetMdl:
    def __init__(self, leetNo, leetName, leet_NotionId, leet_difficulty, leet_status):
        self.leetNo = leetNo
        self.leetName = leetName
        self.leet_NotionId = leet_NotionId
        self.leet_difficulty = leet_difficulty
        self.leet_status = leet_status

    def saveNotionLeet(self):
        conn = dbConnection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS NotionLeet(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        leet_no INTEGER NOT NULL,
        leet_title TEXT NOT NULL,
        leet_NotionId TEXT NOT NULL,
        leet_difficulty TEXT,
        leet_status TEXT)
        ''')

        conn.commit()

        # Status not saved. Extract Value from response JSON Object
        cursor.execute('''
        INSERT INTO NotionLeet(leet_no, leet_title, leet_NotionId, leet_difficulty)
        VALUES (?, ?, ?, ?) ''', (self.leetNo, self.leetName, self.leet_NotionId, self.leet_difficulty))
        conn.commit()
        conn.close()



    def __str__(self):
        return f"{self.leetNo} {self.leetName}"

def getNotionLeetsFromdb():
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM NotionLeet
    ''')
    leets = cursor.fetchall()
    conn.close()
    return leets