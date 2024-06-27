import pandas as pd
import pickle

all_tables = pd.read_html("https://en.wikipedia.org/wiki/UEFA_Euro_2024")

dict_table = {}
group = 'A'
for i  in range(10,16):
    df = all_tables[i]
    df['Team'] = df['Team'].str.replace('\\[a\\]','',regex=True)
    df.pop('Pos')
    df['Matches_Played'] = 0
    df['Win'] = 0
    df['Loss'] = 0
    df['Draw'] = 0
    df['GF'] = 0
    df['GA'] = 0
    df['GD'] = 0
    df['Point'] = 0

    dict_table[group] = df

    group = chr(ord(group) + 1)

with open('dict_table','wb') as output:
    pickle.dump(dict_table,output)
