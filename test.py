import pymysql

def getProfile():
    connection = pymysql.connect(host="localhost", user="root", password="", database="facebase")
    conn = connection.cursor()
    sql = "SELECT P_ID FROM people order by P_ID desc limit 1;"
    conn.execute(sql)
    profile=0
    for row in conn:
        profile=row
    connection.close()
    global c
    c = int(''.join(map(str, profile)))
    return c

h=getProfile()
Id= h + 1
print(h)
print(Id)