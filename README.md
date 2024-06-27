# 2024-Euros-predictor
Python project to predict the outcome of the all the matches in 2024 euros using previous match history

The data used foe the prediction is the macth history of these respective teams in the euros competition only
This data along with the 2024 euros table format has been web scraped off of wikipedia
Poisson distribution is used to find the outcome of these matches

extracting_tables.py and match_history.py contains the web scraping code
data_cleaning.py contains the code for the data cleaning
modelling.py contains the code for creating our model and predicting using the built model

The final outcomes of all the matches can be accessed in Predicted_Scores_for_2024_EUROS.csv
ITALY was predicted to be the winner!!!
