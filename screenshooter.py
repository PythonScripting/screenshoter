import subprocess
from multiprocessing.pool import ThreadPool as Pool
import os

def capture(id_url_path_triplet):
    """ Takes a screenshot by running a PhantomJS process.
    Returns the return code of the process.

    Todo: the fact that capture expects a tuple instead of
    regular arguments is stupid. It's because of `capture_all`.
    Think of a better solution.
    """

    ID, url, path, retries = id_url_path_triplet
    process = subprocess.Popen(['phantomjs', 'take-screenshot.js', url, path])
    process.wait()
    return (ID, process.returncode, retries)

def capture_all(id_url_path_retries):
    pool = Pool(int(os.environ["SCRSH_PHANTOM_THREAD_POOL"]))
    return pool.map(capture, id_url_path_retries)
