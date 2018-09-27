from datetime import datetime


def parse_value(value):
    if isinstance(value, datetime):
        value = str(value)
    return value


def jsonify(records):
    return [{key: parse_value(value) for key, value in
             zip(r.keys(), r.values())} for r in records]


def model_dict(record):
    cls = type(record)
    keys = set(c.name for c in cls)
    return dict((k, parse_value(getattr(record, k))) for k in keys)
