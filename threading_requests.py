import concurrent.futures
import requests
import threading
import time


# threading.local() creates an object that looks like a global but is specific to each individual thread. 
# In the example, this is done with thread_local and get_session()
# local() is in the threading module to specifically solve this problem. 
# It looks a little odd, but you only want to create one of these objects, not one for each thread. 
# The object itself takes care of separating accesses from different threads to different data.
# When get_session() is called, the session it looks up is specific to the particular thread on which it’s running. 
# So each thread will create a single session the first time it calls get_session() and then will simply use that session on 
# each subsequent call throughout its lifetime.

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
