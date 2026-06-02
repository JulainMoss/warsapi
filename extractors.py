def get_busestrams(data):
    clean_data = []
    if 'result' in data:
        items = data['result'] 
        for item in items:
            bus = {'szer_geo': item['Lat'], 'dlug_geo': item['Lon']}
            if 'szer_geo' in bus and 'dlug_geo' in bus:
                clean_data.append(bus)
    return clean_data

def get_stops(data):
    clean_data = []
    if 'result' in data:
        items = data['result'] 
        for item in items:
            print(item['values'])
            stop = {val['key']: val['value'] for val in item['values']}
            if 'szer_geo' in stop and 'dlug_geo' in stop:
                clean_data.append(stop)
    return clean_data