import pandas as pd
import pickle
from scipy.stats import poisson
from heapq import heappop, heappush, heapify

dict_table = pickle.load(open('dict_table','rb'))
df_match_history = pd.read_csv('clean_match_history.csv')
df_macth_fixtures = pd.read_csv('clean_match_fixtures.csv')

df_home = df_match_history[['HomeTeam','HomeGoals','AwayGoals']]
df_away = df_match_history[['AwayTeam','HomeGoals','AwayGoals']]

df_home = df_home.rename(columns={'HomeTeam':'Team', 'HomeGoals':'GoalsScored', 'AwayGoals':'GoalsConceded'})
df_away = df_away.rename(columns={'AwayTeam':'Team', 'HomeGoals':'GoalsConceded', 'AwayGoals':'GoalsScored'})

df_team_strength = pd.concat([df_home,df_away] ,ignore_index=True).groupby('Team').mean()

t1 = []
t2 = []
out = []

#return match point
def predict_points(home,away):
    if home in df_team_strength.index and away in df_team_strength.index:
        lamb_home = df_team_strength.at[home,'GoalsScored'] * df_team_strength.at[away,'GoalsConceded']
        lamb_away = df_team_strength.at[away,'GoalsScored'] * df_team_strength.at[home,'GoalsConceded']

        prob_home, prob_away, prob_draw = 0,0,0

        for x in range(0,11):
            for y in range(0,11):
                p = poisson.pmf(x,lamb_home) * poisson.pmf(y,lamb_away)
                if x==y:
                    prob_draw += p
                elif x>y:
                    prob_home += p
                else:
                    prob_away += p
        if(abs(prob_home-prob_draw)<0.038):
            return (1,1)
        elif(prob_home>prob_away):
            return (3,0)
        else:
            return (0,3)    
    else:
        return (1,1)

def predict_winner(home,away):
    if home in df_team_strength.index and away in df_team_strength.index:
        lamb_home = df_team_strength.at[home,'GoalsScored'] * df_team_strength.at[away,'GoalsConceded']
        lamb_away = df_team_strength.at[away,'GoalsScored'] * df_team_strength.at[home,'GoalsConceded']

        prob_home, prob_away, prob_draw = 0,0,0

        for x in range(0,11):
            for y in range(0,11):
                p = poisson.pmf(x,lamb_home) * poisson.pmf(y,lamb_away)
                if x==y:
                    prob_draw += p
                elif x>y:
                    prob_home += p
                else:
                    prob_away += p
        if prob_home>prob_away:
            return home
        else:
            return away    
    else:
        if home in df_team_strength.index:
            return home
        else:
            return away

#group stages
for group in dict_table:
    matches_done = []
    teams_in_group = dict_table[group]['Team'].values
    for home in teams_in_group:
        for away in teams_in_group:
            if {away,home} not in matches_done and home!=away:
                matches_done.append({home,away})
                t1.append(home)
                t2.append(away)
                points_home, points_away = predict_points(home, away)
                dict_table[group].loc[dict_table[group]['Team'] == home, 'Point'] += points_home
                dict_table[group].loc[dict_table[group]['Team'] == away, 'Point'] += points_away
                if(points_home>points_away):
                    out.append(home)
                elif points_away>points_home:
                    out.append(away)
                else:
                    out.append('Draw')

        dict_table[group] = dict_table[group].sort_values('Point', ascending=False).reset_index()
        dict_table[group] = dict_table[group][['Team', 'Point']]
        dict_table[group] = dict_table[group].round(0)


#knockput stages
knockout = ['WB','3W','WA','RC','WF','3W','RD','RE', 'WE','3W','WD','RF','WC','3W','RA','RB',]
r_of_16 = []

heap=[]
heapify(heap)
for group in dict_table:
    team = dict_table[group]['Team'][2]
    score = dict_table[group]['Point'][2]
    heappush(heap,(-score,team))

for i in knockout:
    if i[0]=='W':
        r_of_16.append(dict_table[i[1]]['Team'][0])
    elif i[0]=='R':
        r_of_16.append(dict_table[i[1]]['Team'][1])
    else:
        score,team = heappop(heap)
        r_of_16.append(team)
    
quarters = []
for i in range(0,16,2):
    first = r_of_16[i]
    second = r_of_16[i+1]
    winner = predict_winner(first,second)
    quarters.append(winner)
    t1.append(first)
    t2.append(second)
    out.append(winner)

semi = []
for i in range(0,8,2):
    first = quarters[i]
    second = quarters[i+1]
    winner = predict_winner(first,second)
    semi.append(winner)
    t1.append(first)
    t2.append(second)
    out.append(winner)

final=[]
for i in range(0,4,2):
    first = semi[i]
    second = semi[i+1]
    winner = predict_winner(first,second)
    final.append(winner)
    t1.append(first)
    t2.append(second)
    out.append(winner)

first = final[0]
second = final[1]
winner = predict_winner(first,second)
final.append(winner)
t1.append(first)
t2.append(second)
out.append(winner)


history = {'Team 1':t1, 'Team 2':t2, "Outcome":out}
final_outcome = pd.DataFrame(history)

final_outcome.to_csv('Predicted_Scores_for_2024_EUROS.csv')

print(winner,"is the winner of 2024 euros")
# print("Group Stages")
# print(final_outcome[0:36])
# print("Round of 16")
# print(final_outcome[36:44])
# print("Quater Finals")
# print(final_outcome[44:48])
# print("Semifinals")
# print(final_outcome[48:50])
# print("Final")
# print(final_outcome[50:51])