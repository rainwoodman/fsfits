import fsfits
from argparse import ArgumentParser
ap = ArgumentParser()

ap.add_argument('input')

ns = ap.parse_args()

def main():
    with fsfits.FSHR.open(ns.input) as fout:
        for key in fout:
            print key
            hdu = fout[key]
            header = hdu.metadata
            print header
            data = hdu[:]
            print data
main()
