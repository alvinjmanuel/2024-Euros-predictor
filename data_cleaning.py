import pandas  as pd

df_matches = pd.read_csv('euros_match_history.csv')
df_fixtures = pd.read_csv('2024_euros_match_fixtures.csv')

df_fixtures['home'] = df_fixtures['home'].str.strip()
df_fixtures['home'] = df_fixtures['home'].str.strip()
df_fixtures.drop('year',axis=1,inplace=True)
df_fixtures.rename(columns={'score': 'outcome'}, inplace=True)

df_fixtures = df_fixtures[['home','away','outcome']]

df_matches['score'] = df_matches['score'].str.replace('[^\\d]','', regex=True)
df_matches['home'] = df_matches['home'].str.strip()
df_matches['away'] = df_matches['away'].str.strip()

homegoals = []
awaygoals = []
num = 0
for i in range(337):
    homegoals.append(df_matches['score'][i][0])
    awaygoals.append(df_matches['score'][i][1])

df_matches['HomeGoals'] = homegoals
df_matches['AwayGoals'] = awaygoals
df_matches.drop('score',axis=1,inplace=True)

df_matches.rename(columns={'home': 'HomeTeam', 'away': 'AwayTeam', 'year':'Year'}, inplace=True)
df_matches = df_matches.astype({'HomeGoals': int, 'AwayGoals':int, 'Year': int})
df_matches['TotalGoals'] = df_matches['HomeGoals'] + df_matches['AwayGoals']

df_matches.to_csv('clean_match_history.csv')
df_fixtures.to_csv('clean_match_fixtures.csv')



# for group in ['A','B','C','D','E','F']:
#     filename = f"group_{group}.csv"
#     df = pd.read_csv(filename)
#     df['Team'] = df['Team'].str.replace('\\[a\\]','',regex=True)
#     df.to_csv(filename,index=False)
