import sqlite3

path = "/Users/ashutosh/The_Great_Eye/Test_dir/Puja' 24 and Bhavesh lagn/processed.db"
conn = sqlite3.Connection(path)
c = conn.cursor()

res = c.execute("SELECT hashCode FROM processedImages")
res = list(res.fetchall())

list_of_strings = []
for item in res:
    for string in item:
        list_of_strings.append(string)

print(list_of_strings)

code = "7e3e14770597434809145291b875903d"

if code in list_of_strings:
    print('hello')
else:
    print('no')

conn.close