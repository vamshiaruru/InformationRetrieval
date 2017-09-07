from threading import Thread
import downloader


class DownloadThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.daemon = True

    def run(self):
        while True:
            link = self.queue.get()
            downloader.downloader(link)
            self.queue.task_done()
