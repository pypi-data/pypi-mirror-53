from seeta_dataset.readonly_dataset import ReadOnlyDataset
from seeta_dataset.writeonly_dataset import WriteOnlyDataset


class DataCenter(object):
    def __init__(self, root):
        self._root = root

    def load_dataset(self, dataset_id):
        return ReadOnlyDataset(self._root, dataset_id)

    def create_dataset(self, record_type, dataset_id=None):
        return WriteOnlyDataset(self._root, dataset_id, record_type)
