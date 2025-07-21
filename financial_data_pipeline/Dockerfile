# Use an official Python runtime as a parent image
FROM python:3.9-bullseye

# Set environment variables
ENV SPARK_VERSION=3.5.1 \
	SPARK_HADOOP_VERSION=3 \
	SPARK_HOME=/opt/spark \
	HADOOP_VERSION=3.3.6 \
	HADOOP_HOME=/opt/hadoop \
	JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
	SCALA_VERSION="2.13-3.8.0" \
	KAFKA_VERSION="3.8.0" \
	KAFKA_HOME="/opt/kafka"

	# Install Java (required for Spark)
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	sudo \
	curl \
	unzip \
	rsync \
	openjdk-11-jdk \
	build-essential \
	software-properties-common \
	net-tools dnsutils iproute2 iputils-ping \
	ssh && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

RUN curl https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz -o hadoop.tar.gz
RUN curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz -o spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz
RUN curl https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}.tgz -o kafka_${SCALA_VERSION}.tgz
RUN wget http://www.nano-editor.org/dist/v2.4/nano-2.4.2.tar.gz
RUN curl https://archive.apache.org/dist/hive/hive-4.0.0/apache-hive-4.0.0-bin.tar.gz -o apache-hive-4.0.0-bin.tar.gz

# Install Python Libraries
COPY requirments.txt requirments.txt
RUN pip install --no-cache-dir -r requirments.txt
RUN rm requirments.txt

# Install nano
RUN tar -xzf nano-2.4.2.tar.gz
WORKDIR /nano-2.4.2
RUN ./configure
RUN make
RUN make install
WORKDIR /
RUN rm nano-2.4.2.tar.gz


# Install Hadoop
RUN mkdir -p /opt
RUN tar -xzf hadoop.tar.gz && \
	mv hadoop-${HADOOP_VERSION} /opt && \
	mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop && \
	rm hadoop.tar.gz	

	
# Install Spark
RUN mkdir -p /opt/spark
RUN tar xvf spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz --directory /opt/spark --strip-components 1 && \
	rm spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz


# Install Hive
RUN tar -xzf apache-hive-4.0.0-bin.tar.gz
RUN sudo mv apache-hive-4.0.0-bin /opt/hive
ENV HIVE_HOME="/opt/hive"

RUN mkdir -p /opt/hadoop/logs	


# Set Spark environment variables
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV HADOOP_HOME="/opt/hadoop"

ENV HADOOP_INSTALL=$HADOOP_HOME
ENV HADOOP_MAPRED_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_HOME=$HADOOP_HOME
ENV HADOOP_HDFS_HOME=$HADOOP_HOME
ENV YARN_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
ENV PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
ENV PATH=$PATH:$HIVE_HOME/bin

ENV HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
ENV HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"

# Kafka Install
RUN	tar -xzf kafka_${SCALA_VERSION}.tgz -C /opt
RUN	mv /opt/kafka_${SCALA_VERSION} /opt/kafka
RUN	rm kafka_${SCALA_VERSION}.tgz

ENV PATH="${KAFKA_HOME}/bin:${PATH}"
ENV KAFKA_TOPIC="transactions_stream"


RUN mkdir -p /root/.dbt

COPY src/config/hadoop/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY src/config/hadoop/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY src/config/hadoop/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
COPY src/config/hadoop/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml
COPY src/config/hadoop/hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh
COPY src/config/dbt/profiles.yml /root/.dbt/profiles.yml
COPY src/config/hadoop/core-site.xml $SPARK_HOME/conf/core-site.xml
COPY src/config/hadoop/hdfs-site.xml $SPARK_HOME/conf/hdfs-site.xml
COPY src/config/spark/log4j.properties $SPARK_HOME/conf/log4j.properties
COPY src/config/kafka/server.properties ${KAFKA_HOME}/config/server.properties
COPY src/config/kafka/zookeeper.properties ${KAFKA_HOME}/config/zookeeper.properties
COPY src/config/hive/hive-site.xml ${HIVE_HOME}/conf/hive-site.xml
COPY src/setup setup
COPY data data

# Set the working directory
WORKDIR /shared_volume

# Expose necessary ports
# Spark Web UI
EXPOSE 4040
# Hadoop ResourceManager Web UI
EXPOSE 8088
# Hadoop NameNode Web UI
EXPOSE 9870
# Expose ports for Zookeeper and Kafka
EXPOSE 2181
EXPOSE 9092
EXPOSE 9093
EXPOSE 9094
# Airflow Web UI
EXPOSE 8085

ENTRYPOINT sh /setup/main.sh && bash
