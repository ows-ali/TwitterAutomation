
import twitterbot as tb 
import  sys 

import os 
from dotenv import load_dotenv 
load_dotenv() 

total_tweets = 2
hashtags = ['100DaysOfCode', '300DaysOfCode']


commentsList = ['Really cool!', 'Nice work ❤️', '👏👏', 'wow 👏', 'well said', 
            'so cool! 🙌', '❤️', 'lovely 😍', 'amazing 👌', 'amazing', 
            'wow ❤️', 'well said 👏', '👏👏👏👏', 'Nice!', 'nice 🔥',
            'feels good 😍', 'Good job! 😊', '❤️🔥🔥😍', 'thoughtful 👌', 'thatz deep',
            'intense 💯', '😊😊', 'i will take it as quote of the day','too much motivation 👌','very inspiring ❤️🔥'
            ]


like_probability = 9
comment_probability = 7 
retweet_probability = 5 
follow_probability = 9

print('=>Script started')
bot = tb.Twitterbot( os.environ.get('id'), os.environ.get('pass'))

# loging in 
# bot.login() 
# calling like_retweet function 



for hashtag in hashtags:
    print('==>On hashtag: ', hashtag, '-',hashtags.index(hashtag)+1,'/',len(hashtags))
    bot.like_retweet(hashtag, total_tweets, commentsList, like_probability, comment_probability, retweet_probability, follow_probability ) 
print('=>Script finished')
