import json
import sys

if len(sys.argv) < 2:
    exit("txt_to_json.py <file>")

file = sys.argv[1]

params = []
data = []

with open(file) as f:
    lines = f.readlines()
    current_line = 1
    for line in lines:
        obj = {}
        if current_line == 1:
            params = line.replace("\"","").replace(" ","_").replace("'","").lower().strip().split(",")
            current_line = current_line+1
            continue
        line = line.replace("\"", "").replace("'","").lower().strip()
        splitted = line.split(",")
        for idx,val in enumerate(params):
            obj[val] = splitted[idx]
        data.append(obj)
    f.close()

with open("converted_data.json","w") as f:
    res = {"data": data}
    json.dump(res,f)