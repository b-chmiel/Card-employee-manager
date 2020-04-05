
from sys import path

import sqlite3
import datetime

import managers.terminalCard as terminalCard
import managers.card as card
import managers.day as day
import managers.incident as incident
import managers.terminal as terminal
import managers.employee as employee

path.append('..\\database')
database = r"database\\employee.db" #TODO correct path
conn = sqlite3.connect(database)
c = conn.cursor()


def test_employee():
    print("get_all_employees >>", employee.get_all_employees(conn))
    print("get_employee(1) >>", employee.get_employee(conn, 1))
    print("create_employee(Richard, Johnson) >>", employee.create_employee(conn, "Richard", "Johnson"))
    print("get_all_employees >>", employee.get_all_employees(conn))
    print("remove_employee(1) >>", employee.remove_employee(conn, 1))
    print("remove_employee(4) >>", employee.remove_employee(conn, 4))
    print("get_all_employees >>", employee.get_all_employees(conn))


def test_terminal():
    print("create_terminal(1) >>", terminal.create_terminal(conn, 1))
    print("create_terminal(5) >>", terminal.create_terminal(conn, 5))
    print("create_terminal(7) >>", terminal.create_terminal(conn, 7))
    print("delete_terminal(1) >>", terminal.delete_terminal(conn, 1))
    print("delete_terminal(4) >>", terminal.delete_terminal(conn, 4))
    print("delete_terminal(1) >>", terminal.delete_terminal(conn, 1))
    print("is_terminal_existing(1) >>", terminal.is_terminal_existing(conn, 1))
    print("is_terminal_existing(5) >>", terminal.is_terminal_existing(conn, 5))


def test_card_employee():
    print("create_card(8) >>", card.create_card(conn, 8))
    print("create_card(8) >>", card.create_card(conn, 8))
    print("assign_card_employee(1, 1) >>", card.assign_card_employee(conn, 1, 1))
    print("assign_card_employee(1, 2) >>", card.assign_card_employee(conn, 1, 2))
    print("assign_card_employee(7, 1) >>", card.assign_card_employee(conn, 7, 1))
    print("assign_card_employee(1, 7) >>", card.assign_card_employee(conn, 1, 7))
    print("get_cards_employees() >>", card.get_cards_employees(conn))
    print("is_card_existing(1) >>", card.is_card_existing(conn, 1))
    print("is_card_existing(7) >>", card.is_card_existing(conn, 7))
    print("change_card_status(1, 2) >>", card.change_card_status(conn, 1, 2))
    print("change_card_status(97, 2) >>", card.change_card_status(conn, 97, 2))
    print("get_assigned_employee(1) >>", card.get_assigned_employee(conn, 1))
    print("get_assigned_employee(97) >>", card.get_assigned_employee(conn, 97))


def test_day():
    print("is_day_exists(1) >>", day.is_day_exists(conn, 1))
    print("is_day_exists(6) >>", day.is_day_exists(conn, 6))
    time_now = datetime.datetime.now()
    
    print("create_day(1, 1,", time_now, ", 1) >>", day.create_day(conn, 1, 1, time_now, 1))
    print("get_days() >>" , day.get_days(conn))
    time_now = datetime.datetime.now()
    print("create_day(2, 2,", time_now, ", 1) >>", day.create_day(conn, 2, 2, time_now, 1))
    print("get_days() >>" , day.get_days(conn))
    time_now = datetime.datetime.now()
    
    print("update_day(1,", time_now, ", 1) >> ", day.update_day(conn, 1, time_now,  1))
    print("get_days() >>" , day.get_days(conn))
    time_now = datetime.datetime.now()
    print("update_day(2,", time_now, ", 2) >> ", day.update_day(conn, 2, time_now, 2))
    print("get_days() >>" , day.get_days(conn))
    print("get_day(1) >>" , day.get_day(conn, 1))
    print("get_day(9) >>" , day.get_day(conn, 9))

def test_terminal_card():
    time_now = datetime.datetime.now()
    print("create_terminal_card(1, 1,", time_now, ") >>", terminalCard.create_terminal_card(conn, 1, 1, time_now))
    print("create_terminal_card(1, 3,", time_now, ") >>", terminalCard.create_terminal_card(conn, 1, 3, time_now))
    print("create_terminal_card(2, 3,", time_now, ") >>", terminalCard.create_terminal_card(conn, 2, 3, time_now))
    print("get_terminal_info(1) >>", terminalCard.get_terminal_info(conn, 1))

#TODO change alter day and create day arguments and tests
def main():
    test_employee()
    test_terminal()
    test_card_employee()
    test_day()
    test_terminal_card()
    conn.close()

if __name__ == "__main__":
    main()    

