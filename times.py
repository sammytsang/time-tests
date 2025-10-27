import datetime as dt

_FMT = "%Y-%m-%d %H:%M:%S"

def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    
    start = dt.datetime.strptime(start_time, _FMT)
    end   = dt.datetime.strptime(end_time, _FMT)

    if number_of_intervals <= 0:
        return []

    total_seconds = (end - start).total_seconds()
    total_gap = gap_between_intervals_s * max(0, number_of_intervals - 1)

    if total_seconds < 0:
        raise ValueError("end_time must be after start_time")
    if total_seconds < total_gap:
        raise ValueError("not enough time to fit intervals with the requested gaps")

    # Each interval duration (seconds)
    seg = (total_seconds - total_gap) / number_of_intervals

    out = []
    cur = start
    for _ in range(number_of_intervals):
        seg_end = cur + dt.timedelta(seconds=seg)
        out.append((cur.strftime(_FMT), seg_end.strftime(_FMT)))
        cur = seg_end + dt.timedelta(seconds=gap_between_intervals_s)
    return out


def compute_overlap_time(range1, range2):
 
    overlaps = []
    for s1, e1 in range1:
        for s2, e2 in range2:
            low  = max(s1, s2)
            high = min(e1, e2)
            if low < high:            # critical guard: only positive-length overlaps
                overlaps.append((low, high))
    return overlaps
