loc_dict = {'Jay Peak':(44.9649, -72.4602),
            'Mt Sutton':(45.1047, -72.5618),
            'Mt Tremblant': (46.1185, -74.5962),
            'St Anne': (47.0754, -70.9049),
            'Le Massif': (47.2848, -70.5697),
            'Stowe': (44.5297, -72.7793)
           }

url_dict = {'Jay Peak':'https://www.onthesnow.com/vermont/jay-peak/skireport.html',
            'Mt Sutton':'https://www.onthesnow.ca/quebec/mont-sutton/skireport.html',
            'Mt Tremblant': 'https://www.onthesnow.ca/quebec/tremblant/skireport.html',
            'St Anne': 'https://www.onthesnow.ca/quebec/mont-sainte-anne/skireport.html',
            'Le Massif': 'https://www.onthesnow.ca/quebec/le-massif/skireport.html',
            'Stowe':  'https://www.onthesnow.com/vermont/stowe-mountain-resort/skireport.html',
           }


for key in loc_dict.keys():
    assert url_dict.get(key) is not None