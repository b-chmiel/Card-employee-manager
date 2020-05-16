import sqlite3


def create_terminal_card(conn, terminalID, cardID, time):
    '''
    Creates terminalCard entry
    Used to keep track of all card transactions

    return: terminalCardID
    '''

    sql = ''' insert into terminalCard(TerminalID, CardID, TimeOfUsage) values(?, ?, ?) '''

    c = conn.cursor()

    c.execute(sql, (terminalID, cardID, time))
    conn.commit()
    return  c.lastrowid

def get_terminal_info(conn, terminalID):
    '''
    return: all transactions from certain terminal
    '''
    
    from .terminal import is_terminal_existing

    if not is_terminal_existing(conn, terminalID):
        return -1

    sql = ''' select * from terminalCard where TerminalID = ? '''
    c = conn.cursor()

    c.execute(sql, (terminalID, ))
    return c.fetchall()