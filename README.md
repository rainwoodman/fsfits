# fsfits

Converting fits filts to a file system hierarchy and the other way around.

    python fits2fs.py inputfits  outputfsdir

    import fsfits

    with fsfits.FSHR.open('outputfsdir') as ff:
        for key in ff:
            hdu = ff[key]
            print hdu.metadata
            print hdu[...]
