import requests
import os
import pandas as pd

import pymysql
from collections import Counter
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://rakkha:Coon102PUA!@localhost/complist"
engine = create_engine(SQLALCHEMY_DATABASE_URI)


# This is SLOW! (Took just over 4 minutes when I timed it.) 
# The file is 237 MB gzipped and 5GB unzipped.
# You may want to download it once and read it from your local file system.
# You can store it compressed, pandas has no problem reading compressed files.
# If you only need data for a specific state, consider changing both occurrences of 
# `us` to the appropriate state code
# (Start at https://lehd.ces.census.gov/data/lodes/LODES7/ if you want to check it out more)

"""
df = pd.read_csv('/Users/rakkhas/Downloads/us_xwalk.csv.gz')

# Data State Groups
sql = 'DROP TABLE tbl_State;\n\n'
sql = sql + '\nCREATE TABLE tbl_State ('
sql = sql + '\nFIPSStateCode INT'
sql = sql + '\n,USPSStateCode VARCHAR(2)'
sql = sql + '\n,StateName VARCHAR(100)'
sql = sql + '\n,PRIMARY KEY(FIPSStateCode)'
sql = sql + '\n);'

sql = sql + '\nINSERT INTO tbl_State(FIPSStateCode, USPSStateCode, StateName)'
firstRow = True

states = df[['st', 'stusps', 'stname']].drop_duplicates().sort_values(by='st', ascending=True, na_position='first')
for index, row in states.iterrows():
    if firstRow == True:
      sql = sql + "\nVALUES (" + str(row['st']) + ",'" + str(row['stusps']) + "','" +  str(row['stname']) + "')"
      firstRow = False
    else:
        sql = sql + "\n,(" + str(row['st']) + ",'" + str(row['stusps']) + "','" +  str(row['stname']) + "')"
sql = sql + '\n);'


if os.path.exists("states.sql"):
  os.remove("states.sql")

f = open("states.sql", "w")
f.write(sql)
f.close()
"""

"""
df = pd.read_csv('/Users/rakkhas/Downloads/us_xwalk.csv.gz',
                 usecols=[12],
                 dtype={
                   'zcta': 'object'
                 })

df3 = df.drop_duplicates().sort_values(by='zcta', ascending=True, na_position='first')

sql = 'INSERT INTO tbl_Zip(ZipCode)'
firstRow = True

for index, row in df3.iterrows():
    if firstRow == True:
      sql = sql + "\nVALUES ('" + str(row['zcta']) + "')"
      firstRow = False
    else:
        sql = sql + "\n,('" + str(row['zcta']) + "')"
sql = sql + '\n;'

if os.path.exists("zipcodes.sql"):
  os.remove("zipcodes.sql")

f = open("zipcodes.sql", "w")
f.write(sql)
f.close()
"""


"""
df = pd.read_csv('/Users/rakkhas/Downloads/us_xwalk.csv.gz',
                 usecols=[1,12],
                 dtype={
                   'st': 'int', 
                   'zcta': 'str'
                 })

df3 = df.drop_duplicates().sort_values(by=['st','zcta'], ascending=True, na_position='first')

sql = 'INSERT INTO tbl_ZipInState(FIPSStateCode, ZipCode)'
firstRow = True

for index, row in df3.iterrows():
    if firstRow == True:
      sql = sql + "\nVALUES (" + str(row['st']) + ",'" +  str(row['zcta']) + "')"
      firstRow = False
    else:
        sql = sql + "\n,(" + str(row['st']) + ",'" +  str(row['zcta']) + "')"
sql = sql + ';'

if os.path.exists("zipcodesinstate.sql"):
  os.remove("zipcodesinstate.sql")

f = open("zipcodesinstate.sql", "w")
f.write(sql)
f.close()
"""

