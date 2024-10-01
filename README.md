## Project 1

### Part 1: Batch Data Analysis with Hadoop

#### Instuctions to run -

1. Navigate to directory /epidemic-engine-project-manushi-mohit/hadoop
2. Ensure docker desktop is running in your system
3. Make sure the CONTAINER_CMD variable in the makefile is changed from '/Applications/Docker.app/Contents/Resources/bin/docker' to docker.
4. Build the docker compose file using command 'docker-compose up --build'
5. Once the docker compose has build, run the makefile using command 'make hadoop_solved'


## Project 2

### Part 1: Data Ingestion and Categorization with Kafka

#### Instuctions to run -

1. Navigate to directory /epidemic-engine-project-manushi-mohit/kafka-server in a terminal window.
2. Ensure docker desktop is running in your system.
3. run command 'docker compose up -d' in the terminal.

### Part 2: Exploring with Apache Spark

#### Instuctions to run -

1. Navigate to directory /epidemic-engine-project-manushi-mohit/spark-explore in a terminal window.
2. Ensure docker desktop is running in your system.
3. run command 'docker compose up -d' in the terminal.
4. Once the kafka and spark are successfully running in the docker containers, go to the logs of the ed-pyspark-jupyter-lab container on your docker desktop and find the link to the jupyter server. It will look something like this - 

2024-04-16 14:09:27     To access the server, open this file in a browser:
2024-04-16 14:09:27         file:///home/jovyan/.local/share/jupyter/runtime/jpserver-18-open.html
2024-04-16 14:09:27     Or copy and paste one of these URLs:
2024-04-16 14:09:27         http://5277b2588fc0:8888/lab?token=1c5767c9ba7097b2adfa9d97cc6ee401ef8d177aa735d4c1
2024-04-16 14:09:27      or http://127.0.0.1:8888/lab?token=1c5767c9ba7097b2adfa9d97cc6ee401ef8d177aa735d4c1

5. Run the EDA.ipynb notebook on the jupyter server to get the EDA and visualizations. 

### Part 3: Advanced Analytics with Apache Spark

#### Instuctions to run -

1. Navigate to directory /epidemic-engine-project-manushi-mohit/machine-learning in a terminal window.
2. There are two notebooks in the directory - sklearnML.ipynb which has the pandas-sklearn ML model for prediction and sparkMLModel.ipynb which has the SparkML models implemented for prediction. 

#### Documentation - 

1. sklearnML.ipynb

The sklearnML.ipynb notebook demonstrates a structured approach to machine learning with Python's sklearn library for target label prediction.
The dataset includes variables like EventType, Timestamp, Location, Severity, Details, and Is_Anomaly, and extensive feature engineering is applied to the Timestamp data to extract additional features such as the hour of event, time of event, day of the week and the month. Label Encoder is applied to the categorical columns for further preprocessing. The columns Timestamp and Details are dropped as they do not provide additional information. We have implemented two models - Decision Tree Classifier and XGBoost Classifier. Grid search is performed for hyperparameter tuning. The model performance is evaluated using confusion matrix, accuracy, F1 score, precision and recall. 

2. sparkMLModel.ipynb

This notebook demonstrates a structured approach to applying spark MLlib for target label prediction.The dataset includes variables like EventType, Timestamp, Location, Severity, Details, and Is_Anomaly, and extensive feature engineering is applied to the Timestamp data to extract additional features such as the hour of event, time of event, and day of week. The preprocessing pipeline further includes StringIndexer, Encoder and VectorAssembler to prepare the data for the SparkML models.  The columns Timestamp and Details are dropped as they do not provide additional information. We have implemented four models - Logistic Regression, Decision Tree Classifier, Random Forest Classifier, GBT Classifer.  The model performance is evaluated using metrics like accuracy, F1 score, precision and recall. 

