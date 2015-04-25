import csv
import re

## emoticons
emoticons_str = r"""
  (?:
    [:=;] # Eyes
    [oO\-]? # Nose (optional)
    [D\)\]\(\]/\\OpP] # Mouth
  )"""
 
## words
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

## compile regex
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(string):
  return tokens_re.findall(string)

def removable(token):
  isEmoticon = True if emoticon_re.search(token) else False
  isRemovable = token in [',', '.', ':', ';', '\\']
  return (isEmoticon or isRemovable)

# pre_processor
def pre_process(string, lowercase=False):
  tokens = tokenize(string)
  tokens = [ token.lower() for token in tokens if not removable(token)]
  return tokens

