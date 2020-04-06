from sys import path
import datetime 
import sqlite3

path.append('..\\database')

import managers.terminalCard as terminalCard
import managers.card as card
import managers.day as day
import managers.incident as incident
import managers.terminal as terminal


database = r"database/employee.db"
conn = sqlite3.connect(database)


def run(terminalID):
    if not is_terminal_existing(terminalID):
        print("In order to use this terminal please first register it!")
        return 0

    time_now = datetime.datetime.now()
    cardID = input("Please provide card character or exit keyword >> ")
    
    if cardID == 'exit':
        return 0
    if len(cardID) != 1:
        print("Incorrect card ID!")
        return 1

    cardID = ord(cardID)
    terminalCard.create_terminal_card(conn, terminalID, cardID, time_now)
    change_day(terminalID, cardID, time_now)
    return 1


def change_day(terminalID, cardID, time_now):
    result = card.was_used_today(conn, cardID)
    isAssigned = card.get_assigned_employee(conn, cardID)
  
    if isAssigned == 0:
        print("Card is not assigned to employee!")
        incident.create_incident(conn, terminalID, cardID, time_now)

    if result > 0:
        update_day(result, time_now, terminalID, cardID)
    if result == 0:
        create_day(cardID, time_now, terminalID)
    if result == -1:
        print("Card is not registered!")
        incident.create_incident(conn, terminalID, cardID, time_now)
    

def update_day(dayID, time_now, terminalID, cardID):
    day.update_day(conn, dayID, time_now, terminalID)
    card.change_card_status(conn, cardID, 0)


def create_day(cardID, time_start, terminal_start):
    employeeID = card.get_assigned_employee(conn, cardID)
    dayID = day.create_day(conn, cardID, employeeID, time_start, terminal_start)
    card.change_card_status(conn, cardID, dayID)
    
    
def is_terminal_existing(terminalID):
    return terminal.is_terminal_existing(conn, terminalID)