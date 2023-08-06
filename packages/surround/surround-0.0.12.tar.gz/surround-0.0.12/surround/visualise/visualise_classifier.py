""" visualise.py

Visualises the output from training a classifier.

Supports both binary and multi class classifiers.

Use cases:
 - Visualising the output from training a model
 - Viewing the output from running batch predictions on a dataset

TODO: Add a flag to set probability thresholds
TODO: Add a flag that describes each aspect of the generated report in human readable terminology

"""

import numpy as np

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, cohen_kappa_score, jaccard_score
from sklearn.utils.multiclass import unique_labels

from ..state import State
from ..visualiser import Visualiser

class VisualiseClassifierData(State):
    """
    The data object used when running the VisualiseClassifier in the command line.
    """

    y_true = []
    y_pred = []
    visualise_output = {}

class VisualiseClassifier(Visualiser):
    """
    Classification visualiser stage. Generates metrics based on a column of ground truth values
    and predicted values to help you evaluate the performance of the estimator.

    .. note:: This stage requires the state object to have ``y_true``, ``y_pred`` and ``visualise_output`` fields.
            Where the ``visualise_output`` field must be a dictionary and the other two lists of values.
    """

    def validate(self, state, config):
        """
        Validate the data given to the visualiser. Checks whether we have the required fields
        to perform visualisation.

        :param state: the object containing the data to visualise
        :type state: :class:`surround.State`
        :param config: the configuration of the current pipeline
        :type config: :class: `surround.Config`
        :return: Whether the data needed is valid
        :rtype: bool
        """

        if not state.y_true.empty:
            state.errors.append("No ground truth data provided.")

        if not state.y_pred.empty:
            state.errors.append("No prediction data provided.")

        if not state.errors and len(state.y_true) != len(state.y_pred):
            state.errors.append("Length of ground truth data and prediction data mismatch")

        if not state.visualise_output:
            state.errors.append("No field defined for the output of the visualiser")

        return len(state.errors) > 0

    def generate_table_from_report(self, report_dict, classes):
        """
        Generate a table containing the metrics per class.

        :param report_dict: the dictionary containing the metric values
        :type report_dict: dict
        :parama classes: list of classes in the data
        :type classes: list
        :return: the table
        :rtype: str
        """

        template = "{:8}|{:10}|{:10}|{:10}|{:10}|{:10}\n"
        result = template.format("", "accuracy", "precision", "recall", "f1-score", "support")

        for category in classes:
            values = report_dict[category]
            result += template.format(
                category,
                "{:.2f}".format(values['accuracy']),
                "{:.2f}".format(values['precision']),
                "{:.2f}".format(values['recall']),
                "{:.2f}".format(values['f1-score']),
                "{:.2f}".format(values['support']))

        return result

    def generate_table_from_overall_report(self, report_dict):
        """
        Generate a table containing the overall metrics.

        :param report_dict: the dictionary containing the metric values
        :type report_dict: dict
        :return: the table
        :rtype: str
        """

        template = "{:14}|{:10}|{:10}|{:10}\n"
        result = template.format("", "precision", "recall", "f1-score")

        macro_avg = report_dict['macro avg']
        result += template.format(
            "macro avg",
            "{:.2f}".format(macro_avg['precision']),
            "{:.2f}".format(macro_avg['recall']),
            "{:.2f}".format(macro_avg['f1-score']))

        weighted_avg = report_dict['weighted avg']
        result += template.format(
            "weighted avg",
            "{:.2f}".format(weighted_avg['precision']),
            "{:.2f}".format(weighted_avg['recall']),
            "{:.2f}".format(weighted_avg['f1-score']))

        return result

    # pylint: disable=too-many-locals
    def visualise(self, surround_data, config):
        """
        Visualises the classifier data, calculating metrics such as accuracy, precision, cohen_kappa,
        f1-score and a confusion matrix. Prints the results to the terminal.

        :param state: the data being visualised
        :type state: :class:`surround.State`
        :param config: the config of the pipeline
        :type config: :class:`surround.Config`
        """

        if not self.validate(surround_data, config):
            for error in surround_data.errors:
                print("ERROR: " + error)
            return

        # Calculate metrics using the y_true and y_pred values
        surround_data.visualise_output = calculate_classifier_metrics(surround_data.y_true, surround_data.y_pred)

        report_dict = surround_data.visualise_output['report']
        classes = surround_data.visualise_output['classes']
        conf_matrix = surround_data.visualise_output['confusion_matrix']
        norm_conf_matrix = surround_data.visualise_output['normalized_confusion_matrix']

        # Generate pretty tables for the console
        overall_metrics = self.generate_table_from_overall_report(report_dict)
        per_category_table = self.generate_table_from_report(report_dict, classes)

        print("============[Classification Report]===================")
        print("Overall Metrics:")
        print(overall_metrics)
        print("Accuracy: %s" % surround_data.visualise_output['accuracy_score'])
        print("Cohen Kappa: %s" % surround_data.visualise_output['cohen_kappa_score'])
        print("==========================")
        print("Metrics per category:")
        print(per_category_table)
        print("==========================")
        print("Confusion Matrix:")

        # Print header of confusion matrix
        max_len = max([len(c) for c in classes])
        print(("{:>{:}} " + "{:^8} " * len(classes)).format("", max_len, *classes))

        # Print rows of confusion matrix, with labels
        template = "{:>{:}}|" + "{:^8}|" * len(classes)
        cm = conf_matrix if not config['show_normalized_confusion_matrix'] else norm_conf_matrix
        for i, _ in enumerate(classes):
            print(template.format(classes[i], max_len, *cm[i]))

        print("============[End of visualisation]===================")

