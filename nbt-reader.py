import json
import os
import struct
from enum import Enum
import gzip

# already after gzip decompression
test_nbt = 'bigtest.nbt'

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

def read_bytes(file):
    while True:
        data = file.read(1).hex()
        if not data:
            return
        yield data

def determine_tag(nbt_file):
    try:
        byte = read_byte(nbt_file)
        return NBT_Tags(byte)
    except ValueError as e:
        raise ValueError('Cannot determine tag\n' + e)

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
        raise RuntimeError(f'Cannot determin read_func for tag: {tag}')
    return read_func

def read_compound(nbt_file):
    file_size = os.fstat(nbt_file.fileno()).st_size
    
    type_compound = {}
    print('Start of Compound')

    while True:
        tag = determine_tag(nbt_file)
        if tag == NBT_Tags.TAG_End:
            break

        tag_name = determine_tag_name(nbt_file)
        tag_data = process_tag(nbt_file, tag)

        type_compound[tag_name] = tag_data

        print(tag, tag_name, end='\t')
        print(tag_data)

    print('End of Compound\n')
    return type_compound

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
    # byte_array_len = read_int(nbt_file)
    byte_array_len = int.from_bytes(nbt_file.read(4))
    print(f'byte_array_len = {byte_array_len}')

    type_byte_array = bytearray(nbt_file.read(byte_array_len))
    return type_byte_array

def read_list(nbt_file):
    elem_tag = determine_tag(nbt_file)
    list_len = int.from_bytes(nbt_file.read(4))

    # print(f'elem_type: {elem_tag} list_len: {list_len}')

    read_func = determine_read_func(elem_tag)
    type_list = [read_func(nbt_file) for _ in range(list_len)]
    return type_list

def read_nbt_file(nbt_file_path):
    with gzip.open(nbt_file_path, 'rb') as nbt_file:
        # if read_byte(nbt_file) != NBT_Tags.TAG_Compound.value:
        #     raise RuntimeError('Invalid nbt file; Should begin with TAG_Compound')

        tag = determine_tag(nbt_file)
        if tag != NBT_Tags.TAG_Compound:
            raise RuntimeError('NBT Data should start with Compound')

        compound_name = determine_tag_name(nbt_file)
        compound_data = read_compound(nbt_file)

    return compound_data
            
def process_tag(nbt_file, tag):
    read_func = determine_read_func(tag)
    tag_data = read_func(nbt_file)
    return tag_data

def main():
    # decompressed_nbt = decompress_nbt(test_nbt)
    # read_nbt_file(decompressed_nbt)
    nbt_data = read_nbt_file(test_nbt)

    # with open('nbt_data.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(nbt_data, json_file)

if __name__ == "__main__":
    main()
