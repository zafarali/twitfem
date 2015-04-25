import csv
import numpy as np


file_name = 'curated/davidt1.csv'

# load the data into memory
with open(file_name, 'rt') as csvfile:
	data = {}
	reader = csv.reader(csvfile)
	for row in reader:
		data[str(row[1])] = {'tweet':row[2], 'class':row[3], 'id':row[1] }


emoticons_str = r"""
  (?:
    [:=;] # Eyes
    [oO\-]? # Nose (optional)
    [D\)\]\(\]/\\OpP] # Mouth
  )"""
 
regex_str = [
  emoticons_str,
  r'<[^>]+>', # HTML tags
  r'(?:@[\w_]+)', # @-mentions
  r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
  r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

  r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
  r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
  r'(?:[\w_]+)', # other words
  r'(?:\S)' # anything else
]

#import the tokenizers and regex module
import re

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(string):
	return tokens_re.findall(string)

def pre_process(string, lowercase=False):
	tokens = tokenize(string)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens


# tweets processed
print('-------TWEETS PROCESSED-----')
for key,val in data.items():
    print(pre_process(val['tweet']))

