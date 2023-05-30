# Python program to read
# json file


import json

# Opening JSON file
f = open('data.json')

# returns JSON object as
# a dictionary
data = json.load(f).encoding="utf-8"

# Iterating through the json
# list
print(data)

# Closing file
f.close()
