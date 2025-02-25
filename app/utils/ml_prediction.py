from app.utils.data_preprocessing import PreProcessing
from app.utils.data_loader import DataLoader
import os
import pandas as pd
from file_operation import FileOperation
from datetime import datetime, date


class Prediction:

    def save_csv(self, data, path):
        data.to_csv(path, header=True, mode='a+')

    def load_file(self, path):
        return pd.read_csv(path)

    def get_best_model_for_cluster(self, cluster_no):
        for file in os.listdir('./Models/'):
            model_name_cluster = file.split('_')[1][1:]
            if (cluster_no == model_name_cluster):
                return file

    def prediction(self, path):
        data_loader = DataLoader()
        data = data_loader.load(path)

        preprocess = PreProcessing(data)
        preprocess.test_preprocessing_steps()

        file_op = FileOperation()
        kmean_model = file_op.load_model('./Clustering_Models/KMeans.pkl')
        clusters = kmean_model.predict(data)

        data['clusters'] = clusters
        clusters = data['clusters'].unique()
        prediction_list = []
        for i in clusters:
            cluster_subset = data[data['clusters'] == i]
            cluster_subset = cluster_subset.drop(['clusters'], axis=1)
            model_file_name = self.get_best_model_for_cluster(str(i))
            model = file_op.load_model('./Models/' + model_file_name)
            result = model.predict(cluster_subset)
            prediction_list.extend(result)
        results = pd.DataFrame(list(zip(prediction_list)), columns=['Predictions'])
        data = pd.concat([data, results], axis=1)
        pred_timestamp = datetime.today().strftime('%Y_%m_%d_%H%M%S')
        self.save_csv(data, './Prediction_Results/Predictions_' + str(pred_timestamp) + '.csv')
        return {'status': 'OK'}
