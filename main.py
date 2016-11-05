import threading
from Queue import Queue
from spider import Spider
from domain import *
from general import *
import sys

PROJECT_NAME = str(sys.argv[2])
HOMEPAGE = str(sys.argv[1])
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 4 # no of threads os can handle
queue = Queue() #thread queue
Spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        t.daemon = True # Non daemon threads need to told to exit. They may prevent main program if not exited properly. Daemon threads automatically get killed after main.
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name ,url)
        queue.task_done()

#Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join() # for multithreading
    crawl()


# Check if there are items in the queue, if so crawl then
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + " links in the queue")
        create_jobs()

create_workers()
crawl()
