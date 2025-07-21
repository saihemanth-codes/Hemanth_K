#!/bin/bash
set -e

zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties &
echo "Zookeeper Started";
kafka-server-start.sh /opt/kafka/config/server.properties &
echo "Server Started 1";
kafka-topics.sh --create --topic transaction_stream --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1;