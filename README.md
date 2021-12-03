# Stock-News-Sentiment-Analysis

The goal was to develop this sentiment analysis during our intership, but we didn't have enough time.

We hope that someone can continue with what we have started.

# Purpose: 
To analyze the news headline of a specific stock. 
This program uses Vader SentimentIntensityAnalyzer to calculate the news headline compound value of a stock for a given day.

# How it is works:

1: 
Gets data from the backend.
The backend team scrapes the page www.mfn.se on data, including dates, companies, news text, course change.

2: 
The first step is to analyze multiple stocks news, for example"ASA, NCC, SODEXO, Volvo Cars," and decides if it is a positive, neutral or negative news.
This is done with the help of sentiment analysis. Each news text is given a value, compound, between -1 and 1, where -1 is
negative and 1 is positive.
Compound is compared with the change in the share price on the current day to see if there is any connection.
The hypothesis is that positive news (positive compound) should result in a positive change in the share price.

3: 
Take compound on each news item for the current day and then calculate an average of compound for that day's news
and compare with the course ending for the day.

4:
Check the time when the news is published and see if it can reasonably have affected the course that day. eg news
after the stock exchange closes, news when the stock exchange is closed, etc.

5: 
Choose Algorithm.
In this case whe have chosen SGDClassifier. 
Which is a good model for prediction our model. You can remove stop words, punctuation 

6: 
Train Algorithm.
Split the data into a training part (training) and a test part (test). Normally training / test is distributed 80:20.
It is important that training and tests are kept separate.

7:
Check with new values (news / compound) to see what Algorithm predicts/ Correlation

