#!/usr/bin/env python
# =============================================================================
# Minet CLI Endpoint
# =============================================================================
#
# CLI enpoint of the Minet library.
#
import csv
import sys
import signal
import shutil
import importlib
from textwrap import dedent
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    FileType,
    RawTextHelpFormatter
)

from minet.__version__ import __version__
from minet.defaults import DEFAULT_THROTTLE
from minet.cli.defaults import DEFAULT_CONTENT_FOLDER
from minet.cli.utils import BooleanAction, die

from minet.cli.crowdtangle.constants import (
    CROWDTANGLE_SORT_TYPES,
    CROWDTANGLE_DEFAULT_RATE_LIMIT,
    CROWDTANGLE_PARTITION_STRATEGIES
)

SUBPARSERS = {}

# Getting terminal size
terminal_size = shutil.get_terminal_size()

# Increasing max CSV file limit to avoid pesky issues
csv.field_size_limit(sys.maxsize)

# Hiding stack traces on ctrl+c
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))


def custom_formatter(prog):
    return RawTextHelpFormatter(
        prog,
        max_help_position=50,
        width=terminal_size.columns,
    )


def omit(d, key_to_omit):
    nd = {}

    for k, v in d.items():
        if k == key_to_omit:
            continue

        nd[k] = v

    return nd


def partition_strategy_type(string):
    if string in CROWDTANGLE_PARTITION_STRATEGIES:
        return string

    try:
        return int(string)
    except ValueError:
        choices = ' or '.join(CROWDTANGLE_PARTITION_STRATEGIES)

        raise ArgumentTypeError('partition strategy should either be %s, or an number of posts.' % choices)


def get_subparser(o, keys):
    parser = None

    for key in keys:
        item = o.get(key)

        if item is None:
            return None

        parser = item['parser']

        if 'subparsers' in item:
            o = item['subparsers']
        else:
            break

    return parser


def check_dragnet():
    try:
        import dragnet
    except:
        die([
            'The `dragnet` library is not installed. The `extract` command won\'t work.',
            'To install it correctly, run the following commands in order:',
            '',
            '  pip install lxml numpy Cython',
            '  pip install dragnet'
        ])