"""
df = pd.read_csv('/Users/rakkhas/Downloads/us_xwalk.csv.gz',
                 usecols=[4, 5],
                 dtype={
                   'cty': 'object',
                   'ctyname': 'object'
                 })
sql = 'INSERT INTO tbl_County(FIPSCountyCode, FIPSCountyName)'
firstRow = True

county = df[['cty', 'ctyname']].drop_duplicates().sort_values(by='cty', ascending=True, na_position='first')
for index, row in county.iterrows():
    if firstRow == True:
      sql = sql + '\nVALUES ("' + str(row['cty']) + '","' +  str(row['ctyname']) + '")'
      firstRow = False
    else:
        sql = sql + '\n,("' + str(row['cty']) + '","' +  str(row['ctyname']) + '")'
sql = sql + ';'


if os.path.exists("county.sql"):
  os.remove("county.sql")

f = open("county.sql", "w")
f.write(sql)
f.close()
"""


"""
df = pd.read_csv('/Users/rakkhas/Downloads/us_xwalk.csv.gz',
                 usecols=[4, 12],
                 dtype={
                   'cty': 'object',
                   'zcta': 'object'
                 })

sql = 'INSERT INTO tbl_ZipInCounty(ZipCode, FIPSCountyCode)'
firstRow = True

county = df[['zcta', 'cty']].drop_duplicates().sort_values(by='cty', ascending=True, na_position='first')
for index, row in county.iterrows():
    if firstRow == True:
      sql = sql + "\nVALUES ('" + str(row['zcta']) + "','" +  str(row['cty']) + "')"
      firstRow = False
    else:
        sql = sql + "\n,('" + str(row['zcta']) + "','" +  str(row['cty']) + "')"
sql = sql + '\n);'

if os.path.exists("county.sql"):
  os.remove("county.sql")

f = open("county.sql", "w")
f.write(sql)
f.close()
"""


"""
# Add dataset into mysql database
df = pd.read_csv('/Users/rakkhas/Downloads/ACSDP5Y2019.csv').drop([0])
# Don't forget to set SET GLOBAL innodb_strict_mode = 0;
df.to_sql('tbl_AmericanCommunitySurveyZipCodeDirty', con = engine, if_exists = 'replace')
"""

"""
def fixPlace(place):
  if place.endswith(" CDP"):
    place = place[:-4]
  elif place.endswith(" village"):
    place = place[:-8]
  elif place.endswith(" zona urbana"):
    place = place[:-12]
  elif place.endswith(" comunidad"):
    place = place[:-10]
  elif place.endswith(" city"):
    place = place[:-5]
  elif place.endswith(" town"):
    place = place[:-5]
  elif place.endswith(" borough"):
    place = place[:-8]
  elif place.endswith(" municipality"):
    place = place[:-13]

  return place

df = pd.read_csv('/Users/rakkhas/Downloads/us_xwalk.csv.gz',
                 usecols=[12,15],
                 dtype={
                   'zcta': 'object',
                   'stplcname': 'object'
                 })
sql = '\nINSERT INTO tbl_Place(ZipCode, Place)'
firstRow = True

states = df[['zcta', 'stplcname']].drop_duplicates().sort_values(by='zcta', ascending=True, na_position='first')
for index, row in states.iterrows():
    if str(row['stplcname']) == 'nan':
      continue

    if firstRow == True:
      sql = sql + '\nVALUES ("' + str(row['zcta']) + '","' +  fixPlace(str(row['stplcname'])[:-4]) + '")'
      firstRow = False
    else:
        sql = sql + '\n,("' + str(row['zcta']) + '","' +  fixPlace(str(row['stplcname'])[:-4]) + '")'
sql = sql + ';'


if os.path.exists("places.sql"):
  os.remove("places.sql")

f = open("places.sql", "w")
f.write(sql)
f.close()


def update(proc, args):
    output = True
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.raw_connection()    
    try:
        cursor = connection.cursor()
        cursor.callproc(proc, args)
        cursor.close()
        connection.commit()        
    except Exception as inst:
        print(inst)
        output = False
    finally:
        connection.close()
    return output

def convertNum(s):
  return s


"""


