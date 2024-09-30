from datasets import load_dataset
import lancedb
import pytest
import main

# ==================== TESTING ====================


@pytest.fixture
def mock_embed_func(monkeypatch):
    def mock_api_call(*args, **kwargs):
        return [0.5, 0.5]

    monkeypatch.setattr(main, "embed", mock_api_call)


@pytest.fixture
def mock_embed_txt_func(monkeypatch):
    def mock_api_call(*args, **kwargs):
        return [0.5, 0.5]

    monkeypatch.setattr(main, "embed_txt", mock_api_call)


def test_main(mock_embed_func, mock_embed_txt_func):
    global dataset
    dataset = load_dataset(
        "CVdatasets/ImageNet15_animals_unbalanced_aug1", split="train"
    )
    main.dataset = dataset

    db = lancedb.connect("./data/tables")

    global tbl
    try:
        tbl = main.create_data(db)
        main.tbl = tbl
    except:
        tbl = db.open_table("animal_images")
        main.tbl = tbl

    print(tbl.to_pandas())

    global test
    test = load_dataset(
        "CVdatasets/ImageNet15_animals_unbalanced_aug1", split="validation"
    )
    main.test = test

    main.image_search(0)
    main.text_search("a full white dog")
