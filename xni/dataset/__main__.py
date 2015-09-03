from pathlib import Path
import argparse

from .io import create


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

    info_parser = subparsers.add_parser('info', help='info help')
    info_parser.add_argument('filename', help='filename help')
    info_parser.set_defaults(func=start_info)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


def _findtiff(path, prefix):
    return sorted([p for p in path.iterdir() if p.match(prefix.strip()+'*') and (p.suffix.lower() in ['.tif', '.tiff'])])


def start_create(args):
    path = Path(args.path)
    images = _findtiff(path, args.image_prefix)
    bgnds = _findtiff(path, args.background_prefix) if args.background_prefix != None else []
    darks = _findtiff(path, args.dark_prefix) if args.dark_prefix != None else []
    # TODO: dataset.create will accept pathlib
    images = [str(im) for im in images]
    bgnds = [str(im) for im in bgnds]
    darks = [str(im) for im in darks]
    for i, name in create(args.output, images, bgnds, darks):
        print(i, name)


def start_info(args):
    import h5py
    fname = args.filename
    with h5py.File(fname, 'r') as f:
        for dset in f:
            print(dset)
            for d in f[dset]:
                print('-', d)


parse_args()
