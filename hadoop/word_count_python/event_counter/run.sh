#!/bin/bash

echo "Attempting to run:"
echo "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \\"
echo "          -file $MAPPER_TASK_1 -mapper $MAPPER_TASK_1 \\"
echo "          -file $REDUCER_TASK_1 -reducer $REDUCER_TASK_1 \\"
echo "          -input $INPUT -output $OUTPUT_1"


#hadoop jar /opt/homebrew/Cellar/hadoop/3.4.0/libexec/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
    -file $MAPPER_TASK_1 -mapper $MAPPER_TASK_1 \
    -file $REDUCER_TASK_1 -reducer $REDUCER_TASK_1 \
    -input $INPUT -output $OUTPUT_1

echo "Completed task 1"

