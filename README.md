# Building a Poison Control API and Emergency Text System from MSDS Data Sheets
>by Jason Theobald, Carlos Capellan, and Lauren Griggs. 
1. The Goal
2. Getting the Data from Amazon AWS
3. Building the Database
4. Fun with SQL
5. Serving up JSON with Flask
6. Creating an Emergency Text Message System with Twilio

## 1. The Goal:
* To create a poison control database with information contained in freely available Material Safety Data Sheets. 
* To enable a user to receive first aid instructions and a list of ingredients in JSON-format via a Flask-powered API
* To create a Twilio-powered emergency text message system that sends a user first aid instructions for a given exposure.

## 2. Getting the Data from Amazon AWS

The data consist of ~230,000 material safety data sheets stored in alphabetically-organized folders of .txt files, most of which are in a standard [format](https://www.osha.gov/Publications/OSHA3514.html) with a predictable structure. The files are available as a public Amazon EBS snapshot `snap-a966d1c8`, which we mounted to our EC2 instance by following [these](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html) instructions. Per Amazon, the data were submitted by Infochimps and are said to come from [hazard.com](hazard.com), which is run by Vermont Safety Information Resources, inc. Most of the sheets appear to be from the 1990s. 

## 3. Building the Database

We created **three tables** (product, ingredients, firstaid). Each MSDS corresponds to one item in the product table (e.g. Glass Cleaner). Each product has one or more ingredients (e.g. Isobutane, Propane) and one or more first aid instructions corresponding to a certain route of exposure (e.g. Eyes: flush with water). 

To load the data, we started by writing a script that iterates through the many directories of `.txt` files, extracts fields matching regular expressions, and inserts them into the product table. We took advantage of the structured nature of the MSDS files while allowing for a certain degree of heterogeneity with our `try_regex()` function:

```
def try_regex(regex,s):
  global error, count
  result = [re.sub('\n','',i.group(1)) for i in re.finditer(regex,s)]
  count += 1
  if result == []:
    error += 1
    return ['']
  return result
```

For every failure of the regex to capture a specific field in the MSDS, we incremented an error variable, ending up with an overall import error rate of **~1.5%.** 

We left the first aid and ingredient information in large chunks of text or with delimeters for later parsing. After loading the product table, we wrote scripts that iterated through the product table 10,000 rows at a time and created the first aid and information tables. Finally, we used `SQL REGEXP` to create new columns (oralLD50, oralLD50units) for products with an oral [LD50](http://en.wikipedia.org/wiki/Median_lethal_dose) value.

## 4. Fun with SQL

## 5. Serving up JSON with Flask
We wanted to create an API with a simple endpoint that would allow a user to search for a product, allow for imprecise string matching, and receive the top 5 hits with associated first aid and ingredient information. 

```
curl poisons.tk/ethanol
```

The SQL query that powers our API relies on the `SOUNDEX()` algorithm to match user input to product name, then ranks the results using the `LEVENSHTEIN()` function [(non-standard)](http://stackoverflow.com/questions/13909885/how-to-add-levenshtein-function-in-mysql), which scores the 'distance' between two strings. Below is the SQL query that powers the Flask API. 

```
SELECT prodid, ingredient, cas, roe, instructions, oralLD50, oralLD50units, overexp, carcino, hazards, msdsnum, msdsdate from product p 
JOIN ingredients i ON i.product_id = p.id
JOIN firstaid f ON f.product_id = p.id
WHERE SOUNDEX(prodid) = SOUNDEX('%s')
ORDER BY LEVENSHTEIN(prodid,'%s') ASC
LIMIT 5;
```

## 6. Creating an Emergency Text Message System with Twilio
>`In case of emergency, text the the name of product to: (479) 431-2442`

We wanted a user to be able to text a product name to a phone number and receive immediate first aid instructions in the event of an exposure. [Twilio](twilio.com) is a fantastic service that allows a user to purchase phone numbers and program them to send a POST request upon receipt of a text message. This POST request gets sent to the Flask API, which returns an XML response, which is then interpreted and parsed into a response SMS by Twilio. 

## Next Steps
Continue to improve database. List on Mashape as freemium API. 























