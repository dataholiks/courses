from keras.preprocessing import image
import numpy as np
from sklearn.metrics import confusion_matrix
from utils import plots
class ClassifierPerformanceEvaluator():
    def __init__(self, grnd_truth, predicted_probas, filenames):
        """
        Class for evaluating classifier performance
        :param grnd_truth: ground truth labels
        :param predicted_probas: probability predictions from the classifier
        """
        self.grnd_truth = grnd_truth
        self.predicted_probas = predicted_probas
        self.filenames = filenames

        # predicted class = class with maximum probability
        self.predicted_classes = predicted_probas.argmax(axis=1)
        self.predicted_class_probas = predicted_probas.max(axis=1)

    def confusion_matrix(self, plot=True):
        """
        Get confusion matrix
        """
        return confusion_matrix(self.grnd_truth, self.predicted_classes)

    def get_n_random_incorrect_preds(self, n):
        """
        :param n: Number of correct random predictions
        :return : index with n elements where predictions are incorrect
        """
        # correct_idxs is tuple, correct_idxs[0] contains indices
        idxs = np.where(self.predicted_classes != self.grnd_truth)
        return np.random.choice(idxs[0], n, replace=False)

    def get_n_random_correct_preds(self, n):
        """
        :param n: Number of correct random predictions
        :return : index with n elements where predictions are correct
        """
        # correct_idxs is tuple, correct_idxs[0] contains indices
        idxs = np.where(self.predicted_classes == self.grnd_truth)
        return np.random.choice(idxs[0], n, replace=False)

    def display_n_random_incorrect_preds(self, n):
        """
        :param n: Number of correct random predictions
        :return : None. Display n incorrectly classified images
        """
        idxs = self.get_n_random_incorrect_preds(n)
        self._display_idxs(idxs)

    def display_n_random_correct_preds(self, n):
        """
        :param n: Number of correct random predictions
        :return : None. Display n correctly classified images
        """
        idxs = self.get_n_random_correct_preds(n)
        self._display_idxs(idxs)

    def _display_idxs(self, idxs):
        """
        :param idx: idx of images to plot
        :return : None. Display images in idxs
        """
        filenames = self.filenames
        titles = 
        xlabels = np.core.defchararray.add(np.array(['predicted class']), self.predicted_classes[idxs].astype(str))
        ylabels = np.core.defchararray.add(np.array(['actual class']), self.grnd_truth[idxs].astype(str))

        plots([image.load_img(filenames[i]) for i in idxs], titles=self.predicted_class_probas[idxs],
              xlabels=xlabels, ylabels=ylabels)

