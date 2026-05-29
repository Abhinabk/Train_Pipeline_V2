from parsing.get_station_delay import station_delay
from storage.readers.load_html import get_station_html
from transformations.common import wide_to_long


def transform_station_delay_to_long(data):
    return wide_to_long(
        data,
        id_vars=["train_no", "date"],
        var_name="station_code",
        value_name="delay",
    )
if __name__ == "__main__":
    html = get_station_html('15959')
    data = station_delay(html,'15959')
    print(transform_station_delay_to_long(data))
