import fitsio
import fsfits
from argparse import ArgumentParser
import json
import numpy
ap = ArgumentParser()

ap.add_argument('--check', action=store_true, default=False, 
        help="Test if output contains identical information to input")


ap.add_argument('input')
ap.add_argument('output')

ns = ap.parse_args()

def main():
    fin = fitsio.FITS(ns.input)
    if ns.check:
        fout = fsfits.FSHR.open(ns.output)
    else:
        fout = fsfits.FSHR.create(ns.output)

    with fout:
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

            if ns.check:
                block = fout["HDU-%04d" % hdui]
                with block:
                    for key in header:
                        assert header[key] == block.metadata[key]

                    assert (block[...] == data).all()
            else:
                block = fout.create_block("HDU-%04d" % hdui,
                    data.shape, data.dtype)
                with block:
                    block.metadata.update(header)
                    block[...] = data

main()
