from gym_display_advertising.data import ProcessedIPinYouData
from pathlib import Path

this_dir = Path(__file__).resolve().parent


def test_parse_ipinyou_data():
    data = ProcessedIPinYouData(
        directory=this_dir / ".." / "data" / "processed_ipinyou"
    )
    train, _ = data.get_merchant_data(merchant_id=2997)
    assert len(train.columns) > 0
    assert train[train.columns[0]].iloc[0] != None
