from textblob import TextBlob
import re
class Textblob_Analyzer():
    """
    This class analyzes individual tweets. First the tweet is cleaned by removing links,
    @s and RTs. Then the cleaned tweet will be analyzed using textblob.
    *** If both subjectivity and polarity are 0 then tweet was not cleaned properly.
    """
    def clean_tweet(self, tweet):
        tweet=re.sub(r'@[A-Za-z0-9]+', '', tweet)#remove any @s
        tweet=re.sub(r'#', '', tweet)#remove hastags
        tweet=re.sub(r'RT[\s]+', '', tweet)#remove retweet symbol(s)
        tweet=re.sub(r'https?:\/\/\S+', '', tweet)#remove hyperlinks
        return tweet

    def subjectivity(self, tweet):
        """
        This method gets the subjectivity of the tweet using textblob which
        measures how opinionated a tweet is, the closer to 1 the more opinionated.
        """
        return TextBlob(tweet).sentiment.subjectivity

    def polarity(self, tweet):
        """
        This method get the polarity which is a number representation of the
        nature of the tweet.
        """
        return TextBlob(tweet).sentiment.polarity

    def analysis(self, tweet):
        """
        Gives a more readable analysis on the tweets polarity.
        Neutral is said to be between -0.1 and 0.1
        Positive is greater than 0.1
        Negative is less than -0.1
        """
        polarity=self.polarity(tweet)
        if polarity > 0.1:
            return "Positive"
        elif polarity <= 0.1 and polarity >= -0.1:
            return "Neutral"
        else:
            return "Negative"
