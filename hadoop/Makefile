# PATH := /usr/local/bin:$(PATH)
# export PATH
# ./add-python.sh
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input
# $(CONTAINER_CMD) run -v simulated_health_events.csv:/app ${RUN_PARAMS} hadoop fs -copyFromLocal /simulated_health_events.csv
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -put simulated_health_events.csv /input/
# $(CONTAINER_CMD) build -t hadoop-wordcount-python ./word_count_python
# $(CONTAINER_CMD) run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} hadoop-wordcount-python
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -mkdir -p /output/
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/output-event-type/*
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/output-location/*
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output
# $(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input

DOCKER_NETWORK = hadoop_default
ENV_FILE = hadoop.env
current_branch := 2.0.0-hadoop3.2.1-java8
CONTAINER_CMD = /Applications/Docker.app/Contents/Resources/bin/docker
RUN_PARAMS = --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} bde2020/hadoop-base:$(current_branch)

wordcount-java:
	$(CONTAINER_CMD) build -t hadoop-wordcount-java ./word_count_java
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -mkdir -p /input/
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -copyFromLocal -f /opt/hadoop-3.2.1/README.txt /input/
	$(CONTAINER_CMD) run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} hadoop-wordcount-java
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/*
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input

wordcount-python:
	chmod a+x ./add-python.sh
	./add-python.sh
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input  || : #ignore doesn't exist
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -mkdir -p /input/
	$(CONTAINER_CMD) run -v ./:/app ${RUN_PARAMS} hadoop fs -copyFromLocal app/simulated_health_events.csv /input/

event-counter: ;
	$(CONTAINER_CMD) build -t hadoop-eventcount ./word_count_python/event_counter
	$(CONTAINER_CMD) run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} hadoop-eventcount
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/output-event-type/*

location-mapreducer: ;
	$(CONTAINER_CMD) build -t hadoop-locationcount ./word_count_python/location_counter
	$(CONTAINER_CMD) run --network ${DOCKER_NETWORK} --env-file ${ENV_FILE} hadoop-locationcount
	
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -cat /output/output-location/*

hadoop_solved: wordcount-python event-counter location-mapreducer
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /output
	$(CONTAINER_CMD) run $(RUN_PARAMS) hadoop fs -rm -r /input

