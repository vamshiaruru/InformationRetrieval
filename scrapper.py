import credentials
import praw
import downloader

SUB_REDDIT = 'news'
NUM_OF_POSTS = 2
NUM_OF_THREADS = 2

reddit = praw.Reddit(client_id=credentials.APP_CLIENT_ID,
                     client_secret=credentials.SECRET,
                     password=credentials.PASSWORD,
                     user_agent='crawler by cant-find-user-name',
                     username=credentials.DEVELOPER)

sub = reddit.subreddit(SUB_REDDIT)
links = [post.url for post in sub.top(limit=NUM_OF_POSTS)]
for link in links:
    downloader.downloader(link)
