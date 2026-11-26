import pytest
from pathlib import Path
from engine.ingest.connector import CorpusConnector
from engine.ingest.integrity import CorpusInspector
from engine.ingest.partitioner import Partitioner
from server.kernel.runtime_config import runtime

def test_dataset_loading_and_validation():
    hasoc_path = runtime.base_dir / "corpus" / "source" / "codemix_hi_en.jsonl"
    adapter = CorpusConnector(
        file_path=str(hasoc_path),
        text_column="text",
        label_column="label"
    )
    records = adapter.load()
    assert len(records) > 0

    val = CorpusInspector.validate(records)
    assert val["is_valid"] is True
    assert val["sample_count"] == len(records)
    assert "0" in val["class_distribution"]
    assert "1" in val["class_distribution"]

def test_dataset_splitting_stratification():
    hasoc_path = runtime.base_dir / "corpus" / "source" / "codemix_hi_en.jsonl"
    adapter = CorpusConnector(str(hasoc_path))
    records = adapter.load()
    train, val, test = Partitioner.split(records, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15, seed=42)

    assert len(train) + len(val) + len(test) == len(records)
    assert len(train) > len(val)

