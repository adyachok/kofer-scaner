# Scanner

![alt text][logo]

[logo]: img/scanner.png "Title"

### Installation

  1. Create Kafka topic:
  
    oc exec -it bus-kafka-1 -c kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic model-metadata-updates --create --partitions 3 --replication-factor 3
    

### Debugging

We created instance of [Kafdrop](https://github.com/obsidiandynamics/kafdrop) with
the aim to facilitate debugging process. The running example instance can be found
in [BIX ZZ project](https://kafdrop-zz-test.22ad.bi-x.openshiftapps.com/)

Kafdrop has reach interface which helps a lot in tracking messages / events.

![alt text][kafdrop]

[kafdrop]: img/kafdrop.png "Title"

Yoiu can easily trace / read all messages in any topic:

![alt text][kafdrop_read]

[kafdrop_read]: img/kafdrop%202.png "Title"