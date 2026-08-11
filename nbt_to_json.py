import json
import base64
from nbt_reader import read_nbt_file

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return base64.b64encode(obj).decode('utf-8')
        return super().default(obj)

def main():
    test_nbt = 'bigtest.nbt'
    nbt_data = read_nbt_file(test_nbt)

    json_data = json.dumps(nbt_data, indent=4, cls=BytesEncoder)
    print(json_data)

if __name__ == "__main__":
    main()
