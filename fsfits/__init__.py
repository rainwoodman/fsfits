import os.path
import json
import numpy

class Block(object):
    def __init__(self, path):
        self.path = path
        try:
            os.makedirs(self.path)
        except OSError:
            pass
        if not os.path.exists(self.path):
            raise IOError("path %s not avalable" % self.path)

        self.datafilename = os.path.join(
                path, 'data.bin')
        self.dtypefilename = os.path.join(
                path, 'dtype.json')
        self.metadatafilename = os.path.join(
                path, 'meta.json')
        self.metadata = {}

    @classmethod
    def open(kls, path):
        self = kls(path)
        with file(self.dtypefilename, 'r') as ff:
            d = json.load(ff)
            self.dtype = numpy.dtype(d['dtype'])
            self.shape = tuple(d['shape'])
        with file(self.metadatafilename, 'r') as ff:
            self.metadata.update(json.load(ff)) 
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.flush()

    def flush(self):
        with file(self.dtypefilename, 'w') as ff:
            d = {}
            d['dtype'] = self.dtype.descr if len(self.dtype) else self.dtype.str
            d['shape'] = self.shape
            json.dump(d, ff)
        with file(self.metadatafilename, 'w') as ff:
            json.dump(self.metadata, ff)

    def __getitem__(self, index):
        with file(self.datafilename, 'r') as ff:
            data = numpy.fromfile(ff, dtype=self.dtype)
            data = data.reshape(self.shape)
            return data[index]

    def __setitem__(self, index, value):
        with file(self.datafilename, 'r+') as ff:
            all = numpy.fromfile(ff, dtype=self.dtype).reshape(self.shape)
        all[index] = value
        with file(self.datafilename, 'r+') as ff:
            all.tofile(ff)

    @classmethod
    def create(kls, path, shape, dtype):
        self = kls(path)
        self.dtype = numpy.dtype(dtype)
        self.shape = shape
        with file(self.datafilename, 'w') as ff:
            n = numpy.prod(self.shape) * self.dtype.itemsize
            if n > 0:
                ff.seek(n - 1)
                ff.write('\0')
            pass
        self.flush()
        return self

class FSHR(object):
    def __init__(self, path):
        self.path = path
        self.blocksfilename = os.path.join(self.path, 'blocks.json')
         
    @classmethod
    def open(kls, path):
        self = kls(path)
        with file(self.blocksfilename, 'r') as ff:
            self.blocks = json.load(ff)
        return self

    @classmethod
    def create(kls, path):
        self = kls(path)
        self.blocks = []
        try:
            os.makedirs(self.path)
        except OSError:
            pass
        if not os.path.exists(self.path):
            raise IOError("path %s not avalable" % self.path)

        self.flush()
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.flush()

    def flush(self):
        with file(self.blocksfilename, 'w') as ff:
            json.dump(self.blocks, ff)

    def create_block(self, blockname, shape, dtype):
        assert blockname not in self.blocks
        bb = Block.create(
                os.path.join(self.path, blockname), 
                    shape, dtype)
        self.blocks.append(blockname)
        self.blocks = sorted(self.blocks)
        return bb

    def __iter__(self):
        return iter(self.blocks)
    def __contains__(self, key):
        return key in self.blocks

    def __getitem__(self, blockname):
        assert blockname in self.blocks
        return Block.open(os.path.join(self.path, blockname))
