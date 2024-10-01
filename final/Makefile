CONTAINER_CMD = /Applications/Docker.app/Contents/Resources/bin/docker
INPUT_DATASET = health_data.csv #change according to the name of the input dataset
OUPUT_FILE_WITH_PREDICTIONS = health_data_predictions.csv #change according to the name of the output dataset or if health_data_predictions.csv already present in the directory

all: kafka-consumer-and-webpage predict-from-dataset predict-from-kafka-consumer #predict-from-kafka-consumer can be replaced with retrain-model if we want our model to be retrained and redeployed after certain amount of time

predict-from-dataset :
	python3 dataset-predictor.py $(INPUT_DATASET) $(OUPUT_FILE_WITH_PREDICTIONS)

predict-from-kafka-consumer :
	python3 kafka-data-predictor.py

retrain-model : 
	python3 retrainModel.py

kafka-consumer-and-webpage : 
	$(CONTAINER_CMD) compose up -d