from __future__ import annotations

import os
import subprocess
from pathlib import Path

from ftag import get_mock_file

from upp.main import main

this_dir = Path(__file__).parent


class TestClass:
    def generate_mock(self, out_file, N=100_000):
        _, f = get_mock_file(num_jets=N, fname=out_file)
        f.close()

    def setup_method(self, method):
        os.makedirs("tmp/upp-tests/integration/temp_workspace/ntuples", exist_ok=True)
        self.generate_mock("tmp/upp-tests/integration/temp_workspace/ntuples/data1.h5")
        self.generate_mock("tmp/upp-tests/integration/temp_workspace/ntuples/data2.h5")
        print("setup_method      method:%s" % method.__name__)

    def teardown_method(self, method):
        subprocess.run(["rm", "-r", "tmp"], check=True)
        print("teardown_method   method:%s" % method.__name__)

    def test_run_pdf_auto(self):
        args = [
            "--config",
            str(Path(this_dir / "fixtures/test_conifig_pdf_auto.yaml")),
            "--split",
            "train",
        ]
        main(args)
        args = [
            "--config",
            str(Path(this_dir / "fixtures/test_conifig_pdf_auto.yaml")),
            "--split",
            "val",
        ]
        main(args)

    def test_run_pdf_upscale(self):
        args = [
            "--config",
            str(Path(this_dir / "fixtures/test_conifig_pdf_upscaled.yaml")),
            "--no-merge",
            "--no-norm",
            "--no-plot",
            "--split",
            "train",
        ]
        main(args)

    def test_run_countup(self):
        args = [
            "--config",
            str(Path(this_dir / "fixtures/test_conifig_countup.yaml")),
            "--no-plot",
            "--split",
            "train",
        ]
        main(args)