# Defining the list of CLI commands
COMMANDS = {

    # Crowdtangle action subparser
    # --------------------------------------------------------------------------
    'crowdtangle': {
        'package': 'minet.cli.crowdtangle',
        'action': 'crowdtangle_action',
        'aliases': ['ct'],
        'title': 'Minet Crowdtangle Command',
        'description': '''
            Gather data from the CrowdTangle APIs easily and efficiently.
        ''',
        'subparsers': {
            'help': 'Action to perform using the CrowdTangle API.',
            'title': 'actions',
            'dest': 'ct_action',
            'common_arguments': [
                {
                    'flag': '--rate-limit',
                    'help': 'Authorized number of hits by minutes. Defaults to %i.' % CROWDTANGLE_DEFAULT_RATE_LIMIT,
                    'type': int,
                    'default': CROWDTANGLE_DEFAULT_RATE_LIMIT
                },
                {
                    'flags': ['-o', '--output'],
                    'help': 'Path to the output file. By default, everything will be printed to stdout.'
                },
                {
                    'flags': ['-t', '--token'],
                    'help': 'CrowdTangle dashboard API token.'
                }
            ],
            'commands': {
                'leaderboard': {
                    'title': 'Minet CrowdTangle Leaderboard Command',
                    'description': '''
                        Gather information and aggregated stats about pages and groups of
                        the designated dashboard (indicated by a given token).
                    ''',
                    'epilog': '''
                        examples:

                        . Fetching accounts statistics for every account in your dashboard:
                            `minet ct leaderboard --token YOUR_TOKEN > accounts-stats.csv`
                    ''',
                    'arguments': [
                        {
                            'flag': '--no-breakdown',
                            'help': 'Whether to skip statistics breakdown by post type in the CSV output.',
                            'dest': 'breakdown',
                            'action': BooleanAction,
                            'default': True
                        },
                        {
                            'flags': ['-f', '--format'],
                            'help': 'Output format. Defaults to `csv`.',
                            'choices': ['csv', 'jsonl'],
                            'default': 'csv'
                        },
                        {
                            'flags': ['-l', '--limit'],
                            'help': 'Maximum number of posts to retrieve. Will fetch every post by default.',
                            'type': int
                        },
                        {
                            'flag': '--list-id',
                            'help': 'Optional list id from which to retrieve accounts.'
                        }
                    ]
                },
                'lists': {
                    'title': 'Minet CrowdTangle Lists Command',
                    'description': '''
                        Retrieve the lists from a CrowdTangle dashboard (indicated by a
                        given token).
                    ''',
                    'epilog': '''
                        examples:

                        . Fetching a dashboard's lists:
                            `minet ct lists --token YOUR_TOKEN > lists.csv`
                    '''
                },
                'posts': {
                    'title': 'Minet CrowdTangle Posts Command',
                    'description': '''
                        Gather post data from the designated dashboard (indicated by
                        a given token).
                    ''',
                    'epilog': '''
                        examples:

                        . Fetching the 500 most latest posts from a dashboard:
                            `minet ct posts --token YOUR_TOKEN --limit 500 > latest-posts.csv`
                    ''',
                    'arguments': [
                        {
                            'flag': '--end-date',
                            'help': 'The latest date at which a post could be posted (UTC!).'
                        },
                        {
                            'flags': ['-f', '--format'],
                            'help': 'Output format. Defaults to `csv`.',
                            'choices': ['csv', 'jsonl'],
                            'default': 'csv'
                        },
                        {
                            'flag': '--language',
                            'help': 'Language of posts to retrieve.'
                        },
                        {
                            'flags': ['-l', '--limit'],
                            'help': 'Maximum number of posts to retrieve. Will fetch every post by default.',
                            'type': int
                        },
                        {
                            'flag': '--list-ids',
                            'help': 'Ids of the lists from which to retrieve posts, separated by commas.'
                        },
                        {
                            'flag': '--partition-strategy',
                            'help': 'Query partition strategy to use to overcome the API search result limits. Should either be `day` or a number of posts.',
                            'type': partition_strategy_type
                        },
                        {
                            'flag': '--resume',
                            'help': 'Whether to resume an interrupted collection. Requires -o/--output & --sort-by date',
                            'action': 'store_true'
                        },
                        {
                            'flag': '--sort-by',
                            'help': 'The order in which to retrieve posts. Defaults to `date`.',
                            'choices': CROWDTANGLE_SORT_TYPES,
                            'default': 'date'
                        },
                        {
                            'flag': '--start-date',
                            'help': 'The earliest date at which a post could be posted (UTC!).'
                        },
                        {
                            'flag': '--url-report',
                            'help': 'Path to an optional report file to write about urls found in posts.',
                            'type': FileType('w')
                        }
                    ]
                },
                'search': {
                    'title': 'Minet CrowdTangle Search Command',
                    'description': '''
                        Search posts on the whole CrowdTangle platform.
                    ''',
                    'epilog': '''
                        examples:

                        . Fetching a dashboard's lists:
                            `minet ct search --token YOUR_TOKEN > posts.csv`
                    ''',
                    'arguments': [
                        {
                            'name': 'terms',
                            'help': 'The search query term or terms.'
                        },
                        {
                            'flag': '--end-date',
                            'help': 'The latest date at which a post could be posted (UTC!).'
                        },
                        {
                            'flags': ['-f', '--format'],
                            'help': 'Output format. Defaults to `csv`.',
                            'choices': ['csv', 'jsonl'],
                            'default': 'csv'
                        },
                        {
                            'flags': ['-l', '--limit'],
                            'help': 'Maximum number of posts to retrieve. Will fetch every post by default.',
                            'type': int
                        },
                        {
                            'flag': '--not-in-title',
                            'help': 'Whether to search terms in account titles also.',
                            'action': 'store_true'
                        },
                        {
                            'flag': '--offset',
                            'help': 'Count offset.',
                            'type': int
                        },
                        {
                            'flag': '--partition-strategy',
                            'help': 'Query partition strategy to use to overcome the API search result limits. Should either be `day` or a number of posts.',
                            'type': partition_strategy_type
                        },
                        {
                            'flags': ['-p', '--platforms'],
                            'help': 'The platforms, separated by comma from which to retrieve posts.'
                        },
                        {
                            'flag': '--sort-by',
                            'help': 'The order in which to retrieve posts. Defaults to `date`.',
                            'choices': CROWDTANGLE_SORT_TYPES,
                            'default': 'date'
                        },
                        {
                            'flag': '--start-date',
                            'help': 'The earliest date at which a post could be posted (UTC!).'
                        },
                        {
                            'flag': '--types',
                            'help': 'Types of post to include, separated by comma.'
                        },
                        {
                            'flag': '--url-report',
                            'help': 'Path to an optional report file to write about urls found in posts.',
                            'type': FileType('w')
                        }
                    ]
                }
            }
        }
    },

    # Extract action subparser
    # -------------------------------------------------------------------------
    'extract': {
        'package': 'minet.cli.extract',
        'action': 'extract_action',
        'title': 'Minet Extract Command',
        'description': '''
            Use multiple processes to extract raw text from a batch of HTML files.
            This command can either work on a `minet fetch` report or on a bunch
            of files. It will output an augmented report with the extracted text.
        ''',
        'epilog': '''
            examples:

            . Extracting raw text from a `minet fetch` report:
                `minet extract report.csv > extracted.csv`

            . Working on a report from stdin:
                `minet fetch url_column file.csv | minet extract > extracted.csv`

            . Extracting raw text from a bunch of files:
                `minet extract --glob "./content/*.html" > extracted.csv`
        ''',
        'before': check_dragnet,
        'arguments': [
            {
                'name': 'report',
                'help': 'Input CSV fetch action report file.',
                'type': FileType('r'),
                'default': sys.stdin,
                'nargs': '?'
            },
            {
                'flags': ['-e', '--extractor'],
                'help': 'Extraction engine to use. Defaults to `dragnet`.',
                'choices': ['dragnet', 'html2text']
            },
            {
                'flags': ['-i', '--input-directory'],
                'help': 'Directory where the HTML files are stored. Defaults to "%s".' % DEFAULT_CONTENT_FOLDER,
                'default': DEFAULT_CONTENT_FOLDER
            },
            {
                'flags': ['-o', '--output'],
                'help': 'Path to the output report file. By default, the report will be printed to stdout.'
            },
            {
                'flags': ['-p', '--processes'],
                'help': 'Number of processes to use. Defaults to 4.',
                'type': int,
                'default': 4
            },
            {
                'flags': ['-s', '--select'],
                'help': 'Columns to include in report (separated by `,`).'
            },
            {
                'flag': '--total',
                'help': 'Total number of HTML documents. Necessary if you want to display a finite progress indicator.',
                'type': int
            }
        ]
    },

    # Facebook actions subparser
    # -------------------------------------------------------------------------
    'facebook': {
        'package': 'minet.cli.facebook',
        'action': 'facebook_action',
        'aliases': ['fb'],
        'title': 'Minet Facebook Command',
        'description': '''
            Collects data from Facebook.
        ''',
        'subparsers': {
            'help': 'Action to perform to collect data on Facebook',
            'title': 'actions',
            'dest': 'fb_action',
            'commands': {
                'comments': {
                    'title': 'Minet Facebook Comments Command',
                    'description': '''
                        Scrape series of comments on Facebook.
                    ''',
                    'epilog': '''
                        examples:

                        . Fetching a dashboard's lists:
                            `minet fb comments`
                    ''',
                    'arguments': [
                        {
                            'name': 'url',
                            'help': 'Url of the post from which to scrape comments.'
                        },
                        {
                            'flags': ['-c', '--cookie'],
                            'help': 'Authenticated cookie to use or browser from which to extract it (support "firefox" and "chrome").',
                            'default': 'firefox'
                        },
                        {
                            'flags': ['-o', '--output'],
                            'help': 'Path to the output report file. By default, the report will be printed to stdout.'
                        }
                    ]
                }
            }
        }
    },

    # Fetch action subparser
    # --------------------------------------------------------------------------
    'fetch': {
        'package': 'minet.cli.fetch',
        'action': 'fetch_action',
        'title': 'Minet Fetch Command',
        'description': '''
            Use multiple threads to fetch batches of urls from a CSV file. The
            command outputs a CSV report with additional metadata about the
            HTTP calls and will generally write the retrieved files in a folder
            given by the user.
        ''',
        'epilog': '''
            examples:

            . Fetching a batch of url from existing CSV file:
                `minet fetch url_column file.csv > report.csv`

            . CSV input from stdin:
                `xsv select url_column file.csv | minet fetch url_column > report.csv`

            . Fetching a single url, useful to pipe into `minet scrape`:
                `minet fetch http://google.com | minet scrape ./scrape.json > scraped.csv`
        ''',
        'arguments': [
            {
                'name': 'column',
                'help': 'Column of the CSV file containing urls to fetch.'
            },
            {
                'name': 'file',
                'help': 'CSV file containing the urls to fetch.',
                'type': FileType('r'),
                'default': sys.stdin,
                'nargs': '?'
            },
            {
                'flags': ['--contents-in-report', '--no-contents-in-report'],
                'help': 'Whether to include retrieved contents, e.g. html, directly in the report\nand avoid writing them in a separate folder. This requires to standardize\nencoding and won\'t work on binary formats.',
                'dest': 'contents_in_report',
                'action': BooleanAction
            },
            {
                'flags': ['-d', '--output-dir'],
                'help': 'Directory where the fetched files will be written. Defaults to "%s".' % DEFAULT_CONTENT_FOLDER,
                'default': DEFAULT_CONTENT_FOLDER
            },
            {
                'flags': ['-f', '--filename'],
                'help': 'Name of the column used to build retrieved file names. Defaults to an uuid v4 with correct extension.'
            },
            {
                'flag': '--filename-template',
                'help': 'A template for the name of the fetched files.'
            },
            {
                'flags': ['-g', '--grab-cookies'],
                'help': 'Whether to attempt to grab cookies from your computer\'s browser.',
                'choices': ['firefox', 'chrome']
            },
            {
                'flags': ['-H', '--header'],
                'help': 'Custom headers used with every requests.',
                'action': 'append',
                'dest': 'headers'
            },
            {
                'flag': '--standardize-encoding',
                'help': 'Whether to systematically convert retrieved text to UTF-8.',
                'action': 'store_true'
            },
            {
                'flags': ['-o', '--output'],
                'help': 'Path to the output report file. By default, the report will be printed to stdout.'
            },
            {
                'flags': ['-s', '--select'],
                'help': 'Columns to include in report (separated by `,`).'
            },
            {
                'flags': ['-t', '--threads'],
                'help': 'Number of threads to use. Defaults to 25.',
                'type': int,
                'default': 25
            },
            {
                'flag': '--throttle',
                'help': 'Time to wait - in seconds - between 2 calls to the same domain. Defaults to %s.' % DEFAULT_THROTTLE,
                'type': float,
                'default': DEFAULT_THROTTLE
            },
            {
                'flag': '--total',
                'help': 'Total number of lines in CSV file. Necessary if you want to display a finite progress indicator.',
                'type': int
            },
            {
                'flag': '--url-template',
                'help': 'A template for the urls to fetch. Handy e.g. if you need to build urls from ids etc.'
            },
            {
                'flags': ['-X', '--request'],
                'help': 'The http method to use. Will default to GET.',
                'dest': 'method',
                'default': 'GET'
            }
        ]
    },

    # Mediacloud action subparser
    # -------------------------------------------------------------------------
    'mediacloud': {
        'package': 'minet.cli.mediacloud',
        'action': 'mediacloud_action',
        'title': 'Minet Mediacloud Command',
        'aliases': ['mc'],
        'description': '''
            Commands related to the MIT Mediacloud API v2.
        ''',
        'arguments': [
            {
                'name': 'topic_id',
                'help': 'Id of the topic'
            },
            {
                'flags': ['-t', '--token'],
                'help': 'Mediacloud API token (also called key).'
            },
            {
                'flags': ['-o', '--output'],
                'help': 'Path to the output report file. By default, the report will be printed to stdout.'
            }
        ],
        # 'subparsers': {
        #     'help': 'Action to perform using the Mediacloud API.',
        #     'title': 'actions',
        #     'dest': 'mc_action',
        #     'common_arguments': [
        #         {
        #             'name': 'topic_id',
        #             'help': 'Id of the topic'
        #         },
        #         {
        #             'flags': ['-t', '--token'],
        #             'help': 'Mediacloud API token (also called key).'
        #         }
        #     ],
        #     'commands': {
        #         'topic': {
        #             'title': 'Minet Mediacloud Topic Command',
        #             'description': '''
        #                 Gather information and aggregated stats about pages and groups of
        #                 the designated dashboard (indicated by a given token).
        #             ''',
        #             'subparsers': {
        #                 'help': 'Topic action to perform.',
        #                 'title': 'topic_actions',
        #                 'dest': 'mc_topic_action',
        #                 'commands': {
        #                     'stories': {
        #                         'title': 'Minet Mediacloud Topic Stories Command',
        #                         'description': 'Retrieves the list of stories from a mediacloud topic.'
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }
    },

    # Scrape action subparser
    # -------------------------------------------------------------------------
    'scrape': {
        'package': 'minet.cli.scrape',
        'action': 'scrape_action',
        'title': 'Minet Scrape Command',
        'description': '''
            Use multiple processes to scrape data from a batch of HTML files.
            This command can either work on a `minet fetch` report or on a bunch
            of files. It will output the scraped items.
        ''',
        'epilog': '''
            examples:

            . Scraping item from a `minet fetch` report:
                `minet scrape scraper.json report.csv > scraped.csv`

            . Working on a report from stdin:
                `minet fetch url_column file.csv | minet scrape scraper.json > scraped.csv`

            . Scraping a single page from the web:
                `minet fetch https://news.ycombinator.com/ | minet scrape scraper.json > scraped.csv`

            . Scraping items from a bunch of files:
                `minet scrape scraper.json --glob "./content/*.html" > scraped.csv`
        ''',
        'arguments': [
            {
                'name': 'scraper',
                'help': 'Path to a scraper definition file.',
                'type': FileType('r')
            },
            {
                'name': 'report',
                'help': 'Input CSV fetch action report file.',
                'type': FileType('r'),
                'default': sys.stdin,
                'nargs': '?'
            },
            {
                'flags': ['-f', '--format'],
                'help': 'Output format.',
                'choices': ['csv', 'jsonl'],
                'default': 'csv'
            },
            {
                'flags': ['-g', '--glob'],
                'help': 'Whether to scrape a bunch of html files on disk matched by a glob pattern rather than sourcing them from a CSV report.'
            },
            {
                'flags': ['-i', '--input-directory'],
                'help': 'Directory where the HTML files are stored. Defaults to "%s".' % DEFAULT_CONTENT_FOLDER,
                'default': DEFAULT_CONTENT_FOLDER
            },
            {
                'flags': ['-o', '--output'],
                'help': 'Path to the output report file. By default, the report will be printed to stdout.'
            },
            {
                'flags': ['-p', '--processes'],
                'help': 'Number of processes to use. Defaults to 4.',
                'type': int,
                'default': 4
            },
            {
                'flag': '--total',
                'help': 'Total number of HTML documents. Necessary if you want to display a finite progress indicator.',
                'type': int
            }
        ]
    },

    # Url Join action subparser
    # -------------------------------------------------------------------------
    'url-join': {
        'package': 'minet.cli.url_join',
        'action': 'url_join_action',
        'title': 'Minet Url Join Command',
        'description': '''
            Join two CSV files by matching them on columns containing urls. In
            fact, the command will index the first file's urls into a
            hierchical trie before attempting to match the second file's ones.
        ''',
        'epilog': '''
            examples:

            . Joining two files:
                `minet url-join url webentities.csv post_url posts.csv > joined.csv`

            . Keeping only some columns from first file:
                `minet url-join url webentities.csv post_url posts.csv -s url,id > joined.csv`
        ''',
        'arguments': [
            {
                'name': 'column1',
                'help': 'Name of the url column in the first file.'
            },
            {
                'name': 'file1',
                'help': 'Path to the first file.',
                'type': FileType('r')
            },
            {
                'name': 'column2',
                'help': 'Name of the url column in the second file.'
            },
            {
                'name': 'file2',
                'help': 'Path to the second file.',
                'type': FileType('r')
            },
            {
                'flags': ['-o', '--output'],
                'help': 'Path to the output joined file. By default, the join will be printed to stdout.'
            },
            {
                'flags': ['-s', '--select'],
                'help': 'Columns from the first file to keep, separated by comma.'
            }
        ]
    },

    # Url Parse action subparser
    # -------------------------------------------------------------------------
    'url-parse': {
        'package': 'minet.cli.url_parse',
        'action': 'url_parse_action',
        'title': 'Minet Url Parse Command',
        'description': '''
            Overload a CSV file containing urls with a selection of additional
            metadata such as their normalized version, domain name etc.
        ''',
        'epilog': '''
            examples:

            . Creating a report about a file's urls:
                `minet url-report url posts.csv > report.csv`

            . Keeping only selected columns from the input file:
                `minet url-report url posts.csv -s id,url,title > report.csv`

            . Multiple urls joined by separator:
                `minet url-report urls posts.csv --separator "|" > report.csv`
        ''',
        'arguments': [
            {
                'name': 'column',
                'help': 'Name of the column containing urls.'
            },
            {
                'name': 'file',
                'help': 'Target CSV file.',
                'type': FileType('r'),
                'default': sys.stdin,
                'nargs': '?'
            },
            {
                'flags': ['-o', '--output'],
                'help': 'Path to the output file. By default, the result will be printed to stdout.'
            },
            {
                'flags': ['-s', '--select'],
                'help': 'Columns to keep in output, separated by comma.'
            },
            {
                'flag': '--separator',
                'help': 'Split url column by a separator?'
            },
            {
                'flag': '--total',
                'help': 'Total number of lines in CSV file. Necessary if you want to display a finite progress indicator.',
                'type': int
            }
        ]
    }
}


