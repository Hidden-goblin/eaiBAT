# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
from eaiBat import EaiBat


class TestEvidenceFolder:
    def setup_class(self):
        self.my_eai = EaiBat()
        self.my_eai.step = ("Given", "first")

    def test_nominal_case(self, tmp_path):
        self.my_eai.evidence_location = tmp_path

        assert self.my_eai.evidence_location == tmp_path
