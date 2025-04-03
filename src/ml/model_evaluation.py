# src/ml/model_evaluation.py
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score
import numpy as np

def plot_confusion_matrix(y_true, y_pred, labels=None, title="Confusion Matrix", save_path=None):
    """
    Plot a labeled confusion matrix.

    Parameters:
    - y_true: array-like of shape (n_samples,)
    - y_pred: array-like of shape (n_samples,)
    - labels: list of label names [optional]
    - title: str, title of the plot
    - save_path: str or Path, optional path to save the figure
    """
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(title)
    if labels:
        ax.xaxis.set_ticklabels(labels)
        ax.yaxis.set_ticklabels(labels)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path)
        print(f"Confusion matrix saved to: {save_path}")
    else:
        plt.show()

def compute_accuracy(y_true, y_pred):
    """
    Compute accuracy score.
    
    Returns:
    - float: accuracy as a decimal between 0 and 1
    """
    return accuracy_score(y_true, y_pred)
