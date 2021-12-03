from pymongo import MongoClient

mongo_url = "mongodb+srv://lia:lia@cluster0.3hztm.mongodb.net/test"
client = MongoClient(mongo_url)
bd = client["company-sentiment-store"]
collection = bd["company"]
resultIsin = []
resultText = []


def get_database():
    i = 0
    for x in collection.find():
        resultIsin.append(x['isin'])
        resultText.append(x['text'])
        length = len(resultIsin)
        while i < length:
            """print(resultIsin[i])
            print(resultText[i])"""
            i += 1


if __name__ == "__main__":
    get_database()
