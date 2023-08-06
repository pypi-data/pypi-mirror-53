'''Generic storage interfaces with a common api
   So far, only file-based interfaces are implemented (.json and .npy)
   
   Here, metrics are for a specific file (root),
   such as a large binary or video file'''

import os
import shutil
import numpy as np

try:
    import simplejson as json
except ImportError:
    import json

class MetricsStorageInterface(object):
    def __init__(self):
        pass
    
    def exists(self, root_file, metric_name):
        pass
    
    def save_metric(self, root_file, metric_name):
        pass
    
    def get_metric(self, root_file, metric_name):
        pass

def _create_tmp(filepath):
    '''Change something.ext into something.tmp.ext'''
    f, ext = os.path.splitext(filepath)
    return f + '.tmp' + ext

class FileBasedStorageInterface(MetricsStorageInterface):
    def __init__(self, file_ext, metrics_dir=None):
        self.file_ext=file_ext
        self.metrics_dir = metrics_dir

    def _get_metric_filename(self, root_file, metric_name, metrics_dir=None):
        '''Rework the filepath of the root file into a filepath to a metric'''
        root_dir, root_name = os.path.split(root_file)
        metrics_dir = (metrics_dir if metrics_dir is not None else
                       self.metrics_dir if self.metrics_dir is not None else
                       os.path.join(root_dir, 'metrics'))
        new_name = root_name.replace('.', '_') + '_' + metric_name + self.file_ext
        filename = os.path.join(metrics_dir, new_name)
        return filename
    
    def exists(self, root_file, metric_name):
        '''Test if a given metric already exists'''
        filepath = self._get_metric_filename(root_file, metric_name)
        return os.path.exists(filepath)
    
    def _get_metric(self, filepath):
        return None
    
    def _save_metric(self, filepath, metric_data):
        pass
    
    def get_metric(self, root_file, metric_name):
        filepath = self._get_metric_filename(root_file, metric_name)
        return self._get_metric(filepath)
    
    def save_metric(self, root_file, metric_name, metric_data):
        filepath = self._get_metric_filename(root_file, metric_name)
        tmp = _create_tmp(filepath)
        self._save_metric(tmp, metric_data)
        shutil.move(tmp, filepath)
    
# Json is a less-than-ideal storage format for binary data, but it's easy:
def _to_flat(x):
    return (x.tolist() if type(x) == np.ndarray else x)

class JsonStorageInterface(FileBasedStorageInterface):
    def __init__(self, metrics_dir=None):
        FileBasedStorageInterface.__init__(self, file_ext='.json', metrics_dir=metrics_dir)
    
    def _get_metric(self, filepath):
        return json.load(filepath)
    
    def _save_metric(self, filepath):
        json.dump(filepath, _to_flat(metric_data)) # Force numpy arrays to lists

# Npy is a actually a great storage format for this:
class NpyStorageInterface(FileBasedStorageInterface):
    def __init__(self, metrics_dir=None):
        FileBasedStorageInterface.__init__(self, file_ext='.npy', metrics_dir=metrics_dir)
    
    def _get_metric(self, filepath):
        return np.load(filepath)
    
    def _save_metric(self, filepath, metric_data):
        np.save(filepath, metric_data)

# This could work by storing a "document" version of a number of different
# metrics in a single file which would cut down on file usage, but make
# it harder to update with new metrics.
##class NpyConsolidatedStorageInterface(MetricsStorageInterface)
#class NpzStorageInterface(MetricsStorageInterface)
# Pytables might be another alternative.
##class PyTablesStorageInterface(MetricsStorageInterface)

##    ........eventually probably a better way for some applications:)
#class SQLStorageInterface(MetricsStorageInterface):

if __name__ == '__main__':
    pass
