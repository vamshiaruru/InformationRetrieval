"""
Get top "NUM_OF_POSTS" links from "SUB_REDDIT" and pass them to downloader to
scrap them.
"""
import credentials
import praw
import downloader

SUB_REDDIT = 'worldnews'
NUM_OF_POSTS = 2
# Change NUM_OF_POSTS to whatever number required

reddit = praw.Reddit(client_id=credentials.APP_CLIENT_ID,
                     client_secret=credentials.SECRET,
                     password=credentials.PASSWORD,
                     user_agent='crawler by cant-find-user-name',
                     username=credentials.DEVELOPER)
# For this to work you need to have a 'credentials.py' file in the same
# directory with all those variables defined. Ask me for it :p

sub = reddit.subreddit(SUB_REDDIT)
for post in sub.hot(limit=NUM_OF_POSTS):
    # we can use top, controversial or rising too in the place of top.
    downloader.downloader(post.url)
