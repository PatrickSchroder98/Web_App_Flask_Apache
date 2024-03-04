import sqlite3
from argon2 import PasswordHasher



class PySQLiteConnection:
    ph = PasswordHasher()

    def __init__(self, path):
        self.path = path

    def readData(self, arg0, arg1):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        result = []
        for row in cur.execute("""SELECT {arg0}, {arg1} FROM Logins""".format(arg0=arg0, arg1=arg1)):
            result.append(row)
        conn.close()
        return result

    def writeData(self, data):
        try:
            conn = sqlite3.connect(self.path)
            cur = conn.cursor()

            check = self.readData('username', 'email')
            for row in check:
                if data[0] == row[0] or data[2] == row[1]:
                    return False
            _hash = self.ph.hash(data[1])
            cur.execute("""INSERT INTO Logins(username, password, email) 
                                VALUES ('{login}', '{pas}', '{mail}')""".format(login=data[0], pas=_hash, mail=data[2]))
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def checkPasswort(self, data):
        db = self.readData("username", "password")
        for row in db:
            if row[0] == data[0]:
                self.ph.verify(row[1], data[1])
                return True
        return False

n = PySQLiteConnection("C:\\Web_App_Flask_Apache\\Model\\Database\\database.sqlite")
n.writeData(["user2", "user", "user2@example.com"])
print(n.checkPasswort(("admin", "admin")))
