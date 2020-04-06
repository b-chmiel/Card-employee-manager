import argparse
import sqlite3
import paho.mqtt.client as mqtt

import backend.manageBack as manageBack

'''
client_name = "Client1"
host_name = "192.168.0.41"
client = mqtt.Client(client_name)
client.connect(host_name)
'''

def main():
    #test()
    manageBack.make_action(parser_function())
    #client.publish("system/manager/set", str(parser_function()))
    #client.subscribe("system/manager/get")


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


if __name__ == "__main__":
    main()
