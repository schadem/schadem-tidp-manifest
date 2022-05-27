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
        manifest: tm.IDPManifest = tm.IDPManifestSchema().load(
            j)  #type: ignore
        assert manifest
        assert manifest.s3_path


def test_classification_manifest_load(caplog):
    caplog.set_level(logging.DEBUG)
    p = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(p, "data/manifest_with_classification.json")
    with open(manifest_path) as f:
        j = json.load(f)
        assert j
        manifest: tm.IDPManifest = tm.IDPManifestSchema().load(
            j)  #type: ignore

        assert manifest
        assert manifest.s3_path
        assert manifest.classification == "EMPLOYMENT_APPLICATION"


def test_classification_manifest_metadata_load(caplog):
    caplog.set_level(logging.DEBUG)
    p = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(
        p, "data/manifest_with_classification_and_metadata.json")
    with open(manifest_path) as f:
        j = json.load(f)
        assert j
        manifest: tm.IDPManifest = tm.IDPManifestSchema().load(
            j)  #type: ignore
        assert manifest
        assert manifest.s3_path
        assert manifest.classification == "EMPLOYMENT_APPLICATION"


def test_manifest_minimal(caplog):
    caplog.set_level(logging.DEBUG)
    p = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(p, "data/manifest_minimal.json")
    with open(manifest_path) as f:
        j = json.load(f)
        assert j
        manifest: tm.IDPManifest = tm.IDPManifestSchema().load(
            j)  #type: ignore

        assert manifest
        assert manifest.s3_path
        assert not manifest.queries_config
        assert not manifest.textract_features


def test_manifest_analyze_id(caplog):
    caplog.set_level(logging.DEBUG)
    p = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(p, "data/analyze_id.json")
    with open(manifest_path) as f:
        j = json.load(f)
        assert j
        manifest: tm.IDPManifest = tm.IDPManifestSchema().load(
            j)  #type: ignore

        assert manifest
        assert manifest.document_pages
        assert len(manifest.document_pages) == 2
        assert not manifest.queries_config
        assert not manifest.textract_features


def test_manifest_merge(caplog):
    caplog.set_level(logging.DEBUG)
    p = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(p, "data/manifest_minimal.json")
    default_manifest_path = os.path.join(p, "data/manifest_default.json")
    with open(default_manifest_path) as f:
        default_manifest_json = json.load(f)
        assert default_manifest_json
        default_manifest: tm.IDPManifest = tm.IDPManifestSchema().load(
            default_manifest_json)  #type: ignore
        with open(manifest_path) as g:
            manifest_json = json.load(g)
            assert manifest_json
            manifest: tm.IDPManifest = tm.IDPManifestSchema().load(
                manifest_json)  #type: ignore
            manifest.merge(default_manifest)
            assert manifest.s3_path == "s3://amazon-textract-public-content/blogs/employeeapp20210510.png"
            assert len(manifest.textract_features) == 1
            assert manifest.textract_features[0] == 'QUERIES'
            manifest.textract_features = ['FORMS', 'QUERIES']
            manifest.merge(default_manifest)
            assert not manifest.textract_features[0] == 'QUERIES'
