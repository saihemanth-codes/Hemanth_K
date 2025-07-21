#!/bin/bash
set -e

echo "Starting Docker";
ssh-keygen -t rsa -N '' -f /root/.ssh/id_rsa;
cat /root/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys;
service ssh start;
ssh-keyscan -H localhost >> ~/.ssh/known_hosts
sh /setup/setup-hadoop.sh;
echo "Hadoop setup done";
sh /setup/load-data.sh;
echo "Data loaded in hadoop";
sh /setup/start-kafka.sh;
sh /setup/start-airflow.sh;
rm -rf /data;
rm -rf /setup;
clear;
