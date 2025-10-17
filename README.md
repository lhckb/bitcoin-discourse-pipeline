### Step 1: Find discussions about BTC
Twitter would be my first option but free API is capped at 100 reads per MONTH, so we're going to reddit
Problem: not all posts and/or comments are relevant. Some are just junk or jokes. This must be filtered prior to sentiment analysis
Filter: only read from relevant subs (Bitcoin, CryptoCurrency, Investing ...)
Filter #1: only read from posts with >1000 comments
Filter: require certain keywords that express opinion (think, believe, good, bad, honestly)
Filter: require at least 10 words
Filter #2: avoid duplicates



PHASE 1:
- praw polling
- airflow orchestration
- update dashboard in intervals
- use existing model (topicbert)

PHASE 2:
- streaming
- train (fine tune) own model



airflow setup:
- configure home to be in project
- set dags folder
- run airflow scheduler, then UI

docker run -d \
  --name my_postgres \
  -e POSTGRES_USER=luis \  
  -e POSTGRES_PASSWORD=devpassword \
  -e POSTGRES_DB=bitcoinpipeline \
  -p 5432:5432 \
  postgres:16

1: created object to represent data acuqired from PRAW. this is the bronze layer. created pgsql table representing this dat. bronze is raw ingestion, no cleaning

2: silver layer will clean data up, explode comments array into own table, remove dupes, standardize text data...

🔹 What to do now in Silver

Structural normalization

Explode comments into a separate table if not done.

Flatten any nested fields.

Convert timestamps to a standard format or float if needed.

Basic text cleaning / normalization

Lowercase text.

Strip extra whitespace.

Remove markdown artifacts, URLs, HTML entities.

Optionally remove emojis if they interfere with analysis.

Add derived metadata (optional, but common)

Word count, character count.

Number of links, hashtags, mentions.

Comment depth, parent post ID, subreddit, etc.

🔹 What to hold off until Gold

Stopword removal, stemming/lemmatization, vectorization, embeddings → These are domain/model-specific and usually applied at Gold.

Aggregations or business metrics → Keep Silver as “cleaned atomic data,” not yet processed for analysis.

TODO:
- add more info like upvote counts from bronze
- add try catches, throw errors