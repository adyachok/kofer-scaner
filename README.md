# Scaner

### Installation

  1. Create Kafka topic:
  
    oc exec -it bus-kafka-1 -c kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic model-metadata-updates --create --partitions 3 --replication-factor 3