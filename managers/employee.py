import sqlite3

#employee
def get_all_employees(conn):
    '''
    return: all employee entries
    '''

    c = conn.cursor()

    c.execute("select * from employee")
    return c.fetchall()

def get_employee(conn, employeeID):
    '''
    return: employee with employeeID
    '''

    sql = ''' select * from employee where ID = ? '''

    c = conn.cursor()

    c.execute(sql, (employeeID,))
    return c.fetchall()

def get_employee_Name(conn, Name, Surname):
    '''
    return: employee with specified Name and Surname
    '''

    sql = ''' select * from employee where Name = ? and Surname = ?'''

    c = conn.cursor()

    c.execute(sql, (Name, Surname))
    return c.fetchall()



def get_assigned_card(conn, employeeID):
    '''
    return: 
            -1 if employee DNE
            0 if card is not assigned
            cardID otherwise
    '''        
    if not get_employee(conn, employeeID):
        return -1

    sql = ''' select * from card where EmployeeID = ? '''
    c = conn.cursor()

    c.execute(sql, (employeeID,))
    card_info = c.fetchone()
    
    if card_info != None:
        return card_info[0]

    return 0


def get_day_of_employee(conn, employeeID):
    '''
    return: all days of given employee or -1 if employee DNE
    '''
    if not get_employee(conn, employeeID):
        return -1

    sql = ''' select * from day where EmployeeID = ? '''

    c = conn.cursor()

    c.execute(sql, (employeeID,))
    return c.fetchall()

def create_employee(conn, Name, Surname):
    '''
    Creates new employee with Name and Surname

    return: employeeID or -1 if employee exists
    '''

      # TODO type checking
    
    if len(get_employee_Name(conn, Name, Surname)):
        return -1
    
    sql = ''' insert into employee(Name, Surname) values(?, ?) '''

    c = conn.cursor()

    c.execute(sql, (Name, Surname))
    conn.commit()
    c.close()
    return c.lastrowid    

def remove_employee(conn, employeeID):
    '''
    Removes employee from employee table

    return: -1 if employee DNE, employeeID otherwise
    '''

    if not get_employee(conn, employeeID):
        return -1

    sql = ''' delete from employee where ID = ? '''

    c = conn.cursor()
    c.execute(sql, (employeeID,))
    conn.commit()
    c.close()
    return employeeID    

