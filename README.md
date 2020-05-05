# Scanner

![alt text][logo]

[logo]: img/scanner.png "Title"

### Description
The Scanner service is meant to query model on business and server metadata it has.
This kind of service fits only [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving) 
instances, but any other pattern can be easily implemented.

**DISCLAIMER** the service is the integral part of ZZ project, but because the 
project is build using **service choreography architecture pattern** there are 
no strong, tight relations in it. This means that every part of ZZ can be 
modified - removed - rewritten accordingly to the needs of customer.


### Interaction process


![alt text][schema]

[schema]: img/how%20scanner%20works.png "Title"


### Installation

#### Run locally


To run locally application requires Kafka broker.

To install seamlessly **Kafka** broker we recommend 
[Kafka-docker](https://github.com/wurstmeister/kafka-docker) project. 
In the project you can find **docker-compose-single-broker.yml**

We suggest to create next alias

```bash alias kafka="docker-compose --file {PATH_TO}/kafka-docker/docker-compose-single-broker.yml up```

#### For local and dev/prod installations

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