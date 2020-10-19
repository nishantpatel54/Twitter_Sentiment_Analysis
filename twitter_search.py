from tweepy import API, Cursor, OAuthHandler
import csv
import config
from datetime import datetime
from twitter_analyzer import Textblob_Analyzer

class Twitter_Search():
    def __init__(self):
        """
        This authenticates the api before a search can be made. All the keys are
        taken from the config.py file.
        """
        self.auth=OAuthHandler(config.api_key, config.api_secret_key)
        self.auth.set_access_token(config.access_token, config.access_secret_token)

    def search(self, query, limit, date):
        """
        This method is used to search twitter using the api and creates a csv file based on the date
        given so this method can used on a weekly basis(seperate file for each week).
        """
        api=API(self.auth, wait_on_rate_limit=True)
        count=0
        file_address=query+"_analysis_" + date + "_to_" + str(datetime.now().date()) + ".csv"
        with open(file_address, "w+", newline='', encoding='utf-8') as file:
            #the headers for the csv file.
            fields=["Date", "User", "Tweet", "Polarity", "Subjectivity", "Analysis", "Retweets", "Likes"]
            writer=csv.DictWriter(file, fieldnames=fields)
            #create the header
            writer.writeheader()
            print("Searching...")
            #loop through the tweets given by the api search method
            for tweet in Cursor(api.search, q=query+" -filter:retweets", result_type='mixed', lang="en").items(limit):
                #get the formatted row so it can be appended to the file
                row=self.get_row(tweet)
                writer.writerow(row)
                count+=1
                print(count)
            print("Search ended! ")
        return count

    def get_row(self, tweet):
        """
        This method is used to create a row that is inserted into the csv it uses
        the analyzer class to get the polarity and subjectivity.
        """
        date=tweet.created_at
        user=tweet.user.screen_name
        retweets=tweet.retweet_count
        likes=tweet.favorite_count
        analyzer=Textblob_Analyzer()
        cleaned_tweet=analyzer.clean_tweet(tweet.text)
        polarity=analyzer.polarity(cleaned_tweet)
        subjectivity=analyzer.subjectivity(cleaned_tweet)
        analysis=analyzer.analysis(cleaned_tweet)
        #return a dictionary for the row that needs to be inserted into the csv.
        return {"Date":date, "User":user, "Tweet":cleaned_tweet, "Polarity":polarity, "Subjectivity":subjectivity, "Analysis":analysis, "Retweets": retweets, "Likes": likes}

if __name__ == '__main__':
    #this is an example of how to use the twitter search class.
    #instantiate the class and use the search method to do a search and store
    search_test=Twitter_Search()
    keyword="donald trump"
    tweet_limit=1000
    date="2020-10-11"
    searched=search_test.search(keyword, tweet_limit, date)
    print(str(searched)+" were pulled and stored")
