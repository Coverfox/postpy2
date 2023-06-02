"""postpy2 extractors. (coverfox_modified)
8-Mar-2023
This is modified version of postpy2 library
(we are preventing usage of
request_override,
any file operations,
external libraries that are not already included in our requirements
)
"""
import json
import logging


logger = logging.getLogger(__name__)


def extract_dict_from_raw_mode_data(raw):
    """extract json to dictionay
    :param raw: jsondata
    :return: :extracted dict
    """
    try:
        return json.loads(raw)
    except json.decoder.JSONDecodeError:
        return {}







def extract_dict_from_headers(data):
    """Extract dict from headers."""
    ret_data = {}
    for header in data:
        try:
            if "disabled" in header and header["disabled"] is True:
                continue
            ret_data[header["key"]] = header["value"]
        except ValueError:
            continue

    return ret_data


def format_object(obj, key_values, is_graphql=False):
    """Format object with variables."""
    logger.debug(
        "format_object (%s) %s - is_graphql: %s\nvariables: %s",
        type(obj),
        obj,
        is_graphql,
        key_values.keys(),
    )
    if isinstance(obj, str):
        if is_graphql:
            return obj
        # fixes 'JSON body parsing issue with environment variable replacement #9'
        for key, value in key_values.items():
            logger.debug(key)
            obj = obj.replace(f"{{{{{key}}}}}", str(value))
        logger.debug("formatted object: %s", obj)
        return obj

    if isinstance(obj, dict):
        return format_dict(obj, key_values, is_graphql)

    if isinstance(obj, list):
        return [format_object(oobj, key_values, is_graphql) for oobj in obj]

    logger.warning("Unhandled object of type %s", type(obj))
    return obj


def format_dict(data, key_values, is_graphql):
    """Format dict with variables."""
    kwargs = {}
    for key, value in data.items():
        logger.debug("format '%s' - is_graphql: %s", key, is_graphql)
        kwargs[key] = format_object(
            value,
            key_values,
            is_graphql=(is_graphql and key in ["body", "json", "query", "data"]),
        )
    return kwargs