"""
df = pd.read_csv('/Users/rakkhas/Downloads/us_xwalk.csv.gz',
                 usecols=[1,2,4,5,12,13],
                 dtype={
                   'st': 'object', 
                   'stusps': 'object',
                   'city': 'object',
                   'cityname': 'object',
                   'zcta': 'object',
                   'zctaname': 'object'
                 })


print(df.head(20))

df = df.drop_duplicates().sort_values(by=['st','zcta'])

zip_count = Counter(df['zcta'])             
df['num_states'] = df['zcta'].apply(lambda x: zip_count[x])
df.to_csv('state_zcta_xref.csv',index=False)
"""

"""
def getValue(key, json):
  if key in json['variables'][j]:
    return str(json['variables'][j][key]).replace('"very well"', 'very well')
  return ""


# Data Profile Groups
sql = 'DROP TABLE IF EXISTS DataProfileGroup;\n'
sql = sql + 'DROP TABLE IF EXISTS DataProfile;\n'

sql = sql + '\nCREATE TABLE DataProfileGroup ('
sql = sql + '\nName VARCHAR(15)'
sql = sql + '\n,Description VARCHAR(150)'
sql = sql + '\n,PRIMARY KEY(Name)'
sql = sql + '\n);'

sql = sql + '\n'

response = requests.get("https://api.census.gov/data/2015/acs/acs5/profile/groups/")
json = response.json()

sql = sql + '\nINSERT INTO DataProfileGroup(Name, Description)'
firstRow = True
for j in json['groups']:
    if firstRow == True:
        sql = sql + "\nVALUES ('" + j['name'] + "','" + j['description'] + "')"
        firstRow = False
    else:
        sql = sql + "\n,('" + j['name'] + "','" + j['description'] + "')"

sql = sql + ';\n\n'


sql = sql + 'CREATE TABLE DataProfile ('
sql = sql + '\nProfileId VARCHAR(25)'
sql = sql + '\n,Label VARCHAR(500)'
sql = sql + '\n,Concept VARCHAR(150)'
sql = sql + '\n,PredicateType VARCHAR(15)'
sql = sql + '\n,ProfileLimit VARCHAR(15)'
sql = sql + '\n,PredicateOnly VARCHAR(15)'
sql = sql + '\n,PRIMARY KEY(ProfileId)'
sql = sql + '\n);'

sql = sql + '\n'

arr = ["https://api.census.gov/data/2015/acs/acs5/profile/groups/DP04.json",
"https://api.census.gov/data/2015/acs/acs5/profile/groups/DP05.json",
"https://api.census.gov/data/2015/acs/acs5/profile/groups/DP02PR.json",
"https://api.census.gov/data/2015/acs/acs5/profile/groups/DP02.json",
"https://api.census.gov/data/2015/acs/acs5/profile/groups/DP03.json"
]

for a in arr:
  response = requests.get(a)
  json = response.json()

  sql = sql + '\nINSERT INTO DataProfile(ProfileId, Label, Concept, PredicateType, ProfileLimit, PredicateOnly)'
  firstRow = True
  for j in json['variables'].keys():
    if firstRow == True:
        sql = sql + '\nVALUES ("' + j + '","' + getValue('label', json) + '","' + getValue('concept', json) + '","' + getValue('predicateType', json) + '","' + getValue('limit', json) + '","' + getValue('predicateOnly', json) + '")'
        firstRow = False
    else:
        sql = sql + '\n,("' + j + '","' + getValue('label', json) + '","' + getValue('concept', json) + '","' + getValue('predicateType', json) + '","' + getValue('limit', json) + '","' + getValue('predicateOnly', json) +  '")'
  sql = sql + ';\n\n'

if os.path.exists("drdata.sql"):
  os.remove("drdata.sql")

f = open("drdata.sql", "w")
f.write(sql)
f.close()
"""
