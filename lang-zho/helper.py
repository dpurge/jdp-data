import config

from pathlib import Path
from io import StringIO
from collections import OrderedDict

def flatten(items):
    for x in items:
        if not x: continue
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in flatten(x):
                yield y
        else:
            yield x

def get_state_file(filename):

    state_folder = Path(config.data_folder)
    
    if not state_folder.is_dir():
        state_folder.mkdir(parents=True)
    
    state_file = state_folder/filename
    
    return state_file

def get_data_file(filename):

    data_folder = Path(config.data_folder)
    
    if not data_folder.is_dir():
        raise Exception(f"Data folder does not exist: {data_folder}")
    
    data_file = data_folder/filename
    
    if not data_file.is_file():
        raise Exception(f"Data file does not exist: {data_file}")
    
    return data_file

def get_vocabulary(text, traditional=False):
    
    data_file = get_data_file('dictionary.csv')
    data = StringIO()
    
    with data_file.open(encoding='utf-8') as f:
        while line := f.readline():
            hant, hans, pinyin, pos, english = line.split("\t")
            if traditional:
                if hant in text:
                    data.write(f"{hant}\t{pinyin}\t{pos}\t{english}")
            else:
                if hans in text:
                    data.write(f"{hans}\t{pinyin}\t{pos}\t{english}")
    return data.getvalue()


def get_pinyin(characters):
    data_file = get_data_file('pinyin.csv')
    
    data = StringIO()
    with data_file.open(encoding='utf-8') as f:
        while line := f.readline():
            char = line[0]
            if char in characters:
                data.write(line)
    return data.getvalue()


def get_ime(items, datafile):
    data_file = get_data_file(f"{datafile}.csv")
    
    data = StringIO()
    with data_file.open(encoding='utf-8') as f:
        while line := f.readline():
            line = line.strip()
            i = line.split("\t")
            if len(i) < 2:
                print(line)
            han = i[0]
            code = i[1]
            if han in items:
                data.write(f"{han}\t{code}\n")
    return data.getvalue()

def merge_items(*items, join_char='/'):
    index = 0
    dictionary = OrderedDict()
    
    for text in items:
        for line in text.split("\n"):
            if not line: continue
            key, *value = line.split("\t")
            if not key in dictionary:
                dictionary[key] = []
            while len(dictionary[key]) < index + 1:
                dictionary[key].append([])
            if value:
                dictionary[key][index].extend(value)
        index += 1
    
    data = StringIO()
    for key, values in dictionary.items():
        value = "\t".join([join_char.join(i) for i in values])
        data.write(f"{key}\t{value}\n")
    return data.getvalue()


def get_decomposition(characters):
    table = {}
    data_file = get_data_file('decomposition.csv')
    
    with data_file.open(encoding='utf-8') as f:
        while line := f.readline():
            #if not line: continue
            key, value = line.split("\t")
            table[key] = value.strip()
    
    def decompose(hz):
        if not hz in table:
            return "?"
        v = table[hz].strip()
        if not v:
            return "?"
        if len(v) <= 1:
            return v
        
        result = ""
        for i in v:
            j = table[i]
            if len(j) <= 1:
                result = f"{result}{j}"
            else:
                result = f"{result}{i}({decompose(i)})"
        return result
    
    data = StringIO()
    for key in characters:
        if not key: continue
        value = decompose(key)
        data.write(f"{key}\t{value}\n")
    return data.getvalue()