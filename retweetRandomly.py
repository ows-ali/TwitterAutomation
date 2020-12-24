
import twitterbot as tb 
import  sys 
from random import randint


handles = [ 'ThePracticalDev', 'TheAtlantic']


print('=>Script started')
bot = tb.Twitterbot('brainyqueen2', 'Muslim#786') 

index = randint(1,len(handles))
handle = handles[index]

print('==>The handle is: ' ,handle)

bot.retweetATweet(handle)

print('=>Script finished')
