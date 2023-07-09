# The Harrow Newsbot

My use case for this app has changed dramatically since early 2023: Twitter's API changes made it absolutely unreasonable to continue operating any sort of small-scale twitter bot, which prompted me to rewrite the bot entirely. Thankfully, other options have come about, and I've found that Mastodon's API is even easier to work with than Twitter's once was. I've also taken the time to entirely rewrite the infrastructure to function on GCP- it should comfortably sit within the free tier of the services used.

I live in a district of a large city: it's quite easy to get news on what's happening in the city at large, but there are few options when I want to keep abreast of what's happening in my local area. Thankfully, my local area has a news organization that's quite active on Twitter. 

Less thankfully, whoever manages this account doesn't do a great job writing the actual tweet:

| Tweet                                                             | Headline                                                                             |
|-------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Awful news from #Ruislip…                                         | Police appeal after woman ‘dragged into a bush’ and strangled in Ruislip             |
| There was an incident in #Stanmore last night…                    | Stolen Range Rover collides with multiple cars and garden wall in Stanmore           |
| #Harrow #News                                                     | Police investigating assault near Harrow and Wealdstone station                      |
| A victim was left in a critical condition… #Edgware #Harrow #News | Police release images after assault in Edgware that left man in a critical condition |
| All the latest #Harrow news…                                      | Affinity Water apologise after leaking pipe reported in Wealdstone                   |
| Breaking news from #Harrow Town Centre this morning…              | Station Road in Harrow forced to close due to burst pipe                             |
| News from South #Harrow last night…                               | Man, 18, arrested for possession of an offensive weapon in South Harrow              |

If you can't tell, it's beyond frustrating, and I frequently miss relatively important news because of these tweets. But what can you do?

You can make a bot.

I've set up this  bot to run every fifteen minutes. Scrapes the first page of [Harrow Online](https://harrowonline.org/), pulls out the headline, then 'toots' those headlines. It's written in Python, uses [mastodon.py](https://mastodonpy.readthedocs.io/en/stable/) to interact with the Mastodon API, and [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) to scrape the headlines.

The infrastructure is managed by Terraform and sits in Google Cloud Platform: the code is sent into a Google Cloud Function, triggered by a Google Cloud Scheduler Pub/Sub event every fifteen minutes. 

Find the bot on [Mastodon](https://mastodon.social/@harrownewsbot): if you're living in Harrow, it might be of use to you! If not, feel free to pull the code and set it up for your own use. 

To do so, you'll need to:
1. Set up an account with Mastodon and generate your own API keys. 
2. Set up an account, project, and service account (with ownership permissions, unless you actively want to hunt down the permissions required) on GCP, and generate a `.json` API key that will sit within the root directory of the project.
3. Make any required edits to the [Terraform variables](/tf/variables.tf), including your GCP project details and Mastodon user ID.
4. Run the Terraform code, pasting in your Mastodon access token at the prompt: fair warning, you will need to enable a fair few APIs that don't immediately relate to the project. This is an issue with Terraform's implementation- you won't be using all of these. This project should comfortably fit within GCP's free tier on all of the resources used.
