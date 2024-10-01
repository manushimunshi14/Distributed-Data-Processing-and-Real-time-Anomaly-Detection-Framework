#!/bin/bash

echo "Attempting to run:"
echo "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \\"
echo "          -file $MAPPER_TASK_2 -mapper $MAPPER_TASK_2 \\"
echo "          -file $REDUCER_TASK_2 -reducer $REDUCER_TASK_2 \\"
echo "          -input $INPUT -output $OUTPUT_2"

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
    -file $MAPPER_TASK_2 -mapper $MAPPER_TASK_2 \
    -file $REDUCER_TASK_2 -reducer $REDUCER_TASK_2 \
    -input $INPUT -output $OUTPUT_2

echo Completed