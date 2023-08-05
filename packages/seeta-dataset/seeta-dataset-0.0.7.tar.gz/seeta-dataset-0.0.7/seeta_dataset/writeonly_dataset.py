import json
import struct
import os
from seeta_dataset import base


class WriteOnlyDataset:
    """Create a new seeta dataset for writing seeta records
    Args:
        base_path: ...
        dataset_id: ...
        record_type: ...
    Examples:
    ```python
    >>> import seeta_dataset as sd
    >>> rt = sd.record_type.new_record_type({
    >>>        "s": BasicType.String,
    >>>        "i": BasicType.Int,
    >>>        "f": BasicType.Float,
    >>>        "l_s": [BasicType.String],
    >>>        "l_i": [BasicType.Int],
    >>>        "m": {
    >>>            "x": BasicType.Int,
    >>>            "y": BasicType.Float,
    >>>            "s": BasicType.String,
    >>>        },
    >>>        "l_m": [{
    >>>            "x": BasicType.Int,
    >>>            "y": BasicType.Float,
    >>>        }]
    >>>    })
    >>> with WriteOnlyDataset("./", "test", rt) as dataset:
    >>>     dataset.write({
    >>>         "s": "ssssss",
    >>>         "i": 1,
    >>>         "f": 1.1,
    >>>         "l_s": ["l_s_1", "l_s_2"],
    >>>         "l_i": [1, 2, 3],
    >>>         "m": {
    >>>             "x": 1,
    >>>             "y": 1.1,
    >>>             "s": "m.s",
    >>>         },
    >>>         "l_m": [{
    >>>             "x": 1,
    >>>             "y": 1.1,
    >>>             "s": "m.s",
    >>>         }, {
    >>>             "x": 1,
    >>>             "y": 1.1,
    >>>             "s": "m.s",
    >>>         }]
    >>>     })
    >>>
    ```
    """
    def __init__(self, base_path, dataset_id=None, record_type=None):
        self._base_path = base_path
        self._dataset_id = dataset_id or base.DEFAULT_DATA_NAME
        self._record_type = record_type

        self._version = 0

        meta_file_path = os.path.join(self._base_path, "{}.meta".format(self._dataset_id))
        if os.path.exists(meta_file_path):
            raise base.FileExistError(meta_file_path)
        self._meta_file = open(meta_file_path, 'w')

        index_file_path = os.path.join(self._base_path, "{}.index".format(self._dataset_id))
        if os.path.exists(index_file_path):
            raise base.FileExistError(index_file_path)
        self._index_file = open(index_file_path, 'wb')

        data_file_path = os.path.join(self._base_path, "{}.data".format(self._dataset_id))
        if os.path.exists(data_file_path):
            raise base.FileExistError(data_file_path)
        self._data_file = open(data_file_path, 'wb')

        self._indexes = []
        self._current = 0

    def get_id(self):
        return self._dataset_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return None
        self.close()
        return True

    def close(self):
        self._meta_file.write(json.dumps(self.dump()))
        self._meta_file.close()
        self._indexes.append(self._current)
        index_data = struct.pack('<{}Q'.format(len(self._indexes)), *self._indexes)
        self._index_file.write(index_data)
        self._index_file.close()
        self._data_file.close()

    def dump(self):
        return {
            'Version': self._version,
            "ID": self._dataset_id,
            "RecordType": self._record_type.dump(),
        }

    def write(self, record):
        buffer = bytearray()
        length = self._record_type.encode(record, buffer)
        self._data_file.write(buffer)
        self._indexes.append(self._current)
        self._current += length


if __name__ == '__main__':
    from seeta_dataset.record_type import new_record_type, BasicType
    rt = new_record_type({
        "s": BasicType.String,
        "i": BasicType.Int,
        "f": BasicType.Float,
        "l_s": [BasicType.String],
        "l_i": [BasicType.Int],
        "m": {
            "x": BasicType.Int,
            "y": BasicType.Float,
            "s": BasicType.String,
        },
        "l_m": [{
            "x": BasicType.Int,
            "y": BasicType.Float,
        }],
        "b": BasicType.ByteArray,
    })
    with WriteOnlyDataset(".", "test", rt) as dataset:
        dataset.write({
            "s": "ssssss",
            "i": 1,
            "f": 1.1,
            "l_s": ["l_s_1", "l_s_2"],
            "l_i": [1, 2, 3],
            "m": {
                "x": 1,
                "y": 1.1,
                "s": "m.s",
            },
            "l_m": [{
                "x": 1,
                "y": 1.1,
                "s": "m.s",
            }, {
                "x": 1,
                "y": 1.1,
                "s": "m.s",
            }],
            "b": bytes(b'abcdefg')
        })

    print("done")
