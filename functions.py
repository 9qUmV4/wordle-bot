import pandas as pd
import string
import numpy as np

def sort_py_percentage(wl: pd.Series) -> pd.Series:
    """Takes a pd.Series list containing words and returns them sorted by percentage. 
    Returns a pd.Series with the word in the Index and percentage as value"""
    # Split up string into single chars
    dt = wl.str.split("", expand=True)
    dt: pd.DataFrame = dt.drop(columns=[0, 6]) # Drop start and end of string (Whitespace chars)
    dt.columns = range(dt.columns.size)

    # Set up dataframe to count appearances of characters based on their position 
    dt_c = pd.DataFrame(data=np.nan, index=list(string.ascii_lowercase), columns=range(5))

    # Fill in the count dataframe
    for c in string.ascii_lowercase:
        dt_tmp: pd.DataFrame = (dt == c).replace({False: 0, True: 1})
        dt_c.loc[c, :] = dt_tmp.sum(axis="index", skipna=True)

    # Calculate percentages
    dt_cn = (dt_c / len(wl))

    # Calculate the percentage for every word
    wl_per = dt
    for col in range(len(dt.columns)):
        con_table = dt_cn.loc[:, col].to_dict()
        wl_per.loc[:,col].replace(con_table, inplace=True)

    wl_per['total'] = wl_per.sum(axis='columns') / 5

    # Add words into dataframe
    wl_per['word'] = wl

    # Sort based on percentage
    wl_per_sort = wl_per.sort_values('total', axis='index', ascending=False)

    wl_per_sort = wl_per_sort.loc[:, ['total', 'word']]
    wl_per_sort = wl_per_sort.set_index('word').squeeze()

    return wl_per_sort
