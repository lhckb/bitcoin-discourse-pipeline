from steps.reddit_bronze import RedditBronze
from steps.reddit_silver import RedditSilver
from utils.logging_init import setup_logging
from common.db import PGSQLConnector

logger = setup_logging()

if __name__ == "__main__":

    bronze = RedditBronze()
    bronze_results = bronze.query_reddit_for_discourse()
    bronze.insert_into_bronze_table(bronze_results)

    silver = RedditSilver(bronze_results)
    silver.explode_comments()
    silver.add_metadata_round_one()
    silver.remove_dupes()
    silver.handle_missing()
    silver.normalize_text()
    silver.add_metadata_round_two()
    silver.convert_unix_to_timestamp()
    silver.insert_into_silver_tables(silver.posts_df, silver.comments_df)

    connector = PGSQLConnector()
    results = connector.select("""
        SELECT * FROM silver_posts;
    """)
    print(results)