def add_arguments(subparser, arguments):
    for argument in arguments:
        if 'name' in argument:
            subparser.add_argument(argument['name'], **omit(argument, 'name'))
        elif 'flag' in argument:
            subparser.add_argument(argument['flag'], **omit(argument, 'flag'))
        else:
            subparser.add_argument(*argument['flags'], **omit(argument, 'flags'))


def build_description(command):
    description = command['title'] + '\n' + ('=' * len(command['title']))

    description += '\n\n' + dedent(command.get('description', ''))

    return description


def build_parser(commands):

    # Building the argument parser
    parser = ArgumentParser(prog='minet')

    parser.add_argument('--version', action='version', version='minet %s' % __version__)

    subparser_index = {}

    subparsers = parser.add_subparsers(
        help='Action to execute',
        title='actions',
        dest='action'
    )

    for name, command in COMMANDS.items():
        subparser = subparsers.add_parser(
            name,
            description=build_description(command),
            epilog=dedent(command.get('epilog', '')),
            formatter_class=custom_formatter,
            aliases=command.get('aliases', [])
        )

        to_index = {
            'parser': subparser,
            'command': command,
            'subparsers': {}
        }

        if 'arguments' in command:
            add_arguments(subparser, command['arguments'])

        # TODO: this could be abstracted in recursive construct
        if 'subparsers' in command:
            subparser_subparsers = subparser.add_subparsers(
                help=command['subparsers']['help'],
                title=command['subparsers']['title'],
                dest=command['subparsers']['dest']
            )

            common_arguments = command['subparsers'].get('common_arguments')

            if common_arguments:
                add_arguments(subparser, common_arguments)

            for subname, subcommand in command['subparsers']['commands'].items():
                subsubparser = subparser_subparsers.add_parser(
                    subname,
                    description=build_description(subcommand),
                    epilog=dedent(subcommand.get('epilog', '')),
                    formatter_class=custom_formatter
                )

                if common_arguments:
                    add_arguments(subsubparser, common_arguments)

                if 'arguments' in subcommand:
                    add_arguments(subsubparser, subcommand['arguments'])

                to_index['subparsers'][subname] = {
                    'parser': subsubparser
                }

        if 'aliases' in command:
            for alias in command['aliases']:
                subparser_index[alias] = to_index

        subparser_index[name] = to_index

    # Help subparser
    help_subparser = subparsers.add_parser('help')
    help_subparser.add_argument('subcommand', help='Name of the subcommand', nargs='*')

    return parser, subparser_index


def main():

    # Building parser
    parser, subparser_index = build_parser(COMMANDS)

    # Parsing arguments and triggering commands
    args = parser.parse_args()

    action = subparser_index.get(args.action)

    if action is not None:

        # Need to check something?
        if 'before' in action['command']:
            action['command']['before']()

        # Lazy loading module for faster startup
        m = importlib.import_module(action['command']['package'])
        fn = getattr(m, action['command']['action'])

        fn(args)

    elif args.action == 'help':
        target = get_subparser(subparser_index, args.subcommand)

        if target is None:
            die('Unknow command "%s"' % ' '.join(args.subcommand))
        else:
            target.print_help()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
