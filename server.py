from flask import Flask, request, json, Response
from datetime import datetime
import cgi
import re
import MySQLdb
import threading

webserver = Flask("test")
conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="dwdstudent2015", db="msds")
cur = conn.cursor()

def clean_up(string):
    try:
        return string.strip()
    except:
        return string

@webserver.route("/<search>")
def api(search):
    search = re.sub(r'\W+', '', search)
    query = """select prodid, ingredient, cas, roe, instructions, 
    oralLD50, oralLD50units, overexp, carcino, hazards, msdsnum, msdsdate from product p 
    join ingredients i on i.product_id = p.id
    join firstaid f on f.product_id = p.id
    where soundex(prodid) = soundex('%s')
    order by levenshtein(prodid,'%s') asc limit 2000;""" % (search,search)

    cur.execute(query)
    output = {}
    data = cur.fetchall()
    for row in data:
        if row[0] not in output and len(output.keys())<5:
            output[row[0]] = {'ingredients':[],'firstaid':[], 'oralLD50': None, 'oralLD50units': None}
    for row in data:
        if row[0] in output:
            cas = row[2]
            if cas == '':
                cas = None
            ingred = {'name':row[1],'cas':cas}
            if ingred not in output[row[0]]['ingredients']:
                output[row[0]]['ingredients'].append(clean_up(ingred))
            fa = {'roe':clean_up(row[3]),'instruction':clean_up(row[4])}
            if fa not in output[row[0]]['firstaid']:
                output[row[0]]['firstaid'].append(clean_up(fa))

            output[row[0]]['oralLD50'] = clean_up(row[5])
            output[row[0]]['oralLD50units'] = clean_up(row[6])
            output[row[0]]['overexp'] = clean_up(row[7])
            output[row[0]]['carcino'] = clean_up(row[8])
            output[row[0]]['hazards'] = clean_up(row[9])
            output[row[0]]['msdsnum'] = clean_up(row[10])
            try:
                output[row[0]]['msdsdate'] = datetime.strptime(re.sub('[\.\/\-\ ]',' ',row[11]), '%m %d %Y')
            except:
                output[row[0]]['msdsdate'] = row[11]
    return Response(json.dumps(output),  mimetype='application/json')

@webserver.route("/",methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        a = request.form["Body"]
	s = re.sub('\W+','',a)
        query = """select prodid, firstaidfull from product p
        where soundex(prodid) = soundex('%s')
        order by levenshtein(prodid,'%s') asc limit 1;""" % (s,s)
        cur.execute(query)
        row = cur.fetchone()
        if row:
            r = """<?xml version="1.0" encoding="UTF-8" ?><Response><Message>PRODUCT: %s || INSTRUCTIONS: %s </Message></Response>""" % (cgi.escape(row[0]),cgi.escape(row[1].capitalize()))
        else: 
            r = """<?xml version="1.0" encoding="UTF-8" ?><Response><Message>NONE FOUND</Message></Response>"""
        return Response(r,  mimetype='text/xml')
    return "Toxicology API!"

def start_server():
    webserver.run(host='0.0.0.0', port=80, debug = True)
    return
    
def stop_server():
    shutdown_after_request = request.environ.get('werkzeug.server.shutdown')
    shutdown_after_request()
    return
    
start_server()
