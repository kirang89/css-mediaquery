#!/usr/bin/env python
# coding=utf8

import re


RE_MEDIA_QUERY = r"^(?:(only|not)?\s*([_a-z][_a-z0-9-]*)|(\([^\)]+\)))(?:\s*and\s*(.*))?$"  # noqa
RE_MQ_EXPRESSION = r"^\(\s*([_a-z-][_a-z0-9-]*)\s*(?:\:\s*([^\)]+))?\s*\)$"
RE_MQ_FEATURE = r"^(?:(min|max)-)?(.+)"
RE_LENGTH_UNIT = "(em|rem|px|cm|mm|in|pt|pc)?\s*$"
RE_RESOLUTION_UNIT = "(dpi|dpcm|dppx)?\s*$"


feature_map = {
    "width": lambda x, y: (pixel(x), pixel(y)),
    "height": lambda x, y: (pixel(x), pixel(y)),
    "device-width": lambda x, y: (pixel(x), pixel(y)),
    "device-height": lambda x, y: (pixel(x), pixel(y)),
    "resolution": lambda x, y: (dpi(x), dpi(y)),
    "aspect-ratio": lambda x, y: (decimal(x), decimal(y)),
    "device-aspect-ratio": lambda x, y: (decimal(x), decimal(y)),
    "grid": lambda x, y: (int(x), int(y)),
    "color": lambda x, y: (int(x) if x else 1, int(y) if y else 0),
    "color-index": lambda x, y: (int(x), int(y)),
    "monochrome": lambda x, y: (int(x), int(y))
}

pixel_unit_map = {
    "em": lambda value: value * 16,
    "rem": lambda value: value * 16,
    "cm": lambda value: value * 96 / 2.54,
    "mm": lambda value: value * 96 / 2.54 / 10,
    "in": lambda value: value * 96,
    "pt": lambda value: value * 72,
    "pc": lambda value: value * 72 / 12,
}


def decimal(ratio):
    try:
        decimal_value = float(ratio)
    except ValueError:
        decimal_value = None

    if not decimal_value:
        matched = re.match(r"^(\d+)\s*\/\s*(\d+)$", ratio)
        decimal_value = float(matched.group(1)) / float(matched.group(2))

    return decimal_value


def dpi(resolution):
    value = float(re.match("\d+", resolution).group(0))
    units = re.search(RE_RESOLUTION_UNIT, str(resolution)).group(1)

    if units == "dpcm":
        return value / 2.54
    elif units == "dppx":
        return value * 96

    return value


def pixel(length):
    value = float(re.match("\d+", length).group(0))
    units = re.search(RE_LENGTH_UNIT, str(length)).group(1)

    if units not in pixel_unit_map.keys():
        return value

    return pixel_unit_map[units](value)


def parse(media_query):
    parsed = []
    for query in media_query.split(","):
        query = query.strip()
        match = re.match(RE_MEDIA_QUERY, query)

        if not match:
            raise Exception("Invalid CSS media query: {}".format(query))

        modifier = match.group(1) or False
        type_ = match.group(2)
        subexp1 = match.group(3).strip() if match.group(3) else ''
        subexp2 = match.group(4).strip() if match.group(4) else ''
        expressions = subexp1 + subexp2
        inverse = modifier and modifier.lower() == "not"
        type_ = type_.lower() if type_ else "all"

        if not expressions:
            parsed.append({
                "inverse": inverse,
                "type": type_,
                "expressions": []
            })
            continue

        matches = re.findall(r"(\([^\)]+\))", expressions)

        if not matches:
            raise Exception("Invalid CSS media query: {}".format(query))

        expression_list = []
        for exp in matches:
            matched = re.match(RE_MQ_EXPRESSION, exp)

            if not matched:
                raise Exception("Invalid CSS media query: {}".format(query))

            feature_to_match = matched.group(1).lower()
            feature = re.match(RE_MQ_FEATURE, feature_to_match)

            expression_list.append({
                "modifier": feature.group(1),
                "feature": feature.group(2),
                "value": matched.group(2)
            })

        parsed.append({
            "inverse": inverse,
            "type": type_,
            "expressions": expression_list
        })

    return parsed


def match_expression(exp, values):
    feature = exp["feature"]
    modifier = exp["modifier"]
    value_exp = exp["value"]
    try:
        value = values[feature]
    except KeyError:
        return False

    if feature in ["orientation", "scan"]:
        return value.lower() == value_exp.lower()
    else:
        value_exp, value = feature_map[feature](value_exp, value)

    if modifier == "min":
        return value >= value_exp
    elif modifier == "max":
        return value <= value_exp

    return value == value_exp


def match_query(query, values):
    inverse = query["inverse"]
    qtype = query["type"]
    matches_type = qtype == "all" or qtype == values["type"]

    if (inverse and matches_type) or not (inverse or matches_type):
        return False

    matches_exp = all([match_expression(e, values) for e in query["expressions"]])  # noqa
    return (matches_exp and not inverse) or (not matches_exp and inverse)


def match(media_query, values):
    return any(match_query(query, values) for query in parse(media_query))
