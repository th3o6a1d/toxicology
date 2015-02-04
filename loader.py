import os,re
import MySQLdb

conn = MySQLdb.connect(host="localhost", user="root", passwd="dwdstudent2015", db="msds")
cur = conn.cursor()


result = [os.path.join(dp, f) for dp, dn, filenames in os.walk('.') for f in filenames if os.path.splitext(f)[1] == '.txt']
count, error, id = [0,0,0]

def try_regex(regex,s,rnl=True):
  global error, count
  if not rnl:
    result = [re.sub('\n','`',i.group(1))for i in re.finditer(regex,s)]
  else:
    result = [re.sub('\n','',i.group(1)) for i in re.finditer(regex,s)]
  count += 1
  if result == []:
    error += 1
    return ['']
  return result

for f in result:
  f = open(f,'r').read()
  s = re.sub(' +',' ',f)
  id+=1
  prodid = try_regex('Product ID:(.*)\n',s)[0]
  msdsnum = try_regex('MSDS Number: (.*)\n',s)[0]
  msdsdate = try_regex('Date:(.*)\n',s)[0]
  respparty = try_regex('Company Name:(.*)\n',s)[0]
  firstaidfull = try_regex('First Aid:([^=]*)',s)[0]
  ingredients = try_regex('Ingred Name:(.*\n.*)\n',s,rnl=False)
  ingredientsfull = "|".join(ingredients)
  ld50 = try_regex('LD50 LC50 Mixture:(.*)\n',s)
  hazards = try_regex('Health Hazards Acute and Chronic:(.*)Explan',re.sub('\n',' ',s))[0]
  carcino = try_regex('Reports of Carcinogenicity:(.*)\n',s)[0]
  overexp = try_regex('Effects of Overexposure:([^=]*)',s)[0]

  cur.execute("""INSERT INTO product VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(id,prodid,msdsnum,msdsdate,respparty,firstaidfull,ingredientsfull,overexp,ld50,carcino,hazards))
  conn.commit()


print 'Error rate: ', 1.0*error/count

conn.close()


