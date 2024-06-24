import re, json

json_pattern = r'(\{.*?\})'

def parse_json(input_string):
    json_strings = re.findall(json_pattern, input_string, re.MULTILINE)
    json_dicts = []
    for json_string in json_strings:
        try:
            json_dict = json.loads(json_string)
            json_dicts.append(json_dict)
        except json.JSONDecodeError:
            continue
    return json_dicts
