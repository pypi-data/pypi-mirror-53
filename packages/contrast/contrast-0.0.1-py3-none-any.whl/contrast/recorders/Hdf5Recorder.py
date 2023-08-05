from . import Recorder
import h5py
import time
import numpy as np
import os

class Hdf5Recorder(Recorder):
    """
    Recorder which writes to hdf5 files.
    """
    def __init__(self, name=None):
        Recorder.__init__(self, name=name)
        self.fp = None

    def act_on_header(self, dct):
        """
        Opens a file when a new scan starts.
        """
        filename = os.path.join(dct['path'], '%06u.h5'%dct['scannr'])
        if os.path.isfile(filename):
            print('************ WARNING ************')
            print('Data already exists! Hdf5Recorder')
            print('won''t write data to this target.')
            print('*********************************')
            self.fp = None
        else:
            self.fp = h5py.File(filename, 'w')
            self.act_on_data({'snapshot':dct['snapshot']}, base='entry/')

    def act_on_data(self, dct, base='entry/measurement/'):
        """
        Write data packets to the h5 file.
        """
        if self.fp is None:
            print('** no hdf5 file open, so not writing anything')
            return
        for key, val in dct.items():
            name = base + key

            # treat dict values recursively
            if type(val) == dict:
                new_dct = {key + '/' + str(k): v for k, v in val.items()}
                self.act_on_data(new_dct, base=base)
                continue

            # decide where to put the new data
            if not name in self.fp:
                # create datasets the first time around
                if isinstance(val, np.ndarray):
                    # arrays
                    d = self.fp.create_dataset(name, shape=(1,)+val.shape, maxshape=(None,)+val.shape, dtype=val.dtype)
                elif isinstance(val, h5py.ExternalLink):
                    # links
                    layout = h5py.VirtualLayout(shape=(1,)+val.shape, maxshape=(None,)+val.shape, dtype=val.dtype)
                    self.fp.create_virtual_dataset(name, layout)
                elif (type(val) == str):
                    # strings
                    d = self.fp.create_dataset(name, shape=(1,), maxshape=(None,), dtype='S100')
                else:
                    # scalars of any type
                    d = self.fp.create_dataset(name, shape=(1,), maxshape=(None,), dtype=type(val))
            else:
                # then resize datasets
                d = self.fp[name]
                d.resize((d.shape[0]+1,) + d.shape[1:])

            # special case: convert strings
            if type(val) == str:
                val = val.encode(encoding='ascii', errors='ignore')

            # write the data
            if isinstance(val, h5py.ExternalLink):
                vsource = h5py.VirtualSource(val.filename, val.path, shape=val.shape)
                d[-1] = vsource
            else:
                # a dataset
                d[-1] = val

    def act_on_footer(self):
        """
        Closes the file after the scan.
        """
        if self.fp is not None:
            self.fp.flush()
            self.fp.close()
