# twcrawl - Twitter Network Crawler

Starts at any given Twitter accounts (for example `realDonaldTrump` and 
`elonmusk`) and follows their relationships to download the profiles of all 
Twitter users into a local database for later batch processing (like 
analyzing the social sentiment).

**Note:** This crawler has been designed to prioritize crawling of accounts with
the most followers. Depending on your use case you might need to first tweak 
the parameters a bit.


## Setup 

All required dependencies are defined in the `requirements.txt` file. Run
`pip install -r requirements.txt` to install all of them if needed. Then copy
the `config.example.json` into a `config.json` and fill in your Twitter
API credentials.


## Usage

Simply run `src/main.py --users users.txt`. `users.txt` should be
a list of twitter handles to use as entry points of the crawling process, one
per each line of the text file.

This will launch an endless running process, which crawls as many users as
possible (and as fast as allowed by the Twitter API limits). You can pause the 
process by simply killing it and continue the crawling process by starting it 
again by executing `src/main.py` again (no more need for the `-i` parameter).

The crawled database will be stored into `data/twitter.sqlite3` (or anywhere 
else if you override the default values in your config file).