import sqlite3, uuid, sys, os.path
from werkzeug.security import generate_password_hash, check_password_hash

db_file = './app.db'


class DB:

    def __init__(self, db):
        self.app = None
        self.con = sqlite3.connect(db, check_same_thread=False)
        self.con.row_factory = sqlite3.Row

    def init_app(self, app, createDB):
        self.app = app
        if createDB:
            self.drop()

        row = self.get("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if row is None:
            self.create()

    # Executes SQL query, returning a single row.
    def get(self, q, args=()):
        cur = self.con.cursor()
        # print(q)
        resp = cur.execute(q, args)
        return resp.fetchone()

    # Executes SQL query, returning a list of rows.
    def select(self, q, args=(), limit=0):
        cur = self.con.cursor()
        # print(q)
        resp = cur.execute(q, args)
        if limit == 0:
            return resp.fetchall()
        return resp.fetchmany(limit)

    # Executes SQL query and commits changes to database.
    def execute(self, q, args):
        cur = self.con.cursor()
        # print(q, args)
        cur.execute(q, args)
        self.con.commit()
        return cur.lastrowid

    # Executes multiple SQL queries and commits changes to database.
    def transaction(self, sql):
        with self.con as conn:
            cur = conn.cursor()
            try:
                for q in sql:
                    # print(q)
                    cur.execute(q)
                conn.commit()
                return True
            except:
                conn.rollback()
                return False

    def drop(self):
        cur = self.con.cursor()
        cur.execute('DROP TABLE IF EXISTS users')
        cur.execute('DROP TABLE IF EXISTS accts')
        cur.execute('DROP TABLE IF EXISTS xacts')
        self.con.commit()

    def create(self):

        # setup initial schema
        print("creating database")
        with open('schema.sql', 'r') as f:
            schema = f.read()
        for sql in schema.split(';'):
            self.execute(sql, [])

        # helper function to retrieve acct_id from a user_id
        def user_acct(id):
            return Acct.by_user_id(id)[0].id

        # helper function to add default users to database
        def add_user(role, name, password, fullname, email, phone):
            uid = User.new(name, password)
            u = User.by_id(uid)
            u.role = role
            u.fullname = fullname
            u.email = email
            u.phone = phone
            u.update()
            return u.id

        # populate default users
        a = add_user('admin', 'admin', 'alice', 'Alice Administrator', 'alice@komradeland.com', '+313 373 8483')
        b = add_user('staff', 'komradebank', 'correct horse battery staple', 'Komrade Bank', 'team@komradebank.com', '555 THE BANK')
        c = add_user('staff', 'carol', '0xbeefcafebabe', 'Sweet Carolina', 'carol@candle.lite', '+777 777 7777')
        d = add_user('user', 'Bobby\" DROP TABLES;--', '\" OR \"1\"=\"1\"', 'Bob Bandit', 'bob@bob.com', '+628 456 7890')

        # initial injection of funds
        initialFunds = 314159265359.00
        Xact.new(user_acct(b), 'private investor donation from komrade pi', initialFunds)
        db.execute('UPDATE accts SET acct_balance = ? WHERE acct_id = ?', [initialFunds, user_acct(b)])

        # populate default transfers
        do_transfer(user_acct(b), user_acct(a), 123456789.00, 'seed funding for administrators')
        do_transfer(user_acct(a), user_acct(c),     31337.00, 'election rigger fees')
        do_transfer(user_acct(c), user_acct(d),       256.00, 'darkweb ransomware job - upfront payment')
        do_transfer(user_acct(c), user_acct(d),      1081.00, 'darkweb ransomware job - final payment')
        do_transfer(user_acct(a), user_acct(d),      9447.00, 'extorted for ransomware decryption key')
        do_transfer(user_acct(b), user_acct(c),        42.00, 'prize money for flag{can_you_get_me?}')


# global database instance
db = DB(db_file)


class User:

    def __init__(self, id, name, passhash, role, fullname, email, phone):
        self.id = id
        self.name = name
        self.passhash = passhash
        self.role = role
        self.fullname = fullname
        self.email = email
        self.phone = phone

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
            return check_password_hash(self.passhash, password)

    def update(self):
        db.execute('''
          UPDATE users 
          SET user_role = ?,
              user_pass = ?,
              user_fullname = ?,
              user_phone = ?,
              user_email = ?
          WHERE user_id = ?
        ''', [
            self.role,
            self.passhash,
            self.fullname,
            self.phone,
            self.email,
            self.id,
        ])

    @staticmethod
    def _from_row(row):
        return User(
            row['user_id'],
            row['user_name'],
            row['user_pass'],
            row['user_role'],
            row['user_fullname'],
            row['user_email'],
            row['user_phone'],
        )

    @staticmethod
    def new(username, password):
        passhash = generate_password_hash(password)
        id = db.execute('INSERT INTO users (user_name, user_pass) VALUES (?, ?)', [username, passhash])
        Acct.new(id)
        return id

    @staticmethod
    def by_id(id):
        row = db.get('SELECT * FROM users WHERE user_id = ?', [id])
        if row is None:
            return None
        return User._from_row(row)

    @staticmethod
    def by_name(name):
        row = db.get('SELECT * FROM users WHERE user_name = ?', [name])
        if row is None:
            return None
        return User._from_row(row)

    @staticmethod
    def by_filter(filter):
        rows = db.select('SELECT * FROM users WHERE user_name LIKE ?', ['%' + filter + '%'])
        users = []
        for row in rows:
            users.append(User._from_row(row))
        return users


class Acct:

    def __init__(self, id, user, balance):
        self.id = id
        self.user = user
        self.balance = balance

    @staticmethod
    def _from_row(row):
        return Acct(
            row['acct_id'],
            row['acct_user'],
            row['acct_balance'],
        )

    @staticmethod
    def new(user_id):
        id = str(uuid.uuid4())
        db.execute('-- TODO: write SQL query to insert new account with provided account id and user id', [id, user_id])
        Xact.new(id, 'starting balance', 0.00)
        do_transfer(Acct.by_user_id(1)[0].id, id, 1337.00, 'KomradeBank New Account Bonus Offer')
        return id

    @staticmethod
    def by_id(acct_id):
        row = db.get('-- TODO: write SQL query to return a single row for a specific account id', [acct_id])
        if row is None:
            return None
        return Acct._from_row(row)

    @staticmethod
    def by_user_id(user_id):
        rows = db.select('-- TODO: write SQL query to return all rows for a specified user id', [user_id])
        accts = []
        for row in rows:
            accts.append(Acct._from_row(row))
        return accts

    @staticmethod
    def by_filter(filter):
        rows = db.select('-- TODO: write SQL query to return all rows where account id matches a LIKE filter', ['%' + filter + '%'])
        accts = []
        for row in rows:
            accts.append(Acct._from_row(row))
        return accts


class Xact:

    def __init__(self, id, timestamp, acct, memo, amount):
        self.id = id
        self.acct = acct
        self.timestamp = timestamp
        self.memo = memo
        self.amount = amount

    @staticmethod
    def _from_row(row):
        return Xact(
            row['xact_id'],
            row['xact_timestamp'],
            row['xact_acct'],
            row['xact_memo'],
            row['xact_amount'],
        )

    @staticmethod
    def new(acct_id, memo, amount):

        # TODO: Implement method to create new transaction.

        # Returns id for the newly inserted transaction. (provided by db.execute())
        return -1

    @staticmethod
    def by_id(xact_id):

        # TODO: Implement method to return the transaction for a given id.

        # Returns Xact object
        return None

    @staticmethod
    def by_acct_id(acct_id):

        # TODO: Implement method to return list of all transactions for a given account id.

        # Returns list of Xact objects
        return []

    @staticmethod
    def by_filter(filter):

        # TODO: Implement method to return list of all transactions where 'xact_memo' matches a LIKE filter.

        # Returns list of Xact objects
        return []


def do_transfer(src, dst, amount, memo):

    # src       - (string) Source account ID
    # dst       - (string) Destination account ID
    # amount    - (float)  Amount of funds to transfer from src -> dst
    # memo      - (string) Description of transfer purpose

    src_acct = Acct.by_id(src)
    dst_acct = Acct.by_id(dst)

    """
    Check that transfer is valid: (return error messages provided below if not)
      a) Both accounts must exist and not be the same.
      b) Amount must be greater than zero.
      c) Source account must have sufficient funds for transfer.
    """

    # return "Transfer Failed - Invalid Accounts."

    # return "Transfer Failed - Invalid amount."

    # return "Transfer Failed - Insufficient funds."


    sql = [
        '-- TODO: write SQL query to insert new transaction for source account',
        '-- TODO: write SQL query to insert new transaction for destination account',
        '-- TODO: write SQL query to update source account balance',
        '-- TODO: write SQL query to update destination account balance',
    ]

    if not db.transaction(sql):
        return "Transfer Failed - Internal Error."

    return "Funds transferred successfully."
