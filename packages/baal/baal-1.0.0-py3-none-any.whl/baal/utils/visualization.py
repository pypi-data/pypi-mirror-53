import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d


def get_best_for_heuristics(trials, heuristic, metric, top_k=5, objective=min, global_best=True):
    """
    Get the `k`-best trials on a `metric` for a specific `heuristic`.
    Args:
        trials: {trialid: dict} all trials
        heuristic: str, name of the heuristic.
        metric: str, name of the metric
        top_k: int, number of trials to return
        objective: function to determine how to sort the metric.
        global_best: bool, if True, compute the `objective` on all sample.
                           Otherwise, use the 100 most recent samples.

    Returns:
        list of the `k`-best trials.
    """
    # If the metric is not in the trial, it may be because the trial has not yet started.
    trials = [trial for trial in trials.values() if
              trial['heuristic'] == heuristic and metric in trial]
    g = (lambda lst: lst) if global_best else (lambda lst: lst[-100:])
    trials = sorted(trials,
                    key=lambda trial: objective(g(trial[metric])),
                    reverse=objective == 'max')[:top_k]
    return trials


def get_all_heuristics(trials):
    """Gather all heuristics from all trials."""
    heuristics = [trial['heuristic'] for trial in trials.values()]
    return np.unique(np.array(heuristics).reshape([-1]))


def smooth_line(y, sigma=2):
    """Smooth the line defined by `y` with a gaussian filter."""
    return gaussian_filter1d(y, sigma=sigma)


def plot_trial(trials, x_axis, y_axis, label_fn, top_k=5, objective=min, global_best=True,
               save_path=None, log=False):
    """
    Plot the following trials.
    Args:
        trials: {trialid: dict} all trials to be plotted.
        x_axis: str, name of the metric for the x axis.
        y_axis: str, name of the metric for the y axis
        label_fn: trial -> str, function that compute the label for a trial.
        top_k: Number of trials per heuristic to plot.
        objective: function to determine how to sort the metric.
        global_best: bool, if True, compute the `objective` on all sample per trial.
                           Otherwise, use the 100 most recent samples.
        save_path: str, if not None, wioll save the figure to the specified path.
    """
    plt.rcParams['figure.figsize'] = 10, 10
    all_best = [i for heuristic in get_all_heuristics(trials) for i in
                get_best_for_heuristics(trials, heuristic, y_axis, top_k, objective, global_best)]

    for trial in all_best:
        if log:
            print(trial)
        if trial['heuristic'] != 'random':
            pass
        data = sorted(zip(trial[x_axis], trial[y_axis]), key=lambda k: k[0])
        x, y = zip(*data)

        lbl = label_fn(trial)
        plt.plot(x, smooth_line(y, 3), label=lbl)

    plt.ylim(0., 1)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.legend()
    if save_path:
        plt.savefig(save_path)
    plt.show()
