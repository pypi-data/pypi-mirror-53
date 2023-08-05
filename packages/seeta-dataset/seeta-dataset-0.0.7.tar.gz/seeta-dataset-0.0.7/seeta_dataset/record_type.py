import struct
from enum import Enum


class BasicType(Enum):
    String = "String"
    Int = "Int"
    Float = "Float"
    ByteArray = "ByteArray"
    List = "List"
    Map = "Map"


size_of_uint64 = struct.calcsize("<Q")


class RecordType:
    def __init__(self, basic_type):
        self._basicType = basic_type
        if basic_type == BasicType.Map:
            self._keys = []
            self._properties = {}
        elif basic_type == BasicType.List:
            self._item = None

    @classmethod
    def from_define(cls, path, define):
        if isinstance(define, dict):
            result = RecordType(BasicType.Map)
            for key, value in define.items():
                result._keys.append(key)
                result._properties[key] = cls.from_define(path + [key], value)
            return result
        elif isinstance(define, list):
            if len(define) != 1:
                raise Exception("Bad length", define, '.'.join(path))
            result = RecordType(BasicType.List)
            result._item = cls.from_define(path + ['item'], define[0])
            return result
        elif isinstance(define, BasicType):
            return RecordType(define)
        else:
            raise Exception("Invalid type", define, '.'.join(path))

    def dump(self):
        result = {
            "BasicType": self._basicType.value,
        }
        if self._basicType == BasicType.Map:
            result["Keys"] = self._keys
            result["Properties"] = dict(zip(self._properties, map(RecordType.dump, self._properties.values())))
        elif self._basicType == BasicType.List:
            result["Item"] = self._item.dump()

        return result

    @classmethod
    def load(cls, dump):
        result = RecordType(BasicType(dump["BasicType"]))
        if dump["BasicType"] == "Map":
            result._keys = dump["Keys"]
            result._properties = dict(zip(dump["Properties"], map(RecordType.load, dump["Properties"].values())))
        elif dump["BasicType"] == "List":
            result._item = RecordType.load(dump["Item"])
        return result

    def encode(self, data, buffer):
        if self._basicType == BasicType.Map:
            assert isinstance(data, dict), "but get: {}".format(data)
            length = len(self._keys)
            header_length = (length + 1) * size_of_uint64
            start = len(buffer)
            header = [0] * (length + 1)
            buffer.extend(bytearray(header_length))
            current = 0
            for i, key in enumerate(self._keys):
                header[i] = current
                property_type = self._properties[key]
                value = data[key]
                item_length = property_type.encode(value, buffer)
                current += item_length
            header[length] = current
            buffer[start:start + header_length] = struct.pack('<{}Q'.format(length + 1), *header)
            return header_length + current
        elif self._basicType == BasicType.List:
            assert isinstance(data, list), "but get: {}".format(data)
            length = len(data)
            header_length = (length + 2) * size_of_uint64
            start = len(buffer)
            header = [length] * (length + 2)
            buffer.extend(bytearray(header_length))
            current = 0
            for i, value in enumerate(data):
                header[i + 1] = current
                item_length = self._item.encode(value, buffer)
                current += item_length
            header[length + 1] = current
            buffer[start:start + header_length] = struct.pack('<{}Q'.format(length + 2), *header)
            return header_length + current
        elif self._basicType == BasicType.String:
            assert isinstance(data, str), "but get: {}".format(data)
            b = data.encode()
            buffer.extend(b)
            return len(b)
        elif self._basicType == BasicType.Int:
            assert isinstance(data, int), "but get: {}".format(data)
            b = struct.pack("<Q", data)
            buffer.extend(b)
            return len(b)
        elif self._basicType == BasicType.Float:
            assert isinstance(data, float), "but get: {}".format(data)
            b = struct.pack("<d", data)
            buffer.extend(b)
            return len(b)
        elif self._basicType == BasicType.ByteArray:
            assert (isinstance(data, bytes) or isinstance(data, bytearray)), "but get: {}".format(data)
            buffer.extend(data)
            return len(data)
        else:
            raise Exception("Should not run here")

    def decode(self, data):
        if self._basicType == BasicType.Map:
            length = len(self._keys)
            header_length = (length + 1) * size_of_uint64
            header = struct.unpack("<{}Q".format(int(header_length / size_of_uint64)), data[0:header_length].tobytes())
            result = {}
            current_pos = 0
            for i, key in enumerate(self._keys):
                next_pos = header[i + 1]
                d = data[header_length + current_pos: header_length + next_pos]
                result[key] = self._properties[key].decode(d)
                current_pos = next_pos
            return result
        elif self._basicType == BasicType.List:

            length = struct.unpack("<Q", data[0:8].tobytes())[0]
            header_length = (length + 2) * size_of_uint64
            header = struct.unpack("<{}Q".format(int(header_length / size_of_uint64)), data[0:header_length].tobytes())
            result = []
            current_pos = 0
            for i in range(length):
                next_pos = header[i + 2]
                d = data[header_length + current_pos:header_length + next_pos]
                result.append(self._item.decode(d))
                current_pos = next_pos

            return result
        elif self._basicType == BasicType.String:
            return data.tobytes().decode()
        elif self._basicType == BasicType.Int:
            return struct.unpack("<Q", data.tobytes())[0]
        elif self._basicType == BasicType.Float:
            return struct.unpack("<d", data.tobytes())[0]
        elif self._basicType == BasicType.ByteArray:
            return data.tobytes()
        else:
            raise Exception("Should not run here")


def new_record_type(define):
    return RecordType.from_define([], define)
