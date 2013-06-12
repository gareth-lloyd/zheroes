import csv, re
from collections import Counter

"ID Number"
"Organisation"
"User Journey1"
"User Journey2"
"User Journey3"
"User Journey4"
"User Journey5"
"Organisation Type"
"Food Cost"
"Food type"
"Pathway/means of entry"
"Elegibility"
"Location"
"Time"
"Email/Website"
"Telephone number"

POSTCODE_MATCHER = re.compile("([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {0,1}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)")

sets = {
"Organisation Type": [],
"Food Cost": [],
"Food type": [],
"Pathway/means of entry": [],
"Elegibility": [],
}


with open('../data/food_sources.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for d in reader:
        results = POSTCODE_MATCHER.search(d['Location'])
        for key, set_ in sets.items():
            set_.append(d[key])

    for key, set_ in sets.items():
        print
        print
        print key
        c = Counter(set_)
        print c

