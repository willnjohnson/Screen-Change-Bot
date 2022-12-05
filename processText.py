import json, re
from datetime import datetime

KEY_FOUND = True

with open('keys.json', 'r') as f:
    keys = re.compile('|'.join(json.load(f)['keyword']))

def cleanText(text):
    return " ".join(re.sub(' +', ' ', text).split())

def splitLeftOnKey(k, text):
    return text.split(k, 1)[0]

def splitRightOnKey(k, text):
    return text.rsplit(k)[-1]

def processText(text):
    text = cleanText(text)
    try:
        k = keys.search(text).group()
        print(f'Before {k}: {splitLeftOnKey(k, text)}')
        print(f'After {k}: {splitRightOnKey(k, text)}')

        return KEY_FOUND
    except: 
        print(f'[{datetime.now().strftime("%m/%d/%Y %H:%M:%S")}]: {text[:40]} ...')
        return not KEY_FOUND
