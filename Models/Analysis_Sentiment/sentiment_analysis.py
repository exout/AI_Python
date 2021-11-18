import re
import nltk
import pandas as pd
import matplotlib.pyplot as plt
# nltk.download('vader_lexicon')
from datetime import time, datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


df = pd.read_csv('tesla-headlines.csv')
df_price = pd.read_csv('tesla-prices.csv')
pd.set_option('display.max_colwidth', None)
df.columns = ['Title', 'Date']  # change to 'title' and  'date'
df['Date'][0] = 'Dec. 9'

new_date_list = []  # create a new list and store new date

for df_time in df['Date']:  # loop trough every row in 'date' column
    match = re.search(r'\w{3}\.\s\d{1,2}\,\s\d{4}|May\s\d{1,2}\,\s\d{4}|\w{3}\.\s\d{1,2}|May\s\d{1,2}', df_time)

    if re.search(r'\w{3}\.\s\d{1,2}\,\s\d{4}|\w{3}\s\d{1,2}\,\s\d{4}', match[0]):
        full_date = match[0]
    else:
        full_date = match[0] + ", 2019" # append year to string

    for format in ('%b. %d, %Y', '%b %d, %Y'):
        try:
            new_date = datetime.strptime(full_date, format).date()
            break  # if format is correct don't test any other formats except ValueError:
        except ValueError:
            pass
    new_date_list.append(new_date)  # add new date to the list
if len(new_date_list) != df.shape[0]:
    print("Error:: Rows don't match")
else:
    df['New Date'] = new_date_list  # add the list to our original dataframe the


results = []
sia = SIA()
for lines in df['Title']:
    score = sia.polarity_scores(lines)  # Run analysis
    score['Headline'] = lines  # add headlines for viewing
    results.append(score)


df['Score'] = pd.DataFrame(results)['compound']

# creates a daily score by summing the scores of the individual articles in each day

df1 = df.groupby(['New Date']).sum()
df_price['Date'] = df_price['Date'].astype('datetime64[ns]')
df_price1 = df_price.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)  # drop unwanted rows
df_price1.set_index('Date', inplace=True)  # set Date column as index


# Now i have the prices, i need to calculate the returns.
df_price1['Returns'] = df_price1['Adj Close'] / df_price1['Adj Close'].shift(1) - 1  # Calculate daily returns

# Check relationship between lagged score against returns (daily)

# Lagged the sentiment score
df1['Score(1)'] = df1.shift(1)


# Match the daily returns with the lagged sentiment score
dfReturnsScore = pd.merge(df_price1[['Returns']], df1[['Score(1)']], left_index=True, right_index=True, how='left')

# Clean the data (again)

dfReturnsScore.fillna(0, inplace=True)  # replace NaN with 0 permanently
dfReturnsScore.plot(x="Score(1)", y="Returns", style="o")
plt.show()


# Design the test and Test for predictive value

dfReturnsScore2 = dfReturnsScore[(dfReturnsScore['Score(1)'] > 0.5) |
                                 (dfReturnsScore['Score(1)'] < -0.5)]

dfReturnsScore2.plot(x="Score(1)", y="Returns", style="o")


final = dfReturnsScore2['Returns'].corr(dfReturnsScore2['Score(1)'])
print(f'The final result of this correlation is {final} -->>')
plt.show()



























