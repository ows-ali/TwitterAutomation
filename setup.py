
import twitterbot as tb 
import  sys 

import os 
from dotenv import load_dotenv 
load_dotenv()


print('=>Script started')
bot = tb.Twitterbot( os.environ.get('id'), os.environ.get('pass'))

# input command to make the script running to connect with browser usnig session id and url printed
input()