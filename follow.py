import twitterbot as tb 
import  sys 
from random import randint
import os 
from dotenv import load_dotenv 
load_dotenv()

# Change below configuration variables
handles = [ 'ThePracticalDev', 'TheAtlantic']

count = 2

# Change above configuration variables
print('=>Script started')
bot = tb.Twitterbot(os.environ.get('id'), os.environ.get('pass'))

index = randint(1,len(handles))
handle = handles[index]

print('==>The handle is: ' ,handle)

bot.followUsers(handle, count)

print('=>Script finished')
