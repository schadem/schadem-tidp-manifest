import logging
import os
import json
import textractmanifest as tm


def test_manifest_load(caplog):
    caplog.set_level(logging.DEBUG)
    p = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(p, "data/simple_feature_manifest.json")
    with open(manifest_path) as f:
        j = json.load(f)
        assert j
        manifest: tm.IDPManifest = tm.IDPManifestSchema().load(j)
        assert manifest
        assert manifest.s3_path
        print(tm.IDPManifestSchema().dumps(manifest))
