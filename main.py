from steps.read_reddit import RedditReader
from time import time
from utils.logging_init import setup_logging

logger = setup_logging()

def read_reddit():
    reader = RedditReader()

    query_start_time_utc = time()

    results = reader.query_reddit_for_discourse(query_start_time_utc)
    
    query_time_delta = time() - query_start_time_utc
    logger.info(f"Query ended in {query_time_delta} seconds")

    logger.info(f"Query produced {len(results)} results")

    return results

if __name__ == "__main__":
    results = read_reddit()