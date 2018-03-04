from collections import OrderedDict

ld = {'Jay Peak':(44.9367723, -72.525403),  # Jay Peak Summit https://goo.gl/maps/q1YWigKsBd62
        'Mt Sutton':(45.0894197, -72.5603979),  # Mt Sutton Chalet 840 https://goo.gl/maps/ZYpM4WYmuM92
        'Mt Tremblant': (46.2124932, -74.5620593),  # Mt Tremblant Summit https://goo.gl/maps/K6QzKPPZjKF2
        'St Anne': (47.087339, -70.931965),  # St Anne Summit https://goo.gl/maps/HgnbNbfU7uG2
        'Le Massif': (47.2816835, -70.6107957),  # Le Massif Resort (at top) https://goo.gl/maps/q7sTMfiJ1zP2
        'Stowe': (44.5310787, -72.8070048),  # Mt Mansfield Summit https://goo.gl/maps/MqwdMnXRPyo
        'St Sauveur': (45.8815953, -74.1598122),  # Mt St-Sauveur Summit https://goo.gl/maps/52H9iGnXsom
        'Smugglers Notch': (44.561464, -72.758678)  # Looks like the top https://goo.gl/maps/kp7Ri8pxi5S2
        }

loc_dict = OrderedDict(sorted(ld.items(), key=lambda t: t[0]))

ud = {'Jay Peak': 'https://www.onthesnow.com/vermont/jay-peak/skireport.html',
        'Mt Sutton': 'https://www.onthesnow.ca/quebec/mont-sutton/skireport.html',
        'Mt Tremblant': 'https://www.onthesnow.ca/quebec/tremblant/skireport.html',
        'St Anne': 'https://www.onthesnow.ca/quebec/mont-sainte-anne/skireport.html',
        'Le Massif': 'https://www.onthesnow.ca/quebec/le-massif/skireport.html',
        'Stowe': 'https://www.onthesnow.com/vermont/stowe-mountain-resort/skireport.html',
        'St Sauveur': 'https://www.onthesnow.ca/quebec/mont-saint-sauveur/skireport.html',
        'Smugglers Notch': 'https://www.onthesnow.com/vermont/smugglers-notch-resort/skireport.html'}

url_dict = OrderedDict(sorted(ud.items(), key=lambda t: t[0]))

for key in loc_dict.keys():
    assert url_dict.get(key) is not None

