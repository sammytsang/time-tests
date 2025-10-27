import pytest
from times import time_range, compute_overlap_time

@pytest.mark.parametrize(
    "time_range_1, time_range_2, expected",
    [
        # 1) Sample-style sanity test
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
            [
                ("2010-01-12 10:30:00","2010-01-12 10:37:00"),
                ("2010-01-12 10:38:00","2010-01-12 10:45:00"),
            ],
        ),
        # 2) No overlap
        (
            time_range("2020-01-01 10:00:00","2020-01-01 11:00:00"),
            time_range("2020-01-01 11:00:01","2020-01-01 12:00:00"),
            [],
        ),
        # 3) Multiple intervals on both sides
        (
            time_range("2020-01-01 10:00:00","2020-01-01 12:00:00", 2, 0),  # [10–11], [11–12]
            time_range("2020-01-01 10:30:00","2020-01-01 12:30:00", 2, 0),  # [10:30–11:30], [11:30–12:30]
            [
                ("2020-01-01 10:30:00","2020-01-01 11:00:00"),
                ("2020-01-01 11:00:00","2020-01-01 11:30:00"),
                ("2020-01-01 11:30:00","2020-01-01 12:00:00"),
            ],
        ),
        # 4) Touching ranges → no overlap
        (
            time_range("2020-01-01 10:00:00","2020-01-01 11:00:00"),
            time_range("2020-01-01 11:00:00","2020-01-01 12:00:00"),
            [],
        ),
    ],
)
def test_overlap_parametrized(time_range_1, time_range_2, expected):
    assert compute_overlap_time(time_range_1, time_range_2) == expected


# Keep negative/validation tests separate
def test_time_range_raises_on_backwards_times():
    with pytest.raises(ValueError, match="end_time must be after start_time"):
        time_range("2020-01-02 10:00:00", "2020-01-02 09:00:00")
