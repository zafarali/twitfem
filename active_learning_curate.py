"""
Usage:

python active_learning_curate.py curated_filename unlabeled_filename save_to_filename batch_size sample_size 

PARAMETERS
curated_filename: name of csv file with curated data
unlabeled_filename: name of csv file with curated data
save_to_filename: filename to save new curated data to
batch_size: number of tweets to curate before retraining
	smaller number improves faster but is more computionally expensive
sample_size: number of samples to take from unlabeled pool when
	picking next tweet to curate. bigger improves faster but
	is more expensive

DESCRIPTION
Train a multinomial naive bayes classifier on tweets with active learning, using uncertainty sampling.
"""
import numpy as np
import matplotlib as plt
import pandas as pd
import random
import csv
import re
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

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
	isRemovable = token in [',', '.', ':', ';']
	return (isEmoticon or isRemovable)


# pre_processor
def pre_process(string, lowercase=False):
	tokens = tokenize(string)
	tokens = [ token for token in tokens if not removable(token)]
	return tokens


def load_curated_tweets(csv_file, encoding='latin-1'):
    df_curated = pd.read_csv(csv_file, encoding=encoding)
    df_curated = df_curated[['id', 'tweet', 'class']]
    return df_curated


def load_unlabeled_tweets(csv_file, encoding='latin-1'):
    df_curated = pd.read_csv(csv_file, encoding=encoding)
    df_curated = df_curated[['id', 'tweet']]
    return df_curated


def build_classifier(df_curated, df_all):
    vec = CountVectorizer(tokenizer=pre_process)
    vec.fit(df_all.tweet)
    bagofwords = vec.transform(df_curated.tweet)
    bagofwords = bagofwords.toarray()
    clf = MultinomialNB().fit(bagofwords, df_curated['class'])
    return vec, clf


def update_classifier(vec, clf, df_new_curated):
    bagofwords = vec.transform(df_new_curated.tweet)
    bagofwords = bagofwords.toarray()
    clf = clf.partial_fit(bagofwords, df_new_curated['class'])


def pick_uncertain_samples(sample_size, batch_size, vec, clf, df_unlabeled):
    # take random sample of unlabeled
    df_unlabeled = df_unlabeled.reindex(np.random.permutation(df_unlabeled.index))
    df_sample = df_unlabeled.iloc[:sample_size]
    print(df_sample.tweet)
    sample = vec.transform(df_sample.tweet)
    
    # predict them
    uncert_score = clf.predict_log_proba(sample)
    uncert_score = [sum(n) for n in uncert_score]
    
    #df_sample['uncert_score'] = uncert_score
    #print()
    #print(df_sample)
    i = np.argpartition(np.array([-n for n in uncert_score]), batch_size)
    df_sample = df_sample.iloc[i]
    #print('df_sample_parted')
    #print(df_sample.tweet)
    df_picked_sample = df_sample.iloc[:batch_size]
    print(len(df_picked_sample))
    
    return df_picked_sample


def curate_tweets(sample_df, curated_df, fn_out, i_end):
    assert 'uncert_score' not in sample_df.columns
    assert 'class' not in sample_df.columns
    sample_df['class'] = np.nan

    #print(sample_df['tweet'])

    print("[0-9] for classes, b for back, s for save, x for exit")

    i = 0
    while i < i_end:
        _id = sample_df.index[i]
        print(sample_df['tweet'].iloc[i])
        resp = input("class --> ")
        if resp == "x":
            tosave = input("Save? (y/n): ")
            if tosave in ["y", "Y", "yes", "YES", "Yes"]:
                curated_df.to_csv(fn_out+'.csv') 
            return None, None
        elif resp == 'b':
            i -= 1
            sample_df.loc[_id, 'class'] = np.nan
        elif resp == 's':
            curated_df.to_csv(out_filename+'.csv') 
        elif 0 <= int(resp) <= 9:
            sample_df.loc[_id, 'class'] = int(resp)
            curated_df.append(sample_df.iloc[i])
            i += 1

        else:
            print ('*** INVALID ENTRY, TRY AGAIN ***')
            
    return sample_df, curated_df


def main(argv):
    try:
        curated_csv = argv[1]
        unlabeled_csv = argv[2]
        batch_size = int(argv[4])
        sample_size = int(argv[5])
        new_curated_fn = argv[3]
    except IndexError:
        print('Missing command line argument.')
        
    unlabeled_df = load_unlabeled_tweets(unlabeled_csv)
    curated_df = load_curated_tweets(curated_csv)
    vec, clf = build_classifier(curated_df, unlabeled_df)

    while(True):
        sample_df = pick_uncertain_samples(sample_size, batch_size, vec, clf, unlabeled_df)
        picked_df, curated_df = curate_tweets(sample_df, curated_df, new_curated_fn, batch_size)
        if picked_df is None:
            break
        print(picked_df)
        clf = update_classifier(vec, clf, picked_df)


if __name__ == '__main__':
    main(sys.argv)