from times import compute_overlap_time, time_range

def test_given_input_like_sample():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    expected = [
        ("2010-01-12 10:30:00","2010-01-12 10:37:00"),
        ("2010-01-12 10:38:00","2010-01-12 10:45:00"),
    ]
    assert compute_overlap_time(large, short) == expected

def test_no_overlap_returns_empty():
    left  = time_range("2020-01-01 10:00:00","2020-01-01 11:00:00")
    right = time_range("2020-01-01 11:00:01","2020-01-01 12:00:00")
    assert compute_overlap_time(left, right) == []

def test_multiple_intervals_on_both_sides():
    a = time_range("2020-01-01 10:00:00","2020-01-01 12:00:00", 2, 0)  # [10:00–11:00], [11:00–12:00]
    b = time_range("2020-01-01 10:30:00","2020-01-01 12:30:00", 2, 0)  # [10:30–11:30], [11:30–12:30]
    expected = [
        ("2020-01-01 10:30:00","2020-01-01 11:00:00"),
        ("2020-01-01 11:00:00","2020-01-01 11:30:00"),
        ("2020-01-01 11:30:00","2020-01-01 12:00:00"),
    ]
    assert compute_overlap_time(a, b) == expected

def test_touching_ranges_count_as_no_overlap():
    # a ends exactly when b starts → expect empty
    a = time_range("2020-01-01 10:00:00","2020-01-01 11:00:00")
    b = time_range("2020-01-01 11:00:00","2020-01-01 12:00:00")
    assert compute_overlap_time(a, b) == []
