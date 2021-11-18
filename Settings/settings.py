import nltk  # natural language toolkit
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA  #

import matplotlib.pyplot as plt
import string  # from some string manipulation tasks
import re
from string import punctuation  # solving punctuation problems
from nltk.corpus import stopwords  # stop words in sentences
from nltk.stem import WordNetLemmatizer  # for stemming the sentences
from nltk.stem import SnowballStemmer  # for stemming the sentences
from autocorrect import spell

import numpy as np
import pandas as pd
from nltk.stem import SnowballStemmer
from Models.Raw_Model.model_raw import sentence_tokenize
