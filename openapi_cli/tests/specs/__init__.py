import os
import json

from ..utils import get_file_dir


SPEC_DIR = get_file_dir(__file__)

with open(os.path.join(SPEC_DIR, "spec.json")) as f:
    TEST_SPEC_YAML = json.loads(f.read())
