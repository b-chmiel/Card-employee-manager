import argparse
import sqlite3

import backend.terminalBack as terminalBack

database = r"database/employee.db"
conn = sqlite3.connect(database)
#TODO check if connected

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("terminalID", help="TerminalID which will be emulated", type=int)
    args = parser.parse_args()

    if not terminalBack.is_terminal_existing(conn, args.terminalID):
        print("In order to use this terminal please first register it!")
        exit()

    print("To exit write \"exit\"")
    while terminalBack.run(conn, args.terminalID):
        pass

    print("Program finished!")
    conn.close()

if __name__ == "__main__":
    main()   