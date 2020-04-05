PRAGMA foreign_keys = OFF;

drop table if exists employee;
drop table if exists terminal;
drop table if exists card;
drop table if exists day;
drop table if exists terminalCard;
drop table if exists incident;

PRAGMA foreign_keys = ON;

--Stores employee data
create table employee
(
    ID integer not null primary key autoincrement,
    Name varchar(255) not null,
    Surname varchar(255) not null
);

--Stores currently registered terminals
create table terminal
(
    ID integer not null primary key
);

--Stores cards and their association with employees and 
--whether card was used to create/update day table
create table card
(
    ID integer not null primary key,
    EmployeeID integer default 0,
    WasUsedToday integer default 0

    --foreign key (EmployeeID) references employee(ID)
);

--Keeps track of employee working time and 
--other metadata
create table day
(
    ID integer not null primary key autoincrement,
    CardID integer,
    EmployeeID integer,
    TimeStart timestamp,
    TimeEnd timestamp,
    TerminalStart integer,
    TerminalEnd integer,

    foreign key (CardID) references card(ID),
    foreign key (EmployeeID) references employee(ID),
    foreign key (TerminalStart) references terminal(ID),
    foreign key (TerminalEnd) references terminal(ID)
);

--Keeps terminal registry of when and what card was used in 
--certain terminal
create table terminalCard
(
    ID integer primary key autoincrement,
    TerminalID integer,
    CardID integer,
    TimeOfUsage timestamp,

    foreign key (TerminalID) references terminal(ID),
    foreign key (CardID) references card(ID)

);

--Keeps data about incidents(usage of unregistered card or 
--unassigned to employee)
create table incident
(
    ID integer primary key autoincrement,
    TerminalID integer,
    CardID integer,
    TimeOfUsage timestamp,

    foreign key (TerminalID) references terminal(ID),
    foreign key (CardID) references card(ID)
);

insert into employee(Name, Surname) values ('John', 'Smith');
insert into employee(Name, Surname) values ('Jan', 'Kowalski');
insert into employee(Name, Surname) values ('John', 'Brown');
insert into employee(Name, Surname) values ('Krystian', 'Zimerman');

insert into terminal(ID) values (1);
insert into terminal(ID) values (2);

insert into card(ID, EmployeeID, WasUsedToday) values (97, 1, 0);
insert into card(ID, EmployeeID, WasUsedToday) values (98, 2, 0);
insert into card(ID, EmployeeID, WasUsedToday) values (99, 3, 0);
insert into card(ID, EmployeeID, WasUsedToday) values (100, 0, 0);