import os
import sys
import json
import base64
from nbt_reader import read_nbt_file

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return base64.b64encode(obj).decode('utf-8')
        return super().default(obj)

def main():
    if len(sys.argv) < 2:
        print(f'Usage: python3 {os.path.basename(__file__)} <input.nbt>')
        exit(1)

    test_nbt = sys.argv[1]
    nbt_data = read_nbt_file(test_nbt)

    json_data = json.dumps(nbt_data, indent=4, cls=BytesEncoder)
    print(json_data)

if __name__ == "__main__":
    main()
