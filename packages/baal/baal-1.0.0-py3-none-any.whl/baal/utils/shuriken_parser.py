import argparse
from collections import defaultdict

import numpy as np
import pandas as pd
from shuriken.api import ShurikenApi

np.set_printoptions(precision=5, linewidth=1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
SHURIKEN_URL = "http://shk-service.eai-shuriken-prod.svc.borgy-k8s.elementai.lan/api/v1"


def get_all_experiments(shk_api):
    response_experiments = shk_api.get_experiments()
    nb_pages = response_experiments['pages']
    experiments = response_experiments['results']
    for page in range(2, nb_pages + 1):
        experiments += shk_api.get_experiments(page=page)['results']
    all_experiments_names = []
    for experiment in experiments:
        all_experiments_names.append(experiment['name'])
    return experiments, all_experiments_names


def get_all_trials(shk_api, experiment_name, metric, extras):
    response_trials = shk_api.get_trials(experiment_name)
    nb_pages = response_trials['pages']
    trials = response_trials['results']
    for page in range(2, nb_pages + 1):
        trials += shk_api.get_trials(experiment_name, page=page)['results']
    all_trials_dict = dict()
    for trial in trials:
        all_trials_dict[trial['id']] = trial['parameters']
        for metric_t in trial['metrics']:
            if metric_t['name'] == metric:
                all_trials_dict[trial['id']].update({metric: metric_t['values']})
            elif metric_t['name'] in extras:
                all_trials_dict[trial['id']].update(
                    {metric_t['name']: metric_t['values'][-1]}
                )
    return all_trials_dict


def format_metrics(all_metrics, metric, sort_by='min'):
    dict_results = defaultdict(list)
    if len(all_metrics) > 0:
        first_key = list(all_metrics.keys())[0]
        hparams = [k for k, v in all_metrics[first_key].items() if k != metric]
        hparams_dict = {k: [] for k in hparams}
        dict_results.update(hparams_dict)
        index = []
        for key in all_metrics:
            dict_metric = all_metrics[key]
            if metric in dict_metric:
                dict_results['max'].append(np.max(dict_metric[metric]))
                dict_results['min'].append(np.mean(dict_metric[metric]))
                dict_results['mean'].append(np.std(dict_metric[metric]))
                dict_results['std'].append(np.min(dict_metric[metric]))
                for k, v in hparams_dict.items():
                    dict_results[k].append(dict_metric[k])
                index.append(key)
        return (pd.DataFrame(dict_results, index=index).sort_values(sort_by), hparams)


def get_dataframe(
    shk_api: ShurikenApi, experiment_name: str, metric: str, extras: [str]
) -> (pd.DataFrame, list):
    all_metrics = get_all_trials(shk_api, experiment_name, metric, extras)
    dataframe = format_metrics(all_metrics, metric)
    return dataframe


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment_name', help='Name of the Shuriken experiment.')
    _metric_help = """Name of the metric you want monitored."""
    parser.add_argument('--metric', default='val_loss', help=_metric_help)
    _extras_help = """Any extra columns that you want appended to the result.
     Only the last value will be kept."""
    parser.add_argument('--output_file', default='out.json', help='Output json filepath.')
    parser.add_argument('--extras', nargs='+', default=[], help=_extras_help)
    return parser.parse_args()


def main():
    args = parse_args()
    api = ShurikenApi(SHURIKEN_URL, None)
    df, columns = get_dataframe(api, args.experiment_name, args.metric, args.extras)
    print(df.head())
    # Output is not pretty use : python -m json.tool < $OUTPUT_FILE
    df.to_json(args.output_file, orient='records')


if __name__ == '__main__':
    main()
