import json

def render(records):
    return "".join(json.dumps(row,sort_keys=True)+"\n" for row in records)
