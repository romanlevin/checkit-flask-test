import os
import sys

src_path = os.path.dirname(__file__)
distlib_path = os.path.join(src_path, 'distlib')

if not distlib_path in sys.path:
    sys.path.insert(0, distlib_path)
