from collections import Counter
import pandas as pd


def countit(df, thisClass):
    numItems = len(df)
    count = Counter()
    for key, row in df.iterrows():
        terms = [ term for term in pre_process( row['tweet'] ) ]
        count.update(terms)
        
    toBeReturned = pd.DataFrame(columns=['class', 'token', 'frequency'])
    tokenList = []
    frequencyList = []
    classList = []
    for token,frequency in count.items():
        tokenList.append(token)
        frequencyList.append(frequency)
        classList.append(thisClass)

    theDict = { 'tokens':tokenList, 'frequency': frequencyList, 'class': classList } 
    return pd.DataFrame.from_dict(theDict)


