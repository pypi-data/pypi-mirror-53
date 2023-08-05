# WebScraping_Instagram_igenemy   
Date for record: 29th September 2019 by Kenneth Hau

    Updated: It's now available on Google Colab. 
    
    Please follow below instruction to install chrome driver on Colab:
    --> !apt install chromium-chromedriver
    --> !cp /usr/lib/chromium-browser/chromedriver /usr/bin
    --> !pip install selenium
    --> set the parameter chromedriver_path = 'chromedriver'
    --> set the parameter chrome_headless = True

    ---------
    This is used to scrape images / videos from Instagam by using chrome driver.
    
    By setting those parameters, you can easily scrape either images or videos or both as well as select your designated path to save them.
    
    It will automatically create folders in a location where you stated in 'save_to_path'. Those folders are named by each username and hashtag
    
    Before scrapping, it will inform you to login your IG account in order to smoothen the scrapping process. Don't worry, it wouldn't store your username and password.
    
    ---------
    Library used:
    selenium, bs4, time, getpass, IPython, urllib, os, re
    
    --------- 
    Reminder:
    Sometimes it may not run properly after intensely scrapping. Please wait for a while and start your scrapping journey again.
    
    ---------
    Limitations:
    - Only allows scrape either by 'username' or 'hashtag' at the same time (but you can easily change 'target_is_hashtag' parameter after finishing your first scrapping)
    - Only allows chromedriver
    - Only allows to set the total number of posts you want
    
    ---------    
    Possible function that can be created in the future:
    Store each post's information (e.g. like, post time, post location, post description, users' number of followers, etc.) into dataframes, or even consolidate them into databases. Therefore, they can be used to do descriptive analysis, train up machine learning models or build up a recommendation system.
    
    
    ---------    
    Parameters & Attributes:
    (1) target : A list of string(s), default: []
            - either target username(s) or hashtag(s), if they are hashtags, 'target_is_hashtag' must be set to True
            
    (2) target_is_hashtag : Boolean, default: False
            - True: you want to scrape by using hashtags
            
    (3) chromedriver_path : String, default: './chromedriver'
            - a path of your chrome driver, you should name your driver as 'chromedrive'
    
    (4) save_to_path : String, default: '.'
            - a path where the image(s) / video(s) will be saved into
    
    (5) chromedriver_autoquit : Boolean, default: True
            - True: automatically quit the driver after finishing the scrapping
            - if you don't want it, you can quit the driver manually by using a build-in function called 'close_driver'
    
    (6) chrome_headless : Boolean, default: True
            - True: run chrome driver in the backend
            - if you want to see how the chrome driver works, you can set it to False
    
    (7) save_img : Boolean, default: True
            - True: save images
    
    (8) save_video : Boolean, default: False
            - True: save videos      
    
    (9) enable_gpu : Boolean, default: False
            - True: enable gpu in chrome driver
    
    (10) ipython_display_image : Boolean, default: False
            - True: display images, only works in notebook but not terminal
            - if you set True when using terminal to display, it will fail to scrape images
    
    ---------  
    Methods:
    (1) login : no parameter is required, return chrome_driver
            - used to access Instagram
            
    (2) scraper : two parameters (chrome_driver, num_post), return a list of all targeted url
    
        (a) chrome_driver : Selenium Webdriver
            - used for web scrapping

        (b) num_post : int, default: 10
            - the total number of posts you want to scrape
            - if this number is beyond the actual number of posts, it will stop scrapping automatically
            
    (3) close_driver : one parameters (chrome_driver)
            - manually close the web driver
    
    ---------
    --> from igenemy import Igenemy

    --> Example 1 (Normal flow):
    
    igenemy = Igenemy(target = ['hkfoodtalk', 'sportscenter'], target_is_hashtag = False, chromedriver_path= './chromedriver',
                  save_to_path = './', chromedriver_autoquit = False,
                  chrome_headless= True, save_img=True, save_video=False, enable_gpu = False, 
                  ipython_display_image = True)
    
    chrome_driver = igenemy.login()
    
    all_target = igenemy.scraper(chrome_driver = chrome_driver, num_post = 10)
    
    igenemy.close_driver(chrome_driver) #manually close if 'chromedriver_autoquit' is False
    

    --> Example 2 (Change attributes):
    
    igenemy.save_to_path = '../' #change path
    
    igenemy.target = ['burger', 'hkmusic','pasta'] #change target
    
    igenemy.target_is_hashtag = True #is it "hashtag" page?
    
    igenemy.save_video = True
    
    igenemy.save_img = True
    
    all_target = igenemy.scraper(chrome_driver = chrome_driver, num_post = 10) 
    
    #you can run 'scraper' again after you change the parameters if you didn't close the chrome driver.