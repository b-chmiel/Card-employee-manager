import datetime 

import managers.terminalCard as terminalCard
import managers.card as card
import managers.day as day
import managers.incident as incident
import managers.terminal as terminal
import managers.employee as employee


def add_employee(conn, Name, Surname):
    result = employee.create_employee(conn, Name, Surname)
    if result == -1:
        print("Employee exists!")
    else:
        print("Employee:", Name, Surname, "ID", result, "added")    


def add_terminal(conn, terminalID):
    result = terminal.create_terminal(conn, terminalID)
    if result == -1:
        print("Terminal exists!")
    else:
        print("Terminal:", result, "added")    


def add_card(conn, cardID):
    result = card.create_card(conn, cardID)
    if result == -1:
        print("Card exists!")
    else:
        print("Card:", result, "added")


def delete_employee(conn, employeeID):
    result = employee.remove_employee(conn, employeeID)
    if result == -1:
        print("Employee DNE")
    else:
        print("Employee:", result, "deleted")

    cardID = employee.get_assigned_card(conn, employeeID)

    if cardID > 0:
        unassign_card(conn, cardID)
        

def delete_terminal(conn, terminalID):
    result = terminal.delete_terminal(conn, terminalID)
    if result == -1:
        print("Terminal DNE")
    else:
        print("Terminal:", result, "deleted")


def delete_card(conn, cardID):
    result = card.delete_card(conn, cardID)
    if result == -1:
        print("Card DNE")
    else:
        print("Card:", result, "deleted")


def list_employees(conn):
    print("Employees")
    print("[ID, NAME, SURNAME]")
    for i in employee.get_all_employees(conn):
        print(i)

def list_terminals(conn):
    print("Terminals")
    print("[ID]")
    for i in terminal.get_terminals(conn):
        print(i)


def list_cards(conn):
    print("Cards")
    print("[ID EMPLOYEE_ID WAS_USED_RECENTLY]")
    for i in card.get_cards_employees(conn):
        print(i)


def list_days(conn):
    print("Days")
    print("[ID CardID EmployeeID TimeStart TimeEnd")
    for i in day.get_days(conn):
        print(i)

def list_incidents(conn):
    print("Incidents")
    print("[ID, TerminalID, CardID, TimeOfUsage]")
    for i in incident.get_incident_info(conn):
        print(i)


def raport(conn, employeeID):
    import csv, os

    if not len(employee.get_employee(conn, employeeID)):
        print("Employee DNE!")
        return

    cursor = conn.cursor()
    
    sql = ''' select * from day where EmployeeID = ? '''
    file_name = "employee_data" + str(employeeID) + ".csv"
    
    cursor.execute(sql, (employeeID,))
    with open(file_name, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    dirpath = os.getcwd() + "/" + file_name
    print ("Data exported Successfully into {}".format(dirpath))
        

def assign_card_employee(conn, cardID, employeeID):
    if not card.is_card_existing(conn, cardID):
        print("Card DNE!")
        return

    if not len(employee.get_employee(conn, employeeID)):
        print("Employee DNE!")
        return

    previous_employee_card = employee.get_assigned_card(conn, employeeID)
    card.assign_card_employee(conn, previous_employee_card, 0)
    card.change_card_status(conn, previous_employee_card, 0)

    card.assign_card_employee(conn, cardID, employeeID)
    card.change_card_status(conn, cardID, 0)
    print("Card", cardID, "assigned to employee", employeeID)


def unassign_card(conn, cardID):
    if not card.is_card_existing(conn, cardID):
        print("Card DNE!")
        return

    card.assign_card_employee(conn, cardID, 0)
    card.change_card_status(conn, cardID, 0)    
    print("Card", cardID, "unassigned")


def main():
    pass

if __name__ == '__main__':
    main()