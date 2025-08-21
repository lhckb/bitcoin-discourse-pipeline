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



/opt/brew/opt/kafka/bin/kafka-server-start /opt/brew/etc/kafka/server.properties