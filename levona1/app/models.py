from app.database import get_db

class User:
    def __init__(self, name, surname, email, password, phone, dni, address, state, admin=False, id_user=None):
        self.id_user = id_user
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.phone = phone
        self.dni = dni
        self.address = address
        self.state = state
        self.admin = admin

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_user:
            cursor.execute("""
                UPDATE users SET name = %s, surname = %s, email = %s, password = %s, phone = %s, dni = %s, address = %s, state = %s, admin = %s WHERE id = %s""",
                (self.name, self.surname, self.email, self.password, self.phone, self.dni, self.address, self.state, int(self.admin), self.id_user))
        else:
            cursor.execute("""
            INSERT INTO users (name, surname, email, password, phone, dni, address, state, admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (self.name, self.surname, self.email, self.password, self.phone, self.dni, self.address, self.state, int(self.admin)))
            self.id_user = cursor.lastrowid
        db.commit()
        cursor.close()


    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        users = [User(id_user=row[0], name=row[1], surname=row[2], email=row[3], password=row[4], phone=row[5], dni=row[6], address=row[7], state=row[8], admin=bool(row[9])) for row in rows]
        cursor.close()
        return users
    
    @staticmethod
    def get_by_id(id_user):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id_user,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(id_user=row[0], name=row[1], surname=row[2], email=row[3], password=row[4], phone=row[5], dni=row[6], address=row[7], state=row[8], admin=bool(row[9]))
        return None
    
    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(id_user=row[0], name=row[1], surname=row[2], email=row[3], password=row[4], phone=row[5], dni=row[6], address=row[7], state=row[8], admin=bool(row[9]))
        return None
    
    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (self.id_user,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'dni': self.dni,
            'address': self.address,
            'state': self.state,
            'admin': self.admin
        }