def calculate_classifier_metrics(y_true, y_pred):
    """
    Calculate the metrics used for the classifier visualiser.

    :param y_true: ground truth values
    :type y_true: iterable
    :param y_pred: predicted values
    :type y_pred: iterable
    :return: report, confusion matrix, accuracy, cohen kappa, classes
    :rtype: dict
    """

    report_dict = classification_report(y_true, y_pred, output_dict=True)
    accuracy = accuracy_score(y_true, y_pred)
    cohen_kappa = cohen_kappa_score(y_true, y_pred)

    # Generate a sorted class list and confusion matrix (sorted by popular class)
    y_true_list = y_true.tolist()
    classes = unique_labels(y_true, y_pred)
    classes = sorted(classes, key=y_true_list.count, reverse=True)
    conf_matrix = confusion_matrix(y_true, y_pred, labels=classes)
    normal_conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
    normal_conf_matrix = np.nan_to_num(normal_conf_matrix)
    accuracy_per_label = jaccard_score(y_true, y_pred, average=None, labels=classes)
    classes = [str(c) if not isinstance(c, str) else c for c in classes]

    # Save accuracy per label to the report dict
    for i, category in enumerate(classes):
        report_dict[category]["accuracy"] = accuracy_per_label[i]

    output = {
        'report': report_dict,
        'confusion_matrix': conf_matrix.tolist(),
        'normalized_confusion_matrix': normal_conf_matrix.tolist(),
        'accuracy_score': accuracy,
        'cohen_kappa_score': cohen_kappa,
        'classes': classes
    }

    return round_dict(output, 4)

def round_dict(data, n_digits):
    """
    Recursively round all floats in a dictionary to n digits.

    :param data: the dictionary
    :type data: dict
    :param n_digits: amount of digits to round to
    :type n_digits: int
    :return: the dictionary with values rounded
    :rtype: dict
    """

    result = data.copy()

    for key, value in data.items():
        if isinstance(value, float):
            result[key] = round(value, n_digits)
        elif isinstance(value, dict):
            result[key] = round_dict(value, n_digits)
        elif isinstance(value, list):
            result[key] = round_list(value, n_digits)

    return result

def round_list(data, n_digits):
    """
    Recursively round all floats in a list to n digits.

    :param data: the list to round
    :type data: list
    :param n_digits: amount of digits to round to
    :type n_digits: int
    :return: the list with values rounded
    :rtype: list
    """

    result = data.copy()

    for i, value in enumerate(data):
        if isinstance(value, float):
            result[i] = round(value, n_digits)
        elif isinstance(value, list):
            result[i] = round_list(value, n_digits)

    return result
