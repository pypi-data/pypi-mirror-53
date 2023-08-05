# generated by eelbrain/scripts/make_example_tests.py
from importlib import import_module
import logging
import os
from pathlib import Path
import re
from tempfile import TemporaryDirectory

import mne
import pytest

from eelbrain import configure
from eelbrain.testing import working_directory


DATASETS = {
    'mne_sample': bool(mne.datasets.sample.data_path(download=False))
}

# find examples
examples_dir = Path(__file__).parents[2] / 'examples'
examples = [x for x in examples_dir.iterdir() if x.is_dir()]


@pytest.mark.parametrize("example_dir", examples)
def test_example(example_dir):
    "Run the example script at ``filename``"
    configure(show=False)
    with TemporaryDirectory() as temp_dir, working_directory(temp_dir):
        temp_dir = Path(temp_dir)
        # link files
        for file in example_dir.iterdir():
            if not file.name.startswith(('.', '_')):
                os.link(file, temp_dir / file.name)

        # run *.py files
        for example in example_dir.glob('*.py'):
            # check for flags
            text = example.read_text()
            if re.findall("^# skip test:", text, re.MULTILINE):
                return
            # check for required modules
            required_modules = re.findall(r"^# requires: (\w+)$", text, re.MULTILINE)
            for module in required_modules:
                print(repr(module))
                try:
                    import_module(module)
                except ImportError:
                    pytest.skip(f"required module {module} not available")
            # check for required datasets
            required_datasets = re.findall(r"^# dataset: (\w+)$", text, re.MULTILINE)
            for dataset in required_datasets:
                if not DATASETS[dataset]:
                    raise pytest.skip(f"required dataset {dataset} not available")

            # reduce computational load
            text = text.replace("n_samples = 1000", "n_samples = 2")

            # execute example
            logging.info(" Executing %s/%s", example_dir.name, example.name)
            exec(text, {})
