import credentials
import praw
import downloader
# from threader import DownloadThread
# from Queue import Queue


SUB_REDDIT = 'politics'
NUM_OF_POSTS = 2
NUM_OF_THREADS = 2

reddit = praw.Reddit(client_id=credentials.APP_CLIENT_ID,
                     client_secret=credentials.SECRET,
                     password=credentials.PASSWORD,
                     user_agent='crawler by cant-find-user-name',
                     username=credentials.DEVELOPER)

sub = reddit.subreddit(SUB_REDDIT)
# links = [post.url for post in sub.hot(limit=NUM_OF_POSTS)]
for post in sub.hot(limit=NUM_OF_POSTS):
    downloader.downloader(post.url)
# queue = Queue()
# for x in range(NUM_OF_THREADS):
#     worker = DownloadThread(queue)
#     worker.start()
# for link in links:
#     queue.put(link)
# queue.join()
