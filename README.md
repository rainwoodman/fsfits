# fsfits

Converting fits filts to a file system hierarchy and the other way around.

Recently it has been pointed out that HDF5 is faster than FITS format by a
large margin.

(http://arxiv.org/pdf/1505.06421v1.pdf)

We think going to raw binary files are even faster. (c) 

Since the file system is also hierarchical as HDF5, the FITS data model can
be easily mapped to a file system hierarchy.

Hence fsfits is born:

    python fits2fs.py inputfits  outputfsdir

    import fsfits

    with fsfits.FSHR.open('outputfsdir') as ff:
        for key in ff:
            hdu = ff[key]
            print hdu.metadata
            print hdu[...]


(c) Note that this claim still has to be backed up by benchmarks.

