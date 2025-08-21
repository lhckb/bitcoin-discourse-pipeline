read:
	uv run python read_reddit.py

kafka-list:
	kafka-topics --bootstrap-server localhost:9092 --list

kafka-create:
	kafka-topics --create --topic $(TOPIC_NAME) --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

kafka-delete:
	kafka-topics --bootstrap-server localhost:9092 --delete --topic $(TOPIC_NAME)

kafka-start:
	kafka-server-start /opt/brew/etc/kafka/server.properties

kafka-producer:
	kafka-console-producer --topic $(TOPIC_NAME) --bootstrap-server http://localhost:9092

kafka-consumer:
	kafka-console-consumer --topic $(TOPIC_NAME) --bootstrap-server http://localhost:9092 --from-beginning