import sqlite3


def create_terminal(conn, terminalID):
    '''
    Creates terminal entry
    
    return: terminalID or -1 if terminal exists
    '''

    # TODO type checking
    
    if is_terminal_existing(conn, terminalID):
        return -1
    
    sql = ''' insert into terminal(ID) values(?) '''

    c = conn.cursor()

    c.execute(sql, (terminalID,))
    conn.commit()
    c.close()
    return terminalID             
    

def delete_terminal(conn, terminalID):
    '''
    Deletes terminal entry from terminal table

    return: -1 if terminal DNE terminalID otherwise
    '''

    if not is_terminal_existing(conn, terminalID):
        return -1

    sql = ''' delete from terminal where ID = ? '''

    c = conn.cursor()
    c.execute(sql, (terminalID,))
    conn.commit()
    c.close()
    return terminalID       


def is_terminal_existing(conn, terminalID):
    '''
    return: 0 if DNE 1 otherwise
    '''
    
    sql = ''' select * from terminal where ID = ? '''

    c = conn.cursor()

    c.execute(sql, (terminalID,))
    conn.commit()
    return len(c.fetchall())


def get_terminals(conn):
    '''
    return: all terminals
    '''
    sql = ''' select * from terminal '''
    
    c = conn.cursor()

    c.execute(sql)
    conn.commit()
    return c.fetchall()
