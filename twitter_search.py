from tweepy import API, Cursor, OAuthHandler
import csv
import config
from datetime import datetime
from twitter_analyzer import Textblob_Analyzer

class Twitter_Search():
    def __init__(self):
        self.auth=OAuthHandler(config.api_key, config.api_secret_key)
        self.auth.set_access_token(config.access_token, config.access_secret_token)

    def search(self, query, limit, date):
        api=API(self.auth, wait_on_rate_limit=True)
        count=0
        file_address="analysis_" + date + "_to_" + str(datetime.now().date()) + ".csv"
        with open(file_address, "w+", newline='', encoding='utf-8') as file:
            fields=["Date", "User", "Tweet", "Polarity", "Subjectivity", "Analysis", "Retweets", "Likes"]
            writer=csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            print("Searching...")
            for tweet in Cursor(api.search, q=query+" -filter:retweets", until=date, lang="en").items(limit):
                if tweet.favorite_count >= 10 and tweet.retweet_count >= 2:
                    row=self.get_row(tweet)
                    writer.writerow(row)
                    count+=1
            print("Search ended! ")
        return count

    def get_row(self, tweet):
        date=tweet.created_at
        user=tweet.user.screen_name
        retweets=tweet.retweet_count
        likes=tweet.favorite_count
        analyzer=Textblob_Analyzer()
        cleaned_tweet=analyzer.clean_tweet(tweet.text)
        polarity=analyzer.polarity(cleaned_tweet)
        subjectivity=analyzer.subjectivity(cleaned_tweet)
        analysis=analyzer.analysis(cleaned_tweet)
        return {"Date":date, "User":user, "Tweet":cleaned_tweet, "Polarity":polarity, "Subjectivity":subjectivity, "Analysis":analysis, "Retweets": retweets, "Likes": likes}

if __name__ == '__main__':
    search_test=Twitter_Search()
    searched=search_test.search("donald trump", 100000, '2020-10-11')
    print(str(searched)+" were pulled and stored")
