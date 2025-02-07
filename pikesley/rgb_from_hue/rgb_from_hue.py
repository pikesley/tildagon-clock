from math import floor


def get_segments():
    """Get the segments."""
    pattern = [1, None, 0, 0, None, 1]
    offsets = {"red": 0, "blue": 2, "green": 4}

    segments = []
    for i in range(6):
        segments.append({"offset": i * 60})
        for component, offset in offsets.items():
            index = (i + offset) % len(
                pattern
            )  # because `deque` isn't the same in micropython
            if pattern[index] is not None:
                segments[-1][component] = pattern[index]

    return segments


segments = get_segments()


def get_sector(degrees):
    """Determine which sector we're in."""
    return int(floor(degrees / 60))


def rgb_from_degrees(degrees):
    """Get RGB from degrees of rotation."""
    sector = get_sector(degrees)
    segment = segments[sector]
    offset = (1 / 60) * (degrees - segment["offset"])

    if sector % 2 == 1:
        offset = 1 - offset

    return [segment.get(x, offset) for x in ["red", "green", "blue"]]


def rgb_from_hue(decimal):
    """Get RGB from hue value (0.0 - 1.0)."""
    return rgb_from_degrees((decimal * 360) % 360)
