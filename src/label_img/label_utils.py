import re


def convertPoints2BndBox(points):
    xmin = float("inf")
    ymin = float("inf")
    xmax = float("-inf")
    ymax = float("-inf")
    for p in points:
        x = p[0]
        y = p[1]
        xmin = min(x, xmin)
        ymin = min(y, ymin)
        xmax = max(x, xmax)
        ymax = max(y, ymax)

    if xmin < 1:
        xmin = 1

    if ymin < 1:
        ymin = 1

    return (int(xmin), int(ymin), int(xmax), int(ymax))


def sorted_alphanumeric(data):
    """
    sort data with alphanumeric order
    Args:
    - data (list of str): data to sort.
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(data, key=alphanum_key)
