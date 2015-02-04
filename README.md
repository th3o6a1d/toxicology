# Building a Poison Control API and Emergency Text System from MSDS Data Sheets
1. The Goal
2. The Data
3. Building the Database
4. Serving up JSON with Flask
5. Creating an Emergency Text Message System with Twilio

## 1. The Goal:
To create a poison control database with information contained in freely available Material Safety Data Sheets. 

To 

To enable a user to receive first aid information via a 

## 1. The Data

The data consist of 230,000 material safety data sheets stored in alphabetically-organized .txt files, most of which are in a standard [format](https://www.osha.gov/Publications/OSHA3514.html) with a predictable structure. The files are available as a public Amazon EBS snapshot `snap-a966d1c8`, which we mounted to our DwD instance following [these](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html) instructions. The data were submitted by Infochimps to Amazon and are said to come from [hazard.com](hazard.com), which is run by Vermont Safety Information Resources, inc.