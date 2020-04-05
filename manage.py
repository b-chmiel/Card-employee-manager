import argparse
import sqlite3

import backend.manageBack as manageBack

database = r"database/employee.db"
conn = sqlite3.connect(database)



def main():
    #test()
    make_action(parser_function())


def make_action(arguments):
    choice = arguments.method_name
    
    if choice == 'add':
        if arguments.e:
            manageBack.add_employee(conn, arguments.e[0], arguments.e[1])
        if arguments.t:
            manageBack.add_terminal(conn, arguments.t)
        if arguments.c:
            manageBack.add_card(conn, arguments.c) 
        else:
            print("Provide object to add: [-e Name Surname] [-t ID] [-c ID]")
    elif choice == 'delete':
        if arguments.e:
            manageBack.delete_employee(conn, arguments.e)
        if arguments.t:
            manageBack.delete_terminal(conn, arguments.t)
        if arguments.c:
            manageBack.delete_card(conn, arguments.c)  
        else:
            print("Provide object to delete: [-e ID] [-t ID] [-c ID]")     
    elif choice == 'list':
        if arguments.objects == 'employees':
            manageBack.list_employees(conn)
        if arguments.objects == 'terminals':
            manageBack.list_terminals(conn)
        if arguments.objects == 'cards':
            manageBack.list_cards(conn)
        if arguments.objects == 'days':
            manageBack.list_days(conn)
        if arguments.objects == 'incidents':
            manageBack.list_incidents(conn)     
    elif choice == 'raport':
        manageBack.raport(conn, arguments.employeeID)
    elif choice == 'assign':
        manageBack.assign_card_employee(conn, arguments.cardID, arguments.employeeID)
    elif choice == 'unassign':
        manageBack.unassign_card(conn, arguments.cardID)


def parser_function():
    parser = argparse.ArgumentParser(description="Manager of employee-card system")
    subparsers = parser.add_subparsers(dest='method_name', description="Main commands to change system state", required=True, title="Main command")
    add_subparser = subparsers.add_parser('add', description="Adding new objects to system")
    add_subparser.add_argument('-e', type=str, metavar='N', nargs=2, help='Name and surname of employee')
    add_subparser.add_argument('-t', type=int, metavar='terminalID')
    add_subparser.add_argument('-c', type=int, metavar='cardID')
    delete_subparser = subparsers.add_parser('delete')
    delete_subparser.add_argument('-e', type=int, metavar='employeeID')
    delete_subparser.add_argument('-t', type=int, metavar='terminalID')
    delete_subparser.add_argument('-c', type=int, metavar='cardID')
    list_subparser = subparsers.add_parser('list')
    list_subparser.add_argument('objects', choices={'employees', 'terminals', 'cards', 'days', 'incidents'})
    raport_subparser = subparsers.add_parser('raport')
    raport_subparser.add_argument('employeeID', type=int)
    assign_subparser = subparsers.add_parser('assign')
    assign_subparser.add_argument('cardID', type=int)
    assign_subparser.add_argument('employeeID', type=int)
    raport_subparser = subparsers.add_parser('unassign')
    raport_subparser.add_argument('cardID', type=int)

    return parser.parse_args() 


def test():
    manageBack.add_employee(conn, "John", "Snow")
    manageBack.add_employee(conn, "John", "Snow")
    manageBack.add_terminal(conn, 8)
    manageBack.add_terminal(conn, 8)
    manageBack.add_card(conn, 1)
    manageBack.add_card(conn, 1)

    manageBack.delete_employee(conn, 1)
    manageBack.delete_employee(conn, 1)
    manageBack.delete_terminal(conn, 1)
    manageBack.delete_terminal(conn, 1)
    manageBack.delete_card(conn, 97)
    manageBack.delete_card(conn, 97)

    manageBack.list_employees(conn)
    manageBack.list_cards(conn)
    manageBack.list_incidents(conn)

    manageBack.raport(conn, 1)
    manageBack.raport(conn, 2)
    
    manageBack.assign_card_employee(conn, 100, 3)
    manageBack.unassign_card(conn, 1)
    manageBack.unassign_card(conn, 100)
    

if __name__ == "__main__":
    main()
