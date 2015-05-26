import fitsio
import fsfits
from argparse import ArgumentParser
import json
import numpy
ap = ArgumentParser()

ap.add_argument('input')
ap.add_argument('output')

ns = ap.parse_args()

def main():
    fin = fitsio.FITS(ns.input)
    with fsfits.FSHR.create(ns.output) as fout:
        for hdui, hdu in enumerate(fin):
            header = hdu.read_header()
            header = dict(header)
            type = hdu.get_exttype()
            if hdu.has_data():
                if type in (
                        'BINARY_TBL',
                        'ASCII_TBL'):
                    data = hdu[:]
                elif type in ('IMAGE_HDU'):
                    data = hdu[:, :]
            else:
                data = numpy.empty(0, dtype='i8')

            with fout.create_block("HDU-%04d" % hdui,
                    data.shape, data.dtype) as block:
                block.metadata.update(header)
                block[...] = data

main()
