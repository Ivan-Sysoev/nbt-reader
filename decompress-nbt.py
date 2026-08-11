import shutil
import gzip
import sys
import os

from pathlib import Path

if len(sys.argv) < 2:
    print(f'Usage: python3 {os.path.basename(__file__)} <input.nbt>')
    exit(1)

nbt_file_path = sys.argv[1]
try:
    output_file = Path(nbt_file_path).stem
    with gzip.open(nbt_file_path, 'rb') as f_in, open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f'Successfully decompressed {nbt_file_path}. Saved as {output_file}')

except Exception as e:
    print(e)
