import os,re
import MySQLdb as mdb

conn = mdb.connect(host="localhost", user="root", passwd="", db="msds")
cur = conn.cursor(mdb.cursors.DictCursor)

error = 0
pk = 0
r = 0
queries = ["SELECT * FROM msds.product WHERE id >"+str(i*10000)+" LIMIT 10000;" for i in range(25)]

for query in queries:
  cur.execute(query)
  rows = cur.fetchall()
  for row in rows:
    ident = row['id']
    ingredients = [i.split('`') for i in row['ingredientsfull'].split('|')]
    for ingredient in ingredients: 
      try:
        i = ingredient[0]
        cas = str(ingredient[1])
        if cas[0:4] != 'CAS:':
          cas = ''
        elif cas[0:4] != '':
          cas = cas[4:]
        pk+=1
        cur.execute("""INSERT INTO ingredients VALUES (%s,%s,%s,%s)""",(pk,i,cas,ident))
        conn.commit()
      except:
        error += 1
print error
conn.close()
