import json_manager as json, os
__data__ = os.getcwd() + '/__data__/places.json'

def run(args):
    args = str(args).lower()
    data = json.ReadFile(__data__)
    filtered = list(filter(lambda key: key.startswith(args), data.keys()))
    
    # If cannot find from above, search shortcases
    if(len(filtered) <= 0):
        filtered = [key for key, value in data.items() if 'shortcase' in value and value['shortcase'].startswith(args.replace(" ", ""))]

    found = []
    for x in filtered:
        indexData = ''
        for k, v in data[x].items():
            indexData += f'| {k.upper()}: {v} |'

        found.append(f'{x.upper()} :: ' + indexData)
    
    # UPDATE DISPLAY WITH INFORMATION
    return found