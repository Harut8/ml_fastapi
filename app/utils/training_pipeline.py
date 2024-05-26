from data_preprocessing import PreProcessing
from data_loader import DataLoader
from app.utils.model_selection import ModelSelection
from app.utils.data_clustering import KMeansClustering
from app.utils.file_operation import FileOperation

from sklearn.model_selection import train_test_split


class TrainingPipeline:
    def __init__(self):
        self.numerical_columns = None
        self.categorical_columns = None

    def train_model(self, path):
        data_loader = DataLoader()

        data = data_loader.load(path)

        preprocess = PreProcessing(data)
        preprocess.preprocessing_steps()

        X = preprocess.X

        kmeans = KMeansClustering(X)
        no_clusters = kmeans.elbow_plot()

        X = kmeans.apply_clustering(no_clusters)

        X['Output'] = preprocess.y
        list_cluster = X['Cluster'].unique()

        for i in list_cluster:
            cluster_subset = X[X['Cluster'] == i]
            cluster_label = cluster_subset['Output']
            cluster_subset.drop(['Output', 'Cluster'], axis=1, inplace=True)
            x_train, x_test, y_train, y_test = train_test_split(cluster_subset, cluster_label, test_size=0.20,
                                                                random_state=0)

            model_selection = ModelSelection()

            best_model, best_model_name, best_model_score = model_selection.get_best_model(x_train, y_train, x_test,
                                                                                           y_test)

            file_op = FileOperation()
            save_file_name = './Models/' + best_model_name + '_C' + str(i) + '_' + str(best_model_score)[:4] + '.txt'
            file_op.save_model(best_model, save_file_name)

        return
