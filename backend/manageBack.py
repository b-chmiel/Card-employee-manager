import datetime 
import sqlite3

import managers.terminalCard as terminalCard
import managers.card as card
import managers.day as day
import managers.incident as incident
import managers.terminal as terminal
import managers.employee as employee
import mqttBroker


database = r"database/employee.db"
conn = sqlite3.connect(database)


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


def make_action(arguments):
    choice = arguments.method_name
    
    if choice == 'add':
        if arguments.e:
            add_employee(conn, arguments.e[0], arguments.e[1])
        if arguments.t:
            add_terminal(conn, arguments.t)
        if arguments.c:
            add_card(conn, arguments.c) 
        if not arguments.e and not arguments.t and not arguments.c:
            print("Provide object to add: [-e Name Surname] [-t ID] [-c ID]")
    elif choice == 'delete':
        if arguments.e:
            delete_employee(conn, arguments.e)
        if arguments.t:
            delete_terminal(conn, arguments.t)
        if arguments.c:
            delete_card(conn, arguments.c)  
        if not arguments.e and not arguments.t and not arguments.c:
            print("Provide object to delete: [-e ID] [-t ID] [-c ID]")     
    elif choice == 'list':
        if arguments.objects == 'employees':
            list_employees(conn)
        if arguments.objects == 'terminals':
            list_terminals(conn)
        if arguments.objects == 'cards':
            list_cards(conn)
        if arguments.objects == 'days':
            list_days(conn)
        if arguments.objects == 'incidents':
            list_incidents(conn)     
    elif choice == 'raport':
        raport(conn, arguments.employeeID)
    elif choice == 'assign':
        assign_card_employee(conn, arguments.cardID, arguments.employeeID)
    elif choice == 'unassign':
        unassign_card(conn, arguments.cardID)
    '''
    elif choice == 'mqtt':
        if arguments.action == 'start':
            import subprocess
            subprocess.call(['python mqttBroker.py'])
            pass
        #elif arguments.action == 'stop':
         #   mqttBroker.stop()     
    '''

def test():
    add_employee(conn, "John", "Snow")
    add_employee(conn, "John", "Snow")
    add_terminal(conn, 8)
    add_terminal(conn, 8)
    add_card(conn, 1)
    add_card(conn, 1)

    delete_employee(conn, 1)
    delete_employee(conn, 1)
    delete_terminal(conn, 1)
    delete_terminal(conn, 1)
    delete_card(conn, 97)
    delete_card(conn, 97)

    list_employees(conn)
    list_cards(conn)
    list_incidents(conn)

    raport(conn, 1)
    raport(conn, 2)
    
    assign_card_employee(conn, 100, 3)
    unassign_card(conn, 1)
    unassign_card(conn, 100)
    

def main():
    #test()
    pass

if __name__ == '__main__':
    main()