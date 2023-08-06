from time import time

from clldutils.clilib import ParserError

from cldfbench import get_dataset, ENTRY_POINT


class DatasetNotFoundException(Exception):
    pass


def add_dataset_spec(parser):
    parser.add_argument(
        'dataset',
        metavar='DATASET',
        help='Dataset spec, either ID of installed dataset or path to python module')
    parser.add_argument(
        '--entry-point',
        help='Name of entry_points to identify datasets',
        default=ENTRY_POINT)


def add_catalog_spec(parser, name):
    parser.add_argument(
        name,
        metavar=name.upper(),
        help='Path to repository clone of {0} data'.format(name.capitalize()))
    parser.add_argument(
        '--{0}-version'.format(name),
        help='Version of {0} data to checkout'.format(name.capitalize()),
        default=None)


def with_dataset(args, func):
    dataset = get_dataset(args.dataset, ep=args.entry_point)
    if not dataset:
        raise DatasetNotFoundException("No matching dataset found!")
    s = time()
    args.log.info('processing %s ...' % dataset.id)
    arg = [dataset]
    if isinstance(func, str):
        func_ = getattr(dataset, '_cmd_' + func, getattr(dataset, 'cmd_' + func, None))
        if not func_:
            raise ParserError('Dataset {0} has no {1} command'.format(dataset.id, func))
        func, arg = func_, []
    print(func)
    func(*arg, **vars(args))
    args.log.info('... done %s [%.1f secs]' % (dataset.id, time() - s))