It was observed that GBT Classifier had best prediction performance and hence we chose that as our final model moving forward. Gradient Boosting Trees (GBT) Classifier  outperforms other models, particularly in this kind of scenarios with highly imbalanced data, because it builds sequential tree models that focus on correcting the errors of previous trees. This method is especially effective in addressing class imbalance by iteratively giving more weight to misclassified data points, thereby enhancing the model's ability to predict minority class labels more accurately.


## Project 3
### Final Integration, Connecting the Parts

#### Instuctions to run -
1. Navigate to directory /epidemic-engine-project-manushi-mohit/final in a terminal window.
2. Ensure docker desktop is running in your system.
3. run command 'docker compose up -d' in the terminal.


#### Documentation

Part 1 : Consuming and Storing Kafka Streaming Data 
- Related python script : consumer.py
- Tasks Accomplished : Kafka Containerization, Streaming Data Consumption, Storing in a Postgres Database and CSV File

Part 2 : SparkML model 
- Related python script : sparkMLModel.ipynb (in /epidemic-engine-project-manushi-mohit/machine-learning)
- The notebook includes preprocessing, feature engineering, model training, model evaluation and the model is saved for future use. 
- The saved model can be found in /epidemic-engine-project-manushi-mohit/final/gbt_model
- Tasks Accomplished : SparkML trained model

Part 3 : Model Retraining
- Related python script : retrainModel.py
- Tasks Accomplished : Model retrains from data above
                       Model is refreshed/redeployed by retraining above
                       Model is refreshed/redeployed by retraining above without downtime
- In retrainModel.py, we have specified code for retraining the model from new data.
- We first consume the data for a specified window size (number of events), make predictions with our existing model on the window and store the predictions. These predictions are then appended to the original data (1-million-row-dataset) and a new model with same hypermeters is trained for the accumulated data. The model is refreshed, redeployed and re-saved for future use. 


Part 4 : Model Prediction
- Related python scripts : kafka-data-predictor.py & dataset-prediction.py
- Tasks Accomplished : Prediction via the model and a dataset sent to it 
                       Prediction is made via the model and windows of the data streamed from Kafka
- For dataset prediction via model, you need to go to the dataset-prediction.py and change the csv file path in the line 
'health_data_df = spark.read.csv("health_data.csv", header=True, inferSchema=True). The dataset should be of same format as given (features and target label should be same as the 1-million row dataset as model is trained on that dataset). The script will perform preprocessing, feature engineering and make predictions, saving them to 'health_data_predictions.csv'. 
- For Kafka-window streaming data prediction via windows of Kafka data, you need to go to the kafka-data-predictor.py and change the global windowSize variable to specify the number of messages consumed in a window. For simplicity, current value is 5. The messages in the window are stored and predictions are made via the model for the same. 


Part 5 : Graphs
- Related files : webpage.html & New_graphs.ipynb 
- Tasks Accomplished : Web page serving graphs
                       Graphs visualizing the events being streamed (the provided 1-million dataset)
                       Graphs visualizing past outbreaks from the data provided to us (1-million dataset)
                       Graphs graph visualizing the next predicted outbreak event (predicted on collected data from Project 2 Part 1)
                       Other graphs : EDA plots on provided 1-million row dataset 
- Once the "web" service is up in docker compose, the webpage can be viewed by going to "http://localhost:8080/" on a web-browser or going to the Docker Dashboard and viewing the link next to the running container. 


Part 6 : Health Checks 
- All docker-compose.yml files in the whole repository. 
- Tasks Accomplished : Everything you produce has docker compose health checks  
                       Everything you produce has docker compose health checks and will restart on fail

Part 7 : PyTests


Part 8 : Makefile
-  Makefile present to produce everything
-  Makefile has different targets, running make target-name will produce the service specified by the target. Running "make" command will produce everything in the docker-compose. 


Part 9 : Other Tasks Accomplished

- Everything you produce runs as a docker compose file
- Everything you produce runs from a python or shell script
















