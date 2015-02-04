import os,re
import MySQLdb as mdb

conn = mdb.connect(host="localhost", user="root", passwd="dwdstudent2015", db="msds")
cur = conn.cursor(mdb.cursors.DictCursor)

error = 0
pk = 0
r = 0
queries = ["SELECT * FROM msds.product WHERE id >"+str(i*10000)+" LIMIT 10000;" for i in range(25)]

regex = re.compile(r'(\.\s+|^)([ \w\/]+):(.*?)(?=(\.[\w \/]+:|\n))')

def ss(s):
  return re.sub(' +',' ',s)

for query in queries:
  cur.execute(query)
  rows = cur.fetchall()

  for row in rows:
    id = row['id']
    firstaid = row['firstaidfull']
    matches = regex.finditer(firstaid)
    for match in matches: 
      pk += 1
      roe = ss(match.group(2))
      inst = ss(match.group(3))
      cur.execute("""INSERT INTO firstaid VALUES (%s,%s,%s,%s)""",(pk,roe,inst,id))
      conn.commit()

print pk
conn.close()

















