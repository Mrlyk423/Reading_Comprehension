# -*- coding: utf-8 -*-
import argparse
import string
import os
import json
import spacy
import unicodedata
import re
import functools
import operator
from tqdm import tqdm
from collections import Counter


parser = argparse.ArgumentParser(description='SQuAD data processing')
parser.add_argument('--train', type=bool, default=False, help='switch to process train/dev data')


DIR = os.getcwd()
OUTPUT_DIR = os.path.join(DIR, 'pro_data')
if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

train_filename = os.path.join(DIR, "data/SQuAD-v1.1-train.json")
dev_filename = os.path.join(DIR, "data/SQuAD-v1.1-dev.json")

# deal with some of the special cases
forms_map = {'1':['1', "one"], '2':['2', "two"], '3':['3', "three"], '4':['4', 'four'], '5':['5', 'fif','five'], '6':['6', 'six'], '7':['7', 'seven'], '8':['8', 'eight'], '9':['9', 'nine'], '15':['15', 'fifteen'], 'one': ['one', 'a'], '1 million': ['a million'], 't located 15 km southwest of Dushanbe': ['located 15 km southwest of Dushanbe'], 'rld around it': ['world around it'], '30s': ['30s', '30']}

nlp = spacy.load("en")

def load_data(filename):
    res = []
    f = open(filename, "r")
    json_str = "".join(f.readlines())
    data = json.loads(json_str)
    for doc in data["data"]:
        #print doc['title']
        for paragraph in doc["paragraphs"]:
            #print paragraph['context']
            for qas in paragraph['qas']:
                qas_dict= {"D":paragraph['context'],"A":qas["answers"],"Q":(qas["question"], qas["id"]), }
                res.append(qas_dict)
    return res

def normalize(w):
    w = w.lower()
    w = re.sub('\"', '\'', w)
    w = re.sub('[\\u2019\\u2018]', '\'', w)
    w = re.sub('[\\u2010\\u2011-]', ' - ', w) # whitespace to hyphen
    w = re.sub('[\\u2012\\u2013\\u2014\\u2015]', ' -- ', w) # whitespace to dash
    for punc in string.punctuation:
        if punc != '-':
            w = w.replace(punc, ' '+punc+' ')
    w = w.strip(' ')
    w = unicodedata.normalize('NFKD',w) # normalize eg è => e, ñ => n
    w = w.encode('ASCII', 'ignore') # encode as ASCII
    w = w.decode('utf-8') # change to string
    return w
    
def tokenize(string):
    # tokenize and lower case
    string = normalize(string.strip())
    str_list = [tok.strip() for tok in string.split(' ') if tok.strip() is not '']
    return str_list
    #return ' '.join([str(w) for w in nlp(string)])

def find_answer(doc_list, str_lists):
    idx = 0
    found = False
    for str_list in str_lists:
        num_str_tok = len(str_list)
        string = ' '.join(str_list)
        try:
            all_forms = forms_map[string] # get a list of all available forms of the given string
        except:
            all_forms = None
        for idx in range(len(doc_list)-num_str_tok+1):
            cur = ' '.join(doc_list[idx:idx+num_str_tok])
            # search in various forms (for special cases)
            if all_forms:
                for form in all_forms:
                    if cur.find(form) == 0:
                        found = True
                        start = idx
                        end = start + num_str_tok - 1
                        text = string
                        break    
            # search in original form
            if cur == string or cur.find(string) == 0:
                found = True
                start = idx
                end = start + num_str_tok - 1
                text = string
                break 
        if found:
            break
    if not found:
        return None
    return start, end, text


def prepare_data(data, train = True):
    # skip no answer example
    # data is a list containing multiple triples {D,A,Q}
    # A is answers list containing several pairs like {"answer_start": "...", "text": "..."}
    #
    # return: {'D':'...', 'Q':('...', id), 'A':[...]}
    # text normalized and lower cased, A contain offset-answer pairs
    normed_data = []
    count = -1
    print("preparing data...")
    not_found_ids = []
    for triple in tqdm(data):
        count += 1
        if len(triple['A'])>0:
            doc = tokenize(triple['D'])
            q = tokenize(triple['Q'][0])
            text = [tokenize(ex['text']) for ex in triple['A']]
            answer = find_answer(doc, text)
            if answer:
                normed_data.append({'D':doc, 'Q':(q, triple['Q'][1]), 'A':[(answer[0],answer[1]),answer[2]]})
            else:
                not_found_ids.append(count)
    print("answers cannont be found in %d/%d examples" %(len(not_found_ids), len(data))) 
    print(str(not_found_ids))
    if(train):
        file_name = os.path.join(OUTPUT_DIR, 'normed_train.txt')
    else:
        file_name = os.path.join(OUTPUT_DIR, 'normed_dev.txt')
    with open(file_name, 'w') as f:
        for example in normed_data:
            f.write("%s\n" % example)
    print("saved in %s" %file_name)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.train:
        data = load_data(train_filename)
        prepare_data(data)
    else:
        data = load_data(dev_filename)
        prepare_data(data, False)
