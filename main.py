import argparse
from time import sleep
import core


parser = argparse.ArgumentParser(description='')
parser.add_argument(
    '-u', '--url', dest='url', type=str, default='',
    help='Graphite url. e.g.: http://graphite.your.domain.com/'
)
parser.add_argument(
    '-d', '--delay', dest='delay', type=int, default=5,
    help='Delay in seconds between each check. e.g.: 5'
)
parser.add_argument(
    '-f', '--from', dest='data_from', type=str, default='2hours',
    help='Initial time to be get from graphite api. e.g.: 2hours'
)
parser.add_argument(
    '-t', '--to', dest='data_to', type=str, default='6minutes',
    help='Last time to be get from graphite api. e.g.: 6minutes'
)
parser.add_argument(
    '-g', '--granularity', dest='granularity', type=str, default='1minutes',
    help='Grouping data. e.g.: 1minutes'
)
parser.add_argument(
    '-s', '--summarize', dest='summarize', type=str, default='avg',
    help='Group typo. e.g.: avg'
)
parser.add_argument(
    '-e', '--environment', dest='environment', type=str,
    help='Your graphite api environment. e.g.: your.folder.for.env'
)
parser.add_argument(
    '-i', '--instances', dest='instances', type=str, nargs='+',
    help='Machines to be checked. e.g.: machine-name1 machine-name2'
)
parser.add_argument(
    '-m', '--metrics', dest='metrics', type=str, nargs='+',
    help='Metrics for each machine. e.g.: mem.mem_used mem.mem_free'
)


def main(
    delay, url, data_from, data_to, granularity, summarize, environment,
    instances, metrics
):
    print (
        delay, url, data_from, data_to, granularity, summarize, environment,
        instances, metrics, delay
    )

    base_url = core.build_url(
        graphite_url=url, data_from=data_from, data_to=data_to,
        environment=environment, summarize=summarize, granularity=granularity
    )
    print (base_url)

    while True:
        for instance in instances:
            core.process(instance=instance, metrics=metrics, base_url=base_url)
            print ('')
        sleep(delay)


if __name__ == '__main__':
    args = parser.parse_args()
    main(
        delay=args.delay, url=args.url, data_from=args.data_from,
        data_to=args.data_to, granularity=args.granularity,
        summarize=args.summarize, environment=args.environment,
        instances=args.instances, metrics=args.metrics
    )
