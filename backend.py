import sqlite3
from basic import getCreateStatement, getVariables
from scouts import add_scout

database = "data.db"
comma_num=len(getVariables())-1

def connect():
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    statement = getCreateStatement()
    cur.execute(statement)
    conn.commit()
    conn.close()

def insert(data):
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("INSERT INTO performance VALUES ("+("?,"*comma_num)+"?)", data)
    conn.commit()
    conn.close()

def unique(team, match):
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("SELECT * FROM performance WHERE team="+team+" and match="+ match)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return len(rows)==0

def view():
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("SELECT * FROM performance")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def search(team):
    try:
        conn=sqlite3.connect(database)
        cur=conn.cursor()
        cur.execute("SELECT * FROM performance WHERE team="+ team)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        rows = sorted(rows, key=lambda x:x[0])
        print(rows)
        return rows
    except Exception:
        return []

def deleteByID(team, match):
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute("DELETE FROM performance WHERE team=" + team + " and match=" + match)
    conn.commit()
    conn.close()

def convert_base(num, base, length):
    decimal_num = int(num, 32)
    result = ""
    while decimal_num > 0:
        result = str(decimal_num % base) + result
        decimal_num = decimal_num // base
    result = [*result]
    if len(result)<length:
        result = ["0"]*(length-len(result))+result
    return result

def parse(csv_line):
    data = csv_line.split(",")
    initials = data[0]
    match = int(data[1])
    team = int(data[2])
    if unique(team, match):
        add_scout(initials, match, team)
        part1 = convert_base(data[7], 5, 9)
        part2 = convert_base(data[8], 3, 27)
        part3 = convert_base(data[9], 2, 18)
        output = data[1:7]+part1+part2+part3+data[10:]
        return [int(i) for i in output]
    else:
        return []


def add2db(csv_line):
    parsed = parse(csv_line)
    if parsed!=[]:
        try: 
            insert(parsed)
            return True
        except:
            return False
    return False

connect()