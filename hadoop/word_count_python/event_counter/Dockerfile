FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

# fixes lack of python in the container
# and that the version of the OS is deprecated
ADD sources.list /etc/apt/sources.list
RUN apt update || : # ignore error
RUN apt install -y python3 python3-pip

# create a directory for the app
RUN mkdir /app
WORKDIR /app
# add the mapper, reducer

# COPY mapper-task-1.py ./
# COPY reducer-task-1.py ./
# COPY mapper-task-2.py ./
# COPY reducer-task-2.py ./
# COPY simulated_health_events.csv ./

ADD mapper-task-1.py ./
ADD reducer-task-1.py ./
ADD simulated_health_events.csv ./
RUN chmod a+x ./*

ENV MAPPER_TASK_1="mapper-task-1.py"
ENV REDUCER_TASK_1="reducer-task-1.py"
ENV INPUT="/input/simulated_health_events.csv"
ENV OUTPUT_1="/output/output-event-type"

ADD run.sh /run.sh
RUN chmod a+x /run.sh

CMD ["/run.sh"]