from keras.preprocessing import image
from skealrn.metrics import confusion_matrix
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
        self.predicted_classes = predicted_probas.max(axis=1)

    def confusion_matrix(self, plot=True):
        """
        Get confusion matrix
        """
        return confusion_matrix(self.grnd_truth, self.predicted_classes)

    def get_n_random_correct_preds(self, n):
        """
        :param n: Number of correct random predictions
        :return : index with n elements where predictions are accurate
        """
        correct_idxs = np.where(self.predicted_classes == self.grnd_truth)
        return np.random.choice(correct_idxs[0], n, replace=False)

    def display_n_random_correct_preds(self, n):
        """
        :param n: Number of correct random predictions
        :return : index with n elements where predictions are accurate
        """
        idxs = self.get_n_random_correct_preds(n)
        self._display_idxs(idxs)

    def _display_idxs(self, idxs):
        """
        :param idx: idx of images to plot
        """
        filenames = self.filenames
        predicted_probas = self.predicted_probas
        predicted_classes = self.predicted_classes
        plots([image.load_img(filenames[i]) for i in idxs], titles=predicted_probas[idxs, predicted_classes[idxs])
