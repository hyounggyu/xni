from pathlib import Path

from ..dataset.io import create


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
