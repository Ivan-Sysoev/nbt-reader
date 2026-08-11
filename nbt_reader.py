import gzip
import struct
from enum import Enum

class NBT_Tags(Enum):
    TAG_End        = b'\x00'
    TAG_Byte       = b'\x01'
    TAG_Short      = b'\x02'
    TAG_Int        = b'\x03'
    TAG_Long       = b'\x04'
    TAG_Float      = b'\x05'
    TAG_Double     = b'\x06'
    TAG_Byte_Array = b'\x07'
    TAG_String     = b'\x08'
    TAG_List       = b'\t'
    TAG_Compound   = b'\n'

def determine_tag(nbt_file):
    try:
        byte = read_byte(nbt_file)
        return NBT_Tags(byte)
    except ValueError as e:
        e.add_note('Cannot determine tag')
        raise

def determine_tag_name(nbt_file):
    tag_name_len = int.from_bytes(nbt_file.read(2))
    tag_name = nbt_file.read(tag_name_len).decode('UTF-8')
    return tag_name

def determine_read_func(tag):
    func_tags = {
        NBT_Tags.TAG_Byte: read_byte,
        NBT_Tags.TAG_Short: read_short,
        NBT_Tags.TAG_Int: read_int,
        NBT_Tags.TAG_Long: read_long,
        NBT_Tags.TAG_Float: read_float,
        NBT_Tags.TAG_Double: read_double,
        NBT_Tags.TAG_Byte_Array: read_byte_array,
        NBT_Tags.TAG_String: read_string,
        NBT_Tags.TAG_List: read_list,
        NBT_Tags.TAG_Compound: read_compound,
    }
    read_func = func_tags.get(tag)
    if not read_func:
        raise RuntimeError(f'Cannot determine read_func for tag: {tag}')
    return read_func

def read_string(nbt_file):
    str_len = int.from_bytes(nbt_file.read(2))
    type_str = nbt_file.read(str_len).decode('UTF-8')
    return type_str

def read_byte(nbt_file):
    type_byte = nbt_file.read(1)
    return type_byte

def read_long(nbt_file):
    type_long = struct.unpack('>q', nbt_file.read(8))
    return type_long[0]

def read_int(nbt_file):
    type_int = struct.unpack('>i', nbt_file.read(4))
    return type_int[0]

def read_short(nbt_file):
    type_short = struct.unpack('>h', nbt_file.read(2))
    return type_short[0]

def read_double(nbt_file):
    type_double = struct.unpack('>d', nbt_file.read(8))
    return type_double[0]

def read_float(nbt_file):
    type_float = struct.unpack('>f', nbt_file.read(4))
    return type_float[0]

def read_byte_array(nbt_file):
    byte_array_len = int.from_bytes(nbt_file.read(4))
    type_byte_array = bytearray(nbt_file.read(byte_array_len))
    return type_byte_array

def read_list(nbt_file):
    elem_tag = determine_tag(nbt_file)
    list_len = int.from_bytes(nbt_file.read(4))

    read_func = determine_read_func(elem_tag)
    type_list = [read_func(nbt_file) for _ in range(list_len)]
    return type_list

def read_compound(nbt_file):
    type_compound = {}

    while True:
        tag = determine_tag(nbt_file)
        if tag == NBT_Tags.TAG_End:
            break

        tag_name = determine_tag_name(nbt_file)
        tag_data = process_tag(nbt_file, tag)

        type_compound[tag_name] = tag_data

    return type_compound

def process_tag(nbt_file, tag):
    read_func = determine_read_func(tag)
    tag_data = read_func(nbt_file)
    return tag_data

def read_nbt_file(nbt_file_path):
    with gzip.open(nbt_file_path, 'rb') as nbt_file:
        tag = determine_tag(nbt_file)
        if tag != NBT_Tags.TAG_Compound:
            raise RuntimeError('NBT Data should start with Compound')

        compound_name = determine_tag_name(nbt_file)
        compound_data = read_compound(nbt_file)

    return compound_data

def main():
    test_nbt = 'bigtest.nbt'
    nbt_data = read_nbt_file(test_nbt)
    print(nbt_data)

if __name__ == "__main__":
    main()
