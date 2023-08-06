"""
These functions are originally located at `Catalyst. Reproducible and fast DL & RL`_

Some methods were formatted and simplified.

.. _`Catalyst. Reproducible and fast DL & RL`:
    https://github.com/catalyst-team/catalyst
"""
import argparse
import copy
import json
import re
from collections import OrderedDict, Mapping
from pathlib import Path
from pydoc import locate
from typing import List, Any, Type, Optional, Union

import yaml

from safitty import core
from .types import Storage


def argparser(**argparser_kwargs) -> argparse.ArgumentParser:
    """Creates typical argument parser with ``--config`` argument
    Args:
        **argparser_kwargs: Arguments for ``ArgumentParser.__init__``, optional.
            See more at `Argparse docs`_
    Returns:
        (ArgumentParser): parser with ``--config`` argument

    .. _`Argparse docs`:
        https://docs.python.org/3/library/argparse.html#argumentparser-objects
    """
    argparser_kwargs = argparser_kwargs
    parser_ = argparse.ArgumentParser(**argparser_kwargs)

    parser_.add_argument(
        "-C", "--config", "--configs",
        nargs="+",
        required=True,
        dest="configs",
        help="Path to a config file/files (YAML or JSON)",
        metavar="{PATH}"
    )
    return parser_


class OrderedLoader(yaml.Loader):
    pass


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


OrderedLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def is_file_supported(suffix: str) -> bool:
    """
    Check a path to be supported by safitty (only YAML or JSON)

    Args:
        suffix (str): path extension

    Returns:
        bool: File is YAML or JSON
    """
    return suffix in [".json", ".yml", ".yaml"]


def is_path_readable(path: Union[Path, str]) -> bool:
    """
    Check a path to be a safitty-readable

    Args:
        path (Union[Path, str]): path to file

    Returns:
        bool: Can be read with ``safitty.load``
    """
    path = Path(path)
    return path.exists() and is_file_supported(path.suffix)


def load(
    path: Union[str, Path],
    ordered: bool = False,
    data_format: str = None,
    encoding: str = "utf-8"
) -> Storage:
    """Loads config by giving path. Supports YAML and JSON files.
    Args:
        path (str): path to config file (YAML or JSON)
        ordered (bool): if true the config will be loaded as ``OrderedDict``
        data_format (str): ``yaml``, ``yml`` or ``json``. If not specified,
            safitty looks at ``path.suffix``
        encoding (str): encoding to read the config
    Returns:
        (Storage): Config
    Raises:
        Exception: if path ``config_path`` doesn't exists or file format is not YAML or JSON
    Examples:
        >>> load(path="./config.yml", ordered=True)
    """
    path = Path(path)

    if not path.exists():
        raise Exception(f"Path '{path}' doesn't exist!")

    if data_format is not None:
        suffix = data_format.lower()
        if not suffix.startswith("."):
            suffix = f".{suffix}"
    else:
        suffix = path.suffix

    if not is_file_supported(suffix):
        raise ValueError(f"Unknown file format '{suffix}'")

    storage = None
    with path.open(encoding=encoding) as stream:
        if suffix == ".json":
            object_pairs_hook = OrderedDict if ordered else None
            file = "\n".join(stream.readlines())
            if file != "":
                storage = json.loads(file, object_pairs_hook=object_pairs_hook)

        elif suffix in [".yml", ".yaml"]:
            loader = OrderedLoader if ordered else yaml.Loader
            storage = yaml.load(stream, loader)

    if storage is None:
        return dict()

    return storage


def save(
    storage: Storage,
    path: Union[str, Path],
    data_format: str = None,
    encoding: str = "utf-8",
    ensure_ascii: bool = False,
    indent: int = 2,
) -> None:
    """
    Saves config to file. Path must be either YAML or JSON
    Args:
        storage (Storage): config to save
        path (Union[str, Path]): path to save
        data_format (str): ``yaml``, ``yml`` or ``json``. If not specified,
            safitty looks at ``path.suffix``
        encoding (str): Encoding to write file. Default is ``utf-8``
        ensure_ascii (bool): Used for JSON, if True non-ASCII
            characters are escaped in JSON strings.
        indent (int): Used for JSON
    """
    path = Path(path)

    if data_format is not None:
        suffix = data_format
    else:
        suffix = path.suffix

    if not is_file_supported(suffix):
        raise ValueError(f"Unknown file format '{suffix}'")

    with path.open(encoding=encoding, mode="w") as stream:
        if suffix == ".json":
            json.dump(
                storage, stream,
                indent=indent, ensure_ascii=ensure_ascii
            )
        elif suffix in [".yml", ".yaml"]:
            yaml.dump(storage, stream)


