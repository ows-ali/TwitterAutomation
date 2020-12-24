from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver import ActionChains 
# from selenium.webdriver.remote.webdriver import WebDriver

from random import uniform as randfloor

import time

import os 
from dotenv import load_dotenv 
load_dotenv()
from random import randint

class Twitterbot: 
  
    def __init__(self, email, password): 
  
        self.email = email 
        self.password = password

 
        print('==>opening browser')

        try:
            print('==>Trying to connect with existing browser')

            self.bot = self.create_driver_session(os.environ.get('session_id'), os.environ.get('executor_url'))
            print('==>Connected with existing browser')
            time.sleep(3)
            # print ('==>cur url', self.bot.current_url)


        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            print('error')
            print('Opening new browser')
            self.bot = webdriver.Firefox()
            
            executor_url = self.bot.command_executor._url
            session_id = self.bot.session_id

            print('\n','==>Recommended: Copy below two values in your .env file','\n')
            print ('session_id', session_id)
            print ('executor_url',executor_url)
            print('\n')
            self.login()
            pass

    def create_driver_session(self, session_id, executor_url):
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        new_driver.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        return new_driver

    def login(self):

  
        bot = self.bot 

        print('==>Opening twitter')
        time.sleep(randfloor(1,2)) 

        bot.get('https://twitter.com/login') 


        print('==>Logging in on twitter')
        time.sleep(randfloor(0,2)) 
        
  
        email = bot.find_element_by_xpath( 

            '/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input'
        ) 
        password = bot.find_element_by_xpath( 

            '/html/body/div/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input'
        )

        # sends the email to the email input
        email.send_keys(self.email)
        # sends the password to the password input
        password.send_keys(self.password)
        # executes RETURN key action 
        password.send_keys(Keys.RETURN) 
  
        time.sleep(randfloor(3,5)) 
  
    def like_retweet(self, hashtag, total_tweets, commentsList, like_probability, comment_probability, retweet_probability, follow_probability ): 
  
        """ 
        This function automatically retrieves 
        the tweets and then likes and retweets them 
  
        Arguments: 
            hashtag {string} -- twitter hashtag 
            total_tweets {number} -- total number of tweets for that hashtag
            commentsList {list of strings} -- comments list to choose a comment randomly
            like_probability {number} -- Range 1-10 
            comment_probability {number} -- Range 1-10 
            retweet_probability {number} -- Range 1-10 
            follow_probability {number} -- Range 1-10 
        """
        comments = 0
        bot = self.bot 
        print('==>Moving to results of hashtag: ', hashtag)
        time.sleep(randfloor(2,4)) 

        # fetches the latest tweets with the provided hashtag 
        bot.get( 
            'https://twitter.com/search?q=%23' + hashtag+'&src=typed_query&f=live'
        ) 
  
        time.sleep(randfloor(1,3)) 
  
        # using set so that only unique links 
        # are present and to avoid unnecessary repetition 
        links = set()  
  

        iteration = 0

        while len(links) < total_tweets:
            # executing javascript code  
            # to scroll the webpage 
            bot.execute_script( 
                'window.scrollTo(0, document.body.scrollHeight)'
            ) 
  
            time.sleep(randfloor(1,2)) 

            # using list comprehension  
            # for adding all the tweets link to the set 
            # this particular piece of code might 
            # look very complicated but the only reason 
            # I opted for list comprehension because is 
            # lot faster than traditional loops 
            
            [ 
                links.add(elem.get_attribute('href')) for elem in bot.find_elements_by_xpath("//a[@dir ='auto']") 
            ] 
            print('===>looped at iteration: ', iteration, ' Total links=', len(links), '\n', links,'\n')
            iteration += 1


        print('==>Reducing the extra links if more than total_tweets')
        print('==>total links before: ', len(links))
        if len(links) > total_tweets:
                
            for i in range(total_tweets,len(links)):
                links.pop()
        else:
            print('==>links length is smaller so skipping')
        print('==>total links after: ', len(links))

        print('==>Starting now visiting all the tweet links')

        tweetIter = 1
        for link in links:             
            
            print('===>Moving to tweet: ', tweetIter, '/', len(links))
            time.sleep(randfloor(2, 4)) 

            bot.get(link) 
  
            try: 

                print('===>Liking the tweet if random probability is <= like_probability: ', like_probability)
                time.sleep(randfloor(3, 5)) 
                like_prob = randint(1,10)
                print ('probability found to be: ',like_prob)
                
                if (like_prob <= like_probability):
                    print('===>So liking the tweet')

                    bot.find_element_by_css_selector( 
                        '.css-18t94o4[data-testid ="like"]'
                    ).click() 

                    time.sleep(randfloor(3,6)) 

                    print('===>Commenting the tweet if random probability is <= comment_probability: ', comment_probability)
                    time.sleep(randfloor(3, 5)) 
                    comment_prob = randint(1,10)
                    print('===>Comment probability found to be: ', comment_prob)


                    if comment_prob <= comment_probability:
                        print('===>So commenting')

                        bot.find_element_by_xpath("//div[@aria-label='Reply']").click()


                        commentIndex = randint(0,len(commentsList)-1)
                        print('===>printing comment number {0}, which is {1}'.format(commentIndex+1, commentsList[commentIndex]))

                        actions = ActionChains(bot) 

                        actions.send_keys(commentsList[commentIndex]).perform()
                        time.sleep(randfloor(1,3))

                        bot.find_element_by_xpath("//div[@data-testid='tweetButton']").click()

                        comments += 1
                        print('===>Commented! now waiting few seconds')
                        time.sleep(randint(3,6))
                    else: 
                        print('So skipping commenting')

                    print('===>Retweeting the tweet if random probability is <= retweet_probability: ', retweet_probability)
                    time.sleep(randfloor(2, 3)) 

                    retweet_prob = randint(1,10)
                    if (retweet_prob <= retweet_probability):
                        print('===>probability found to be: ',retweet_prob,' so retweeting the tweet')

                        # retweet button selector                 
                        bot.find_element_by_css_selector( 
                            '.css-18t94o4[data-testid ="retweet"]'
                        ).click() 
                        
                        time.sleep(randfloor(1, 3)) 
                        print('===>Confirming retweet without comment')
                        # initializes action chain 
                        actions = ActionChains(bot) 
                        # sends RETURN key to retweet without comment 
                        actions.send_keys(Keys.RETURN).perform() 
                        time.sleep(randfloor(1, 3)) 
                    else: 
                        print('===>probability found to be: ',retweet_prob,' so skipping retweeting the tweet')

                else:
                    print('===>So skipping liking the tweet (as well as any other action on this tweet)')

            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)
                pass
            tweetIter+=1
            print('===>Going back')
            time.sleep(randfloor(2,4))
            bot.execute_script("window.history.go(-1)")
        print('===>Finished liking and retweeting function, now moving to home')
        # fetches the main homepage 
        bot.get('https://twitter.com/') 

    def retweetATweet(self, handle):
        bot = self.bot 

        print('==>Going on profile of given handle')
        bot.get('https://twitter.com/'+handle)
        
        time.sleep(randfloor(2, 4)) 
        
        bot.find_element_by_css_selector( 
            '.css-18t94o4[data-testid ="retweet"]'
        ).click() 
        
        time.sleep(randfloor(1, 3)) 
        print('===>Confirming retweet without comment')
        # initializes action chain 
        actions = ActionChains(bot) 
        # sends RETURN key to retweet without comment 
        actions.send_keys(Keys.RETURN).perform() 
        time.sleep(randfloor(1, 3))
    
    def followUsers(self, handle, count):
        bot = self.bot
        
        print('==>Going on profile of given handle')

        bot.get('https://twitter.com/'+handle)

        time.sleep(randfloor(3, 6))

        print('==>Going to list of followers')
        bot.get('https://twitter.com/'+handle+'/followers')

        time.sleep(randfloor(3, 5))
        iteration=0
        while iteration <= count:
                
            try:
                elem = bot.find_element_by_xpath("//*[text()='Follow']")           
                print('==>User: ', iteration,'/',count)
                print('==>Now clicking follow button')
                time.sleep(randfloor(4,6))
                elem.click()

                print('==>Checking if Follow text stays changed, or revert (in case of limit reached)')
                time.sleep(randfloor(4,6))
                
                if elem.text == 'Follow': 
                    print('==>Follow limit reached, so exiting please try again later (and preferably set count to be less than or equal to 30')
                else: 
                    print('Text changed to be: ', elem.text)

            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print (message)
            iteration+=1

