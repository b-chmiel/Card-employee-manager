from sys import path
#path.append('..\\backend')

import sqlite3
import datetime

from .backend import manageBack


database = r"database\\employee.db"
conn = sqlite3.connect(database)
c = conn.cursor()


def test_add():
    manageBack.add_employee(conn, "Boris", "Johnson")
    manageBack.add_employee(conn, "Boris", "Johnson")
    manageBack.add_terminal(conn, 1)
    manageBack.add_terminal(conn, 5)
    manageBack.add_card(conn, 1)
    manageBack.add_card(conn, 99)


def test_delete():
    pass


def test_list():
    pass


def test_raport():
    pass


def test_assign():
    pass


def main():
    test_add()


if __name__ == '__main__':
    main()


