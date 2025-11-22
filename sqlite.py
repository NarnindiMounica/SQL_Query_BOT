import sqlite3

#connect to sqlite3

connection = sqlite3.connect("student.db")

#create a cursor object to create table and insert record

cursor = connection.cursor()

#creating a table

table_info= '''

CREATE TABLE STUDENT
(
NAME VARCHAR(25),
CLASS VARCHAR(25),
SECTION VARCHAR(25),
MARKS INT
)
'''

cursor.execute(table_info)

#inserting records into table
cursor.execute('''INSERT INTO STUDENT VALUES("Mounica", "AI", "A", 98) ''')
cursor.execute('''INSERT INTO STUDENT VALUES("Ram", "Data Science", "A", 78)''')
cursor.execute('''INSERT INTO STUDENT VALUES("Gaurav", "AI", "B", 58)''')
cursor.execute('''INSERT INTO STUDENT VALUES("John", "SQL", "A", 96 )''')
cursor.execute('''INSERT INTO STUDENT VALUES("Sara", "Data Science", "B", 66 )''')

#display all the records
print("The inserted records are:")
data=cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
    print(row)

#commit changes in DB
connection.commit()

#close connection to DB
connection.close()



