# A Bot for a terrible Twitter Newsfeed

Like many people, I live in a city district: it's quite easy to get news on what's happening in the city at large, but there are few options when I want to keep abreast of what's happening in my local area. Thankfully, my local area has a news organization that's quite active on Twitter. 

Less thankfully, whoever manages this account doesn't do a great job writing the actual tweet:

| Tweet                                                             | Headline                                                                             |
|-------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| #Barnet                                                           | Man in his 80s dies after collision in Tesco car park in Barnet                      |
| #Harrow #News                                                     | Police investigating assault near Harrow and Wealdstone station                      |
| A victim was left in a critical condition… #Edgware #Harrow #News | Police release images after assault in Edgware that left man in a critical condition |
| All the latest #Harrow news…                                      | Affinity Water apologise after leaking pipe reported in Wealdstone                   |
| Breaking news from #Harrow Town Centre this morning…              | Station Road in Harrow forced to close due to burst pipe                             |
| News from South #Harrow last night…                               | Man, 18, arrested for possession of an offensive weapon in South Harrow              |

If you can't tell, it's beyond frustrating, and I frequently miss relatively important news because of these tweets. What can you do?

You can make a bot.

I've set up this Twitter bot to run every fifteen minutes on a home server. It checks for new tweets, goes through any URL and pulls out the headline, than retweets Harrow Online's tweets with text straight from the headline. It's written in Python and uses [tweepy](https://www.tweepy.org/) to interact with the Twitter API and [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) to scrape the headlines.

Find the bot on [Twitter](https://twitter.com/harrowtitlebot): if you're living in Harrow, it might be of use to you! If not, feel free to pull the code and set it up for your own use. 

To do so, you'll need to:
1. Set up developer permissions with twitter and generate your own API keys: I've provided an example config file, you'll just have to rename it ```config.py```. 
2. Put it in an environment that will allow it to run on a regular basis of your choosing.