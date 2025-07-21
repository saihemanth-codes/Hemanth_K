#!/bin/bash
set -e

hdfs dfs -mkdir data

hdfs dfs -put /data/accounts.csv data/accounts.csv
hdfs dfs -put /data/cards.csv data/cards.csv
hdfs dfs -put /data/clients.csv data/clients.csv
hdfs dfs -put /data/disps.csv data/disps.csv
hdfs dfs -put /data/districts.csv data/districts.csv
hdfs dfs -put /data/loans.csv data/loans.csv
hdfs dfs -put /data/orders.csv data/orders.csv