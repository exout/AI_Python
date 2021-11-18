import matplotlib.pyplot as plt
import pandas as pd
import re  # import Regular Expression
from datetime import time, datetime
import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

df = pd.read_csv('tesla-headlines-sa.csv', encoding='windows-1250', header=None)
dfEodPrice = pd.read_csv("tsla-eod-prices.csv")
df.columns = ['Title', 'Date']
pd.set_option('display.max_colwidth', None)
df['Date'][0] = 'Dec. 9'

New_Date_List = []  # create a list to store the cleaned dates

for dateOfArticles in df['Date']:  # loop every row in the "Date" column
    match = re.search(r'\w{3}\.\s\d{1,2}\,\s\d{4}|May\s\d{1,2}\,\s\d{4}|\w{3}\.\s\d{1,2}|May\s\d{1,2}', dateOfArticles)

    if re.search(r'\w{3}\.\s\d{1,2}\,\s\d{4}|\w{3}\s\d{1,2}\,\s\d{4}', match[0]):
        fulldata = match[0]  # don't append year to string
    else:
        fulldata = match[0] + ", 2019"  # append year to strings

    for ftm in ('%b. %d, %Y', '%b %d, %Y'):
        try:
            newDate = datetime.strptime(fulldata, ftm).date()
            break  # if format is correct, don't test any other formats exept ValueError:
        except ValueError:
            pass

    New_Date_List.append(newDate)  # add new date to the list
if len(New_Date_List) != df.shape[0]:
    print("Error: Rows don't match")
else:
    df['New Date'] = New_Date_List  # add the list to our original dataframe the

results = []

for lines in df['Title']:
    pol_score = SIA().polarity_scores(lines)  # Run analysis
    pol_score['Headline'] = lines  # add headlines for viewing
    results.append(pol_score)

df['Score'] = pd.DataFrame(results)['compound']

# print(f'the results is ===>>> {results}')

"""we want to compare the relationship between the TSLA stock returns and our sentiment score. 
If there is a significant relationship, 
then our sentiment scores might have some predictive value."""

# creates a daily score by summing the scores of the individual articles in each day

df1 = df.groupby(['New Date']).sum()
dfEodPrice['Date'] = dfEodPrice['Date'].astype('datetime64[ns]')


dfEodPrice2 = dfEodPrice.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)  # drop unwanted rows
dfEodPrice2.set_index('Date', inplace=True)  # set Date column as index


# Now that we have our prices, we need to calculate our returns.
dfEodPrice2['Returns'] = dfEodPrice2['Adj Close'] / dfEodPrice2['Adj Close'].shift(1) - 1  # Calculate daily returns

# Step 3: Check relationship between lagged score against returns (daily)


"""
let’s start the analysis. Here are the steps:

1. Lagged the sentiment score
2. Match the daily returns with the lagged sentiment score
3. Clean the data (again)
4. Design the test
5. Test for predictive value

"""

df1['Score(1)'] = df1.shift(1)
# print(df1.shape[0])
# print(dfEodPrice2.shape[0])

dfReturnsScore = pd.merge(dfEodPrice2[['Returns']], df1[['Score(1)']], left_index=True, right_index=True, how='left')


# Clean the data (again) missing data NaN

dfReturnsScore.fillna(0, inplace=True)  # replace NaN with 0 permanently
dfReturnsScore.plot(x="Score(1)", y="Returns", style="o")

plt.show()

dfReturnsScore2 = dfReturnsScore[(dfReturnsScore['Score(1)'] > 0.5) |
                                 (dfReturnsScore['Score(1)'] < -0.5)]

dfReturnsScore2.plot(x="Score(1)", y="Returns", style="o")
plt.show()


# Ideally, we want something like this:

final = dfReturnsScore2['Returns'].corr(dfReturnsScore2['Score(1)'])
print(final)

# Step 5: Test for predictive value







