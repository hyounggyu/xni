import argparse

# Absolute import because Flask app
from xni.manage.dataset import start_create
from xni.manage.viewer import start_view, start_remoteview
from xni.manage.monitor import start_monitor

def parse_args():
    parser = argparse.ArgumentParser(prog='xni.manage')
    parser.add_argument('--version', help='version help')

    subparsers = parser.add_subparsers(help='sub commands')

    create_parser = subparsers.add_parser('create', help='create help')
    create_parser.add_argument('path', help='path help')
    create_parser.add_argument('-o', '--output', help='output help')
    create_parser.add_argument('-i', '--image-prefix', help='image prefix help')
    create_parser.add_argument('-b', '--background-prefix', help='background image prefix help', required=False)
    create_parser.add_argument('-d', '--dark-prefix', help='dark image prefix help', required=False)
    create_parser.set_defaults(func=start_create)

    view_parser = subparsers.add_parser('view', help='view help')
    view_parser.add_argument('filename', help='filename help')
    view_parser.add_argument('--group', help='group help', required=False)
    view_parser.add_argument('--dataset', help='dataset help', required=False)
    view_parser.set_defaults(func=start_view)

    remoteview_parser = subparsers.add_parser('remoteview', help='removeview help')
    remoteview_parser.add_argument('--ip', help='ip help', required=False)
    remoteview_parser.add_argument('--port', help='port help', required=False)
    remoteview_parser.add_argument('--step', help='slice help ex.', required=False, type=int)
    remoteview_parser.set_defaults(func=start_remoteview)

    monitor_parser = subparsers.add_parser('monitor', help='monitor help')
    monitor_parser.add_argument('--port', help='port help', required=False, type=int)
    monitor_parser.set_defaults(func=start_monitor)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

parse_args()