def type_from_str(dtype: str) -> Type:
    """Returns type by giving string
    Args:
        dtype (str): string representation of type
    Returns:
        (Type): type
    Examples:
        >>> type_from_str("str")
        str
        >>> type_from_str("int")
        int
        >>> type(type_from_str("int"))
        type
    """
    return locate(dtype)


def parse_content(value: str) -> Any:
    """Parses strings ``value:dtype`` into typed value. If you don't want to parse ``:`` as type
        then wrap input with quotes
    Args:
        value (str): string with form ``value:dtype`` or ``value``
    Returns:
        (Any): value of type ``dtype``, if ``dtype`` wasn't specified value will be parsed as string
    Examples:
        >>> parse_content("True:bool")
        True # type is bool
        >>> parse_content("True:str")
        "True" # type is str
        >>> parse_content("True")
        "True" # type is str
        >>> parse_content("'True:bool'")
        'True:bool' # type is str
        >>> parse_content("some str")
        "some str" # type is str
        >>> parse_content("1:int")
        1 # type is int
        >>> parse_content("1:float")
        1.0 # type is float
        >>> parse_content("[1,2]:list")
        [1, 2] # type is list
        >>> parse_content("'[1,2]:list'")
        '[1,2]:list' # type is str
    """
    quotes_wrap = """^["'][^ ].*[^ ]["']$"""
    if re.match(quotes_wrap, value) is not None:
        value_content = value[1:-1]
        return value_content

    content = value.rsplit(":", 1)
    if len(content) == 1:
        value_content, value_type = content[0], "str"
    else:
        value_content, value_type = content

    result = value_content

    if value_type in ["set", "list", "dict", "frozenset"]:
        try:
            result = eval(f"{value_type}({value_content})")
        except Exception:
            result = value_content
    else:
        value_type = type_from_str(value_type)
        if value_type is not None:
            result = value_type(value_content)

    return result


def update_from_args(config: Storage, args: List[str]) -> Storage:
    """Updates configuration file with list of arguments
    Args:
        config (Storage): configuration dict
        args (List[str]): list of arguments with form ``--key:dtype:value:dtype``
    Returns:
        (Storage): updated config
    """
    updated_config = copy.deepcopy(config)

    for argument in args:
        names, value = argument.split("=")
        names = names.lstrip("-").strip("/")

        value = parse_content(value)
        names = [parse_content(name) for name in names.split("/")]

        updated_config = core.set(updated_config, *names, value=value)

    return updated_config


def update(config: Storage, updated_config: Storage) -> Storage:
    """Updates configuration with an additional config
    Args:
        config (Storage): configuration dict
        updated_config (Storage): dict with updates
    Returns:
        (Storage): updated config
    """
    result = copy.copy(config)
    for k, v in updated_config.items():
        if isinstance(v, Mapping):
            result[k] = update(result.get(k, {}), v)
        else:
            result[k] = v
    return result


def load_from_args(
        *,
        parser: Optional[argparse.ArgumentParser] = None,
        arguments: Optional[List[str]] = None,
        ordered: bool = False
) -> (argparse.Namespace, Storage):
    """Parses command line arguments, loads config and updates it with unknown args
    Args:
        parser (ArgumentParser, optional): an argument parser
            if none uses ``safitty.argparser()`` by default
        arguments (List[str], optional): arguments to parse, if None uses command line arguments
        ordered (bool): if True loads the config as an ``OrderedDict``
    Returns:
        (Namespace, Storage): arguments from args and a
            config dict with updated values from unknown args
    Examples:
        >>> load_from_args(
        >>>    arguments="-C examples/config.json examples/another.yml --paths/jsons/0:int=uno".split()
        >>> )
    """
    parser = parser or argparser()

    args, uargs = parser.parse_known_args(args=arguments)
    config = {}
    if hasattr(args, "config"):
        config = load(args.config, ordered=ordered)

    if hasattr(args, "configs"):
        for i, config_path in enumerate(args.configs):
            config_ = load(config_path, ordered=ordered)
            config = update(config, config_)
    config = update_from_args(config, uargs)
    return args, config
