import requests
from bs4 import BeautifulSoup
import pandas as pd

euros_years = [1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020]

def get_matches(year):
    web = f'https://en.wikipedia.org/wiki/UEFA_Euro_{year}'

    response = requests.get(web)
    context = response.text
    soup = BeautifulSoup(context, 'lxml')


    matches = soup.find_all('div',class_='footballbox')

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find('th',class_='fhome').get_text())
        score.append(match.find('th',class_='fscore').get_text())
        away.append(match.find('th',class_='faway').get_text())
        
    dict_matches = {'home':home, 'score':score, 'away':away}
    df_matches = pd.DataFrame(dict_matches)
    df_matches['year'] = year

    return df_matches

euros = [get_matches(year) for year in euros_years]
df_euros = pd.concat(euros, ignore_index=True)
df_euros.dropna(inplace=True)

df_euros.to_csv('euros_match_history.csv', index=False) 

df_fixtures = get_matches(2024)
df_fixtures.dropna(inplace=True)
df_fixtures.to_csv('2024_euros_match_fixtures.csv', index=False)