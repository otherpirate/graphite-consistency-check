import requests
from models import Metric


def build_url(
    graphite_url, data_from, data_to, environment, summarize, granularity
):
    initial_url = '{}render?from=-{}&until=-{}&target=summarize({}.'.format(
        graphite_url, data_from, data_to, environment
    )
    final_url = ',%22{}%22,%22{}%22)&format=json'.format(
        granularity, summarize
    )
    return initial_url + '{}.{}' + final_url


def process(instance, metrics, base_url):
    result = []
    for metric in metrics:
        print ('Processing: {} to {}...'.format(metric, instance))
        points = get_data_points_from_graphite_api(
            base_url.format(instance, metric)
        )

        result.append(Metric(metric, points))

    problems = compare_metrics(result)
    print ('{}: {} problems'.format(instance, len(problems)))
    for problem in problems:
        print '  {}'.format(problem)


def get_data_points_from_graphite_api(url):
    json = requests.get(url=url).json()
    return json[0]['datapoints']


def compare_metrics(metrics):
    print ('Comparing metrics...')
    metric_group = {}

    for metric in metrics:
        for point in metric.points:
            if point.index not in metric_group:
                metric_group[point.index] = {}

            metric_group[point.index].update({
                metric.name: point.value
            })

    gaps = []
    for group, items in metric_group.items():
        if len(items) != len(metrics):
            gaps.append([group, items])
    return gaps
