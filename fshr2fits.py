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
    fout = fitsio.FITS(ns.output, mode='rw', clobber=True)
    fin = fsfits.FSHR.open(ns.input)

    with fin:
        for hdukey in fin:
            print hdukey
            hdu = fin[hdukey]
            hduid = int(hdukey[4:])
            header = hdu.metadata
            extname = hdu.metadata.get('EXTNAME', None)
            extver = hdu.metadata.get('EXTVER', None)
            print extname, extver
            if hdu.dtype is not None:
                if len(hdu.dtype) == 0:
                    fout.write_image(hdu[...], 
                            extver=extver, extname=extname, header=header)
                else:
                    fout.write_table(hdu[...], 
                            extver=extver, extname=extname, header=header)
            else:
                fout.write_image(numpy.empty(1, dtype='u1'), 
                        extver=extver, extname=extname, header=header)
main()
