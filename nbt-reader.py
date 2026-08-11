from os import name
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
    except ValueError:
        return None

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
        NBT_Tags.TAG_Compound: read_compound
    }
    read_func = func_tags.get(tag)
    if not read_func:
        raise RuntimeError(f'Cannot determin read_func for tag: {tag}')
    return read_func

def read_compound(nbt_file):
    print('Compound started')
    return None

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
    pass

def read_list(nbt_file):
    elem_tag = determine_tag(nbt_file)
    list_len = int.from_bytes(nbt_file.read(4))

    print(f'elem_type: {elem_tag} list_len: {list_len}')

    read_func = determine_read_func(elem_tag)
    type_list = [read_func(nbt_file) for _ in range(list_len)]
    return type_list

def read_nbt_file(nbt_file_path):
    with gzip.open(nbt_file_path, 'rb') as nbt_file:
        # if read_byte(nbt_file) != NBT_Tags.TAG_Compound.value:
        #     raise RuntimeError('Invalid nbt file; Should begin with TAG_Compound')

        for _ in range(20):
            tag = determine_tag(nbt_file)
            if tag == NBT_Tags.TAG_End:
                print('End of TAG_Compound')
                continue

            tag_name = determine_tag_name(nbt_file)
            print(tag, tag_name, end='\t')

            print(process_tag(nbt_file, tag))
            
def process_tag(nbt_file, tag):
    if tag == NBT_Tags.TAG_String:
        type_str = read_string(nbt_file)
        return type_str

    if tag == NBT_Tags.TAG_Long:
        type_long = read_long(nbt_file)
        return type_long

    if tag == NBT_Tags.TAG_Byte:
        type_byte = read_byte(nbt_file)
        return type_byte

    if tag == NBT_Tags.TAG_Short:
        type_short = read_short(nbt_file)
        return type_short

    if tag == NBT_Tags.TAG_Int:
        type_int = read_int(nbt_file)
        return type_int

    if tag == NBT_Tags.TAG_Float:
        type_float = read_float(nbt_file)
        return type_float

    if tag == NBT_Tags.TAG_Double:
        type_double = read_double(nbt_file)
        return type_double

    if tag == NBT_Tags.TAG_Byte_Array:
        pass

    if tag == NBT_Tags.TAG_List:
        type_list = read_list(nbt_file)
        return type_list

def main():
    # decompressed_nbt = decompress_nbt(test_nbt)
    # read_nbt_file(decompressed_nbt)
    read_nbt_file(test_nbt)

if __name__ == "__main__":
    main()
