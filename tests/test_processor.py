import pytest
from processor.adas_processor import ADASProcessor


def test_ttc_calculation():
    processor = ADASProcessor(ttc_threshold=2.0)

    # Speed = 72 km/h → 20 m/s, distance = 40 m → TTC = 2.0s
    ttc = processor.compute_ttc(72, 40)
    assert round(ttc, 2) == 2.0

    # Speed = 0 → TTC = inf
    assert processor.compute_ttc(0, 30) == float('inf')


def test_check_fcw_trigger():
    processor = ADASProcessor(ttc_threshold=2.0)

    # TTC below threshold → FCW = True
    data = {"speed_kph": 100, "distance_m": 20}
    result = processor.check_fcw(data)
    assert result["fcw"] is True
    assert result["ttc"] < 2.0

    # TTC above threshold → FCW = False
    data = {"speed_kph": 60, "distance_m": 100}
    result = processor.check_fcw(data)
    assert result["fcw"] is False
    assert result["ttc"] > 2.0
