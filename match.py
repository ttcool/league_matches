import json
import pymongo
con = pymongo.Connection('localhost',port=27017)
matches = con.db.matches
match = json.load(open('match.json'))
for i in match:
    matches.save(i)


