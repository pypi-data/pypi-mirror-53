import glob, os, argparse

"""handle command line inputs"""
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=False,
                help="path to directory of files")
ap.add_argument("-e", "--extension", required=False,
                help="file extension")
args = vars(ap.parse_args())

path = args.get('path')
ext = args.get('extension')

if not path:
    """path defaults to current directory"""
    path = './'

if not ext:
    """extension defaults to csv"""
    ext = "csv"

"""create list of files in path with extension"""
files = [file for file in glob.glob(path + "*." + ext, recursive=True)]

for file in files:
    print(file)
