# Python program to read
# json file


import json

# Opening JSON file
f = open('simple.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
print(data)

# Closing file
f.close()
