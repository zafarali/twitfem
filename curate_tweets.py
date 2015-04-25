import pandas as pd
import numpy as np

def curate_tweets(filename, col_id, col_tweet, num_rows, out_filename):
    df_in = pd.read_csv(filename, encoding='latin-1')
    col_id = 'id'
    col_tweet = 'tweet'
    num_rows = 1000
    out_filename = 'feminist_classified'


    rows = np.random.choice(df_in.index.values, num_rows)
    df_out = df_in.ix[rows]
    df_out = df_out[[col_id, col_tweet]]
    assert 'class' not in df_out.columns
    df_out['class'] = np.nan
    print('{} records, {} with unique tweet text'.format(len(df_out), len(df_out[col_tweet].unique())))
    df_out.reset_index(drop=True, inplace=True)
    
    i = 0
    end_i = len(df_out) - 1

    print("[0-9] for classes, b for back, s for save, x for exit")

    while i < end_i:
        print(df_out[col_tweet].iloc[i])
        resp = input("class --> ")
        if resp == "x":
            i = end_i
            tosave = input("Save? (y/n): ")
            if tosave in ["y", "Y", "yes", "YES", "Yes"]:
                df_out.to_csv(out_filename+'.csv')     
        elif resp == 'b':
            i -= 1
            df_out.loc[i, 'class'] = np.nan
        elif resp == 's':
            df_out.to_csv(out_filename+'.csv') 
        elif 0 <= int(resp) <= 9:
            df_out.loc[i, 'class'] = int(resp)
            i += 1
  
        else:
            print ('*** INVALID ENTRY, TRY AGAIN ***')
