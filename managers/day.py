import sqlite3


def create_day(conn, cardID, employeeID, time_start, terminal_start):
    '''
    Creates day entry which is only created
    when employee used his card first time in day

    return: dayID
    '''

    sql = ''' insert into day(CardID, EmployeeID, TimeStart, TerminalStart) values(?, ?, ?, ?) '''

    c = conn.cursor()

    c.execute(sql, (cardID, employeeID, time_start, terminal_start))
    conn.commit()
    return  c.lastrowid


def update_day(conn, dayID, time_end, terminal_end):
    '''
    Updates day entry which was created previously iff 
    employee second time uses his card

    return: dayID
    '''

    if not is_day_exists(conn, dayID):
        return -1

    sql = ''' update day
    set TimeEnd = ?,
    TerminalEnd = ?
    where ID = ? '''

    c = conn.cursor()

    c.execute(sql, (time_end, terminal_end, dayID))
    conn.commit()
    return  c.lastrowid

def get_day(conn, dayID):
    '''
    return: day with given dayID
    '''

    if not is_day_exists(conn, dayID):
        return -1

    sql = ''' select * from day where ID = ? '''

    c = conn.cursor()

    c.execute(sql, (dayID,))
    return c.fetchall()

def get_days(conn):
    '''
    return: all day entries from db
    '''

    c = conn.cursor()

    c.execute("select * from day")
    return c.fetchall()

def is_day_exists(conn, dayID):
    '''
    return: 1 if exists 0 otherwise
    '''
    
    sql = ''' select * from day where ID = ? '''

    c = conn.cursor()

    c.execute(sql, (dayID,))
    conn.commit()
    return len(c.fetchall())


