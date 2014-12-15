import subprocess
from multiprocessing.pool import ThreadPool as Pool

def capture(id_url_path_triplet):
    """ Takes a screenshot by running a PhantomJS process.
    Returns the return code of the process.

    Todo: the fact that capture expects a tuple instead of
    regular arguments is stupid. It's because of `capture_all`.
    Think of a better solution.
    """

    ID, url, path = id_url_path_triplet
    process = subprocess.Popen(['phantomjs', 'screenshot.js', url, path])
    process.wait()
    return (ID, process.returncode)

def capture_all(id_url_path_triplets, pool_size=5):
    pool = Pool(pool_size)
    return pool.map(capture, id_url_path_triplets)
