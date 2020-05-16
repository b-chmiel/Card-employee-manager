import sqlite3


def create_card(conn, cardID):
    '''
    Creates new card and adds it to db

    return: cardID or -1 if card exists
    '''
    # TODO type checking
    
    if is_card_existing(conn, cardID):
        return -1
    
    sql = ''' insert into card(ID) values(?) '''

    c = conn.cursor()

    c.execute(sql, (cardID,))
    conn.commit()
    c.close()
    return cardID  


def assign_card_employee(conn, cardID, employeeID):
    '''
    Assigning card without checking anything
    
    return: cardID
    '''
    sql = ''' update card
                set EmployeeID = ?
            where
                ID = ? '''

    c = conn.cursor()

    c.execute(sql, (employeeID, cardID))
    conn.commit()
    c.close()
    return cardID            


def get_cards_employees(conn):
    '''
    return: cards contents
    '''
    c = conn.cursor()

    c.execute("select * from card")
    return c.fetchall()


def is_card_existing(conn, cardID):
    sql = ''' select * from card where ID = ? '''

    c = conn.cursor()

    c.execute(sql, (cardID,))
    conn.commit()
    return len(c.fetchall())

def was_used_today(conn, cardID):
    '''
    Check if card was used to create day table

    return: 
             greater than 0 if was used (gives day number)
             0 if was not used
            -1 if DNE
            -2 if is not assigned
    '''
    
    if not is_card_existing(conn, cardID):
        return -1
    sql = ''' select * from card where ID = ? '''
    c = conn.cursor()

    c.execute(sql, (cardID,))
    card_info = c.fetchone()
    
    #if card is not assigned
    if card_info[1] == 0:
        return -2

    return card_info[2]

def change_card_status(conn, cardID, status):
    '''
    Changes value of wasUsedToday field
    Sets given status

    return: current status, -1 if card DNE
    '''

    if not is_card_existing(conn, cardID):
        return -1

    sql = ''' update card
                    set WasUsedToday = ?
                where
                    ID = ? '''

    c = conn.cursor()

    c.execute(sql, (status, cardID))
    conn.commit()
    return status

    
def get_assigned_employee(conn, cardID):
    '''
    return: 
            -1 if card DNE
            0 if card is not assigned
            employeeID otherwise
    '''        
    if not is_card_existing(conn, cardID):
        return -2

    sql = ''' select * from card where ID = ? '''
    c = conn.cursor()

    c.execute(sql, (cardID,))
    card_info = c.fetchone()
    
    return card_info[1]    


def delete_card(conn, cardID):
    '''
    Deletes card entry from card table

    return: -1 if card DNE cardID otherwise
    '''

    if not is_card_existing(conn, cardID):
        return -1

    sql = ''' delete from card where ID = ? '''

    c = conn.cursor()
    c.execute(sql, (cardID,))
    conn.commit()
    c.close()
    return cardID


