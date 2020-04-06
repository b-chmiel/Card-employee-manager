import argparse
import sqlite3

import backend.terminalBack as terminalBack

#TODO check if connected

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("terminalID", help="TerminalID which will be emulated", type=int)
    args = parser.parse_args()

    print("To exit write \"exit\"")
    while terminalBack.run(args.terminalID):
        pass


if __name__ == "__main__":
    main()   