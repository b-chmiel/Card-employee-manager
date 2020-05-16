import sqlite3

def create_incident(conn, terminalID, cardID, time):
    '''
    Inserts incident data to db

    return: index of incident
    '''
    sql = ''' insert into incident(TerminalID, CardID, TimeOfUsage) values(?, ?, ?) '''

    c = conn.cursor()

    c.execute(sql, (terminalID, cardID, time))
    conn.commit()
    return  c.lastrowid

def get_incident_info(conn):
    '''
    return: incidents data
    '''
    
    c = conn.cursor()

    c.execute("select * from incident")
    return c.fetchall()

