import json
import struct
from os import path
import random
from seeta_dataset.record_type import RecordType
from seeta_dataset import base
import glob


class ReadOnlyDataset:
    """Read seeta records from seeta dataset
    Args:
        base_path: ...
        dataset_id: ...
    Examples:
    ```python
    read seeta dataset in order
    >>> dataset = ReadOnlyDataset("./", "test")
    >>> for data in dataset.read():
    >>>     print(data)
    read seeta dataset randomly
    >>> dataset = ReadOnlyDataset("./", "test")
    >>> for data in dataset.random_read():
    >>>     print(data)
    ```
    """
    def __init__(self, base_path, dataset_id):
        dataset_id = dataset_id or base.DEFAULT_DATA_NAME
        if not path.isfile(path.join(base_path, "{}.meta".format(dataset_id))):
            dataset_id = glob.glob("{}/*.data".format(base_path))[0].split(".")[0]
        self._dataset_id = dataset_id
        self._base_path = base_path

        meta_file_path = path.join(self._base_path, "{}.meta".format(self._dataset_id))
        with open(meta_file_path, 'r') as meta_file:
            meta_data = meta_file.read()
            meta_obj = json.loads(meta_data)
            self._version = meta_obj["Version"]
            self._record_type = RecordType.load(meta_obj["RecordType"])

        index_file_path = path.join(self._base_path, "{}.index".format(self._dataset_id))
        with open(index_file_path, 'rb') as index_file:
            index_data = index_file.read()
            self._indexes = struct.unpack("<{}Q".format(int(len(index_data)/struct.calcsize("Q"))), index_data)

        data_file_path = path.join(self._base_path, "{}.data".format(self._dataset_id))
        self._data_file = open(data_file_path, 'rb')
        self._cursor = 0

    def read(self, start=0, count=None):
        if count is None:
            count = self.record_count() - start
        current_pos = self._indexes[start]
        self._data_file.seek(current_pos, 0)
        for i in range(count):
            next_pos = self._indexes[start+i+1]
            d = self._data_file.read(next_pos-current_pos)
            yield self._record_type.decode(memoryview(d))
            current_pos = next_pos

    def random_read(self):
        start_index = list(range(len(self._indexes) - 1))
        random.shuffle(start_index)
        for si in start_index:
            start_pos = self._indexes[si]
            end_pos = self._indexes[si + 1]
            self._data_file.seek(start_pos, 0)
            d = self._data_file.read(end_pos - start_pos)
            yield self._record_type.decode(memoryview(d))

    def record_count(self):
        return len(self._indexes)-1

    def data_size(self):
        return self._indexes[-1]

    def get(self):
        start_pos = self._indexes[self._cursor]
        end_pos = self._indexes[self._cursor + 1]
        d = self._data_file.read(end_pos - start_pos)
        self._cursor += 1
        return self._record_type.decode(memoryview(d))

    def set_cursor(self, index):
        start = self._indexes[index]
        self._data_file.seek(start, 0)
        self._cursor = index

    def close(self):
        self._data_file.close()


if __name__ == "__main__":
    dataset = ReadOnlyDataset(".", "test")
    for data in dataset.read():
        print(data)
