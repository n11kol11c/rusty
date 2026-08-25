"""
foundation — An all-in-one comprehensive Python utility library providing advanced INI file
management, network scanning, JSON/CSV/XML processing, subprocess execution,
metadata management, type-system utilities, decorators, HTML/CSS generation,
keyboard input handling, and CLI tools. 

=============================================================================
ARCHITECTURE OVERVIEW
=============================================================================

The library is organized into several major subsystems, each residing in the
same module and sharing common base classes, type aliases, and utility functions.

1.  INI Parser & Management (INIO subsystem)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The largest subsystem (~7,000+ lines) built around the `INIO` class and a
    hierarchy of typed INI node objects. It provides:

    - ``CObject`` / ``CObjectMeta`` — Abstract base class and metaclass for all
      INI node types. Every non-abstract subclass must define ``TYPE_NAME: str``,
      is automatically registered with ``INIOTypeRegistry``, and may expose
      ``@validator`` and ``@processor`` decorated methods.
    - ``INIRegion``, ``INIComment``, ``INIKeyValue``, ``INIONotImplemented`` —
      Concrete INI node types representing sections, comments, key-value
      pairs, and unrecognized lines respectively.
    - ``Node`` / ``VirtualNode`` — Tree-node representations used by the
      ``ConfigGraph`` class for graph-based INI manipulation.
    - ``ConfigGraph`` — Builds a directed graph of ``Node`` instances from
      ``INIO`` data, enabling advanced traversal and transformation.
    - ``ExportObserver`` / ``INIExporter`` — Watch for changes and export INI
      data to alternative formats.
    - ``IniValidator`` — Validates INI structure against configurable rules.
    - ``IniWatcher`` — Filesystem-watches an INI file via ``watchdog`` and
      triggers reload callbacks on change.
    - ``IniSerializer`` — Handles serialization to and from formats such as
      JSON, TOML, and YAML.
    - ``IniDiff`` — Computes structural diffs between two INI states.
    - ``IniPlaceholderEngine`` — Resolves ``${...}`` and ``{{...}}`` style
      placeholders within INI values, supporting nested lookups and defaults.
    - ``IniAuditLogger`` — Logs all mutations to INI data for auditing.
    - ``INIO`` (line 1331) — The core INI engine. Maintains five internal
      representations (``full_file``, ``raw_lines``, ``data``, ``keys``,
      ``regions``) and exposes a complete CRUD API with placeholder resolution,
      batch operations, rollback, and file I/O.
    - ``INIODEBUG`` (line 6119) — Debug wrapper around ``INIO`` that logs every
      operation to stdout for troubleshooting.
    - ``INIODESCRIBE`` (line 6343) — Introspection utility that prints the
      structure and metadata of any INI file.
    - ``INIOTyped[T]`` (line 6598) — Generic type-aware INIO that validates
      values against Python type annotations.
    - ``INIOHINTS`` (line 6614) — Lightweight hint/annotation layer for INI
      schema documentation.
    - ``INIODOCS`` (line 6638) — Generates human-readable documentation from
      INI structure and hints.
    - ``INIOMODEL`` (line 6689) — Model-driven INIO that maps INI regions to
      dataclass-like model definitions with automatic serialization.
    - ``INIOApi`` (line 6897) — REST-like API wrapper that exposes INI data
      over HTTP endpoints using GET/POST/PUT/DELETE semantics.
    - ``INIOAI`` (line 7140) — AI-assisted INI query interface using OpenAI
      for natural-language interaction with INI data.
    - ``INIODecorators[T]`` (line 7310) — Decorator-based INI integration that
      binds class methods to INI sections for automatic persistence.
    - ``namespace`` (line 7808) — Class decorator / marker for semantic name-
      spacing of related INI configurations.
    - ``INIOExecute`` (line 7868) — Executes shell commands using INI-stored
      configuration for command construction.
    - ``INIOActivity`` (line 8016) — Activity-tracking layer that records
      all INIO operations with timestamps for replay or audit.
    - ``batch`` (line 9384) — Function that runs shell commands and returns
      a ``Batch`` result object with filtering methods.

2.  Network Scanning (Nmap subsystem)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    A type-safe Python interface to Nmap-style network scanning built around
    the ``Nmap`` class:

    - ``NmapComponent`` — Base class providing common port-type logic (single,
      range, sequence) with validation and parsing.
    - ``OSDetection`` — Detects the local operating system (``win``, ``linux``,
      ``darwin``) and provides normalized names.
    - ``NmapPackage`` — Represents a complete Nmap command package with
      host targets, port specifications, switches, and exclusion rules;
      produces a ready-to-execute CLI string via ``compile()``.
    - ``Ports`` — Comprehensive port representation with nested classes:
      ``Single``, ``Sequence``, ``Range``, ``ExclusionRange``, ``ServicePort``,
      ``TopPortsExtendable``.
    - ``Hosts`` — Host target management with support for IP addresses,
      CIDR ranges, DNS names, and file-based host lists.
    - ``Switches`` — Scan switch/flags management covering timing templates
      (``-T0`` through ``-T5``), output formats, protocol selection,
      and custom arguments.
    - ``Nmap`` — Top-level orchestrator that composes ``NmapPackage``,
      ``Hosts``, ``Ports``, and ``Switches`` into a complete scan
      specification and executes it via subprocess.

3.  Data Format Handlers
    ~~~~~~~~~~~~~~~~~~~~~
    - ``JSW`` (line 8216) — JSON configuration manager with type-safe
      getters, diff tracking, snapshot/rollback, atomic save, and
      namespace support using special path prefixes (``$`` for root,
      ``@`` for values, ``%`` for sub-namespaces).
    - ``CSV`` (line 9107) — CSV reader/writer with dialect detection,
      schema validation, and optional Pandas integration.
    - ``CSVIO`` (line 11820) — Transactional CSV I/O engine supporting
      schema enforcement, row-level transactions, rollback, and
      validation via ``CSVSchemaError`` and ``CSVTransactionError``.
    - ``XML`` (line 9202) — XML reader/writer with tree traversal,
      XPath-like queries, and element construction helpers.

4.  Subprocess & I/O
    ~~~~~~~~~~~~~~~~~
    - ``Batch`` (line 9314) — Immutable result container for shell command
      output (``stdout``, ``stderr``, ``returncode``) with chainable
      filtering methods: ``grep()``, ``awk()``, ``cut()``, ``wc()``,
      ``sort()``, ``uniq()``, ``head()``, ``tail()``, ``join()``,
      ``to_int()``, ``to_csv()``, ``to_json()``, ``dict()``, ``list()``.
    - ``wrapio`` (line 9478) — Static utility class with introspection
      and enforcement decorators: ``do_not_return()`` (raises if the
      function returns a value), ``inline()`` (validates the function
      body is a single return statement via bytecode inspection).

5.  Monadic Result & Signal Types
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    - ``Result[Generic[T, E]]`` (line 12299) — A typed result container
      inspired by Rust's ``Result``, with severity levels SUCCESS, WARN,
      ERROR, FAIL, and ABORT. Provides ``unwrap()``, ``expect()``,
      ``map()``, ``map_err()``, ``and_then()``, ``or_else()``,
      ``to_exception()``, and truthy-on-success semantics.
    - ``Signal`` (line 13190) — Lightweight signal/slot event emitter
      supporting named signals, listener registration, and emission.

6.  Type System & Descriptors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    - ``Define`` (line 13848) — Descriptor protocol that enforces type
      constraints on class attributes at runtime, supporting ``T``,
      ``Optional[T]``, ``List[T]``, ``Dict[K, V]``, and union types.
    - ``define`` (line 13781) — Function that creates a ``Define`` descriptor.
    - ``define_once`` (line 14017) — Metaclass that prevents re-assignment
      of ``Define`` descriptors after their first initialization.
    - ``FrozenVar`` (line 10478) — Immutable variable wrapper with
      ``freeze()`` support; deeply copies mutable containers.
    - ``freeze`` (line 10533) — Function that wraps an arbitrary value
      in a ``FrozenVar``.
    - ``const`` (line 10422) — Function that returns an immutable
      container (raises ``TypeError`` on attribute set).
    - ``Namespace[Generic[_T]]`` (line 15426) — Generic namespace class
      for typed attribute containers.
    - ``VirtualMachineCode[Generic[_T]]`` (line 15499) — Runtime code
      execution sandbox with typed return values.
    - ``Protected`` (line 13393) — Access-control utility that protects
      attributes from external mutation.
    - ``std_typed`` / ``typed`` / ``restrict`` / ``as_`` / ``trust``
      (various lines) — Type-coercion and casting utilities.

7.  Metadata & Markers
    ~~~~~~~~~~~~~~~~~~~
    - ``Meta`` (line 13474) — Singleton metadata class storing project
      information (author, version, GitHub URLs, license) with
      read-only properties.
    - ``export`` (line 14368) — Class-based marker (via ``_ExportMeta``
      metaclass) that declares a value as part of the public API.
    - ``extern`` (line 14434) — Class-based marker (via ``_ExternMeta``
      metaclass) that declares a value as externally defined.
    - ``default`` (line 14452) — Transparent sentinel wrapper for
      function default values, proxying all attribute access and
      operators so the sentinel is invisible in normal use.
    - ``empty`` (line 14607) — Sentinel singleton representing an
      absent or unset value, distinct from ``None``.
    - ``include`` (line 13530) — Dynamic module import utility with
      error handling and caching.
    - ``include_once`` (line 13655) — Prevents repeated imports of
      the same module in a single session.

8.  HTML/CSS Generation
    ~~~~~~~~~~~~~~~~~~~~
    - ``CSSFunctions`` (line 15783) — Static methods for CSS functional
      notation: ``url()``, ``var()``, ``calc()``, ``min()``, ``max()``,
      ``clamp()``, ``rgb()``, ``rgba()``, ``hex()``, ``hsl()``,
      ``hsla()``, ``use()``, ``raw()``.
    - ``CSSImport`` — Represents a CSS ``@import`` rule.
    - ``CSSKeyframes`` — Represents CSS ``@keyframes`` with step management.
    - ``CSSMediaQuery`` / ``CSSMedia`` — Media query representation
      and factory methods (``max_width()``, ``min_width()``, ``dark()``,
      ``light()``, etc.).
    - ``CSSRule`` — Pseudo-class helpers (``_hover``, ``_active``,
      ``_focus``, ``_nth_child``, ``_not``, etc.) and selector
      combinators (``attr()``, ``combine()``, ``global_``, ``class_``,
      ``id`` inner classes).
    - ``CSSStyle`` — A CSS rule block with target, properties, nested
      sub-styles, and rendering methods (``render_inline()``,
      ``render_block()``).
    - ``CSSStyleSheet`` — Collects imports, keyframes, styles, and
      media queries; provides ``add()``, ``render()``, and ``save()``.
    - ``CSSStyleScema`` — TypedDict defining the complete set of CSS
      property fields.
    - ``HTMLElement`` (line 16244) — Base class for all HTML elements
      with ``tag_name``, ``is_void``, ``is_raw``, ``attributes``,
      ``children``, and ``render()``.
    - ``HTMLDocument`` (line 16303) — Full HTML document builder with
      ``add_style()``, ``add_body()``, ``add_script()``, ``render()``,
      and ``save()``.
    - ``JSEvents`` — TypedDict for JavaScript event-handler attributes
      (``on_click``, ``on_keydown``, etc.).
    - ``HTMLSchema`` — TypedDict for HTML element attributes.
    - Concrete element classes: ``Div``, ``Span``, ``P``, ``H1``, ``H2``,
      ``H3``, ``A``, ``Button``, ``Ul``, ``Li``, ``Form``, ``Label``,
      ``Section``, ``Nav``, ``Header``, ``Footer``, ``Img`` (void),
      ``Input`` (void), ``Br`` (void), ``Hr`` (void), ``Link`` (void),
      ``Meta`` (void, guarded), ``Script`` (guarded), ``PHP`` (guarded),
      ``StyleTag`` (guarded).
    - ``TagSchema`` — String-based validator that checks for expected
      HTML tag names.
    - ``DomType`` — Decorated trait class with nested types for
      ``DOCTYPE``, ``HTML``, ``HEAD``, ``META``, ``TITLE``, ``LINK``,
      ``STYLE``, ``BODY``.

9.  Security & Encoding
    ~~~~~~~~~~~~~~~~~~~~
    - ``ENT`` (line 14872) — HTML entity encoding/decoding for the
      five standard entities (``&``, ``<``, ``>``, ``"``, ``'``).
    - ``htmlspecialchars`` (line 14887) — Converts special characters
      to HTML entities with configurable quote style and encoding.
    - ``_FILTERS`` (line 14630) — Filter pipeline base class.
    - ``filter_flags`` (line 14728) — Bitmask-style filter flags.
    - ``filter_var`` (line 14739) — Variable filtering with
      pluggable filter functions and validation rules.

10. Utility Functions & Decorators
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    - ``do_not_return`` (line 173) — Ensures a function returns ``None``.
    - ``noop_decor_callback`` / ``inline`` (lines 185, 191) — Identity
      decorators for documentation and typing purposes.
    - ``export`` (line 195) — No-op decorator for API surface marking.
    - ``critical`` / ``pure`` / ``memoize`` (lines 208-214) —
      Documentation decorators for function semantics.
    - ``trait(name)`` (line 631) — Marks a string as a trait identifier.
    - ``validator(func)`` (line 646) — Marks a method as an INI validator.
    - ``processor(stage)`` (line 667) — Marks a method as an INI processor.
    - ``copy_node`` (line 907) — Deep-copies an INI ``Node`` tree.
    - ``describe`` (line 6676) — Prints INI file structure to stdout.
    - ``register_command`` / ``_run_command`` / ``batch`` / ``_inio_batch``
      (lines 9365-9453) — Shell command registration and batch execution.
    - ``const`` (line 10422) — Wraps a value to prevent mutation.
    - ``freeze`` (line 10533) — Creates a ``FrozenVar``.
    - ``classhasattr`` (line 12173) — Checks for a class-level attribute.
    - ``resolvedotpath`` / ``resolvepath`` (lines 12188-12199) — Path
      resolution utilities.
    - ``private`` / ``sealed`` (lines 15177, 15246) — ``@final``
      decorator aliases for marking methods/classes as non-overridable.
    - ``die`` (line 15240) — Prints a message and exits with code 1.
    - ``public`` (line 16834) — Identity decorator marking public API.
    - ``standalone`` (line 16903) — Exits with code 1 if the module
      is imported rather than run directly.
    - ``compare`` / ``default`` / ``invoke`` / ``new`` (lines 16669-
      16774) — Simple value-comparison, default-value, scope-checking,
      and identity utilities.

    Decorators for class metadata:
    - ``guard`` (line 15548) — Prevents instantiation and subclassing.
    - ``mark_as_property`` (line 15561) — Attaches a metadata flag.
    - ``namespace`` (line 15586) — Marks a class as a semantic namespace.
    - ``tag`` (line 15607) — Validates an HTML tag attribute.
    - ``distrait_check`` (line 15656) — Checks ``__traits__`` attribute.
    - ``trait`` (line 15683) — Validates trait membership.
    - ``void`` (line 15740) — Marks a class as an HTML void element.
    - ``sloted`` (line 16633) — Validates ``__slots__`` attribute.
    - ``has_sloted_value`` (line 16642) — Validates a ``__slots__`` value.

    Other utility classes:
    - ``foreach`` (line 14948) — Iterator abstraction with chainable
      transformations.
    - ``settick`` (line 14998) — Timer/elapsed-time utility.
    - ``flush`` (line 15053) — Deletes local-scope variables matching
      a predicate.
    - ``findpath`` (line 15087) — Searches upward for a named directory.
    - ``globalize`` (line 15108) — Finds a directory and adds it to
      ``sys.path[0]``.
    - ``free`` (line 15126) — Deletes a variable from the caller's scope.
    - ``pragm``a (line 14085) — Compiler-like directive marker.

11. Keyboard & Input
    ~~~~~~~~~~~~~~~~~
    - ``VK`` (line 15281, ``IntEnum``) — Complete Windows virtual-key
      code enumeration covering all standard VK_ codes.
    - ``KeyHandler`` (line ~2700) — Keyboard hook/listener using the
      ``keyboard`` library, supporting callback registration, chord
      detection, and hotkey binding.
    - ``KeySignal`` (line 12208) — Dataclass representing a key event
      with key name, modifiers, and timestamp.
    - ``SIGINT`` (line 12249, ``IntEnum``) — Signal number enumeration.

12. CLI Tools
    ~~~~~~~~~~
    - ``NETPULSE_LOG_FILE`` / ``NETPULSE_BANNER`` (lines 16982-16984) —
      Constants for the NetPulse internet speed test CLI.
    - NetPulse functions (lines 16995-17243):
      ``netpulse_print_banner``, ``netpulse_format_speed``,
      ``netpulse_speed_rating``, ``netpulse_ping_rating``,
      ``netpulse_animate_progress``, ``netpulse_get_server_info``,
      ``netpulse_run_ping_test``, ``netpulse_run_download_test``,
      ``netpulse_run_upload_test``, ``netpulse_display_result_row``,
      ``netpulse_display_results``, ``netpulse_list_servers``,
      ``netpulse_save_results``, ``netpulse_show_history``,
      ``netpulse_clear_history``, ``netpulse_run_full_test``,
      ``netpulse_parse_args``, ``netpulse_clear_screen``.

13. Miscellaneous
    ~~~~~~~~~~~~~~
    - ``Vector[Generic[T]]`` (line 16942) — 2D/3D vector with typed
      ``x``, ``y``, ``z`` components and runtime type validation.
    - ``_ProxyBinary`` / ``_ProxyUnary`` / ``_ProxyGetSet`` /
      ``_ProxySetItem`` / ``_ProxyDelItem`` / ``_ProxyContains``
      (lines 14528-14563) — Internal proxy factories used by the
      ``default`` sentinel for transparent operator delegation.
    - ``_BoundPrivate`` (line 15213) — Descriptor for bound private
      method access.
    - ``CMeta`` (line 217) / ``CNarator`` (line 256) — Early base
      classes in the metaclass hierarchy.

=============================================================================
KEY DESIGN PATTERNS
=============================================================================

- **Monolithic single-module architecture** — All subsystems coexist in one
  module (~17,200 lines), sharing common types, base classes, and utilities.
- **Typed node hierarchy** — ``CObject`` / ``CObjectMeta`` provides an
  abstract base class with automatic type registration, validator/processor
  collection, and trait metadata for all INI node types.
- **Graph-based INI manipulation** — ``ConfigGraph`` and ``Node`` / ``VirtualNode``
  enables structural transformation of INI data as a directed graph.
- **Placeholder resolution engine** — ``IniPlaceholderEngine`` resolves
  ``${...}`` and ``{{...}}`` placeholders with nested lookups and fallback
  values, integrated directly into the ``INIO`` class.
- **Chainable batch execution** — ``Batch`` provides Unix-pipeline-style
  command chaining via method calls (``grep`` → ``awk`` → ``sort`` → etc.).
- **Monadic result type** — ``Result[T, E]`` follows Rust conventions with
  multiple severity levels and functional combinators.
- **Descriptor-based type enforcement** — ``Define`` uses the Python descriptor
  protocol to provide runtime type checking for class attributes.
- **Transparent sentinel** — ``default`` wraps marker values while proxying
  all attribute access, operators, and calls so the sentinel is invisible.
- **Metaclass for immutability** — ``define_once`` metaclass prevents
  re-assignment of ``Define`` descriptors, enforcing write-once semantics.
- **Introspective decorators** — ``validator`` / ``processor`` use function
  attributes collected by the metaclass at class creation time.
- **Builder pattern for HTML/CSS** — ``CSSStyleSheet``, ``CSSStyle``,
  ``HTMLDocument`` all support method-chaining construction.
- **Singleton metadata** — ``Meta`` uses a metaclass to enforce a single
  project-metadata instance.
- **Filesystem watching** — ``IniWatcher`` wraps ``watchdog`` for live
  reload of INI files.
- **Export/import markers** — ``export`` and ``extern`` use metaclasses to
  declare public API surface and external dependencies at the class level.

=============================================================================
IMPORT USAGE
=============================================================================

    from components.foundation import INIO, Result, Nmap, Batch, Meta
    from components.foundation import CSSStyleSheet, HTMLDocument
    from components.foundation import Ports, Hosts, Switches

=============================================================================
DEPENDENCIES
=============================================================================

Third-party packages: ``openai``, ``toml``, ``yaml``, ``keyboard``,
``pandas``, ``pyttsx3``, ``fpdf``, ``colorama``, ``rich``, ``speedtest``,
``speedtest_cli``, ``watchdog`` (optional), ``tkinter`` (standard library
on most platforms).

=============================================================================
"""

from __future__ import annotations

import shutil
import csv
import re
import sys
import subprocess
import contextlib
import io
import os
import string
import random
import functools
import types
import asyncio
import inspect
import json
import openai
import toml
import time
import hashlib
import copy
import traceback
import keyboard
import threading
import pandas as pd
import datetime
import logging
import dataclasses
import pyttsx3
import enum
import typing
import ipaddress
import typing_extensions
import typing_inspection
import tkinter as tk
import warnings
import collections
import importlib
import pathlib
import argparse
import ctypes
import colorama
import speedtest
import speedtest_cli
import rich
import rich.abc
import rich.align
import rich.ansi
import rich.bar
import rich.box
import rich.cells
import rich.color
import rich.color_triplet
import rich.columns
import rich.console
import rich.constrain
import rich.containers
import rich.default_styles
import rich.emoji
# import rich.emoji_data
import rich.errors
import rich.file_proxy
import rich.filesize
import rich.highlighter
import rich.json
import rich.jupyter
import rich.layout
import rich.live
import rich.live_render
import rich.logging
import rich.markdown
import rich.measure
import rich.padding
import rich.pager
import rich.pager
import rich.palette
import rich.panel
import rich.pretty
import rich.progress
import rich.progress_bar
import rich.prompt
import rich.region
import rich.repr
import rich.rule
import rich.scope
import rich.screen
import rich.segment
# import rich.sizing
import rich.spinner
import rich.status
import rich.style
import rich.styled
import rich.syntax
import rich.table
import rich.terminal_theme
import rich.text
import rich.theme
import rich.traceback
import rich.tree
# import rich.win32_console
from types import NotImplementedType
from colorama import Fore, Back, Style
from collections import defaultdict
from tkinter import ttk, font
from enum import Enum, auto, IntEnum
from dataclasses import dataclass
from weakref import WeakValueDictionary
from functools import wraps
from fpdf import FPDF
from configparser import ConfigParser
from dataclasses import dataclass, field, fields, is_dataclass
from typing import (
    Any, 
    Callable, 
    Literal, 
    Type, 
    Set, 
    Tuple, 
    List, 
    Dict, 
    Optional, 
    ClassVar, 
    Iterable, 
    Union, 
    TypeVar, 
    Generic, 
    get_origin, 
    get_args,
    Protocol,
    runtime_checkable,
    overload,
    cast,
    final,
    NewType,
    Iterator,
    NoReturn,
    TypedDict,
    NotRequired,
    Unpack,
    TypeAlias,
    Self,
    ParamSpec,
    LiteralString
)
from typing_extensions import disjoint_base
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from copy import deepcopy

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    Observer = None

logging.basicConfig(level=logging.INFO)

colorama.init(autoreset=True)
T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])
U = TypeVar("U")
E = TypeVar("E", bound=BaseException)
P = ParamSpec("P")
R = TypeVar("R")
_T = TypeVar("T")
_F = TypeVar("F", bound=Callable[..., Any])

_MetaType = typing.Union[str, None, int, float]

mixed = NewType("mixed", typing.Any)
number = NewType("number", int)
byte = NewType("byte", bytes)
array = NewType("array", dict)
sequence = NewType("sequence", str)

def do_not_return(obj):
    if isinstance(obj, type):
        for name, attr in obj.__dict__.items():
            if callable(attr):
                setattr(obj, name, do_not_return(attr))
        return obj

    def wrapper(*args, **kwargs):
        obj(*args, **kwargs)
        return None
    return wrapper

def noop_decor_callback(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return cast(F, wrapper)

def inline(func: F) -> F:
    return noop_decor_callback(func)

@final
def export(identifier: str, value: Any, *, ephemeral: Type[Any]):
    """
    No-op decorator that accepts:
    - identifier: str ("self" or "function_name")
    - value: any variable (for annotation)
    """
    def decorator(func: F) -> F:
        func._export_identifier = identifier
        func._export_value_type = type(value)
        func._export_ephemeral = ephemeral
        return cast(F, func)
    return decorator

def critical(func: F) -> F:
    return noop_decor_callback(func)

def pure(func: F) -> F:
    return noop_decor_callback(func)

def memoize(func: F) -> F:
    return noop_decor_callback(func)

@warnings.deprecated(
    "CMeta not in production use anymore."
    " Use class \'FoundationMeta\' insted."
)
class CMeta:
    """Library metadata class."""
    
    __slots__ = ("_version", "_build")

    def __init__(self, version=(1, 0, 0), build="") -> None:
        if not isinstance(version, tuple) or not all(isinstance(v, int) for v in version):
            raise ValueError("version must be a tuple of integers (major, minor, patch)")
        self._version = version
        self._build = build

    @property
    def version(self) -> tuple:
        """Return version tuple (major, minor, patch)."""
        return self._version

    @property
    def build(self) -> str:
        """Return build string."""
        return self._build

    @property
    def version_str(self) -> str:
        """Return version as string, e.g., '1.0.0'."""
        return ".".join(map(str, self._version))

    @property
    def full_version(self) -> str:
        """Return full version including build, e.g., '1.0.0-beta1'."""
        return f"{self.version_str}{'-' + self._build if self._build else ''}"

    def __repr__(self) -> str:
        return f"CMeta(version='{self.version_str}', build='{self._build}')"

    def __str__(self) -> str:
        return self.full_version

class FoundationMeta:
    __slots__ = ("_version", "_author", "_github", "_clonelink")

    def __init__(
        self: Self,
        version: tuple[int, int, int],
        *,
        author: str,
        github: str,
        clonelink: str
    ) -> None:
        self._version = version
        self._author = author
        self._github = github
        self._clonelink = clonelink
        return None
    
    @property
    def version(self) -> tuple:
        return self._version
    
    @version.setter
    def version(self) -> NoReturn:
        raise TypeError(f"Cannot modify foundation production version manualy.")
    
    @version.deleter
    def version(self) -> NoReturn:
        raise TypeError(f"Cannot delete foundation production version manualy.")
    
    
CMETADEPREC = CMeta(version=(1, 0, 0), build="confio")
foundation_meta = FoundationMeta(
    version=(2,1,14),
    author="n11kol11c",
    github="https://github.com/n11kol11c/foundation",
    clonelink="https://github.com/n11kol11c/foundation.git"
)

def vcompare(current: tuple[int, int, int], excepted: tuple[int, int, int]) -> bool:
    for i in range(0, 3):
        if current[i] == excepted[i]:
            continue
        else:
            return False
    return True


class CNarator:
    """
    INIONarator is a text-to-speech narrator for INI data operations.
    
    It can:
        - Narrate reading, setting, and deleting keys
        - Narrate entire sections or full INI data
        - Narrate file load and save operations with success or error messages
        - Track a history of narrated events
        - Register callbacks to react to narrated events
        - Customize voice, rate, and volume for TTS output

    Attributes:
        data (Dict[str, Dict[str, Any]]): The INI data stored in memory.
        engine (pyttsx3.Engine): The text-to-speech engine.
        callbacks (List[Callable[[str, Dict[str, Any]], None]]): Registered callback functions.
        history (List[Dict[str, Any]]): History of narrated messages and contexts.
    """
    def __init__(self, ini_data: Optional[Dict[str, Dict[str, Any]]] = None, voice: Optional[str] = None, rate: int = 150, volume: float = 1.0) -> None:
        """
        Initialize the IniNaratorSpeaker.

        Args:
            ini_data (Optional[Dict[str, Dict[str, Any]]]): Initial INI data to narrate.
            voice (Optional[str]): Name of the TTS voice to use. Defaults to system default.
            rate (int): Speech rate in words per minute. Default is 150.
            volume (float): Speech volume between 0.0 and 1.0. Default is 1.0.
        """
        self.data = deepcopy(ini_data) if ini_data else {}
        self.engine = pyttsx3.init()
        self.callbacks: List[Callable[[str, Dict[str, Any]], None]] = []
        self.history: List[Dict[str, Any]] = []
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)
        if voice:
            voices = self.engine.getProperty("voices")
            for v in voices:
                if voice.lower() in v.name.lower():
                    self.engine.setProperty("voice", v.id)
                    break

    def register_callback(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        Register a callback function to be executed on every narrated event.

        Args:
            callback (Callable[[str, Dict[str, Any]], None]): Function that receives the narrated
                message and a context dictionary containing metadata.
        """
        self.callbacks.append(callback)

    def _speak(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Internal method to speak a message and update history.

        Args:
            message (str): Message to be spoken.
            context (Optional[Dict[str, Any]]): Metadata about the event.
        """
        timestamp = datetime.now().isoformat()
        self.history.append({"timestamp": timestamp, "message": message, "context": context or {}})
        for cb in self.callbacks:
            cb(message, context or {})
        self.engine.say(message)
        self.engine.runAndWait()

    def narrate_set(self, section: str, key: str, value: Any):
        """
        Narrate setting or updating a key in a section.

        Args:
            section (str): INI section name.
            key (str): Key to set or update.
            value (Any): New value for the key.
        """
        old = self.data.get(section, {}).get(key)
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        msg = f"The value of {key} in section {section} has been changed from {old} to {value}."
        self._speak(msg, {"action": "set", "section": section, "key": key, "old": old, "new": value})

    def narrate_delete(self, section: str, key: str):
        """
        Narrate deleting a key from a section.

        Args:
            section (str): INI section name.
            key (str): Key to delete.
        """
        old = self.data.get(section, {}).pop(key, None)
        msg = f"The key {key} in section {section} has been deleted. Its previous value was {old}."
        self._speak(msg, {"action": "delete", "section": section, "key": key, "old": old})

    def narrate_read(self, section: Optional[str] = None, key: Optional[str] = None):
        """
        Narrate reading a key, section, or the entire INI data.

        Args:
            section (Optional[str]): Section to read. If None, reads all INI data.
            key (Optional[str]): Specific key to read. Requires section to be provided.

        Returns:
            Any: The value of the key, the dictionary of a section, or the entire INI data.
        """
        if section and key:
            value = self.data.get(section, {}).get(key)
            msg = f"The current value of {key} in section {section} is {value}."
            self._speak(msg, {"action": "read", "section": section, "key": key, "value": value})
            return value
        elif section:
            value = self.data.get(section, {})
            msg = f"The contents of section {section} are: {value}."
            self._speak(msg, {"action": "read_section", "section": section, "value": value})
            return value
        else:
            msg = f"The complete INI data is: {self.data}."
            self._speak(msg, {"action": "read_all", "value": self.data})
            return self.data

    def narrate_file_load(self, filepath: Union[str, Path]):
        """
        Narrate loading an INI file and compute its hash.

        Args:
            filepath (Union[str, Path]): Path to the INI file.

        Returns:
            List[str]: List of file lines if load is successful.
        """
        path = Path(filepath)
        if not path.exists():
            self._speak(f"The file {filepath} was not found.", {"action": "file_load", "file": str(path)})
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            content_hash = hashlib.md5("".join(lines).encode("utf-8")).hexdigest()
            self._speak(f"The INI file {filepath} has been loaded successfully with hash {content_hash}.", {"action": "file_load", "file": str(path), "hash": content_hash})
            return lines
        except Exception as e:
            self._speak(f"Failed to load INI file {filepath}: {e}", {"action": "file_load_error", "file": str(path), "error": str(e)})

    def narrate_file_save(self, filepath: Union[str, Path]):
        """
        Narrate saving the current INI data to a file.

        Args:
            filepath (Union[str, Path]): Path to save the INI file.
        """
        path = Path(filepath)
        try:
            with open(path, "w", encoding="utf-8") as f:
                for section, keys in self.data.items():
                    f.write(f"[{section}]\n")
                    for k, v in keys.items():
                        f.write(f"{k} = {v}\n")
                    f.write("\n")
            self._speak(f"The INI file has been saved to {filepath}.", {"action": "file_save", "file": str(path)})
        except Exception as e:
            self._speak(f"Failed to save INI file {filepath}: {e}", {"action": "file_save_error", "file": str(path), "error": str(e)})

class CObjectMeta(type):
    """
    Metaclass for INIObject subclasses.

    Responsibilities:
    - Enforces that TYPE_NAME is defined for non-abstract classes.
    - Automatically registers the class in INIOTypeRegistry.
    - Collects all methods marked with @validator and @processor.
    - Initializes the class traits set.

    Attributes:
        None
    """
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)

        if ns.get("__abstract__", False):
            return cls

        type_name = ns.get("TYPE_NAME")
        if not isinstance(type_name, str):
            raise TypeError(f"{name} must define TYPE_NAME: str")

        INIOTypeRegistry.register(type_name, cls)

        cls.__validators__ = []
        cls.__processors__ = []
        cls.__traits__ = set()

        for obj in ns.values():
            if getattr(obj, "__ini_validator__", False):
                cls.__validators__.append(obj)
            if getattr(obj, "__ini_processor__", False):
                cls.__processors__.append(obj)

        return cls

""", metaclass=INIObjectMeta"""
class CObject(ABC):
    """
    Abstract base class for all INI nodes (sections, key-value pairs, comments, etc).

    Attributes:
        TYPE_NAME (ClassVar[str]): Unique identifier for the type.
        __validators__ (ClassVar[List[Callable]]): List of validator methods.
        __processors__ (ClassVar[List[Callable]]): List of processor methods.
        __traits__ (ClassVar[set]): Set of class-level traits.
        raw (str): Raw string representation of the INI line.
        lineno (Optional[int]): Line number in the source INI file.
    """
    __abstract__ = True

    TYPE_NAME: ClassVar[str]
    __validators__: ClassVar[List[Callable]]
    __processors__: ClassVar[List[Callable]]
    __traits__: ClassVar[set]

    raw: str
    lineno: Optional[int]

    def __init__(self, raw: str, *, lineno: Optional[int] = None):
        """
        Initialize the INIObject.

        Args:
            raw (str): Original text of the line.
            lineno (Optional[int]): Line number in the source file.
        """
        self.raw = raw
        self.lineno = lineno
        self._run_validators()

    def _run_validators(self):
        """Run all validators associated with this node."""
        for validator in self.__validators__:
            validator(self)

    def process(self, value: Any, stage: str) -> Any:
        """
        Run all processor methods for a given stage on the value.

        Args:
            value (Any): Input value to process.
            stage (str): Stage name to filter processors.

        Returns:
            Any: Processed value after applying all relevant processors.
        """
        for proc in self.__processors__:
            if proc.__ini_processor__ == stage:
                value = proc(self, value)
        return value

    @classmethod
    def traits(cls) -> Iterable[str]:
        """
        Get the traits assigned to this class.

        Returns:
            Iterable[str]: List of trait names.
        """
        return cls.__traits__

    @classmethod
    def describe(cls) -> Dict[str, Any]:
        """
        Describe the class, including its type, traits, validators, and processors.

        Returns:
            Dict[str, Any]: Dictionary containing class metadata.
        """
        return {
            "type": cls.TYPE_NAME,
            "traits": sorted(cls.__traits__),
            "validators": [v.__name__ for v in cls.__validators__],
            "processors": [
                (p.__name__, p.__ini_processor__) for p in cls.__processors__
            ],
        }
    @abstractmethod
    def serialize(self) -> str:
        """
        Convert the node back to its INI string representation.

        Returns:
            str: Serialized line for writing to a file.
        """
        ...

class CType(Enum):
    """
    Enum representing the type of an INI node.

    Values:
        REGION: Section header
        KEY: Key identifier
        VALUE: Value alone
        COMMENT: Comment line
        EMPTY: Empty line
        NOT_IMPLEMENTED: Unsupported line
        UNKNOWN: Fallback type
    """
    REGION = auto()
    KEY = auto()
    VALUE = auto()
    COMMENT = auto()
    EMPTY = auto()
    NOT_IMPLEMENTED = auto()
    UNKNOWN = auto()

@dataclass(slots=True)
class CNode:
    """
    Lightweight representation of a parsed INI node.

    Attributes:
        type (INIOType): The kind of node.
        raw (str): Original line text.
        lineno (Optional[int]): Line number in the source file.
    """
    type: CType
    raw: str
    lineno: Optional[int] = None
    
class INIOTypeRegistry:
    """
    Global registry for INIObject subclasses.

    Provides registration, lookup, and inspection for all node types.
    """
    _registry: ClassVar[WeakValueDictionary[str, Type["CObject"]]] = (
        WeakValueDictionary()
    )

    @classmethod
    def register(cls, type_name: str, typ: Type["CObject"]) -> None:
        """
        Register a new INIObject type.

        Args:
            type_name (str): Unique string identifier for the type.
            typ (Type[INIObject]): Class to register.

        Raises:
            RuntimeError: If type_name already exists.
        """
        if type_name in cls._registry:
            raise RuntimeError(f"Duplicate INIObject type '{type_name}'")
        cls._registry[type_name] = typ

    @classmethod
    def resolve(cls, type_name: str) -> Type["CObject"]:
        """
        Retrieve a registered type by name.

        Args:
            type_name (str): Name of the type.

        Returns:
            Type[INIObject]: Registered class.
        """
        return cls._registry[type_name]

    @classmethod
    def all_types(cls) -> Dict[str, Type["CObject"]]:
        """
        Get a copy of all registered types.

        Returns:
            Dict[str, Type[CObject]]: Mapping type_name -> class.
        """
        return dict(cls._registry)

def trait(name: str):
    """
    Class decorator to assign a trait to an CObject subclass.

    Args:
        name (str): Trait name to assign.

    Returns:
        Callable: Decorator.
    """
    def decorator(cls):
        cls.__traits__.append(name)
        return cls
    return decorator

def validator(func: Callable[["CObject"], None]):
    """
    Method decorator to mark a method as a validator.

    Validators run automatically during initialization.

    Args:
        func (Callable[[CObject], None]): Validator method.

    Returns:
        Callable: Wrapped method with __ini_validator__ attribute.
    """
    func.__ini_validator__ = True

    @wraps(func)
    def wrapper(self):
        return func(self)

    return wrapper


def processor(stage: str):
    """
    Method decorator to mark a method as a processor for a specific stage.

    Processors can modify values during transformations (e.g., pre-serialize).

    Args:
        stage (str): Name of the stage when the processor should run.

    Returns:
        Callable: Decorated method.
    """
    def decorator(func):
        func.__ini_processor__ = stage

        @wraps(func)
        def wrapper(self, value):
            return func(self, value)

        return wrapper
    return decorator

@trait("structural")
@trait("container")
class INIRegion(CObject):
    """
    Represents a section header in an INI file.

    Attributes:
        name (str): Section name.
    """
    __traits__ = []
    TYPE_NAME = "region"

    name: str

    def __init__(self, name: str, raw: str, *, lineno=None):
        """
        Initialize a section.

        Args:
            name (str): Section name.
            raw (str): Original line text.
            lineno (Optional[int]): Line number in source.
        """
        self.name = name
        super().__init__(raw, lineno=lineno)

    @validator
    def _validate_name(self):
        """Ensure section name is not empty."""
        if not self.name:
            raise ValueError("Region name cannot be empty")

    def serialize(self) -> str:
        """Return INI-formatted section header."""
        return f"[{self.name}]"

@trait("non-semantic")
@trait("preserved")
class INIComment(CObject):
    """
    Represents a comment line in an INI file.

    Attributes:
        text (str): Comment text.
        marker (str): Comment marker (';' or '#').
    """
    __traits__ = []
    TYPE_NAME = "comment"

    text: str
    marker: str

    def __init__(self, text: str, raw: str, marker=";", *, lineno=None):
        self.text = text
        self.marker = marker
        super().__init__(raw, lineno=lineno)

    def serialize(self) -> str:
        """Return serialized comment line."""
        return f"{self.marker}{self.text}"

@trait("semantic")
@trait("assignable")
class INIKeyValue(CObject):
    """
    Represents a key-value pair in an INI file.

    Attributes:
        key (str): Key identifier.
        value (Any): Value associated with the key.
        separator (str): Separator character ('=' by default).
    """
    __traits__ = []
    TYPE_NAME = "key_value"

    key: str
    value: Any
    separator: str

    def __init__(self, key: str, value: Any, raw: str, sep="=", *, lineno=None):
        self.key = key
        self.value = value
        self.separator = sep
        if not hasattr(self, "__validators__"):
            self.__validators__ = []
        if not hasattr(self, "__processors__"):
            self.__processors__ = []
        super().__init__(raw, lineno=lineno)

    @validator
    def _validate_key(self):
        """Ensure key is non-empty and contains no spaces."""
        if not self.key or " " in self.key:
            raise ValueError("Invalid key identifier")

    @processor("pre-serialize")
    def _stringify_value(self, value):
        """Ensure value is converted to string before serialization."""
        return str(value)

    def serialize(self) -> str:
        """Return serialized key-value line."""
        val = self.process(self.value, "pre-serialize")
        return f"{self.key}{self.separator}{val}"

@trait("error")
class INIONotImplemented(CObject):
    """
    Represents unsupported or unknown INI lines.

    Attributes:
        reason (str): Optional explanation for why the line is not implemented.
    """
    __traits__ = []
    TYPE_NAME = "not_implemented"

    reason: str

    def __init__(self, raw: str, reason="unsupported", *, lineno=None):
        self.reason = reason
        super().__init__(raw, lineno=lineno)

    def serialize(self) -> str:
        """Return raw line as-is, since it's not implemented."""
        return self.raw

class Node:
    """
    Base node in the config graph.
    """
    def __init__(self, key: str, value: Any, section: str = "DEFAULT"):
        self.key = key
        self._value = value
        self.section = section
        self._observers: List[Callable[['Node'], None]] = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self._notify()

    def attach_observer(self, fn: Callable[['Node'], None]):
        self._observers.append(fn)

    def _notify(self):
        for fn in self._observers:
            fn(self)

    def __repr__(self):
        return f"<Node {self.section}.{self.key}={self.value}>"


class VirtualNode(Node):
    """
    Node whose value is computed from other nodes.
    """
    def __init__(self, key: str, compute: Callable[[], Any], section: str = "DEFAULT"):
        super().__init__(key, None, section)
        self._compute = compute

    @property
    def value(self):
        return self._compute()

    @value.setter
    def value(self, _):
        raise ValueError("Cannot set value of a VirtualNode directly")


class ConfigGraph:
    """
    Reactive INI graph that holds nodes, resolves dependencies, and allows
    transactional edits.
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self._transaction_stack: List[Dict[str, Any]] = []

    def add_node(self, node: Node):
        full_key = f"{node.section}.{node.key}"
        self.nodes[full_key] = node

    def get(self, section: str, key: str) -> Optional[Node]:
        return self.nodes.get(f"{section}.{key}")

    def transaction(self):
        """
        Begin a transaction context to allow undo.
        """
        snapshot = {k: copy_node(v) for k, v in self.nodes.items()}
        self._transaction_stack.append(snapshot)

    def commit(self):
        self._transaction_stack.pop()

    def rollback(self):
        snapshot = self._transaction_stack.pop()
        self.nodes = snapshot

    def serialize(self) -> str:
        """
        Serialize the graph back to INI format.
        """
        sections: Dict[str, List[str]] = {}
        for node in self.nodes.values():
            sections.setdefault(node.section, []).append(f"{node.key}={node.value}")
        lines = []
        for sec, kvs in sections.items():
            if sec != "DEFAULT":
                lines.append(f"[{sec}]")
            lines.extend(kvs)
        return "\n".join(lines)


def copy_node(node: Node) -> Node:
    """
    Make a shallow copy of a node.
    """
    if isinstance(node, VirtualNode):
        return VirtualNode(node.key, node._compute, node.section)
    return Node(node.key, node.value, node.section)

class ExportObserver:
    """
    Observer that triggers callbacks when nodes or config change.
    """

    def __init__(self):
        """
        Initialize the observer with an empty callback list.
        """
        self._callbacks: List[Callable[[], None]] = []

    def attach(self, callback: Callable[[], None]):
        """
        Attach a callback function.
        """
        self._callbacks.append(callback)

    def notify(self):
        """
        Notify all attached callbacks.
        """
        for cb in self._callbacks:
            try:
                cb()
            except Exception as e:
                logging.error(f"Error in export observer callback: {e}")

class INIExporter:
    """
    Converts INI files, ConfigParser objects, or AST nodes to Excel or PDF.
    Supports advanced styling, filtering, virtual keys, and reactive observers.
    """

    def __init__(self, source: Union[str, ConfigParser, List[Any]]):
        """
        Initialize the exporter.

        Args:
            source: INI file path, ConfigParser object, or list of AST nodes.
        """
        self.observer = ExportObserver()
        if isinstance(source, str):
            parser = ConfigParser()
            parser.read(source)
            self.parser = parser
        elif isinstance(source, ConfigParser):
            self.parser = source
        elif isinstance(source, list):
            self.parser = self._from_nodes(source)
        else:
            raise TypeError("source must be str, ConfigParser, or list of nodes")

    def _from_nodes(self, nodes: List[Any]) -> ConfigParser:
        """
        Convert INI AST nodes to ConfigParser.
        Supports INIRegion, INIKeyValue, VirtualKeys.
        """
        parser = ConfigParser()
        current_section = "DEFAULT"
        for node in nodes:
            if hasattr(node, "TYPE_NAME"):
                if node.TYPE_NAME == "region":
                    current_section = getattr(node, "name", "DEFAULT")
                elif node.TYPE_NAME == "key_value":
                    key = getattr(node, "key")
                    value = getattr(node, "value")
                    parser.setdefault(current_section, {})[key] = str(value)
                elif node.TYPE_NAME == "multiline":
                    key = getattr(node, "key")
                    value = "\n".join(getattr(node, "lines"))
                    parser.setdefault(current_section, {})[key] = value
                elif node.TYPE_NAME == "not_implemented":
                    continue
        return parser

    def to_excel(
        self,
        path: str,
        sheet_by_section: bool = True,
        highlight_sections: Optional[List[str]] = None,
    ):
        """
        Export INI content to Excel with advanced styling.

        Args:
            path: Output Excel file path.
            sheet_by_section: If True, each INI section is a separate sheet.
            highlight_sections: Optional list of sections to highlight.
        """
        self.observer.notify()

        writer = pd.ExcelWriter(path, engine="xlsxwriter")
        workbook = writer.book
        highlight_format = workbook.add_format(
            {"bg_color": "#FFFF99", "bold": True, "border": 1}
        )
        default_format = workbook.add_format({"border": 1})

        if sheet_by_section:
            for section in self.parser.sections():
                rows = []
                for key, value in self.parser.items(section):
                    rows.append({"Key": key, "Value": value})
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=section[:31], index=False)
                worksheet = writer.sheets[section[:31]]
                for r, row in enumerate(rows, start=1):
                    for c, _ in enumerate(row):
                        fmt = (
                            highlight_format
                            if highlight_sections and section in highlight_sections
                            else default_format
                        )
                        worksheet.write(r, c, row[list(row.keys())[c]], fmt)
        else:
            rows = []
            for section in self.parser.sections():
                for key, value in self.parser.items(section):
                    rows.append({"Section": section, "Key": key, "Value": value})
            df = pd.DataFrame(rows)
            df.to_excel(writer, sheet_name="INI", index=False)
            worksheet = writer.sheets["INI"]
            for r, row in enumerate(rows, start=1):
                for c, _ in enumerate(row):
                    worksheet.write(r, c, row[list(row.keys())[c]], default_format)

        writer.save()
        logging.info(f"Excel exported to {path}")

    def to_pdf(
        self,
        path: str,
        include_timestamp: bool = True,
        table_style: Optional[Dict[str, Any]] = None,
    ):
        """
        Export INI content to PDF with tables, headers, footers, and optional styling.

        Args:
            path: Output PDF file path.
            include_timestamp: Include export timestamp in header.
            table_style: Optional dict of table formatting parameters.
        """
        self.observer.notify()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "INI Configuration Export", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        if include_timestamp:
            pdf.cell(0, 8, f"Exported: {datetime.datetime.now()}", ln=True, align="C")
        pdf.ln(5)

        for section in self.parser.sections():
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"[{section}]", ln=True)
            pdf.set_font("Arial", "", 12)
            for key, value in self.parser.items(section):
                pdf.multi_cell(0, 8, f"{key} = {value}")
            pdf.ln(5)

        pdf.output(path)
        logging.info(f"PDF exported to {path}")

    def attach_export_observer(self, callback: Callable[[], None]):
        """
        Attach observer for automatic export updates.
        """
        self.observer.attach(callback)

    def transaction(self):
        """
        Begin a transaction: snapshot current parser state.
        """
        self._snapshot = copy.deepcopy(self.parser)

    def commit(self):
        """
        Commit transaction: discard snapshot.
        """
        self._snapshot = None

    def rollback(self):
        """
        Rollback transaction: restore parser to snapshot state.
        """
        if hasattr(self, "_snapshot") and self._snapshot:
            self.parser = self._snapshot
            self._snapshot = None

class IniValidator:
    """
    Validates INI data against a predefined schema.

    Example schema:
    {
        "section_name": {
            "key_name": {"type": int, "required": True, "default": 0},
            "other_key": {"type": str, "required": False}
        }
    }
    """

    def __init__(self, schema: Dict[str, Dict[str, Dict[str, Any]]]):
        self.schema = schema

    def validate(self, ini_data: Dict[str, Dict[str, Any]]) -> None:
        """
        Validates the INI data structure.
        Raises ValueError with detailed error messages if invalid.
        """
        errors = []
        for section, keys in self.schema.items():
            if section not in ini_data:
                errors.append(f"Missing section: {section}")
                continue
            for key, rules in keys.items():
                value = ini_data[section].get(key, rules.get("default"))
                if rules.get("required", False) and key not in ini_data[section]:
                    errors.append(f"Missing required key: {section}.{key}")
                if "type" in rules and value is not None and not isinstance(value, rules["type"]):
                    errors.append(f"Invalid type for {section}.{key}: expected {rules['type']}, got {type(value)}")
        if errors:
            raise ValueError("INI Validation failed:\n" + "\n".join(errors))

class IniWatcher:
    """
    Watches INI files for changes and triggers callbacks.
    """

    def __init__(self, filepath: Union[str, Path], callback: Callable[[str], None]):
        if Observer is None:
            raise ImportError("watchdog package is required for IniWatcher")
        self.filepath = Path(filepath)
        self.callback = callback
        # self._observer: Optional[Observer] = None
        self._observer: Optional[Observer] = None
        self._hash = self._compute_hash()

    def _compute_hash(self) -> str:
        if not self.filepath.exists():
            return ""
        return hashlib.md5(self.filepath.read_bytes()).hexdigest()

    def _on_modified(self, event):
        if Path(event.src_path) != self.filepath:
            return
        new_hash = self._compute_hash()
        if new_hash != self._hash:
            self._hash = new_hash
            self.callback(str(self.filepath))

    def start(self):
        handler = FileSystemEventHandler()
        handler.on_modified = self._on_modified
        self._observer = Observer()
        self._observer.schedule(handler, str(self.filepath.parent), recursive=False)
        self._observer.start()

    def stop(self):
        if self._observer:
            self._observer.stop()
            self._observer.join()


class IniSerializer:
    """
    Serializes INI data to JSON, YAML, TOML, or string formats.
    """

    def __init__(self, ini_data: Dict[str, Dict[str, Any]]):
        self.data = deepcopy(ini_data)

    def to_json(self, pretty: bool = True) -> str:
        return json.dumps(self.data, indent=4 if pretty else None)

    def to_yaml(self) -> str:
        return yaml.dump(self.data, sort_keys=False)

    def to_toml(self) -> str:
        return toml.dumps(self.data)

    def to_ini_string(self, align: bool = True) -> str:
        output = []
        for section, keys in self.data.items():
            output.append(f"[{section}]")
            if align:
                max_len = max((len(k) for k in keys), default=0)
            else:
                max_len = 0
            for k, v in keys.items():
                if align:
                    output.append(f"{k.ljust(max_len)} = {v}")
                else:
                    output.append(f"{k} = {v}")
            output.append("")
        return "\n".join(output)

class IniDiff:
    """
    Compares two INI data dictionaries and produces diffs or patch instructions.
    """

    def __init__(self, base_data: Dict[str, Dict[str, Any]], new_data: Dict[str, Dict[str, Any]]):
        self.base = base_data
        self.new = new_data

    def diff(self) -> Dict[str, Dict[str, Tuple[Any, Any]]]:
        """
        Returns a dictionary of changed keys: {section: {key: (old, new)}}
        """
        changes = {}
        all_sections = set(self.base) | set(self.new)
        for section in all_sections:
            sec_changes = {}
            keys = set(self.base.get(section, {})) | set(self.new.get(section, {}))
            for key in keys:
                old_val = self.base.get(section, {}).get(key)
                new_val = self.new.get(section, {}).get(key)
                if old_val != new_val:
                    sec_changes[key] = (old_val, new_val)
            if sec_changes:
                changes[section] = sec_changes
        return changes

    def patch(self, target: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Applies the diff to a target INI dictionary and returns the updated dictionary.
        """
        result = deepcopy(target)
        for section, keys in self.diff().items():
            if section not in result:
                result[section] = {}
            for key, (_, new_val) in keys.items():
                result[section][key] = new_val
        return result


class IniPlaceholderEngine:
    """
    Resolves advanced dynamic placeholders in INI values.
    Supports:
        - @env(VAR)
        - @random.int(a, b)
        - @key references
        - Conditional placeholders
    """

    def __init__(self, ini_data: Dict[str, Dict[str, Any]], env: Optional[Dict[str, str]] = None):
        self.data = ini_data
        self.env = env or os.environ

    def _resolve_env(self, var_name: str) -> str:
        return self.env.get(var_name, "")

    def _resolve_key(self, key_path: str) -> str:
        parts = key_path.split(".")
        if len(parts) != 2:
            return ""
        section, key = parts
        return str(self.data.get(section, {}).get(key, ""))

    def resolve_value(self, value: str) -> str:
        """
        Resolves placeholders in a single string value.
        """
        if not isinstance(value, str):
            return value

        value = re.sub(r"@env\(([^)]+)\)", lambda m: self._resolve_env(m.group(1)), value)
        value = re.sub(r"@key\(([^)]+)\)", lambda m: self._resolve_key(m.group(1)), value)
        def cond_replace(m):
            cond, val_true, val_false = m.groups()
            return val_true if cond.strip().lower() == "true" else val_false
        value = re.sub(r"@if\(([^,]+),([^,]+),([^)]+)\)", cond_replace, value)
        return value

    def resolve_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Resolves all placeholders in the INI data.
        """
        resolved = deepcopy(self.data)
        for section, keys in resolved.items():
            for key, value in keys.items():
                keys[key] = self.resolve_value(value)
        return resolved

class IniAuditLogger:
    """
    Tracks all mutations to INI data and logs them.
    """

    def __init__(self, ini_data: Dict[str, Dict[str, Any]], log_file: Optional[str] = None):
        self.data = deepcopy(ini_data)
        self.log_file = log_file
        self.logger = logging.getLogger("IniAuditLogger")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(handler)

    def set(self, section: str, key: str, value: Any) -> None:
        old = self.data.get(section, {}).get(key)
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        self.logger.info(f"[SET] {section}.{key}: {old} -> {value}")

    def delete(self, section: str, key: str) -> None:
        old = self.data.get(section, {}).pop(key, None)
        self.logger.info(f"[DELETE] {section}.{key}: {old}")

    def get(self, section: str, key: str) -> Any:
        return self.data.get(section, {}).get(key)

class INIO:
    """
    INIO — Advanced INI File Loader, Parser, and Mutator

    This class provides a **full control INI file engine** that allows reading,
    parsing, editing, cleaning, resolving, and writing `.ini` configuration files.

    ---------------------------------------------
    CORE INTERNAL STORAGE STRUCTURES
    ---------------------------------------------

    1) self.full_file : list[str]
        - Exact file contents line-by-line
        - Includes comments, blank lines, formatting
        - This is the authoritative source when writing back to disk

    2) self.raw_lines : list[str]
        - Stripped lines without comments or blank lines
        - Used for fast parsing and logic checks

    3) self.data : dict[str, dict[str, str]]
        - Structured representation:
            {
                "region": {
                    "key": "value"
                }
            }

    4) self.keys : dict[str, str]
        - Flat representation:
            {
                "region.key": "value"
            }

    5) self.regions : list[str]
        - Ordered list of region names in file order

    ---------------------------------------------
    PLACEHOLDER SYSTEM
    ---------------------------------------------

    INIO supports recursive placeholder resolution:

        @key           → resolves from same region
        @region.key    → resolves from another region

    Circular references are automatically detected and skipped to prevent infinite loops.

    Example:
        [global]
        host = 127.0.0.1

        [api]
        url = http://@global.host:8080

    After resolution:
        url = http://127.0.0.1:8080

    ---------------------------------------------
    FILE MUTATION PHILOSOPHY
    ---------------------------------------------

    Most methods:
        1. Modify file content line-by-line
        2. Update self.full_file
        3. Rebuild self.data, self.keys, self.regions, self.raw_lines
        4. Write back to disk

    This ensures file and memory are always synchronized.

    ---------------------------------------------
    ADVANCED FEATURES
    ---------------------------------------------

    ✔ Placeholder resolution (recursive, cross-region)  
    ✔ Duplicate key pruning  
    ✔ Empty key removal  
    ✔ Empty region removal  
    ✔ Region normalization  
    ✔ Value population for empty keys  
    ✔ Key mutation (edit existing key)  
    ✔ Key assignment (append new key to region)  
    ✔ Region creation  
    ✔ Full in-memory rebuild from file  
    ✔ File-safe writes with encoding & error handling  

    ---------------------------------------------
    DESIGN WARNINGS (IMPORTANT)
    ---------------------------------------------

    - Many methods rewrite the entire file.
    - full_file is the source of truth for writing.
    - data dict CANNOT store duplicate keys (Python limitation).
    - Duplicate keys only exist in full_file, not in data.
    - Improper modification of full_file can delete your file.
    - Always backup before heavy operations.

    ---------------------------------------------
    INTENDED USE CASES
    ---------------------------------------------

    - Configuration automation frameworks
    - Build system configuration generators
    - Developer tools that require exact INI formatting control
    - Template-based config engines
    - DevOps config mutation pipelines

    ---------------------------------------------
    EXAMPLE USAGE
    ---------------------------------------------

    ini = INIO("config.ini")
    ini.load()

    print(ini.data["server"]["host"])
    ini.assign("server", "port", "8080")
    ini.resolve("api")
    ini.populate("server", "localhost")
    ini.normalize("server")

    ---------------------------------------------
    SAFETY NOTE
    ---------------------------------------------

    This class performs real disk writes.
    Always backup files before mass operations.
    """

    def __init__(
        self,
        path: str,
        *,
        mode: Literal["r", "w", "a"] = "r",
        encoding: str = "utf-8",
        errors: Literal["strict", "ignore", "replace"] = "strict",
        r: bool = True,
        k: bool = True,
        keys: dict[str, str] | None = None,
        restrict: bool | None = None,
        raises: Type[Exception] | None = None,
        fallback: Any | Callable | None = None,
        aliases: dict[Any, dict[Any, Any]] | list[Any] | None = None,
        components: dict[str, list[str]] | None = None,
    ) -> None:
        """
        **Initialize INIO instance**
        
        Parameters:
        - `path` (*str*): Path to the `.ini` file.
        - `mode` (*Literal["r", "w", "a"]*): File mode. Default is `'r'`.
        - `encoding` (*str*): File encoding. Default `'utf-8'`.
        - `errors` (*Literal["strict", "ignore", "replace"]*): How to handle encoding errors.
        - `r` (*bool*): Whether to load regions (sections).
        - `k` (*bool*): Whether to load keys.
        - `keys` (*dict[str, str]*, optional): Predefined keys dictionary.
        - `restrict` (*bool, optional*): Future use for restrictions.
        - `raises` (*Exception class, optional*): Custom exception to raise.
        - `fallback` (*Any | Callable, optional*): Fallback value or function.
        - `aliases` (*dict or list, optional*): Aliases for keys or regions.
        - `components` (*dict[str, list[str]], optional*): Custom placeholder characters.

        Raises:
        - `TypeError` if `path` is not a string
        - `ValueError` if `path` does not end with `.ini`
        """
        if not isinstance(path, str):
            raise TypeError(
                f"Invalid data type for path, got {type(path).__name__}"
            )

        if not path.lower().endswith(".ini"):
            raise ValueError("File must have a .ini extension")

        self.path = path
        self.mode = mode
        self.encoding = encoding
        self.errors = errors
        self.r = r
        self.k = k
        self.restrict = restrict
        self.regions: list[str] = []
        self.keys = keys or {}
        self.raises = raises
        self.fallback = fallback
        self.aliases = aliases
        self.components = components or {"placeholders": ["@", "?", "*"]}
        self.raw_lines: list[str] = []
        self.data: dict[str, dict[str, str]] = {}
        self.full_file: list[str] = []
        self.POPULATE_STATEMENTS: list[str] = ["&", "&default", "&none", "none"]
        self.INI_DATA_TYPES: dict[str, list[str]] = {"bool": ["true", "false", "none"]}
        self.POPULATE_DEFAULT: str = "&default"
        self.POPULATE_NUMBER: str = "0"
        self.POPULATE_RANDOM = lambda length=8: ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        self.POPULATE_RANDOM_NUMBER = lambda lenght=8: ''.join(random.choices(string.digits, k=lenght))
        self.resolved_data: dict[str, dict[str, str]] = {}
        self.arrow: str = "→"
        self.connection = INIO.Conn(self)
        self.expo = INIO.Expo()
        self.ebx = INIO.EBX()
        self.stdoutput = INIO.STDOP(self)
        self.pretty = INIO.Pretty()
        self.filesystem = INIO.Filesystem()
        self.wrap = INIO.Wrap()
        self._locked: bool | None = False
        self._hooks: Any | None = None
        self.awaitable = INIO.Awaitable(self)

    @property
    def meta(self):
        return {
            "Author": "Matija",
            "Project Name": "INIO",
            "Version": "0.1.0",
            "License": "MIT"
        }

    def _resolve_placeholder_value(self, value: str, region: str, visited: Set[Tuple[str, str]] = None) -> str:
        """
        Recursively resolve placeholders in the value.
        Supports cross-region placeholders: @region.key
        Detects circular references.
        """
        visited = visited or set()
        parts = value.split()
        for i, part in enumerate(parts):
            if part.startswith("@"):
                key_str = part[1:]
                if "." in key_str:
                    r, k = key_str.split(".", 1)
                else:
                    r, k = region, key_str

                if (r, k) in visited:
                    continue

                visited.add((r, k))
                replacement = self.data.get(r, {}).get(k, "")
                replacement = self._resolve_placeholder_value(replacement, r, visited)
                parts[i] = replacement

        return " ".join(parts)
    
    def _rebuild_memory(self):
        """
        Rebuild self.data, self.raw_lines, self.keys, self.regions from full_file.
        """
        self.data.clear()
        self.raw_lines.clear()
        self.keys.clear()
        self.regions.clear()

        current_section = None

        for line in self.full_file:
            stripped = line.strip()

            if stripped:
                self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                if current_section not in self.data:
                    self.data[current_section] = {}
                    self.regions.append(current_section)
                continue

            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                self.keys[f"{current_section}.{k}"] = v

    def _write_file(self):
        """
        Write self.full_file to disk, ensuring newline consistency.
        """
        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

    def _resolve_value(self, value: str, current_region: str, visited: set = None) -> str:
        """
        Recursively resolve placeholders in a value string, supporting cross-region references.

        Placeholders are in the format:
            - `@key` → looks in the same region (`current_region`)
            - `@region.key` → looks in a different region

        Circular references are automatically detected and skipped to prevent infinite loops.

        Parameters:
        -----------
        value : str
            The string containing potential placeholders to resolve.
        current_region : str
            The region/section where the placeholder resolution starts.
        visited : set[tuple[str, str]], optional
            Set of already visited (region, key) tuples to prevent circular resolution.

        Returns:
        --------
        str
            The input string with all placeholders replaced by their resolved values.

        Example:
        --------
        [global]
        version=1.0

        [build]
        ver=@global.version
        full_ver=@ver.BUILD

        _resolve_value("@ver.BUILD", "build") -> "1.0.BUILD"
        """
        if visited is None:
            visited = set()

        parts = value.split()
        for part in parts:
            if part.startswith("@"):
                ref = part[1:]
                if "." in ref:
                    ref_region, ref_key = ref.split(".", 1)
                else:
                    ref_region, ref_key = current_region, ref

                if (ref_region, ref_key) in visited:
                    continue

                visited.add((ref_region, ref_key))
                ref_val = self.data.get(ref_region, {}).get(ref_key, "")
                resolved_val = self._resolve_value(ref_val, ref_region, visited)
                value = value.replace(part, resolved_val)
        return value

    def _update_memory_and_file(self, new_full_file: list[str]):
        """
        Updates all in-memory structures and rewrites the actual INI file.

        Updates:
            - self.full_file : list[str] → full file lines (including comments)
            - self.raw_lines : list[str] → stripped lines, no empty lines/comments
            - self.data      : dict[str, dict[str,str]] → parsed regions and keys
            - Actual file on disk

        Parameters:
        -----------
        new_full_file : list[str]
            Full file content to replace existing content.

        Behavior:
        ---------
        - Clears previous structures
        - Rebuilds self.raw_lines and self.data
        - Writes new_full_file to disk

        Example:
        --------
        _update_memory_and_file([
            "[global]",
            "version=1.0",
            "[build]",
            "ver=@global.version"
        ])
        """
        self.full_file = new_full_file
        self.raw_lines = [line for line in new_full_file if line.strip() and not line.strip().startswith(("#", ";"))]
        self.data = {}
        current_section = None
        for line in new_full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                continue
            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in new_full_file:
                f.write(line if line.endswith("\n") else line + "\n")
    
    def _prune_duplicates_in_region_dev_copy(self, region: str) -> list[str]:
        """
        Remove duplicate keys in a specific region, keeping only the first occurrence.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Args:
            region (str): The section/region to process.

        Returns:
            list[str]: List of duplicate keys removed, formatted as "region.key".
        """
        if region not in self.data:
            return []

        removed_keys: list[str] = []
        new_full_file: list[str] = []
        current_section: str | None = None
        seen_keys_in_section: set[str] = set()

        for line in self.full_file:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                if current_section == region:
                    seen_keys_in_section = set()
                new_full_file.append(line)
                continue

            if not stripped or stripped.startswith(("#", ";")):
                new_full_file.append(line)
                continue

            if current_section == region and "=" in stripped:
                key = stripped.split("=", 1)[0].strip()
                identifier = f"{region}.{key}"

                if key in seen_keys_in_section:
                    removed_keys.append(identifier)
                    continue
                seen_keys_in_section.add(key)
            new_full_file.append(line)

        self.full_file = new_full_file

        self.raw_lines = []
        self.data = {}
        current_section = None

        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()
            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                continue

            if "=" in stripped and current_section is not None:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return removed_keys
    
    def _prune_empty_keys_dev_copy(self, region: str) -> list[str]:
        """
        Remove all keys without a value in the specified region.

        Updates:
            - self.full_file
            - self.raw_lines
            - self.data
            - actual INI file

        Args:
            region (str): Section/region to clean.

        Returns:
            list[str]: List of keys that were removed.
        """
        removed = []
        new_full_file = []
        current_section: str | None = None

        try:
            with open(self.path, "r", encoding=self.encoding, errors=self.errors) as f:
                lines = f.readlines()

            for line in lines:
                stripped = line.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    new_full_file.append(line)
                    continue

                if not stripped or stripped.startswith(("#", ";")):
                    new_full_file.append(line)
                    continue
                
                if current_section == region and "=" in stripped:
                    k, v = map(str.strip, stripped.split("=", 1))
                    if not v:
                        removed.append(k)
                        continue

                new_full_file.append(line)

            self.full_file = new_full_file

            self.raw_lines = []
            self.data = {}
            current_section = None

            for line in self.full_file:
                stripped = line.strip()
                if not stripped or stripped.startswith(("#", ";")):
                    continue

                for c in ("#", ";"):
                    if c in stripped:
                        stripped = stripped.split(c, 1)[0].strip()

                if not stripped:
                    continue

                self.raw_lines.append(stripped)

                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    self.data.setdefault(current_section, {})
                    continue

                if "=" in stripped and current_section is not None:
                    k, v = map(str.strip, stripped.split("=", 1))
                    self.data[current_section][k] = v

            with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
                for line in self.full_file:
                    f.write(line if line.endswith("\n") else line + "\n")

            return removed

        except FileNotFoundError:
            if self.raises:
                raise self.raises(f"INI file not found: {self.path}")
            return []
    
    def _resolve_dev_copy(self, region: str) -> dict[str, str]:
        """
        Resolve placeholders in the values of a specific region.

        Supports:
            - Same region: @key
            - Cross-region: @region.key

        Circular placeholders are detected and skipped.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Args:
            region (str): The section/region to process.

        Returns:
            dict[str, str]: Mapping of keys updated with resolved values.
        """
        if region not in self.data:
            return {}

        updated_keys = {}
        new_full_file = []
        current_section: str | None = None

        def resolve_value(val: str, current_region: str, visited: set = None) -> str:
            """Recursively resolve placeholders with circular detection"""
            if visited is None:
                visited = set()
            original_val = val
            for placeholder in val.split():
                if placeholder.startswith("@"):
                    ref = placeholder[1:]
                    if "." in ref:
                        ref_region, ref_key = ref.split(".", 1)
                    else:
                        ref_region, ref_key = current_region, ref

                    if (ref_region, ref_key) in visited:
                        continue 
                    visited.add((ref_region, ref_key))
                    ref_val = self.data.get(ref_region, {}).get(ref_key, "")
                    ref_val = resolve_value(ref_val, ref_region, visited)
                    val = val.replace(f"@{ref if '.' in ref else ref_key}", ref_val)
            return val

        try:
            for line in self.full_file:
                stripped = line.strip()
                line_to_add = line

                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    new_full_file.append(line_to_add)
                    continue

                if current_section == region and "=" in stripped:
                    key, value = map(str.strip, stripped.split("=", 1))
                    resolved_value = resolve_value(value, region)
                    if resolved_value != self.data[region].get(key, ""):
                        updated_keys[key] = resolved_value
                        line_to_add = f"{key}={resolved_value}\n"

                new_full_file.append(line_to_add)

            self.full_file = new_full_file
            self.raw_lines = []
            self.data = {}
            current_section = None

            for line in self.full_file:
                stripped = line.strip()
                if not stripped or stripped.startswith(("#", ";")):
                    continue
                for c in ("#", ";"):
                    if c in stripped:
                        stripped = stripped.split(c, 1)[0].strip()
                if not stripped:
                    continue
                self.raw_lines.append(stripped)

                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    self.data.setdefault(current_section, {})
                    continue
                if "=" in stripped and current_section is not None:
                    k, v = map(str.strip, stripped.split("=", 1))
                    self.data[current_section][k] = v

            with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
                for line in self.full_file:
                    f.write(line if line.endswith("\n") else line + "\n")

            return updated_keys

        except FileNotFoundError:
            if self.raises:
                raise self.raises(f"INI file not found: {self.path}")
            return {}

    def _prune_empty_regions_dev_copy(self) -> list[str]:
        """
        Remove all empty regions (sections with no keys) from the INI file.

        Updates:
            - self.full_file
            - self.raw_lines
            - self.data
            - actual INI file

        Returns:
            list[str]: List of removed region names.
        """
        removed_regions = []
        new_full_file = []
        current_section: str | None = None
        buffer_lines: list[str] = []

        try:
            with open(self.path, "r", encoding=self.encoding, errors=self.errors) as f:
                lines = f.readlines()
                
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    if current_section is not None:
                        keys_in_section = [l for l in buffer_lines if "=" in l]
                        if not keys_in_section:
                            removed_regions.append(current_section)
                        else:
                            new_full_file.extend(buffer_lines)

                    current_section = stripped[1:-1].strip()
                    buffer_lines = [line]
                    continue

                buffer_lines.append(line)

            if current_section is not None:
                keys_in_section = [l for l in buffer_lines if "=" in l]
                if not keys_in_section:
                    removed_regions.append(current_section)
                else:
                    new_full_file.extend(buffer_lines)

            self.full_file = new_full_file

            self.raw_lines = []
            self.data = {}
            current_section = None

            for line in self.full_file:
                stripped = line.strip()
                if not stripped or stripped.startswith(("#", ";")):
                    continue

                for c in ("#", ";"):
                    if c in stripped:
                        stripped = stripped.split(c, 1)[0].strip()
                if not stripped:
                    continue

                self.raw_lines.append(stripped)

                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    self.data.setdefault(current_section, {})
                    continue

                if "=" in stripped and current_section is not None:
                    k, v = map(str.strip, stripped.split("=", 1))
                    self.data[current_section][k] = v

            with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
                for line in self.full_file:
                    f.write(line if line.endswith("\n") else line + "\n")

            return removed_regions

        except FileNotFoundError:
            if self.raises:
                raise self.raises(f"INI file not found: {self.path}")
            return []

    def _resolve_placeholders(self, value: str, region: str, visited: Set[Tuple[str, str]] | None = None) -> str:
        """
        Resolve placeholders in a string for a specific region.

        Supports:
        - @key           → same region
        - @region.key    → cross-region
        - multiple placeholders in a single value
        - recursive resolution with cycle detection

        Args:
            value (str): The value containing placeholders.
            region (str): The current region where the value resides.
            visited (set[tuple[str,str]]): Used internally to prevent circular references.

        Returns:
            str: The value with all placeholders replaced.
        """
        if visited is None:
            visited = set()

        placeholders = re.findall(r"@([A-Za-z0-9_.]+)", value)
        for ph in placeholders:
            if '.' in ph:
                target_region, target_key = ph.split('.', 1)
            else:
                target_region, target_key = region, ph

            if (target_region, target_key) in visited:
                continue
            visited.add((target_region, target_key))

            replacement = self.data.get(target_region, {}).get(target_key, "")
            replacement = self._resolve_placeholders(replacement, target_region, visited)

            value = value.replace(f"@{ph}", replacement)

        return value
    
    def resolve(self, region: str) -> dict[str, str]:
        """
        Resolve placeholders in a specific region and update the INI file.

        This method:
        - Resolves same-region placeholders (@key) and cross-region placeholders (@region.key)
        - Updates self.data, self.raw_lines, self.full_file
        - Writes changes back to the actual INI file

        Circular references are detected and skipped.

        Args:
            region (str): The region/section to process.

        Returns:
            dict[str, str]: Keys in the region that were updated with resolved values.
        """
        if region not in self.data:
            return {}

        updated_keys: dict[str, str] = {}
        new_full_file: list[str] = []
        current_section: str | None = None

        for line in self.full_file:
            stripped = line.strip()
            line_to_add = line
    
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                new_full_file.append(line_to_add)
                continue

            if current_section == region and "=" in stripped:
                key, value = map(str.strip, stripped.split("=", 1))
                resolved_value = self._resolve_placeholders(value, region)

                if resolved_value != self.data[region].get(key, ""):
                    updated_keys[key] = resolved_value
                    line_to_add = f"{key}={resolved_value}\n"

            new_full_file.append(line_to_add)

        self.full_file = new_full_file
        self.raw_lines.clear()
        self.data.clear()
        self.keys.clear()
        self.regions.clear()

        current_section = None
        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue
            self.raw_lines.append(stripped)
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue
            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                self.keys[f"{current_section}.{k}"] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return updated_keys

    def load(self) -> bool:
        """
        **Load the INI file and parse all data in one pass.**

        This method does the following:
        - Reads the file and stores all lines in `self.raw_lines` (stripped lines)
        - Stores the full file in `self.full_file` as a list of strings (original lines, with comments)
        - Removes comments and inline comments for parsing
        - Populates:
            - `self.data` as `dict[str, dict[str, str]]`
            - `self.regions` as a list of section names
            - `self.keys` as a flat dict `region.key = value`

        **Example:**
        ```python
        ini = INIO("config.ini")
        ini.load()
        print(ini.raw_lines)  # stripped lines without inline comments
        print(ini.full_file)  # full file as list of original lines
        print(ini.regions)    # ['server', 'auth']
        print(ini.keys)       # {'server.host': 'localhost', 'auth.token': 'abc123'}
        print(ini.data)       # {'server': {'host': 'localhost', 'port': '8080'}, ...}
        ```
        Returns:
        - True if the file loaded successfully
        - False if file not found and no custom exception
        """
        self.raw_lines.clear()
        self.regions.clear()
        self.keys.clear()
        self.data.clear()
        self.full_file: list[str] = []

        current_section: str | None = None

        try:
            with open(self.path, mode=self.mode, encoding=self.encoding, errors=self.errors) as file:
                for line in file:
                    self.full_file.append(line.rstrip("\n"))

                    stripped_line = line.strip()
                    if not stripped_line:
                        continue

                    self.raw_lines.append(stripped_line)

                    for comment_char in ("#", ";"):
                        if comment_char in stripped_line:
                            stripped_line = stripped_line.split(comment_char, 1)[0].strip()

                    if not stripped_line:
                        continue

                    if stripped_line.startswith("[") and stripped_line.endswith("]"):
                        current_section = stripped_line[1:-1].strip()
                        self.regions.append(current_section)
                        if current_section not in self.data:
                            self.data[current_section] = {}
                        continue

                    if "=" in stripped_line and current_section is not None:
                        key, value = map(str.strip, stripped_line.split("=", 1))
                        self.data[current_section][key] = value
                        self.keys[f"{current_section}.{key}"] = value
                    else:
                        if self.raises:
                            raise ValueError(f"Invalid line in INI file: {line.strip()}")
            return True

        except FileNotFoundError as error:
            if self.raises:
                raise self.raises(f"INI file not found: {self.path}") from error
            return False

    def reload(self):
        """Reload the file from disk and rebuild memory."""
        if not os.path.exists(self.path):
            self.full_file = []
        else:
            with open(self.path, "r", encoding=self.encoding, errors=self.errors) as f:
                self.full_file = f.readlines()
        self._rebuild_memory()

    def empty(
        self,
        t: Literal["@var", "@region", "@key"],
        var: str | None = None,
        region: str | None = None,
        key: str | None = None
    ) -> bool:
        """
        Check if a variable, region, or key is empty.
        """

        if t == "@var":
            return not var

        elif t == "@region":
            if not region or not region.strip():
                return True
            if region not in self.data:
                return True
            if not self.data[region]:
                return True
            return False

        elif t == "@key":
            if not key or not key.strip():
                return True

            if region:
                if region not in self.data:
                    return True
                if key not in self.data[region]:
                    return True

                value = self.data[region][key]
                return value is None or not str(value).strip()
            for reg in self.regions:
                if key in self.data.get(reg, {}):
                    value = self.data[reg][key]
                    return value is None or not str(value).strip()

            return True

        return True

    def getregions(self) -> list[str]:
        """
        **Get all region (section) names from the INI file.**

        Returns:
        - List of section names as strings

        ```python
        ini.getregions()  # ['server', 'auth']
        ```
        """
        return self.regions

    def getkeys(self) -> dict[str, str]:
        """
        **Get all keys from the INI file.**

        Keys are stored in the format `region.key` for flat access.

        Returns:
        - Dictionary of keys and their values

        ```python
        ini.getkeys()  # {'server.host': 'localhost', 'auth.token': 'abc123'}
        ```
        """
        return self.keys

    def rexist(self, region: str) -> bool:
        """
        Check if a region exists in the INI file.
        Uses `self.data` for accurate detection.
        """
        return region in self.data

    def kexists(self, region: str, key: str) -> bool:
        """
        Check if a key exists in a specific region.
        """
        if region not in self.data:
            return False
        return key in self.data[region]
    
    def normalize(self, region: str) -> list[str]:
        """
        Normalize a region by removing duplicate keys (after resolving placeholders).

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Args:
            region (str): The section to normalize.

        Returns:
            list[str]: Keys that were removed.
        """
        if region not in self.data:
            return []

        removed: list[str] = []
        seen_keys: set[str] = set()
        new_full_file: list[str] = []
        current_section: str | None = None

        for line in self.full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                new_full_file.append(line)
                continue

            if not stripped or stripped.startswith(("#", ";")):
                new_full_file.append(line)
                continue

            if "=" in line and current_section == region:
                key, value = map(str.strip, line.split("=", 1))
                resolved_value = self.resolve(region).get(key, value)
                if key in seen_keys:
                    removed.append(key)
                    continue
                seen_keys.add(key)

            new_full_file.append(line)

        self.full_file = new_full_file

        self.raw_lines = [l for l in self.full_file if l.strip() and not l.strip().startswith(("#", ";"))]
        self.data.clear()
        self.keys.clear()
        self.regions.clear()
        current_section = None
        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue
            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                self.keys[f"{current_section}.{k}"] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return removed

    def populate(self, region: str, value: str) -> list[str]:
        """
        Populate empty keys in a region with the same value.

        Empty means:
            - key=
            - key=   (whitespace)
            - key value resolves to empty after stripping

        Args:
            region (str): Target section name
            value (str): Value to assign to empty keys

        Returns:
            list[str]: Keys that were populated
        """
        populated: list[str] = []
        new_full_file: list[str] = []
        current_section: str | None = None

        try:
            with open(self.path, "r", encoding=self.encoding, errors=self.errors) as file:
                for line in file:
                    stripped = line.strip()

                    if stripped.startswith("[") and stripped.endswith("]"):
                        current_section = stripped[1:-1].strip()
                        new_full_file.append(line)
                        continue

                    if not stripped or stripped.startswith(("#", ";")):
                        new_full_file.append(line)
                        continue

                    if current_section == region and "=" in stripped:
                        key, val = map(str.strip, stripped.split("=", 1))
                        if not val:
                            populated.append(key)
                            newline = f"{key}={value}\n"
                            new_full_file.append(newline)
                            continue

                    new_full_file.append(line)

            self.full_file = new_full_file

            self.raw_lines = []
            self.data = {}
            current_section = None

            for line in self.full_file:
                stripped = line.strip()

                if not stripped or stripped.startswith(("#", ";")):
                    continue

                for c in ("#", ";"):
                    if c in stripped:
                        stripped = stripped.split(c, 1)[0].strip()

                if not stripped:
                    continue

                self.raw_lines.append(stripped)

                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    self.data.setdefault(current_section, {})
                    continue

                if "=" in stripped and current_section is not None:
                    k, v = map(str.strip, stripped.split("=", 1))
                    self.data[current_section][k] = v

            with open(self.path, "w", encoding=self.encoding, errors=self.errors) as file:
                file.writelines(self.full_file)

            return populated

        except FileNotFoundError:
            if self.raises:
                raise self.raises(f"INI file not found: {self.path}")
            return []
        
    def mutate(self, region: str, key: str, value: str) -> bool:
        """
        Set the value of a key inside a region.

        Updates the real file first, then synchronizes:
            - self.full_file
            - self.raw_lines
            - self.data

        Args:
            region (str): Section name
            key (str): Key name
            value (str): New value

        Returns:
            bool: True if key was updated, False if region or key not found
        """
        new_full_file: list[str] = []
        current_section: str | None = None
        updated = False

        try:
            with open(self.path, "r", encoding=self.encoding, errors=self.errors) as file:
                for line in file:
                    stripped = line.strip()

                    if stripped.startswith("[") and stripped.endswith("]"):
                        current_section = stripped[1:-1].strip()
                        new_full_file.append(line)
                        continue

                    if current_section == region and "=" in stripped:
                        key_part, rest = stripped.split("=", 1)
                        if key_part.strip() == key:
                            new_full_file.append(f"{key}={value}\n")
                            updated = True
                            continue

                    new_full_file.append(line)

            if not updated:
                return False

            self.full_file = new_full_file

            self.raw_lines = []
            self.data = {}
            current_section = None

            for line in self.full_file:
                stripped = line.strip()

                if not stripped or stripped.startswith(("#", ";")):
                    continue

                for c in ("#", ";"):
                    if c in stripped:
                        stripped = stripped.split(c, 1)[0].strip()

                if not stripped:
                    continue

                self.raw_lines.append(stripped)

                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    self.data.setdefault(current_section, {})
                    continue

                if "=" in stripped and current_section is not None:
                    k, v = map(str.strip, stripped.split("=", 1))
                    self.data[current_section][k] = v

            with open(self.path, "w", encoding=self.encoding, errors=self.errors) as file:
                file.writelines(self.full_file)

            return True

        except FileNotFoundError:
            if self.raises:
                raise self.raises(f"INI file not found: {self.path}")
            return False

    def assign(self, region: str, key: str | dict[str, str], value: str | None = None) -> bool:
        """
        Append new key=value(s) at the end of a region and immediately write to the file.

        - key can be a str (single key) or dict[str, str] for multiple keys.
        - Does not overwrite existing keys.
        - Updates self.full_file, self.raw_lines, self.data, and the actual INI file.

        Returns True if at least one key was added, False otherwise.
        """
        if isinstance(key, dict):
            items_to_add = key
        else:
            if value is None:
                raise ValueError("Must provide value when key is a string")
            items_to_add = {key: value}

        new_full_file: list[str] = []
        current_section: str | None = None
        region_found = False
        inserted_any = False
        last_key_index: int | None = None

        for idx, line in enumerate(self.full_file):
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                if current_section == region:
                    region_found = True
                    last_key_index = idx

            if current_section == region and "=" in stripped:
                last_key_index = idx

            new_full_file.append(line)

        if not region_found:
            return False

        insert_index = last_key_index + 1 if last_key_index is not None else len(new_full_file)

        existing_keys = set(self.data.get(region, {}).keys())
        for k, v in items_to_add.items():
            if k in existing_keys:
                continue
            new_full_file.insert(insert_index, f"{k}={v}\n")
            insert_index += 1
            inserted_any = True

        if not inserted_any:
            return False

        self.full_file = new_full_file
        self.raw_lines = []
        self.data = {}
        self.keys = {}
        self.regions = []

        current_section = None
        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()

            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue

            if "=" in stripped and current_section:
                k2, v2 = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k2] = v2
                self.keys[f"{current_section}.{k2}"] = v2

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return True

    def register(self, region: str) -> None:
        """
        Add a new region at the end of the INI file.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Args:
            region (str): Name of the new region to add.
        """
        if region in self.data:
            return

        new_line = f"[{region}]\n"
        if self.full_file and not self.full_file[-1].endswith("\n"):
            self.full_file[-1] += "\n"
        self.full_file.append(new_line)

        self.data[region] = {}
        self.regions.append(region)
        self.raw_lines.append(f"[{region}]")

        with open(self.path, "a", encoding=self.encoding, errors=self.errors) as f:
            f.write(new_line)

    
    def prune_empty_keys(self, region: str) -> list[str]:
        """
        Remove keys with empty values in a specific region.

        Placeholder-aware: resolved value is checked.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - Actual file

        Parameters:
        -----------
        region : str
            The region to clean empty keys from.

        Returns:
        --------
        list[str]
            Keys that were removed.
        """
        removed = []
        new_full_file = []
        current_section = None

        for line in self.full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                new_full_file.append(line)
                continue

            if current_section == region and "=" in stripped:
                key, value = map(str.strip, stripped.split("=", 1))
                resolved_value = self._resolve_value(value, region)
                if not resolved_value.strip():
                    removed.append(key)
                    continue

            new_full_file.append(line)

        self._update_memory_and_file(new_full_file)
        return removed
    
    def prune_empty_regions(self) -> list[str]:
        """
        Remove regions that contain no keys (after placeholder resolution).

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - Actual file

        Returns:
        --------
        list[str]
            Names of removed regions.
        """
        removed = []
        new_full_file = []
        current_section = None
        region_has_keys = False

        for line in self.full_file + [""]:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]") or line == "":
                if current_section and not region_has_keys:
                    removed.append(current_section)
                    if new_full_file and new_full_file[-1].strip() == f"[{current_section}]":
                        new_full_file.pop()
                current_section = stripped[1:-1].strip() if stripped else None
                region_has_keys = False
                if stripped:
                    new_full_file.append(line)
                continue

            if current_section and "=" in stripped:
                key, value = map(str.strip, stripped.split("=", 1))
                resolved_value = self._resolve_value(value, current_section)
                if resolved_value.strip():
                    region_has_keys = True

            new_full_file.append(line)

        self._update_memory_and_file(new_full_file)
        return removed
    
        
    # def resolve(self, region: str) -> dict[str, str]:
    #     """
    #     Resolve placeholders in a specific region and update the INI file.
    # 
    #     This method:
    #     - Resolves same-region placeholders (@key) and cross-region placeholders (@region.key)
    #     - Updates self.data, self.raw_lines, self.full_file
    #     - Writes changes back to the actual INI file
    # 
    #     Circular references are detected and skipped.
    # 
    #     Args:
    #         region (str): The region/section to process.
    # 
    #     Returns:
    #         dict[str, str]: Keys in the region that were updated with resolved values.
    #     """
    #     if region not in self.data:
    #         return {}
    # 
    #     updated_keys: dict[str, str] = {}
    #     new_full_file: list[str] = []
    #     current_section: str | None = None
    # 
    #     for line in self.full_file:
    #         stripped = line.strip()
    #         line_to_add = line
    # 
    #         if stripped.startswith("[") and stripped.endswith("]"):
    #             current_section = stripped[1:-1].strip()
    #             new_full_file.append(line_to_add)
    #             continue
    #         
    #         if current_section == region and "=" in stripped:
    #             key, value = map(str.strip, stripped.split("=", 1))
    #             resolved_value = self._resolve_placeholders(value, region)
    # 
    #             if resolved_value != self.data[region].get(key, ""):
    #                 updated_keys[key] = resolved_value
    #                 line_to_add = f"{key}={resolved_value}\n"
    # 
    #         new_full_file.append(line_to_add)
# 
    #     self.full_file = new_full_file
    #     self.raw_lines.clear()
    #     self.data.clear()
    #     self.keys.clear()
    #     self.regions.clear()
    # 
    #     current_section = None
    #     for line in self.full_file:
    #         stripped = line.strip()
    #         if not stripped or stripped.startswith(("#", ";")):
    #             continue
    #         self.raw_lines.append(stripped)
    #         if stripped.startswith("[") and stripped.endswith("]"):
    #             current_section = stripped[1:-1].strip()
    #             self.data.setdefault(current_section, {})
    #             self.regions.append(current_section)
    #             continue
    #         if "=" in stripped and current_section:
    #             k, v = map(str.strip, stripped.split("=", 1))
    #             self.data[current_section][k] = v
    #             self.keys[f"{current_section}.{k}"] = v
    # 
    #     with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
    #         for line in self.full_file:
    #             f.write(line if line.endswith("\n") else line + "\n")
    # 
    #     return updated_keys


    def get(self, region: str, key: str) -> str | None:
        """
        Retrieve the value of a key in a specific region.

        Args:
            region (str): The section/region name.
            key (str): The key name.

        Returns:
            str | None: Value of the key if found, else None.
        """
        if region not in self.data:
            return None
        return self.data[region].get(key)

    def gather(self, region: str) -> dict[str, str] | None:
        """
        Retrieve all keys and values from a specific region.

        Args:
            region (str): The section/region name.

        Returns:
            dict[str, str] | None: Dictionary of key-value pairs in the region,
                                    or None if the region does not exist.
        """
        return dict(self.data.get(region, {}))
    
    def get_duplicates(self, region: str) -> dict[str, str]:
        """
        Find keys in a region that share the same value, resolving placeholders.

        Placeholders in the format @key will be temporarily replaced with
        the value of that key in the same region to detect duplicates.

        Args:
            region (str): Section/region name.

        Returns:
            dict[str, str]: Dictionary of keys whose **effective values** are
                            duplicates. Keys are the INI keys, values are
                            the original (possibly placeholder) values.

        Example:
            [build]
            name=matija
            fullname=@name
            debug=true

            get_duplicates_with_placeholders("build")
            # Output: {'name': 'matija', 'fullname': '@name'}
        """
        if region not in self.data:
            return {}

        resolved = {}
        for k, v in self.data[region].items():
            resolved[k] = self._resolve_placeholder_value(v, region)

        value_to_keys: Dict[str, List[str]] = {}
        for k, v in resolved.items():
            value_to_keys.setdefault(v, []).append(k)

        duplicates = {}
        for val, keys in value_to_keys.items():
            if len(keys) > 1:
                for key in keys:
                    duplicates[key] = val

        return duplicates
    
    def delete(self, region: str, key: str) -> bool:
        """
        Delete a specific key in a region from the INI file.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Args:
            region (str): The section/region name.
            key (str): The key to delete.

        Returns:
            bool: True if the key was found and deleted, False otherwise.
        """
        if region not in self.data or key not in self.data[region]:
            return False

        new_full_file = []
        current_section: str | None = None
        deleted = False

        for line in self.full_file:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                new_full_file.append(line)
                continue

            if not stripped or stripped.startswith(("#", ";")):
                new_full_file.append(line)
                continue

            if current_section == region and "=" in stripped:
                k = stripped.split("=", 1)[0].strip()
                if k == key:
                    deleted = True
                    continue

            new_full_file.append(line)
            
        self.full_file = new_full_file

        self.raw_lines = []
        self.data = {}
        current_section = None

        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()
            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                continue

            if "=" in stripped and current_section is not None:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                
        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return deleted

    def rremove(self, region: str) -> bool:
        """
        Remove an entire region (section) from the INI file.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Args:
            region (str): The section/region to remove.

        Returns:
            bool: True if the region existed and was removed, False otherwise.
        """
        if region not in self.data:
            return False

        new_full_file = []
        current_section: str | None = None
        removing = False

        for line in self.full_file:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                removing = (current_section == region)
                if not removing:
                    new_full_file.append(line)
                continue

            if not removing:
                new_full_file.append(line)

        self.full_file = new_full_file

        self.raw_lines = []
        self.data = {}
        current_section = None

        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()
            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                continue

            if "=" in stripped and current_section is not None:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return True

    
    def prune_duplicate_keys(self, region: str) -> list[str]:
        """
        Remove duplicate keys with the same name within a specific region.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - Actual file

        Parameters:
        -----------
        region : str
            The target region to prune duplicates.

        Returns:
        --------
        list[str]
            Names of keys that were removed.
        """
        removed: list[str] = []
        new_full_file: list[str] = []
        current_section: str | None = None
        seen_keys: set[str] = set()

        for line in self.full_file:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                new_full_file.append(line)
                if current_section == region:
                    seen_keys.clear()
                continue

            if current_section == region and "=" in stripped:
                key = stripped.split("=", 1)[0].strip()
                if key in seen_keys:
                    removed.append(key)
                    continue
                seen_keys.add(key)

            new_full_file.append(line)

        self._update_memory_and_file(new_full_file)
        return removed

    def prune_duplicates(self) -> list[str]:
        """
        Remove duplicate keys in all regions, keeping only the first occurrence.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Returns:
            list[str]: List of duplicate keys that were removed, formatted as "region.key".
        """
        removed_keys: list[str] = []
        new_full_file: list[str] = []
        current_section: str | None = None
        seen_keys_in_section: set[str] = set()

        for line in self.full_file:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                seen_keys_in_section = set()
                new_full_file.append(line)
                continue

            if not stripped or stripped.startswith(("#", ";")):
                new_full_file.append(line)
                continue

            if "=" in stripped and current_section is not None:
                key = stripped.split("=", 1)[0].strip()
                identifier = f"{current_section}.{key}"

                if key in seen_keys_in_section:
                    removed_keys.append(identifier)
                    continue

                seen_keys_in_section.add(key)

            new_full_file.append(line)

        self.full_file = new_full_file

        self.raw_lines = []
        self.data = {}
        current_section = None

        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()
            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                continue

            if "=" in stripped and current_section is not None:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return removed_keys

    def prune_duplicate_regions(self) -> list[str]:
        """
        Remove duplicate regions (section headers) from the INI file, keeping only the first occurrence.

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Returns:
            list[str]: List of duplicate region names that were removed.
        """
        seen_regions: set[str] = set()
        removed_regions: list[str] = []
        new_full_file: list[str] = []
        current_section: str | None = None
        skip_section: bool = False

        for line in self.full_file:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                if current_section in seen_regions:
                    removed_regions.append(current_section)
                    skip_section = True
                else:
                    seen_regions.add(current_section)
                    skip_section = False
                    new_full_file.append(line)
                continue

            if skip_section:
                continue

            new_full_file.append(line)

        self.full_file = new_full_file

        self.raw_lines = []
        self.data = {}
        current_section = None

        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()
            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                continue

            if "=" in stripped and current_section is not None:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return removed_regions

    def plain_sanitize(self, remove_comments: bool = False, preserve_inline: bool = True) -> dict[str, list[str]]:
        """
        Fully sanitize the INI file with flexible comment removal.

        Operations performed:
            1. Remove duplicate region headers (keep first occurrence)
            2. Remove duplicate keys in each region (keep first occurrence)
            3. Remove keys without value
            4. Remove empty regions
            5. Optionally remove comments and/or inline comments

        Updates:
            - self.data
            - self.raw_lines
            - self.full_file
            - actual INI file

        Args:
            remove_comments (bool): If True, removes comments.
            preserve_inline (bool): If True, preserves full-line comments but removes inline comments.

        Returns:
            dict[str, list[str]]: Report of removed items:
                {
                    "regions": removed duplicate regions,
                    "keys": removed duplicate keys,
                    "empty_keys": removed empty keys,
                    "empty_regions": removed empty regions,
                    "comments": removed comment lines or inline comments
                }
        """
        report = {
            "regions": self.prune_duplicate_regions(),
            "keys": [],
            "empty_keys": [],
            "empty_regions": [],
            "comments": []
        }

        for region in list(self.data.keys()):
            removed_keys = self.prune_duplicates_in_region(region)
            report["keys"].extend(removed_keys)

        for region in list(self.data.keys()):
            empty_keys = [f"{region}.{k}" for k, v in self.data[region].items() if not v.strip()]
            for k in empty_keys:
                self.delete(region, k)
            report["empty_keys"].extend(empty_keys)

        for region in list(self.data.keys()):
            if not self.data[region]:
                self.remove_region(region)
                report["empty_regions"].append(region)
                
        if remove_comments:
            new_full_file = []
            for line in self.full_file:
                stripped = line.strip()

                if stripped.startswith(("#", ";")):
                    if not preserve_inline:
                        report["comments"].append(line)
                        continue
                    else:
                        new_full_file.append(line)
                        continue

                for c in ("#", ";"):
                    if c in line:
                        parts = line.split(c, 1)
                        if preserve_inline:
                            report["comments"].append(f"{c}{parts[1]}")
                            line = parts[0].rstrip()
                        else:
                            report["comments"].append(line)
                            line = ""
                            break

                if line.strip():
                    new_full_file.append(line)

            self.full_file = new_full_file

            self.raw_lines = []
            self.data = {}
            current_section = None

            for line in self.full_file:
                stripped = line.strip()
                if not stripped:
                    continue

                self.raw_lines.append(stripped)

                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    self.data.setdefault(current_section, {})
                    continue

                if "=" in stripped and current_section is not None:
                    k, v = map(str.strip, stripped.split("=", 1))
                    self.data[current_section][k] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return report

    def sanitize_strict(
        self,
        remove_comments: bool = False,
        preserve_inline: bool = True,
        dry_run: bool = False
    ) -> dict[str, list[str]]:
        """
        Fully sanitize the INI file with placeholder resolution, comment removal, and dry-run mode.

        Operations performed:
            1. Remove duplicate region headers
            2. Remove duplicate keys per region (considering placeholders)
            3. Remove keys with empty values (considering placeholders)
            4. Remove empty regions
            5. Optionally remove comments and/or inline comments

        Placeholders:
            Values that start with "@" will be resolved recursively within the INI file.
            Example:
                [build]
                name=matija
                fullname=@name

            fullname is treated as "matija" when checking duplicates or emptiness.

        Args:
            remove_comments (bool): If True, removes comments.
            preserve_inline (bool): If True, preserves full-line comments but removes inline comments.
            dry_run (bool): If True, performs all operations in memory only, without writing changes to file.

        Returns:
            dict[str, list[str]]: Report of removed items:
                {
                    "regions": removed duplicate regions,
                    "keys": removed duplicate keys,
                    "empty_keys": removed empty keys,
                    "empty_regions": removed empty regions,
                    "comments": removed comments or inline comments
                }
        """
        def resolve_placeholder(value: str, region: str, depth=0) -> str:
            if depth > 10 or not value.startswith("@"):
                return value
            key_name = value[1:]
            if "." in key_name:
                r, k = key_name.split(".", 1)
            else:
                r, k = region, key_name
            if r in self.data and k in self.data[r]:
                return resolve_placeholder(self.data[r][k], r, depth + 1)
            return value

        full_file = list(self.full_file)
        data = {r: dict(self.data[r]) for r in self.data}
        raw_lines = list(self.raw_lines)

        report = {
            "regions": [],
            "keys": [],
            "empty_keys": [],
            "empty_regions": [],
            "comments": []
        }

        seen_regions = set()
        new_full_file = []
        skip_section = False
        current_section = None

        for line in full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                if current_section in seen_regions:
                    report["regions"].append(current_section)
                    skip_section = True
                else:
                    seen_regions.add(current_section)
                    skip_section = False
                    new_full_file.append(line)
                continue

            if skip_section:
                continue
            new_full_file.append(line)

        full_file = new_full_file

        current_section = None
        seen_values_in_section: set[str] = set()
        new_full_file2 = []

        for line in full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                seen_values_in_section = set()
                new_full_file2.append(line)
                continue

            if not stripped or stripped.startswith(("#", ";")):
                new_full_file2.append(line)
                continue

            if "=" in line and current_section is not None:
                key, value = map(str.strip, line.split("=", 1))
                resolved_value = resolve_placeholder(value, current_section)
                if resolved_value in seen_values_in_section:
                    report["keys"].append(f"{current_section}.{key}")
                    continue
                seen_values_in_section.add(resolved_value)

            new_full_file2.append(line)

        full_file = new_full_file2

        current_section = None
        new_full_file3 = []

        for line in full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                new_full_file3.append(line)
                continue

            if not stripped or stripped.startswith(("#", ";")):
                new_full_file3.append(line)
                continue

            if "=" in line and current_section is not None:
                key, value = map(str.strip, line.split("=", 1))
                resolved_value = resolve_placeholder(value, current_section)
                if not resolved_value.strip():
                    report["empty_keys"].append(f"{current_section}.{key}")
                    continue

            new_full_file3.append(line)

        full_file = new_full_file3

        if remove_comments:
            new_full_file4 = []
            for line in full_file:
                stripped = line.strip()
                if stripped.startswith(("#", ";")):
                    if not preserve_inline:
                        report["comments"].append(line)
                        continue
                    else:
                        new_full_file4.append(line)
                        continue

                for c in ("#", ";"):
                    if c in line:
                        parts = line.split(c, 1)
                        if preserve_inline:
                            report["comments"].append(f"{c}{parts[1]}")
                            line = parts[0].rstrip()
                        else:
                            report["comments"].append(line)
                            line = ""
                            break

                if line.strip():
                    new_full_file4.append(line)

            full_file = new_full_file4
        current_section = None
        region_lines: list[str] = []
        new_full_file5 = []
        for line in full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                if current_section is not None and not region_lines:
                    report["empty_regions"].append(current_section)
                    if new_full_file5 and new_full_file5[-1].strip() == f"[{current_section}]":
                        new_full_file5.pop()
                current_section = stripped[1:-1].strip()
                region_lines = []
                new_full_file5.append(line)
                continue

            if stripped and not stripped.startswith(("#", ";")):
                region_lines.append(line)

            new_full_file5.append(line)

        if current_section is not None and not region_lines:
            report["empty_regions"].append(current_section)
            if new_full_file5 and new_full_file5[-1].strip() == f"[{current_section}]":
                new_full_file5.pop()

        full_file = new_full_file5

        if not dry_run:
            self.full_file = full_file
            self.raw_lines = [line for line in full_file if line.strip() and not line.strip().startswith(("#", ";"))]
            self.data = {}
            current_section = None
            for line in full_file:
                stripped = line.strip()
                if not stripped or stripped.startswith(("#", ";")):
                    continue
                if stripped.startswith("[") and stripped.endswith("]"):
                    current_section = stripped[1:-1].strip()
                    self.data.setdefault(current_section, {})
                    continue
                if "=" in stripped and current_section is not None:
                    k, v = map(str.strip, stripped.split("=", 1))
                    self.data[current_section][k] = v

            with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
                for line in full_file:
                    f.write(line if line.endswith("\n") else line + "\n")

        return report
    
    # def rexist(self, region: str) -> bool:
    #     """
    #     Check if a region exists in the INI file.
    #     Uses `self.data` for accurate detection.
    #     """
    #     return region in self.data

    # def kexists(self, region: str, key: str) -> bool:
    #     """
    #     Check if a key exists in a specific region.
    #     """
    #     if region not in self.data:
    #         return False
    #     return key in self.data[region]

    def get_region(self, region: str) -> Dict[str, str]:
        """
        Return all key-value pairs in a region as dict[str, str].
        """
        return dict(self.data.get(region, {}))

    def get_duplicates(self, region: str) -> Dict[str, str]:
        """
        Return all keys in the region that have duplicate values,
        resolving placeholders first.
        """
        if region not in self.data:
            return {}

        resolved = {}
        for k, v in self.data[region].items():
            resolved[k] = self._resolve_placeholder_value(v, region)

        value_to_keys: Dict[str, List[str]] = {}
        for k, v in resolved.items():
            value_to_keys.setdefault(v, []).append(k)

        duplicates = {}
        for val, keys in value_to_keys.items():
            if len(keys) > 1:
                for key in keys:
                    duplicates[key] = val

        return duplicates

    def resolve_region(self, target: str, copy: bool = True) -> Dict[str, str]:
        """
        Resolve a temporary region directive like [@target] by optionally copying
        keys from the previous real region. Updates memory only; does NOT write file.
    
        Parameters:
            target (str): Name of the target directive (without @)
            copy (bool): If True, copy keys from the previous region
    
        Returns:
            Dict[str, str]: Keys that were added/updated
        """
        updated: Dict[str, str] = {}
        new_full_file: list[str] = []
        new_data: Dict[str, Dict[str, str]] = {}
        new_keys: Dict[str, str] = {}
        new_regions: list[str] = []
    
        prev_region: str | None = None
        target_found = False
        current_section: str | None = None
    
        for line in self.full_file:
            stripped = line.strip()

            if stripped.startswith("[") and stripped.endswith("]"):
                section_name = stripped[1:-1].strip()
                current_section = section_name

                if section_name == f"@{target}":
                    target_found = True
                    if prev_region is None or prev_region not in self.data:
                        new_full_file.append(f"[{target}]\n")
                        current_section = target
                        new_data[current_section] = {}
                        new_regions.append(current_section)
                        continue
                    
                    new_full_file.append(f"[{target}]\n")
                    current_section = target
                    new_data[current_section] = {}
                    new_regions.append(current_section)
    
                    if copy:
                        for k, v in self.data[prev_region].items():
                            resolved = v
                            parts = resolved.split()
                            for i, part in enumerate(parts):
                                if part.startswith("@"):
                                    key_str = part[1:]
                                    if "." in key_str:
                                        r, key_name = key_str.split(".", 1)
                                    else:
                                        r, key_name = prev_region, key_str
                                    replacement = self.data.get(r, {}).get(key_name, "")
                                    parts[i] = replacement
                            resolved = " ".join(parts)
                            updated[k] = resolved
                            new_full_file.append(f"{k}={resolved}\n")
                            new_data[current_section][k] = resolved
                            new_keys[f"{current_section}.{k}"] = resolved
                    continue

                if not section_name.startswith("@"):
                    prev_region = section_name

                if current_section not in new_data:
                    new_data[current_section] = {}
                    new_regions.append(current_section)

            new_full_file.append(line)
            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                new_data.setdefault(current_section, {})[k] = v
                new_keys[f"{current_section}.{k}"] = v

        self.full_file = new_full_file
        self.data = new_data
        self.keys = new_keys
        self.regions = new_regions
    
        return updated

    def sanitize(
        self,
        remove_comments: bool = False,
        remove_duplicate_keys: bool = False,
        remove_duplicate_regions: bool = False,
        space_between_regions: bool = False,
        dry_run: bool = False,
        resolve_placeholders: bool = False
    ) -> Dict[str, List[str]]:
        """
        Full sanitization of the INI file with optional behaviors, including
        temporary placeholder resolution for duplicate detection.

        Parameters:
            remove_comments (bool): Remove all comments (# or ;) if True.
            remove_duplicate_keys (bool): Remove duplicate keys by name in a region.
            remove_duplicate_regions (bool): Remove duplicate regions by name.
            space_between_regions (bool): Add empty line before and after each region.
            dry_run (bool): If True, do not modify memory or file.
            resolve_placeholders (bool): Temporarily resolve placeholders in keys and region names
                                         for duplicate detection only.

        Returns:
            Dict[str, List[str]]: Report of removed items:
                - 'regions': duplicate regions removed
                - 'keys': duplicate keys removed
                - 'comments': comments removed
        """
        report = {
            "regions": [],
            "keys": [],
            "comments": []
        }

        new_full_file: list[str] = []
        seen_regions: set[str] = set()
        current_section: str | None = None
        seen_keys: set[str] = set()

        for line in self.full_file:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("[") and stripped.endswith("]"):
                region_name = stripped[1:-1].strip()
                if resolve_placeholders:
                    region_name_resolved = self._resolve_placeholder_value(region_name, region_name)
                else:
                    region_name_resolved = region_name

                if remove_duplicate_regions:
                    if region_name_resolved in seen_regions:
                        report["regions"].append(region_name)
                        current_section = None
                        seen_keys.clear()
                        continue
                seen_regions.add(region_name_resolved)
                current_section = region_name
                seen_keys.clear()

                if space_between_regions and new_full_file and new_full_file[-1].strip() != "":
                    new_full_file.append("")

                new_full_file.append(f"[{region_name}]\n")

                if space_between_regions:
                    new_full_file.append("")

                continue

            # Remove comments
            if remove_comments and stripped.startswith(("#", ";")):
                report["comments"].append(line)
                continue

            if remove_comments:
                for c in ("#", ";"):
                    if c in line:
                        parts = line.split(c, 1)
                        report["comments"].append(f"{c}{parts[1]}")
                        line = parts[0].rstrip()
                        break
                if not line.strip():
                    continue

            if remove_duplicate_keys and "=" in line and current_section:
                key = line.split("=", 1)[0].strip()
                if resolve_placeholders:
                    key_resolved = self._resolve_placeholder_value(key, current_section)
                else:
                    key_resolved = key

                if key_resolved in seen_keys:
                    report["keys"].append(f"{current_section}.{key}")
                    continue
                seen_keys.add(key_resolved)

            new_full_file.append(line)

        if not dry_run:
            self.full_file = new_full_file
            self._rebuild_memory()
            self._write_file()

        return report

    
    def spacefy_full(self) -> None:
        """
        Ensure that each INI region has exactly one blank line after it.

        This function:
            - Adds a blank line after each region (except the last one)
            - Preserves comments and key-value lines
            - Updates memory structures:
                - self.full_file
                - self.raw_lines
                - self.data
            - Updates the actual INI file

        Example:
            Before:
            [global]
            key1=value1
            [build]
            key2=value2

            After:
            [global]
            key1=value1

            [build]
            key2=value2
        """
        new_full_file = []
        current_section: str | None = None

        for i, line in enumerate(self.full_file):
            stripped = line.strip()
            new_full_file.append(line)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()

                if i + 1 < len(self.full_file):
                    next_line = self.full_file[i + 1].strip()
                    if next_line != "":
                        new_full_file.append("\n")

        cleaned_full_file = []
        previous_empty = False
        for line in new_full_file:
            if line.strip() == "":
                if not previous_empty:
                    cleaned_full_file.append("\n")
                previous_empty = True
            else:
                cleaned_full_file.append(line)
                previous_empty = False

        self.full_file = cleaned_full_file

        self.raw_lines = [line for line in self.full_file if line.strip() and not line.strip().startswith(("#", ";"))]
        
        self.data.clear()
        self.keys.clear()
        self.regions.clear()
        current_section = None
        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue
            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                self.keys[f"{current_section}.{k}"] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

    def spacefy(self) -> None:
        """
        Ensure there is exactly one blank line **after each region** (except the last one).

        Updates:
            - self.full_file
            - self.raw_lines
            - self.data
            - self.keys
            - self.regions
            - Actual INI file

        Example:
            Before:
            [global]
            key1=value1
            [build]
            key2=value2

            After:
            [global]
            key1=value1

            [build]
            key2=value2
        """
        new_full_file: list[str] = []
        current_section: str | None = None
        buffer_region_lines: list[str] = []

        for line in self.full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                if current_section is not None and buffer_region_lines:
                    new_full_file.extend(buffer_region_lines)
                    if new_full_file[-1].strip() != "":
                        new_full_file.append("\n")
                    buffer_region_lines = []

                current_section = stripped[1:-1].strip()
                buffer_region_lines.append(line)
            else:
                buffer_region_lines.append(line)

        if buffer_region_lines:
            new_full_file.extend(buffer_region_lines)

        cleaned_full_file: list[str] = []
        previous_empty = False
        for line in new_full_file:
            if line.strip() == "":
                if not previous_empty:
                    cleaned_full_file.append("\n")
                previous_empty = True
            else:
                cleaned_full_file.append(line)
                previous_empty = False

        self.full_file = cleaned_full_file

        self.raw_lines = [line for line in self.full_file if line.strip() and not line.strip().startswith(("#", ";"))]

        self.data.clear()
        self.keys.clear()
        self.regions.clear()
        current_section = None
        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue
            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                self.keys[f"{current_section}.{k}"] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

    
    def length(self) -> int:
        """
        Get the number of lines in the file.

        Returns:
            int: Number of lines, or -1 if file does not exist.
        """
        if not os.path.isfile(self.path):
            return -1
        with open(self.path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)

    def size(self) -> int:
        """
        Get the size of the file in bytes.

        Returns:
            int: File size in bytes, or -1 if file does not exist.
        """
        if not os.path.isfile(self.path):
            return -1
        return os.path.getsize(self.path)
    
    def clear(self) -> None:
        """
        Remove all comments from the INI file, including:

            - Full-line comments starting with `#` or `;`
            - Inline comments on key-value lines

        Updates:
            - self.full_file
            - self.raw_lines
            - self.data
            - self.keys
            - self.regions
            - Writes changes back to the actual INI file

        Example:
            Before:
                ; This is a comment
                [global]
                version=1.0  ; inline comment

            After:
                [global]
                version=1.0
        """
        new_full_file: list[str] = []

        for line in self.full_file:
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith(";"):
                continue

            for c in ("#", ";"):
                if c in line:
                    parts = line.split(c, 1)
                    line = parts[0].rstrip()
                    break

            if line.strip():
                new_full_file.append(line)

        self.full_file = new_full_file
        self.raw_lines = [line for line in new_full_file if line.strip()]
        self.data.clear()
        self.keys.clear()
        self.regions.clear()

        current_section: str | None = None
        for line in self.full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue

            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                self.keys[f"{current_section}.{k}"] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

    def get_duplicate_keys(self, region: str) -> list[str]:
        """
        Return a list of keys in the given region that appear more than once in the file.

        Checks the raw file lines, not self.data (dict cannot store duplicates).

        Parameters:
            region (str): The region to check.

        Returns:
            list[str]: Keys that are duplicated within the region.
        """
        in_region = False
        seen = set()
        duplicates = set()

        for line in self.full_file:
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                current_region = stripped[1:-1].strip()
                in_region = current_region == region
                continue

            if in_region and "=" in stripped:
                key = stripped.split("=", 1)[0].strip()
                if key in seen:
                    duplicates.add(key)
                else:
                    seen.add(key)

        return list(duplicates)
    
    def copyto(self, region: str, to: str) -> None:
        """
        Copy all keys and values from `region` to another region `to`.
        If the target region does not exist, it is created at the end of the file.

        Parameters:
            region (str): Source region to copy from.
            to (str): Target region to copy to.
        """
        if region not in self.data:
            raise ValueError(f"Source region '{region}' does not exist.")

        target_exists = to in self.data

        lines_to_add = []

        if not target_exists:
            if self.full_file and self.full_file[-1].strip() != "":
                lines_to_add.append("\n")
            lines_to_add.append(f"[{to}]\n")

        for key, value in self.data[region].items():
            lines_to_add.append(f"{key}={value}\n")

        self.full_file.extend(lines_to_add)

        self._rebuild_memory()
        self._write_file()
        
    def leftout(self) -> list[str]:
        """
        Remove keys that exist outside of any region (floating keys).
    
        Returns:
            list[str]: List of removed keys in the format 'key=value'.
        """
        new_full_file: list[str] = []
        current_section: str | None = None
        removed_keys: list[str] = []
    
        for line in self.full_file:
            stripped = line.strip()
    
            if not stripped or stripped.startswith(("#", ";")):
                new_full_file.append(line)
                continue
            
            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                new_full_file.append(line)
                continue

            if "=" in line and current_section is None:
                removed_keys.append(stripped)
                continue

            new_full_file.append(line)
    
        self.full_file = new_full_file
        self._rebuild_memory()
        self._write_file()
    
        return removed_keys
    
    def copy_key(self, region: str, key: str, to: str) -> tuple[str, str]:
        """
        Copy a specific key from `region` to `to`, placing it at the end
        of the `to` region. Creates the region if it does not exist.
        """

        if region not in self.data:
            raise ValueError(f"Source region '{region}' does not exist.")
        if key not in self.data[region]:
            raise ValueError(f"Key '{key}' does not exist in region '{region}'.")

        value = self.data[region][key]
        lines = list(self.full_file)
        new_lines: list[str] = []
        in_target = False
        inserted = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            new_lines.append(line)

            if stripped.startswith("[") and stripped.endswith("]"):
                current = stripped[1:-1].strip()

                if current == to:
                    in_target = True
                    continue

                if in_target and not inserted:
                    new_lines.insert(len(new_lines)-1, f"{key}={value}\n")
                    inserted = True
                    in_target = False

        if in_target and not inserted:
            new_lines.append(f"{key}={value}\n")
            inserted = True

        if not inserted:

            if new_lines and new_lines[-1].strip() != "":
                new_lines.append("\n")
            new_lines.append(f"[{to}]\n")
            new_lines.append(f"{key}={value}\n")

        self.full_file = new_lines
        self._rebuild_memory()
        self._write_file()

        return key, value
    
    def put(self, content: dict[str, str]) -> bool:
        """
        Append key=value pairs to the end of the file.

        - Updates self.full_file, self.data, self.keys, self.raw_lines, and the actual INI file.
        - Does not check for region (just appends at the very end).

        Returns True if at least one key was added, False otherwise.
        """
        if not content:
            return False

        inserted_any = False

        for k, v in content.items():
            self.full_file.append(f"{k}={v}\n")
            inserted_any = True

        if not inserted_any:
            return False

        self.raw_lines = []
        self.data = {}
        self.keys = {}
        self.regions = []

        current_section: str | None = None
        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()

            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue

            if "=" in stripped and current_section:
                k2, v2 = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k2] = v2
                self.keys[f"{current_section}.{k2}"] = v2

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return True
    
    def inp(self, content: list[str]) -> bool:
        """
        Append lines to the end of the file.

        - content: list of strings, each line like "key=value" or "[section]"
        - Updates self.full_file, self.data, self.keys, self.raw_lines, and writes immediately to file.
        - Does not check for region; appends at the very end.

        Returns True if at least one line was added, False otherwise.
        """
        if not content:
            return False

        inserted_any = False

        for line in content:
            if line.strip():
                self.full_file.append(line if line.endswith("\n") else line + "\n")
                inserted_any = True

        if not inserted_any:
            return False

        self.raw_lines = []
        self.data = {}
        self.keys = {}
        self.regions = []

        current_section: str | None = None
        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            for c in ("#", ";"):
                if c in stripped:
                    stripped = stripped.split(c, 1)[0].strip()

            if not stripped:
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                self.data.setdefault(current_section, {})
                self.regions.append(current_section)
                continue

            if "=" in stripped and current_section:
                k, v = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k] = v
                self.keys[f"{current_section}.{k}"] = v

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return True
    
    def backup(self, to: str) -> bool:
        """
        Create a backup copy of the current INI file.

        Parameters:
        -----------
        to : str
            Destination path for the backup file.

        Returns:
        --------
        bool
            True if backup succeeded, False otherwise.
        """
        try:
            if not os.path.isfile(self.path):
                return False
  
            os.makedirs(os.path.dirname(to), exist_ok=True)

            with open(self.path, "r", encoding=self.encoding, errors=self.errors) as src, \
                 open(to, "w", encoding=self.encoding, errors=self.errors) as dst:
                for line in src:
                    dst.write(line)

            return True

        except Exception as e:
            if self.raises:
                raise self.raises(f"Failed to backup file: {e}")
            return False
        
    def template(self, region: str, content: dict[str, str]) -> dict:
        """
        Create a region template without modifying the file.

        Returns a dict that can later be passed to execute().
        """
        if not region or not isinstance(content, dict):
            return {}

        return {
            "region": region,
            "content": dict(content)
        }
    
    def execute(self, tpl: dict) -> bool:
        """
        Append a region template to the end of the INI file.

        tpl format:
        {
            "region": str,
            "content": dict[str, str]
        }
        """
        if not tpl or "region" not in tpl or "content" not in tpl:
            return False

        region = tpl["region"]
        content = tpl["content"]

        if not isinstance(content, dict):
            return False

        if self.full_file and self.full_file[-1].strip():
            self.full_file.append("\n")

        self.full_file.append(f"[{region}]\n")

        for k, v in content.items():
            self.full_file.append(f"{k}={v}\n")

        self.full_file.append("\n")

        self.data.clear()
        self.keys.clear()
        self.regions.clear()
        self.raw_lines.clear()

        current_section = None

        for line in self.full_file:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ";")):
                continue

            self.raw_lines.append(stripped)

            if stripped.startswith("[") and stripped.endswith("]"):
                current_section = stripped[1:-1].strip()
                if current_section not in self.data:
                    self.data[current_section] = {}
                    self.regions.append(current_section)
                continue

            if "=" in stripped and current_section:
                k2, v2 = map(str.strip, stripped.split("=", 1))
                self.data[current_section][k2] = v2
                self.keys[f"{current_section}.{k2}"] = v2

        with open(self.path, "w", encoding=self.encoding, errors=self.errors) as f:
            for line in self.full_file:
                f.write(line if line.endswith("\n") else line + "\n")

        return True
    
    def flush(self) -> bool:
        """
        Clear all contents of the INI file.

        Updates:
            - self.full_file
            - self.raw_lines
            - self.data
            - self.keys
            - self.regions
            - Actual file on disk

        Returns:
            True if file cleared, False if file does not exist.
        """
        if not os.path.exists(self.path):
            return False

        self.full_file.clear()
        self.raw_lines.clear()
        self.data.clear()
        self.keys.clear()
        self.regions.clear()

        with open(self.path, "w", encoding=self.encoding, errors=self.errors):
            pass

        return True

    def destroy(self) -> bool:
        """
        Delete the INI file from disk completely.

        Updates:
            - Clears all in-memory structures

        Returns:
            True if file was deleted, False if file did not exist.
        """
        if not os.path.exists(self.path):
            return False

        try:
            os.remove(self.path)
        except Exception:
            return False

        self.full_file.clear()
        self.raw_lines.clear()
        self.data.clear()
        self.keys.clear()
        self.regions.clear()

        return True
    
    def rename_region(self, old: str, new: str) -> bool:
        """
        Rename a region in memory and file.
        Updates self.data, self.full_file, self.keys, self.regions.
        Returns True if renamed, False if old region not found.
        """
        if old not in self.data:
            return False

        self.data[new] = self.data.pop(old)
        self.regions = [new if r == old else r for r in self.regions]
        self.keys = {k.replace(f"{old}.", f"{new}."): v for k, v in self.keys.items()}

        new_file = []
        for line in self.full_file:
            if line.strip() == f"[{old}]":
                new_file.append(f"[{new}]\n")
            else:
                new_file.append(line)
        self.full_file = new_file
        self._rebuild_memory()
        self._write_file()
        return True
    
    def rename_key(self, region: str, old_key: str, new_key: str) -> bool:
        """
        Rename a key within a region.
        Updates self.data, self.full_file, self.keys.
        Returns True if successful, False if region/key not found.
        """
        if region not in self.data or old_key not in self.data[region]:
            return False

        self.data[region][new_key] = self.data[region].pop(old_key)
        self.keys = {k.replace(f"{region}.{old_key}", f"{region}.{new_key}"): v
                     for k, v in self.keys.items()}

        new_file = []
        for line in self.full_file:
            if line.strip().startswith(f"{old_key}=") and line.strip().split("=", 1)[0].strip() == old_key:
                new_file.append(f"{new_key}={self.data[region][new_key]}\n")
            else:
                new_file.append(line)
        self.full_file = new_file
        self._rebuild_memory()
        self._write_file()
        return True
    
    def batch(self, *steps, strict: bool = True, debug: bool = False) -> list:
        """
        Execute multiple INIO operations sequentially and safely.

        Args:
            *steps:
                - bound INIO methods (ini.load)
                - callables accepting INIO (lambda ini: ini.flush())
                - tuples: (callable, *args)

            strict:
                If True (default):
                    - ANY error aborts execution
                    - memory is rolled back
                    - exception is raised

                If False:
                    - errors are collected
                    - execution continues
                    - rollback still happens at the end if errors occurred

            debug:
                If True:
                    - prints step-by-step execution info

        Returns:
            list: results of each step (or Exception objects if strict=False)
        """

        snapshot = {
            "full_file": list(self.full_file),
            "raw_lines": list(self.raw_lines),
            "data": {k: dict(v) for k, v in self.data.items()},
            "keys": dict(self.keys),
            "regions": list(self.regions),
        }

        results: list = []
        errors: list = []

        def log(msg: str):
            if debug:
                print(msg)

        log("▶ INIO.batch started")

        for index, step in enumerate(steps, start=1):
            try:
                log(f"  → Step {index}: {step}")

                if isinstance(step, tuple):
                    fn, *args = step
                    result = fn(*args)

                else:
                    try:
                        result = step()
                    except TypeError:
                        result = step(self)

                results.append(result)
                log(f"    OK: {result}")

            except Exception as e:
                log(f"    ERROR: {e}")
                errors.append(e)
                results.append(e)

                if strict:
                    log("↩ Rolling back (strict mode)")
                    self.full_file = snapshot["full_file"]
                    self.raw_lines = snapshot["raw_lines"]
                    self.data = snapshot["data"]
                    self.keys = snapshot["keys"]
                    self.regions = snapshot["regions"]
                    raise

        if errors:
            log("↩ Rolling back (non-strict mode)")
            self.full_file = snapshot["full_file"]
            self.raw_lines = snapshot["raw_lines"]
            self.data = snapshot["data"]
            self.keys = snapshot["keys"]
            self.regions = snapshot["regions"]

        log("INIO.batch finished")
        return results

    def snapshot(self) -> dict:
        """
        Capture a full in-memory snapshot of the INIO state.

        Useful for:
        - undo / rollback
        - dry-runs
        - transactional edits

        Returns:
            dict: Deep copy of internal state
        """
        return {
            "full_file": list(self.full_file),
            "raw_lines": list(self.raw_lines),
            "data": {k: dict(v) for k, v in self.data.items()},
            "keys": dict(self.keys),
            "regions": list(self.regions),
        }
        
    def restore(self, snapshot: dict) -> None:
        """
        Restore INIO memory state from a snapshot.
        """
        self.full_file = snapshot["full_file"]
        self.raw_lines = snapshot["raw_lines"]
        self.data = snapshot["data"]
        self.keys = snapshot["keys"]
        self.regions = snapshot["regions"]

    def diff(self) -> list[str]:
        """
        Compare memory content to disk content.

        Returns:
            List of human-readable diff lines
        """
        if not os.path.exists(self.path):
            return ["[disk missing]"]

        with open(self.path, "r", encoding=self.encoding, errors=self.errors) as f:
            disk = f.read().splitlines()

        mem = [l.rstrip("\n") for l in self.full_file]

        diff = []
        for i, (d, m) in enumerate(zip(disk, mem), start=1):
            if d != m:
                diff.append(f"Line {i}: disk='{d}' != mem='{m}'")

        if len(mem) > len(disk):
            diff.append("Memory has extra lines")

        return diff
    
    def pattern_search(self, pattern: str) -> dict[str, list[str]]:
        """
        Search keys and values using regex.

        Returns:
            dict: region -> matched keys
        """
        rx = re.compile(pattern)
        matches: dict[str, list[str]] = {}

        for region, keys in self.data.items():
            for k, v in keys.items():
                if rx.search(k) or rx.search(v):
                    matches.setdefault(region, []).append(k)

        return matches
    
    def validate_struct(self) -> list[str]:
        """
        Validate INI structure.

        Returns:
            List of problems found
        """
        errors: list[str] = []

        for region in self.regions:
            if not region:
                errors.append("Empty region name")

            keys = self.data.get(region, {})
            for k in keys:
                if not k:
                    errors.append(f"Empty key in [{region}]")

        return errors

    def merge(self, other: "INIO", overwrite: bool = False) -> None:
        """
        Merge another INIO into this one.
        """
        for region, keys in other.data.items():
            self.data.setdefault(region, {})
            for k, v in keys.items():
                if overwrite or k not in self.data[region]:
                    self.data[region][k] = v
                    
    def export(self) -> dict[str, dict[str, str]]:
        """
        Export INI data as pure Python dict.
        """
        return {r: dict(kv) for r, kv in self.data.items()}

    def clone(self, path: str) -> bool:
        """
        Clone current INI file to a new location.
        """
        try:
            with open(path, "w", encoding=self.encoding) as f:
                f.writelines(self.full_file)
            return True
        except OSError:
            return False
        
    def trace(self) -> str:
        """
        Return a detailed diagnostic snapshot.
        """
        return (
            f"INI Trace\n"
            f" Path: {self.path}\n"
            f" Regions: {len(self.regions)}\n"
            f" Keys: {len(self.keys)}\n"
            f" Lines: {len(self.full_file)}"
        )

    def lock(self) -> None:
        """
        Lock the INI instance to prevent file writes.
        
        Usage:
        ```
        if getattr(self, "_locked", False):
            raise RuntimeError("INI is locked (write prevented)")
        ```
        """
        self._locked = True

    def unlock(self) -> None:
        """
        Unlock the INI instance to allow file writes.
        
        Usage:
        ```
        if getattr(self, "_locked", False):
            raise RuntimeError("INI is locked (write prevented)")
        ```
        """
        self._locked = False
        
    def file_mode(self):
        return bool(self._locked)
        
    def is_readonly(self) -> bool:
        """
        Check if file is read-only on disk.
        """
        return not os.access(self.path, os.W_OK)
    
    def findall(self, key: str) -> list[str]:
        """
        Find all regions containing a key.
        """
        return [r for r, kv in self.data.items() if key in kv]
    
    def file_stats(self) -> dict[str, int]:
        """
        Return statistics about the INI file.
        """
        return {
            "regions": len(self.regions),
            "keys": sum(len(v) for v in self.data.values()),
            "lines": len(self.full_file),
            "empty_regions": sum(1 for r in self.regions if not self.data.get(r)),
        }
        
    def strip_comments(self) -> None:
        """
        Remove all comments from the INI file.
        """
        self.full_file = [
            line for line in self.full_file
            if not line.strip().startswith(("#", ";"))
        ]
        
    def swap_regions(self, a: str, b: str) -> bool:
        """
        Swap two regions' contents.
        """
        if a not in self.data or b not in self.data:
            return False

        self.data[a], self.data[b] = self.data[b], self.data[a]
        return True
    
    def bulk_assign(self, region: str, mapping: dict[str, str]) -> int:
        """
        Assign multiple keys at once.
        """
        if region not in self.data:
            self.data[region] = {}

        count = 0
        for k, v in mapping.items():
            self.data[region][k] = v
            count += 1

        return count
    
    def dry_run(self, fn, *args, **kwargs):
        """
        Execute a function without modifying disk.
        """
        snap = self.snapshot()
        try:
            return fn(*args, **kwargs)
        finally:
            self.restore(snap)
            
    def require(self, region: str, keys: list[str]) -> None:
        """
        Assert required keys exist.
        """
        missing = [k for k in keys if k not in self.data.get(region, {})]
        if missing:
            raise KeyError(f"Missing keys in [{region}]: {missing}")

    def hook(self, event: str, fn) -> None:
        """
        Register lifecycle hook.
        """
        self._hooks.setdefault(event, []).append(fn)

    def _emit(self, event: str):
        for fn in self._hooks.get(event, []):
            fn(self)

    def stdbatch(self, *ops, **opts):
        return self.wrap.batch(*ops, **opts)(self)

    
    class Region:
        def __init__(self, ini: "INIO", name: str, base: str | None = None):
            """
            Represents a region in an INI file.
            - name: target region name
            - base: optional region to extend
            """
            self.ini = ini
            self.name = name
            self.base = base

        def extend(self) -> None:
            """Copy keys from base region into this region if base exists."""
            if not self.base or self.base not in self.ini.data:
                return

            self.ini.data.setdefault(self.name, {})
            for k, v in self.ini.data[self.base].items():
                if k not in self.ini.data[self.name]:
                    self.ini.data[self.name][k] = v

            self.ini.keys.update({f"{self.name}.{k}": v for k, v in self.ini.data[self.name].items()})
        
        def resolve(self):
            """
            Fully resolve keys including inherited ones.
            Leaves region name as [region], just copies missing keys from base.
            """
            if not self.base:
                return

            base_data = self.ini.data.get(self.base, {})
            current_data = self.ini.data.get(self.name, {})

            for k, v in base_data.items():
                if k not in current_data:
                    current_data[k] = self.ini._resolve_placeholder_value(v, self.base)

            self.ini.data[self.name] = current_data
            self.ini.keys.update({f"{self.name}.{k}": v for k, v in current_data.items()})
        
        def resolve_functions(self):
            """
            Scan all regions/keys for placeholders starting with `!`.
            Replace them with return value of corresponding Python function.
            """
            func_map = {
                "get_date": lambda: __import__("datetime").datetime.now().isoformat(),
                "get_user": lambda: os.getlogin(),
            }

            for region, keys in self.data.items():
                for key, value in keys.items():
                    if isinstance(value, str) and value.startswith("!"):
                        func_name = value[1:]
                        if func_name in func_map:
                            self.data[region][key] = func_map[func_name]()
    
    class Expo:
        """
        Expo — Extended Exception Framework for INIO

        Provides a structured, extensible hierarchy of exceptions
        with rich metadata, debugging support, and Python-native behavior.
        """

        class INIOError(Exception):
            def __init__(self, message: str = "", *, context: dict | None = None):
                self.message = message or self.__class__.__name__
                self.context = context or {}
                super().__init__(self.message)

            def __str__(self) -> str:
                return self.message

            def __repr__(self) -> str:
                return f"{self.__class__.__name__}({self.message!r}, context={self.context!r})"

            def __eq__(self, other) -> bool:
                return (
                    isinstance(other, self.__class__) and
                    self.message == other.message and
                    self.context == other.context
                )

            def __hash__(self) -> int:
                return hash((self.__class__, self.message))

            def __reduce__(self):
                return (self.__class__, (self.message,), {"context": self.context})


        class FileError(INIOError):
            def __init__(self, path: str, message: str):
                self.path = path
                super().__init__(message, context={"path": path})

        class FileNotFound(FileError, FileNotFoundError):
            def __init__(self, path: str):
                super().__init__(path, f"INI file not found: {path}")

        class FilePermission(FileError, PermissionError):
            def __init__(self, path: str):
                super().__init__(path, f"Permission denied: {path}")

        class FileWriteError(FileError, IOError):
            def __init__(self, path: str):
                super().__init__(path, f"Failed to write file: {path}")

        class RegionError(INIOError):
            def __init__(self, region: str, message: str):
                self.region = region
                super().__init__(message, context={"region": region})

        class InvalidRegion(RegionError, KeyError):
            def __init__(self, region: str):
                super().__init__(region, f"Region does not exist: [{region}]")

        class DuplicateRegion(RegionError, ValueError):
            def __init__(self, region: str):
                super().__init__(region, f"Duplicate region detected: [{region}]")

        class DataError(Exception):
            def __init__(self, *args):
                super().__init__(*args)
                
        class ReadError(Exception):
            def __init__(self, *args):
                super().__init__(*args)
                
        class TunnelError(Exception):
            def __init__(self, *args):
                super().__init__(*args)
                
        class ConnectionException(RuntimeError):
            def __init__(self, *args):
                super().__init__(*args)
        class KeyErrorEx(INIOError):
            def __init__(self, region: str, key: str, message: str):
                self.region = region
                self.key = key
                super().__init__(
                    message,
                    context={"region": region, "key": key}
                )

        class InvalidKey(KeyErrorEx, KeyError):
            def __init__(self, region: str, key: str):
                super().__init__(region, key, f"Key does not exist: {region}.{key}")

        class DuplicateKey(KeyErrorEx, ValueError):
            def __init__(self, region: str, key: str):
                super().__init__(region, key, f"Duplicate key detected: {region}.{key}")

        class PlaceholderError(INIOError):
            def __init__(self, placeholder: str, message: str):
                self.placeholder = placeholder
                super().__init__(
                    message,
                    context={"placeholder": placeholder}
                )

        class UnresolvedPlaceholder(PlaceholderError):
            def __init__(self, placeholder: str):
                super().__init__(
                    placeholder,
                    f"Unresolved placeholder: {placeholder}"
                )

        class CircularPlaceholder(PlaceholderError, RuntimeError):
            def __init__(self, chain: list[str]):
                self.chain = chain
                super().__init__(
                    " → ".join(chain),
                    "Circular placeholder reference detected"
                )

        class ValidationError(INIOError, ValueError):
            def __init__(self, message: str, *, field: str | None = None):
                ctx = {"field": field} if field else {}
                super().__init__(message, context=ctx)
                
    class EBX(Exception):
        """
        ExpoBaseException

        A maximal base exception class that explicitly overrides and
        forwards all meaningful Python Exception / BaseException methods.

        This is intended as a foundation for a full exception hierarchy.
        """
        def __init__(self, *args):
            super().__init__(*args)
            self.args = args
        def __str__(self):
            return super().__str__()
        def __repr__(self):
            return f"{self.__class__.__name__}{self.args!r}"
        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, BaseException):
                return NotImplemented
            return self.args == other.args
        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return NotImplemented
            return not result
        def __hash__(self):
            return hash((self.__class__, self.args))

        def __getattribute__(self, name):
            return super().__getattribute__(name)

        def __setattr__(self, name, value):
            super().__setattr__(name, value)

        def __delattr__(self, name):
            super().__delattr__(name)

        def with_traceback(self, tb):
            return super().with_traceback(tb)

        @property
        def __cause__(self):
            return super().__getattribute__("__cause__")

        @__cause__.setter
        def __cause__(self, value):
            super().__setattr__("__cause__", value)

        @property
        def __context__(self):
            return super().__getattribute__("__context__")

        @__context__.setter
        def __context__(self, value):
            super().__setattr__("__context__", value)

        @property
        def __suppress_context__(self):
            return super().__getattribute__("__suppress_context__")

        @__suppress_context__.setter
        def __suppress_context__(self, value):
            super().__setattr__("__suppress_context__", value)

        def __reduce__(self):
            return (self.__class__, self.args)

        def __reduce_ex__(self, protocol):
            return self.__reduce__()


        def __dir__(self):
            return super().__dir__()

        def __bool__(self):
            return True

    class STDOP:
        """
        Extreme execution stopper bound to INIO state.
        """

        def __init__(self, ini: "INIO"):
            self._ini = ini
            self.locked = False
            self.reason: str | None = None

        def if_not_loaded(self, msg: str = "INI not loaded") -> None:
            if not self._ini.connection.loaded():
                self.panic(msg)

        def if_dirty(self, msg: str = "INI memory differs from disk") -> None:
            if self._ini.connection.dirty():
                self.panic(msg)

        def if_empty(self, msg: str = "INI loaded but empty") -> None:
            if self._ini.connection.empty():
                self.panic(msg)

        def if_missing_region(self, region: str) -> None:
            if region not in self._ini.data:
                self.panic(f"Missing region: {region}")

        def if_missing_key(self, region: str, key: str) -> None:
            if region not in self._ini.data or key not in self._ini.data[region]:
                self.panic(f"Missing key: {region}.{key}")


        def lock(self, reason: str) -> None:
            """
            Prevent any future writes.
            """
            self.locked = True
            self.reason = reason

        def unlock(self) -> None:
            self.locked = False
            self.reason = None

        def panic(self, reason: str) -> None:
            """
            Hard stop execution.
            """
            self.reason = reason
            raise RuntimeError(f"[INIO STOP] {reason}")

        def exit(self, code: int = 1) -> None:
            """
            Immediate process termination.
            """
            os._exit(code)


        def assert_writable(self) -> None:
            """
            Call before ANY write.
            """
            if self.locked:
                raise RuntimeError(f"[INIO STOP] Writes locked: {self.reason}")


        def status(self) -> dict[str, str | bool]:
            return {
                "locked": self.locked,
                "reason": self.reason,
                "loaded": self._ini.connection.loaded(),
                "dirty": self._ini.connection.dirty(),
                "empty": self._ini.connection.empty(),
                "file": os.path.isfile(self._ini.path),
            }

        def debug(self) -> str:
            s = self.status()
            return (
                "INIO STOP STATUS\n"
                f"  Locked : {s['locked']}\n"
                f"  Reason : {s['reason']}\n"
                f"  Loaded : {s['loaded']}\n"
                f"  Dirty  : {s['dirty']}\n"
                f"  Empty  : {s['empty']}\n"
                f"  File   : {s['file']}"
            )
            
    class Pretty:
        """
        Comprehensive terminal output and styling utilities for INIO.

        Features:
        - ANSI colors and text styles (bold, underline, blink, reverse)
        - Status labels: OK, WARN, ERROR, INFO, DEBUG, SUCCESS, FAIL
        - Formatted blocks, titles, banners, separators, lines
        - Pretty-print dicts, lists, tables, key-value pairs
        - Console printing with optional flush
        - Flexible and fully classmethod-based (no instantiation required)

        Usage:
            INIO.Pretty.ok("Loaded successfully")
            INIO.Pretty.block("CONFIG", INIO.Pretty.dump(ini.data))
        """

        RESET = "\033[0m"
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"

        BOLD = "\033[1m"
        DIM = "\033[2m"
        UNDERLINE = "\033[4m"
        BLINK = "\033[5m"
        REVERSE = "\033[7m"

        OK = GREEN + BOLD
        SUCCESS = GREEN + BOLD
        WARN = YELLOW + BOLD
        FAIL = RED + BOLD
        ERR = RED + BOLD
        INFO = CYAN + BOLD
        DEBUG = MAGENTA + BOLD

        @classmethod
        def paint(cls, text: str, *styles: str) -> str:
            """Apply one or more ANSI styles to a text string."""
            return "".join(styles) + text + cls.RESET

        @staticmethod
        def line(char: str = "─", width: int = 60) -> str:
            """Generate a horizontal line separator."""
            return char * width

        @staticmethod
        def title(text: str, char: str = "=") -> str:
            """Create a boxed title with top and bottom bars."""
            bar = char * len(text)
            return f"{bar}\n{text}\n{bar}"

        @classmethod
        def block(cls, title: str, content: str, color: str = "") -> str:
            """Create a formatted block with optional colored title."""
            header = cls.paint(title, cls.BOLD, color)
            return f"{header}\n{cls.line()}\n{content}"

        @classmethod
        def ok(cls, text: str) -> str:
            return cls.paint(f"✔ {text}", cls.OK)

        @classmethod
        def success(cls, text: str) -> str:
            return cls.paint(f"✔ {text}", cls.SUCCESS)

        @classmethod
        def warn(cls, text: str) -> str:
            return cls.paint(f"⚠ {text}", cls.WARN)

        @classmethod
        def fail(cls, text: str) -> str:
            return cls.paint(f"✖ {text}", cls.FAIL)

        @classmethod
        def error(cls, text: str) -> str:
            return cls.paint(f"✖ {text}", cls.ERR)

        @classmethod
        def info(cls, text: str) -> str:
            return cls.paint(f"ℹ {text}", cls.INFO)

        @classmethod
        def debug(cls, text: str) -> str:
            return cls.paint(f"» {text}", cls.DEBUG)
        
        @classmethod
        def std_ok(cls, text: str) -> str:
            return cls.paint(f"{text}", cls.OK)

        @classmethod
        def std_success(cls, text: str) -> str:
            return cls.paint(f"{text}", cls.SUCCESS)

        @classmethod
        def std_warn(cls, text: str) -> str:
            return cls.paint(f"{text}", cls.WARN)

        @classmethod
        def std_fail(cls, text: str) -> str:
            return cls.paint(f"{text}", cls.FAIL)

        @classmethod
        def std_error(cls, text: str) -> str:
            return cls.paint(f"{text}", cls.ERR)

        @classmethod
        def std_info(cls, text: str) -> str:
            return cls.paint(f"{text}", cls.INFO)

        @classmethod
        def std_debug(cls, text: str) -> str:
            return cls.paint(f"{text}", cls.DEBUG)

        @staticmethod
        def dump(obj, indent: int = 2) -> str:
            """
            Pretty-print a dict, list, or simple value.

            Args:
                obj: dict, list, or any object
                indent: Number of spaces per indentation

            Returns:
                Human-readable string
            """
            if isinstance(obj, dict):
                return "\n".join(" " * indent + f"{k}: {v}" for k, v in obj.items())
            if isinstance(obj, list):
                return "\n".join(" " * indent + f"- {v}" for v in obj)
            return str(obj)

        @staticmethod
        def dump_table(data: list[dict[str, str]], headers: list[str] | None = None, indent: int = 2) -> str:
            """
            Pretty-print a list of dictionaries as a table.

            Args:
                data: List of dictionaries (rows)
                headers: Optional list of column headers
                indent: Spaces before each row

            Returns:
                Formatted table string
            """
            if not data:
                return "<empty table>"

            if headers is None:
                headers = list(data[0].keys())

            col_widths = {h: max(len(h), *(len(str(row.get(h, ""))) for row in data)) for h in headers}

            lines = []
            header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
            sep_line = "-+-".join("-" * col_widths[h] for h in headers)
            lines.append(header_line)
            lines.append(sep_line)

            for row in data:
                line = " | ".join(str(row.get(h, "")).ljust(col_widths[h]) for h in headers)
                lines.append(" " * indent + line)

            return "\n".join(lines)

        @staticmethod
        def print(text: str, flush: bool = True) -> None:
            """Print text directly to console."""
            print(text, flush=flush)

        @classmethod
        def banner(cls, text: str, width: int = 60, char: str = "*") -> str:
            """Create a centered banner."""
            text = f" {text} "
            if len(text) > width:
                width = len(text)
            side = (width - len(text)) // 2
            return f"{char*side}{text}{char*side}"

        @classmethod
        def key_value(cls, key: str, value: str, key_color: str = "", value_color: str = "") -> str:
            """Format a single key-value pair with optional colors."""
            k = cls.paint(key, key_color)
            v = cls.paint(value, value_color)
            return f"{k} = {v}"
        
    class Conn:
        """
        Connection / state inspector for INIO instances.

        Provides a read-only interface to inspect the health, consistency, 
        and loading status of an INI file loaded into an INIO object.

        Features:
        ----------
        - Check if the file exists on disk.
        - Verify if the file is loaded into memory.
        - Check if regions, keys, or data exist.
        - Detect empty or uninitialized INI structures.
        - Compare memory vs. disk for unsaved changes.
        - Produce detailed human-readable diagnostic reports.
        - Raise exceptions if critical components are missing.

        Usage:
        ------
        ```python
        ini = INIO("config.ini")
        ini.load()

        conn = ini.Conn(ini)

        print(conn.loaded())      # True if INI loaded
        print(conn.empty())       # True if no keys present
        print(conn.dirty())       # True if memory != disk

        print(conn.summary())     # Full connection snapshot
        print(conn.debug())       # Pretty debug report
        conn.assert_loaded()      # Raises if file not loaded
        ```
        """

        def __init__(self, ini_instance: "INIO") -> None:
            """
            Initialize connection inspector for a given INIO instance.

            Parameters
            ----------
            ini_instance : INIO
                The INIO object to inspect.
            """
            self._ini = ini_instance

        def file(self) -> bool:
            """Check if the INI file exists on disk."""
            return os.path.isfile(self._ini.path)

        def loaded(self) -> bool:
            """Check if the INI file is loaded into memory (self.full_file)."""
            return bool(self._ini.full_file)
        
        def ok(self) -> bool:
            """Check if the INI file is loaded into memory (self.full_file)."""
            return bool(self._ini.full_file)

        def data(self) -> bool:
            """Check if parsed INI data exists (self.data dict)."""
            return bool(self._ini.data)

        def regions(self) -> bool:
            """Check if any regions are loaded."""
            return bool(self._ini.regions)

        def keys(self) -> bool:
            """Check if any keys are loaded in the INI."""
            return bool(self._ini.keys)

        def empty(self) -> bool:
            """
            Check if the file is loaded but contains no keys.

            Returns True if the file is loaded but no keys are present.
            """
            return self.loaded() and not self.keys()

        def dirty(self) -> bool:
            """
            Detect if memory is out-of-sync with disk.

            Compares `self._ini.full_file` to the actual file on disk.
            Returns True if the file has unsaved changes.
            """
            if not self.file() or not self.loaded():
                return False

            try:
                with open(self._ini.path, "r", encoding=self._ini.encoding, errors=self._ini.errors) as f:
                    disk_lines = [l.rstrip("\n") for l in f.readlines()]
            except OSError:
                return False

            memory_lines = [l.rstrip("\n") for l in self._ini.full_file]
            return disk_lines != memory_lines

        def unparsed_regions(self) -> list[str]:
            """
            Return a list of regions that exist in `full_file` but have no keys parsed.
            Useful for detecting empty sections.
            """
            empty_regions = []
            for region in self._ini.regions:
                if not self._ini.data.get(region):
                    empty_regions.append(region)
            return empty_regions

        def summary(self) -> dict[str, bool | list[str]]:
            """
            Return a comprehensive snapshot of the INI health.

            Returns a dictionary with keys:
                - file: exists on disk
                - loaded: file loaded into memory
                - data: parsed data exists
                - regions: any regions loaded
                - keys: any keys loaded
                - empty: loaded but no keys
                - dirty: memory ≠ disk
                - ok: loaded and data present
                - unparsed_regions: list of empty regions
            """
            return {
                "file": self.file(),
                "loaded": self.loaded(),
                "data": self.data(),
                "regions": self.regions(),
                "keys": self.keys(),
                "empty": self.empty(),
                "dirty": self.dirty(),
                "ok": self.loaded() and self.data(),
                "unparsed_regions": self.unparsed_regions(),
            }

        def debug(self) -> str:
            """
            Return a formatted, human-readable diagnostic report.

            Example Output:
            ----------------
            INIO Connection Debug
              File exists       : True
              Loaded into memory: True
              Data parsed       : True
              Regions           : 3
              Keys              : 12
              Empty             : False
              Dirty             : False
              OK                : True
              Unparsed regions  : ['comments', 'placeholders']
            """
            s = self.summary()
            report_lines = [
                "INIO Connection Debug",
                f"  File exists       : {s['file']}",
                f"  Loaded into memory: {s['loaded']}",
                f"  Data parsed       : {s['data']}",
                f"  Regions           : {len(self._ini.regions)}",
                f"  Keys              : {len(self._ini.keys)}",
                f"  Empty             : {s['empty']}",
                f"  Dirty             : {s['dirty']}",
                f"  OK                : {s['ok']}",
                f"  Unparsed regions  : {s['unparsed_regions']}",
            ]
            return "\n".join(report_lines)

        def assert_loaded(self) -> None:
            """
            Assert that the INI file is loaded and data is parsed.

            Raises:
                RuntimeError: if the file is not loaded or data is missing
            """
            if not self.loaded():
                raise RuntimeError("INI file is not loaded into memory")

            if not self.data():
                raise RuntimeError("INI file is loaded but no data was parsed")
            
    class Filesystem:
        """
        Filesystem utilities bound to INIO.

        Provides high-level file operations for INI files without modifying INIO memory:
        - Create INI files
        - Append structured content (dict of dicts)
        - Read file content (raw or parsed)
        - Overwrite, flush, or delete files
        - Backup INI files safely

        Note:
        -----
        - Does NOT parse placeholders.
        - Does NOT modify memory (self.data / self.full_file).
        - Does NOT validate INI syntax beyond simple formatting.
        """

        @staticmethod
        def create(path: str, overwrite: bool = False, ensure_dir: bool = True) -> bool:
            """
            Create a new empty INI file.

            Args:
                path: Target file path.
                overwrite: If True, overwrite an existing file.
                ensure_dir: If True, create parent directories if missing.

            Returns:
                True if file was created, False otherwise.
            """
            if not path.lower().endswith(".ini"):
                return False

            if os.path.exists(path) and not overwrite:
                return False

            directory = os.path.dirname(path)
            if directory and ensure_dir:
                os.makedirs(directory, exist_ok=True)

            with open(path, "w", encoding="utf-8"):
                pass

            return True

        @staticmethod
        def read_raw(path: str) -> str | None:
            """
            Read the raw INI file content as a string.

            Args:
                path: Path to the INI file.

            Returns:
                File content as a string, or None if file is missing.
            """
            if not os.path.exists(path):
                return None

            with open(path, "r", encoding="utf-8") as f:
                return f.read()

        @staticmethod
        def read_structured(path: str) -> dict[str, dict[str, str]] | None:
            """
            Read INI file content into a nested dictionary.

            Args:
                path: Path to the INI file.

            Returns:
                dict[region][key] = value, or None if file missing.
            """
            if not os.path.exists(path):
                return None

            data: dict[str, dict[str, str]] = {}
            current_region: str | None = None

            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped or stripped.startswith(("#", ";")):
                        continue
                    if stripped.startswith("[") and stripped.endswith("]"):
                        current_region = stripped[1:-1].strip()
                        data.setdefault(current_region, {})
                        continue
                    if "=" in stripped and current_region:
                        k, v = map(str.strip, stripped.split("=", 1))
                        data[current_region][k] = v

            return data

        @staticmethod
        def append(path: str, content: dict[str, dict[str, str]]) -> bool:
            """
            Append new regions and keys to an INI file.

            Args:
                path: Path to the INI file.
                content: dict[region][key] = value to append.

            Returns:
                True if at least one line was written, False otherwise.
            """
            if not os.path.exists(path) or not content:
                return False

            lines: list[str] = []

            for region, keys in content.items():
                lines.append(f"\n[{region}]\n")
                for k, v in keys.items():
                    lines.append(f"{k}={v}\n")

            with open(path, "a", encoding="utf-8") as f:
                f.writelines(lines)

            return True

        @staticmethod
        def overwrite(path: str, content: dict[str, dict[str, str]]) -> bool:
            """
            Overwrite the INI file with new content.

            Args:
                path: Path to the INI file.
                content: dict[region][key] = value to write.

            Returns:
                True if file was written, False otherwise.
            """
            if not path.lower().endswith(".ini"):
                return False

            lines: list[str] = []

            for region, keys in content.items():
                lines.append(f"[{region}]\n")
                for k, v in keys.items():
                    lines.append(f"{k}={v}\n")

            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return True

        @staticmethod
        def flush(path: str) -> bool:
            """
            Delete all content from the INI file without removing it.

            Args:
                path: Path to the INI file.

            Returns:
                True if flushed successfully, False otherwise.
            """
            if not os.path.exists(path):
                return False

            with open(path, "w", encoding="utf-8"):
                pass

            return True

        @staticmethod
        def destroy(path: str) -> bool:
            """
            Delete the INI file from disk.

            Args:
                path: Path to the INI file.

            Returns:
                True if file was deleted, False otherwise.
            """
            if not os.path.exists(path):
                return False
            try:
                os.remove(path)
                return True
            except OSError:
                return False

        @staticmethod
        def backup(path: str, to: str) -> bool:
            """
            Make a backup of an INI file.

            Args:
                path: Path to the original INI file.
                to: Path to store the backup.

            Returns:
                True if backup succeeded, False otherwise.
            """
            if not os.path.exists(path):
                return False

            try:
                directory = os.path.dirname(to)
                if directory:
                    os.makedirs(directory, exist_ok=True)
                with open(path, "r", encoding="utf-8") as src, open(to, "w", encoding="utf-8") as dst:
                    dst.writelines(src.readlines())
                return True
            except OSError:
                return False
            
    class Wrap:
        """
        Execution control, safety guards, and transactional helpers for INIO.

        This class provides decorator-based tools to enhance INIO methods with:
        - transactional execution
        - disk/memory safety
        - automatic rollback
        - dry-run evaluation
        - backup protection
        - invariant enforcement
        - user-facing warnings

        All decorators are optional and composable.

        Intended usage:
            @INIO.Wrap.atomic()
            @INIO.Wrap.requires_loaded()
            def rename_region(...):
                ...

            @INIO.Wrap.read_only()
            def get_keys(...):
                ...
        """

        @staticmethod
        def _capture_state(ini: "INIO") -> dict:
            """
            Capture a deep snapshot of INIO's mutable state.
            """
            return {
                "full_file": list(ini.full_file),
                "data": {r: dict(v) for r, v in ini.data.items()},
                "keys": dict(ini.keys),
                "regions": list(ini.regions),
            }

        @staticmethod
        def _restore_state(ini: "INIO", state: dict) -> None:
            """
            Restore INIO state from snapshot.
            """
            ini.full_file = state["full_file"]
            ini.data = state["data"]
            ini.keys = state["keys"]
            ini.regions = state["regions"]

        @classmethod
        def requires_loaded(cls):
            """
            Require the INI file to be loaded into memory.
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    if not self.full_file:
                        raise RuntimeError("INI file not loaded")
                    return func(self, *args, **kwargs)
                return wrapper
            return decorator

        @classmethod
        def requires_file(cls):
            """
            Require the INI file to exist on disk.
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    if not os.path.isfile(self.path):
                        raise FileNotFoundError(self.path)
                    return func(self, *args, **kwargs)
                return wrapper
            return decorator

        @classmethod
        def read_only(cls):
            """
            Enforce that a method performs no mutations.
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    before = cls._capture_state(self)
                    result = func(self, *args, **kwargs)
                    after = cls._capture_state(self)

                    if before != after:
                        raise RuntimeError(
                            f"Read-only violation in {func.__name__}"
                        )
                    return result
                return wrapper
            return decorator

        @classmethod
        def dry_run(cls):
            """
            Execute a method but discard all changes.
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    state = cls._capture_state(self)
                    result = func(self, *args, **kwargs)
                    cls._restore_state(self, state)
                    return result
                return wrapper
            return decorator


        @classmethod
        def atomic(cls):
            """
            Ensure atomic execution.

            On failure:
                - memory is restored
                - file is untouched
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    state = cls._capture_state(self)
                    try:
                        return func(self, *args, **kwargs)
                    except Exception:
                        cls._restore_state(self, state)
                        raise
                return wrapper
            return decorator

        @classmethod
        def with_backup(cls, *, suffix: str = ".bak"):
            """
            Create a file backup before execution.
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    if os.path.isfile(self.path):
                        try:
                            self.loc.backup(self.path, self.path + suffix)
                        except Exception:
                            pass
                    return func(self, *args, **kwargs)
                return wrapper
            return decorator

        @classmethod
        def warn_if_dirty(cls):
            """
            Warn if memory differs from disk before execution.
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    if hasattr(self, "conn") and self.conn.dirty():
                        print(
                            self.Pretty.warn(
                                "Memory state differs from disk"
                            )
                        )
                    return func(self, *args, **kwargs)
                return wrapper
            return decorator

        @classmethod
        def validate_regions(cls):
            """
            Ensure all region names are unique and valid.
            """
            def decorator(func):
                def wrapper(self: "INIO", *args, **kwargs):
                    result = func(self, *args, **kwargs)
                    if len(set(self.regions)) != len(self.regions):
                        raise RuntimeError("Duplicate region names detected")
                    return result
                return wrapper
            return decorator

        @classmethod
        def batch(cls, *functions) -> Any | None | ("INIO"):
            """
            Execute multiple INIO callables atomically.

            Usage:
            ```
                INIO.Wrap.batch(
                    lambda ini: ini.rename_region("a", "b"),
                    lambda ini: ini.rename_key("b", "x", "y"),
                )(ini)
            ```
            """
            def executor(ini: "INIO"):
                state = cls._capture_state(ini)
                try:
                    for fn in functions:
                        fn(ini)
                except Exception:
                    cls._restore_state(ini, state)
                    raise
            return executor
        
        @staticmethod
        def ini_feature(name: str):
            def decorator(cls):
                features = getattr(cls, "__features__", set())
                features.add(name)
                cls.__features__ = features
                return cls
            return decorator
        
    class Awaitable:
        def __init__(self, parent: "INIO"):
            self._inio = parent

        async def _call(self, fn, *args, **kwargs):
            """
            Run sync INIO methods without blocking the event loop.
            """
            return await asyncio.to_thread(fn, *args, **kwargs)

        async def load(self):
            return await self._call(self._inio.load)

        async def save(self):
            return await self._call(self._inio._write_file)

        async def assign(self, region, key, value):
            return await self._call(self._inio.assign, region, key, value)

        async def delete(self, region, key):
            return await self._call(self._inio.delete, region, key)

        async def delete_region(self, region):
            return await self._call(self._inio.delete_region, region)

        async def populate(self, region, value=None):
            if value is None:
                return await self._call(self._inio.populate, region)
            return await self._call(self._inio.populate, region, value)

        async def normalize(self, region):
            return await self._call(self._inio.normalize, region)

        async def resolve(self, region):
            return await self._call(self._inio.resolve, region)

        async def get(self, region, key):
            return self._inio.data.get(region, {}).get(key)

        async def regions(self):
            return list(self._inio.regions)

        async def keys(self):
            return list(self._inio.keys.keys())

        async def raw_lines(self):
            return list(self._inio.raw_lines)

        async def full_file(self):
            return list(self._inio.full_file)
        
        @staticmethod
        async def destroy(path: str) -> bool:
            """
            Delete the INI file from disk.

            Args:
                path: Path to the INI file.

            Returns:
                True if file was deleted, False otherwise.
            """
            if not os.path.exists(path):
                return False
            try:
                os.remove(path)
                return True
            except OSError:
                return False
            
class INIODEBUG(INIO):
    """
    Advanced debugging extension for INIO.
    Adds decorators, state snapshots, tracing, and timing.
    """

    def __init__(self, *args, debug=True, strict=False, **kwargs):
        self.debug_enabled = debug
        self.debug_strict = strict
        self._trace_stack = []

        super().__init__(*args, **kwargs)

        if self.debug_enabled:
            print("[INIODEBUG] Initialized")

    def debug_call(name: str | None = None):
        """Logs function calls and arguments."""
        def decorator(fn: Callable):
            label = name or fn.__name__

            @functools.wraps(fn)
            def wrapper(self, *args, **kwargs):
                if self.debug_enabled:
                    print(f"[CALL] {label}()")
                    if args:
                        print(f"  args={args}")
                    if kwargs:
                        print(f"  kwargs={kwargs}")
                return fn(self, *args, **kwargs)

            return wrapper
        return decorator

    def debug_time(fn: Callable):
        """Measures execution time."""
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            start = time.perf_counter()
            try:
                return fn(self, *args, **kwargs)
            finally:
                if self.debug_enabled:
                    elapsed = (time.perf_counter() - start) * 1000
                    print(f"[TIME] {fn.__name__}: {elapsed:.2f} ms")
        return wrapper

    def debug_exceptions(fn: Callable):
        """Catches and logs exceptions with full context."""
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            except Exception as e:
                print(f"[EXCEPTION] {fn.__name__}: {e}")
                traceback.print_exc()
                if self.debug_strict:
                    raise
                return None
        return wrapper

    def snapshot_state(fn: Callable):
        """Stores a state snapshot before and after execution."""
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            before = self._capture_state()
            result = fn(self, *args, **kwargs)
            after = self._capture_state()

            if self.debug_enabled:
                self._compare_state(before, after, fn.__name__)

            return result
        return wrapper



    def _capture_state(self) -> dict:
        """Capture internal state for comparison."""
        return {
            "lines": len(self.full_file),
            "regions": len(self.data),
            "keys": len(self.keys),
        }

    def _compare_state(self, before: dict, after: dict, context: str):
        print(f"[STATE] {context}")
        for k in before:
            if before[k] != after[k]:
                print(f"  {k}: {before[k]} → {after[k]}")

    def _push_trace(self, name: str):
        self._trace_stack.append(name)
        if self.debug_enabled:
            print(f"[TRACE →] {' > '.join(self._trace_stack)}")

    def _pop_trace(self):
        self._trace_stack.pop()

    @debug_call()
    @debug_time
    @debug_exceptions
    @snapshot_state
    def load(self, *args, **kwargs):
        self._push_trace("load")
        try:
            return super().load(*args, **kwargs)
        finally:
            self._pop_trace()

    @debug_call("batch")
    @debug_time
    @debug_exceptions
    @snapshot_state
    def batch(self, *steps, strict=True, debug=False):
        self._push_trace("batch")
        try:
            return super().batch(*steps, strict=strict, debug=True)
        finally:
            self._pop_trace()

    @debug_call("_update_memory_and_file")
    @debug_exceptions
    @snapshot_state
    def _update_memory_and_file(self, new_full_file):
        return super()._update_memory_and_file(new_full_file)


    def dump_state(self):
        print("\n[INIODEBUG] FULL STATE DUMP")
        print("Path:", self.path)
        print("Regions:", list(self.data.keys()))
        print("Keys:", self.keys)
        print("Lines:", len(self.full_file))
        print("Trace:", " > ".join(self._trace_stack) or "<idle>")

    def trace_tree(self):
        """Human-readable trace stack."""
        return " > ".join(self._trace_stack)

    def assert_region(self, region: str):
        if region not in self.data:
            raise KeyError(f"Region '{region}' does not exist")

    def assert_key(self, region: str, key: str):
        self.assert_region(region)
        if key not in self.data[region]:
            raise KeyError(f"Key '{key}' not found in [{region}]")

    def load(self, *args, **kwargs) -> Any:
        print(f"[INIODEBUG] Calling load(*{args}, **{kwargs})")
        try:
            result = super().load(*args, **kwargs)
            print("[INIODEBUG] Load successful.")
            return result
        except Exception as e:
            print(f"[INIODEBUG] Load failed: {e}")
            traceback.print_exc()
            raise

    def _update_memory_and_file(self, new_full_file: list[str]):
        """Override with a debug trace of changes before commit."""
        print("[INIODEBUG] Updating memory and file with new content:")
        for i, line in enumerate(new_full_file):
            print(f"  {i:3}: {repr(line)}")
        return super()._update_memory_and_file(new_full_file)

    def batch(self, *steps, strict: bool = True, debug: bool = False) -> list:
        """
        Override batch to enforce detailed debug even if debug=False is passed.
        """
        print(f"[INIODEBUG] Batch called with {len(steps)} steps, strict={strict}, debug={debug}")
        return super().batch(*steps, strict=strict, debug=True)

    def trace(self) -> str:
        """Returns pretty formatted diagnostic info."""
        base = super().trace()
        stats = self.file_stats()
        debug_info = (
            "\n-- DEBUG INFO --\n"
            f" Path: {self.path}\n"
            f" Regions: {stats['regions']}\n"
            f" Keys: {stats['keys']}\n"
            f" Lines: {stats['lines']}\n"
            f" Empty Regions: {stats['empty_regions']}\n"
        )
        return base + debug_info

    def dump_state(self):
        """
        Dump internal state for debugging:
         • full file lines
         • rawlines
         • parsed data
         • flat keys
        """
        print("[INIODEBUG] === Internal State Dump ===")
        print("--- Full File (raw) ---")
        for line in self.full_file:
            print(repr(line))
        print("\n--- Raw Lines (stripped) ---")
        print(self.raw_lines)
        print("\n--- Data (parsed) ---")
        for region, mapping in self.data.items():
            print(f"[{region}]")
            for key, val in mapping.items():
                print(f"   {key} = {val}")
        print("\n--- Flat Keys ---")
        print(self.keys)
        print("[INIODEBUG] === End Dump ===")

    def safe_execute(self, *steps, **kwargs):
        """
        A wrapper around batch that catches exceptions and
        prints full traceback without stopping the program.
        """
        try:
            return self.batch(*steps, **kwargs)
        except Exception as e:
            print("[INIODEBUG] safe_execute caught exception:")
            traceback.print_exc()
            return None
        

class INIODESCRIBE:
    """
    INIODESCRIBE
    ============

    A declarative, fluent, Python-native description language
    for expressing *configuration intent*.

    This class does NOT parse INI files.
    It describes *what a configuration means* and *how it should behave*.

    The goal is:
    - readability
    - discoverability
    - IDE friendliness
    - expressive power
    - long-term evolution of configs

    Think of this as a DSL embedded in Python.
    """

    def __init__(self, path: str):
        """
        Create a new configuration description.

        Args:
            path (str): Path to the INI file this description applies to.
        """
        self.path = path
        self._sections: dict[str, dict] = {}
        self._current_section: str | None = None
        self._current_key: str | None = None
        self._frozen = False

    def section(self, name: str):
        """
        Declare or switch to a section.

        Example:
            describe.section("server")
        """
        self._assert_not_frozen()
        self._sections.setdefault(name, {})
        self._current_section = name
        self._current_key = None
        return self

    def key(self, name: str):
        """
        Declare a key inside the current section.

        Must be called after section().

        Example:
            .section("server").key("port")
        """
        self._assert_not_frozen()

        if not self._current_section:
            raise RuntimeError("key() called before section()")

        self._sections[self._current_section][name] = {
            "type": None,
            "default": None,
            "required": False,
            "rules": [],
            "doc": None,
            "enum": None,
            "transform": None,
            "alias": None,
            "deprecated": False,
            "env": None,
            "cli": None,
            "on_change": None,
        }

        self._current_key = name
        return self

    def as_str(self):
        """Declare key as string."""
        return self._set_type(str)

    def as_int(self):
        """Declare key as integer."""
        return self._set_type(int)

    def as_float(self):
        """Declare key as float."""
        return self._set_type(float)

    def as_bool(self):
        """Declare key as boolean."""
        return self._set_type(bool)

    def as_path(self):
        """Declare key as filesystem path."""
        import pathlib
        return self._set_type(pathlib.Path)

    def list_of(self, subtype):
        """
        Declare key as list of values.

        Example:
            .list_of(int)
        """
        return self._set_type(("list", subtype))

    def map_of(self, key_type, value_type):
        """
        Declare key as mapping.

        Example:
            .map_of(str, int)
        """
        return self._set_type(("map", key_type, value_type))

    def _set_type(self, typ):
        self._assert_key()
        self._sections[self._current_section][self._current_key]["type"] = typ
        return self

    def default(self, value):
        """Declare default value."""
        self._assert_key()
        self._sections[self._current_section][self._current_key]["default"] = value
        return self

    def required(self):
        """Mark key as required."""
        self._assert_key()
        self._sections[self._current_section][self._current_key]["required"] = True
        return self

    def enum(self, *values):
        """
        Restrict key to a fixed set of values.

        This is semantic intent, not enforcement here.
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["enum"] = values
        return self

    def doc(self, text: str):
        """
        Attach documentation to the key.
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["doc"] = text
        return self

    def alias(self, name: str):
        """
        Declare an alternate name for the key.
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["alias"] = name
        return self

    def deprecated(self, reason: str | None = None):
        """
        Mark a key as deprecated.

        Optional reason can be provided.
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["deprecated"] = reason or True
        return self

    def env(self, var_name: str):
        """
        Bind key to an environment variable.

        Example:
            .env("PORT")
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["env"] = var_name
        return self

    def cli(self, flag: str):
        """
        Bind key to a CLI flag.

        Example:
            .cli("--port")
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["cli"] = flag
        return self

    def transform(self, fn):
        """
        Declare a transformation function applied to the value.
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["transform"] = fn
        return self

    def on_change(self, fn):
        """
        Register a callback for when the value changes.
        """
        self._assert_key()
        self._sections[self._current_section][self._current_key]["on_change"] = fn
        return self

    def freeze(self):
        """
        Freeze the description, preventing further modification.
        """
        self._frozen = True
        return self

    def clone(self):
        """
        Create a deep copy of this description.
        """
        import copy
        return copy.deepcopy(self)

    def describe(self) -> str:
        """
        Return a human-readable description of the configuration.
        """
        lines = []
        for section, keys in self._sections.items():
            lines.append(f"[{section}]")
            for key, meta in keys.items():
                desc = meta["doc"] or ""
                lines.append(f"  {key}: {desc}")
            lines.append("")
        return "\n".join(lines)

    def build(self):
        """
        Build an INIO instance and attach this description.

        The INIO object may later interpret or enforce this metadata.
        """
        ini = INIO(self.path)
        ini._description = self._sections
        return ini

    def _assert_key(self):
        if not self._current_key:
            raise RuntimeError("No active key()")

    def _assert_not_frozen(self):
        if self._frozen:
            raise RuntimeError("INIODESCRIBE is frozen and cannot be modified")


class INIOTyped(Generic[T]):
    """
    Typed configuration value wrapper.

    This class exists purely for static typing.
    """

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    def __repr__(self):
        return f"INIOTyped({self.value!r})"
    
class INIOHINTS:
    """
    Attribute-access proxy for configuration data.

    Enables:
        cfg.server.port
    instead of:
        cfg["server"]["port"]
    """

    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, name):
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return INIOHINTS(value)
            return value
        raise AttributeError(name)

    def __repr__(self):
        return f"<INIOHINTS {list(self._data.keys())}>"
    
class INIODOCS:
    """
    Documentation generator for INIODESCRIBE.
    """

    def __init__(self, description: dict):
        self.description = description

    def to_markdown(self) -> str:
        """
        Generate Markdown documentation.
        """
        lines = ["# Configuration Reference", ""]
        for section, keys in self.description.items():
            lines.append(f"## [{section}]")
            lines.append("")
            for key, meta in keys.items():
                line = f"- **{key}**"
                if meta.get("type"):
                    line += f" (`{meta['type']}`)"
                if meta.get("doc"):
                    line += f": {meta['doc']}"
                lines.append(line)
            lines.append("")
        return "\n".join(lines)

    def to_text(self) -> str:
        """
        Generate plain text documentation.
        """
        lines = []
        for section, keys in self.description.items():
            lines.append(f"[{section}]")
            for key, meta in keys.items():
                lines.append(f"  {key} - {meta.get('doc', '')}")
            lines.append("")
        return "\n".join(lines)
    
def describe(path: str):
    """
    Decorator that attaches an INIODESCRIBE
    definition to a function or class.
    """

    def wrapper(obj):
        desc = INIODESCRIBE(path)
        obj.__ini_description__ = desc
        return obj

    return wrapper

class INIOMODEL:
    """
    INIOMODEL
    =========

    A dataclass-backed configuration engine.

    This class bridges INI configuration data with Python dataclasses,
    turning configuration into a *typed object graph*.

    Core ideas:
    -----------
    • Configuration is an object, not a dict
    • Dataclasses define intent, structure, and defaults
    • INI provides values
    • Types are enforced at runtime and visible to static analyzers
    • Nested dataclasses = nested sections
    • Lists, dicts, enums, unions are supported
    • Minimal magic, maximum clarity

    This class does NOT parse INI files.
    It consumes already-parsed data (e.g. from INIO).

    Why this exists:
    ----------------
    Because good configuration should:
    • be typed
    • be discoverable
    • be inspectable
    • be refactor-safe
    • feel like normal Python
    """


    def __init__(
        self,
        model: Type,
        *,
        section: str | None = None,
        strict: bool = True,
        frozen: bool = False,
    ):
        """
        Args:
            model:
                A dataclass type defining the configuration structure.

            section:
                Optional INI section name to bind this model to.
                If omitted, the dataclass name is used.

            strict:
                If True, unknown keys raise errors.

            frozen:
                If True, the resulting object is immutable.
        """
        if not is_dataclass(model):
            raise TypeError("INIOMODEL requires a dataclass type")

        self.model = model
        self.section = section or model.__name__.lower()
        self.strict = strict
        self.frozen = frozen


    def build(self, data: dict) -> Any:
        """
        Build a dataclass instance from INI data.

        Args:
            data:
                Parsed INI data (section -> key -> value)

        Returns:
            An instance of the dataclass model.
        """
        section_data = data.get(self.section, {})
        instance = self._build_dataclass(self.model, section_data)

        if self.frozen:
            self._freeze(instance)

        return instance


    def _build_dataclass(self, cls: Type, values: dict):
        kwargs = {}
        used_keys = set()

        for f in fields(cls):
            key = self._field_key(f)
            used_keys.add(key)

            if key in values:
                raw = values[key]
                value = self._coerce_value(f.type, raw)
                kwargs[f.name] = value
            else:
                if f.default is not dataclasses.MISSING:
                    kwargs[f.name] = f.default
                elif f.default_factory is not dataclasses.MISSING:
                    kwargs[f.name] = f.default_factory()
                else:
                    raise KeyError(
                        f"Missing required config key: [{self.section}].{key}"
                    )

        if self.strict:
            extra = set(values) - used_keys
            if extra:
                raise KeyError(
                    f"Unknown config keys in [{self.section}]: {sorted(extra)}"
                )

        return cls(**kwargs)

    def _coerce_value(self, typ, value):
        """
        Convert raw INI values into typed Python values.

        This supports:
        - primitives
        - Optional[T]
        - list[T]
        - dict[K, V]
        - nested dataclasses
        - enums
        """
        origin = get_origin(typ)
        args = get_args(typ)

        if origin is typing.Union and type(None) in args:
            real_type = args[0] if args[1] is type(None) else args[1]
            return None if value in ("", None) else self._coerce_value(real_type, value)

        if origin is list:
            subtype = args[0]
            if isinstance(value, str):
                value = [v.strip() for v in value.split(",")]
            return [self._coerce_value(subtype, v) for v in value]

        if origin is dict:
            ktype, vtype = args
            if isinstance(value, str):
                pairs = value.split(",")
                result = {}
                for p in pairs:
                    k, v = p.split("=", 1)
                    result[self._coerce_value(ktype, k)] = self._coerce_value(vtype, v)
                return result
            return {
                self._coerce_value(ktype, k): self._coerce_value(vtype, v)
                for k, v in value.items()
            }

        if inspect.isclass(typ) and is_dataclass(typ):
            if not isinstance(value, dict):
                raise TypeError("Nested dataclass requires mapping value")
            return self._build_dataclass(typ, value)

        if inspect.isclass(typ) and hasattr(typ, "__members__"):
            return typ[value]

        if typ is bool:
            return str(value).lower() in ("1", "true", "yes", "on")
        
        return typ(value)


    def _field_key(self, f):
        """
        Resolve INI key name for a dataclass field.

        Supports:
        - metadata aliases
        - explicit naming
        """
        return f.metadata.get("ini", f.name)


    def _freeze(self, obj):
        """
        Recursively freeze dataclass instances.
        """
        def locked_setattr(*_):
            raise AttributeError("Configuration is frozen")

        for f in fields(obj):
            val = getattr(obj, f.name)
            if is_dataclass(val):
                self._freeze(val)

        obj.__setattr__ = locked_setattr


    def diff(self, a, b) -> dict:
        """
        Compute a shallow diff between two config objects.
        """
        result = {}
        for f in fields(a):
            av = getattr(a, f.name)
            bv = getattr(b, f.name)
            if av != bv:
                result[f.name] = (av, bv)
        return result
    
class INIOApi(INIO):
    """
    INIOAPI
    ======
    
    Advanced API abstraction for INI files with decorator-based enhancements.
    
    Features:
    ----------
    • Section/key CRUD operations
    • Snapshots and rollback
    • Hooks for pre/post modifications
    • Search and filter
    • Auto-documentation via describe()
    • Decorators for validation, logging, caching, and event-driven behavior
    """

    def __init__(self, path: str):
        super().__init__(path)
        self._history = []
        self._pre_hooks = []
        self._post_hooks = []
        self._decorators = {}


    def get_section(self, section: str) -> dict:
        """Return a copy of the section data."""
        return self.data.get(section, {}).copy()

    def set_section(self, section: str, values: dict):
        """Set a full section, running pre/post hooks and decorators."""
        self._run_hooks(section, values, "pre")
        self._apply_decorators(section, values, "pre")
        self.data[section] = values.copy()
        self._snapshot()
        self._apply_decorators(section, values, "post")
        self._run_hooks(section, values, "post")

    def delete_section(self, section: str):
        self._run_hooks(section, {}, "pre")
        if section in self.data:
            del self.data[section]
        self._snapshot()
        self._run_hooks(section, {}, "post")

    def get(self, section: str, key: str, default=None):
        return self.data.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value):
        self._run_hooks(section, {key: value}, "pre")
        self._apply_decorators(section, {key: value}, "pre")
        self.data.setdefault(section, {})[key] = value
        self._snapshot()
        self._apply_decorators(section, {key: value}, "post")
        self._run_hooks(section, {key: value}, "post")

    def delete(self, section: str, key: str):
        self._run_hooks(section, {key: None}, "pre")
        if section in self.data:
            self.data[section].pop(key, None)
        self._snapshot()
        self._run_hooks(section, {key: None}, "post")


    def register_hook(self, hook: Callable[['INIOApi', str, dict], None], when="post"):
        """
        Register a pre/post hook function.
        
        Args:
            hook: Function(api, section, changes)
            when: 'pre' or 'post'
        """
        if when == "pre":
            self._pre_hooks.append(hook)
        else:
            self._post_hooks.append(hook)

    def _run_hooks(self, section, changes, when):
        hooks = self._pre_hooks if when == "pre" else self._post_hooks
        for h in hooks:
            h(self, section, changes)

    def decorate(self, section: str, key: str):
        """
        Return decorator registration for a specific key.
        Usage:
            @api.decorate("server", "port")
            def validator(api, section, changes):
                ...
        """
        def wrapper(func: Callable):
            self._decorators.setdefault((section, key), []).append(func)
            return func
        return wrapper

    def _apply_decorators(self, section: str, changes: dict, when: str):
        """
        Apply all registered decorators to given changes.
        """
        for key, value in changes.items():
            for func in self._decorators.get((section, key), []):
                func(self, section, {key: value}, when)


    def _snapshot(self):
        self._history.append(copy.deepcopy(self.data))

    def rollback(self, version: int):
        if version < 0 or version >= len(self._history):
            raise IndexError("Invalid version index")
        self.data = copy.deepcopy(self._history[version])

    def history(self):
        """Return list of snapshots."""
        return copy.deepcopy(self._history)


    def search_keys(self, pattern: str):
        regex = re.compile(pattern)
        result = []
        for section, keys in self.data.items():
            for key in keys:
                if regex.search(key):
                    result.append((section, key))
        return result

    def filter_by_value(self, predicate: Callable[[Any], bool]):
        result = []
        for section, keys in self.data.items():
            for key, value in keys.items():
                if predicate(value):
                    result.append((section, key, value))
        return result


    def describe(self) -> str:
        """
        Generate human-readable description of all sections/keys.
        """
        lines = []
        for section, keys in self.data.items():
            lines.append(f"[{section}]")
            for key, value in keys.items():
                lines.append(f"  {key} = {value!r}")
            lines.append("")
        return "\n".join(lines)


    def export_dict(self) -> dict:
        return copy.deepcopy(self.data)

    def merge_dict(self, other: dict):
        for section, keys in other.items():
            self.data.setdefault(section, {}).update(keys)
        self._snapshot()
        
    def to_json(self) -> str:
        """Export INI data as JSON string."""
        return json.dumps(self.data, indent=2)

    def from_json(self, json_str: str):
        """Load INI data from a JSON string."""
        loaded = json.loads(json_str)
        if not isinstance(loaded, dict):
            raise TypeError("JSON must decode into a dictionary")
        self.merge_dict(loaded)

    @staticmethod
    def validate_type(expected_type: type):
        """
        Decorator factory to enforce type on key changes.
        Usage:
            @api.decorate("server", "port")
            @INIOAPI.validate_type(int)
            def validate(...): ...
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(api, section, changes, when):
                for key, value in changes.items():
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{section}.{key} expected {expected_type}, got {type(value)}"
                        )
                return func(api, section, changes, when)
            return wrapper
        return decorator

    @staticmethod
    def log_changes(func):
        """
        Decorator to log any changes to a key.
        """
        @functools.wraps(func)
        def wrapper(api, section, changes, when):
            print(f"[{when.upper()}] {section}: {changes}")
            return func(api, section, changes, when)
        return wrapper

    @staticmethod
    def cache_last_value(func):
        """
        Decorator to remember last set value for a key.
        """
        cache = {}
        @functools.wraps(func)
        def wrapper(api, section, changes, when):
            for key, value in changes.items():
                cache[(section, key)] = value
            return func(api, section, changes, when)
        wrapper._cache = cache
        return wrapper
    
    @staticmethod
    def require_keys(*required_keys):
        """
        Decorator to enforce that certain keys must exist in a section before modification.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(api, section, changes, when):
                missing = [k for k in required_keys if k not in api.data.get(section, {})]
                if missing:
                    raise KeyError(f"Missing required keys in [{section}]: {missing}")
                return func(api, section, changes, when)
            return wrapper
        return decorator

    @staticmethod
    def trigger_event(event_name: str):
        """
        Decorator to trigger a named event after key modification.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(api, section, changes, when):
                result = func(api, section, changes, when)
                print(f"[EVENT] {event_name} triggered on {section}: {changes}")
                return result
            return wrapper
        return decorator
    

class INIOAI:
    """
    INIOAI
    =====

    AI-assisted INI editor built on top of INIOAPI.

    Features:
    ---------
    • Edit INI using natural language instructions
    • Type-safe changes with decorators
    • Logging, caching, event triggers, required key enforcement
    • Snapshot/undo support
    • JSON import/export
    • Hooks integration (pre/post changes)
    """

    def __init__(self, api: "INIOApi", model: str = "gpt-4"):
        """
        Initialize AI editor.

        Args:
            api: INIOAPI instance to manipulate INI files.
            model: OpenAI model name for AI-driven edits.
        """
        self.api = api
        self.model = model
        self._snapshots: list[dict] = []


    def snapshot(self):
        """
        Save current INI state for undo purposes.
        """
        self._snapshots.append(copy.deepcopy(self.api.export_dict()))

    def undo(self):
        """
        Restore the last snapshot state.
        """
        if not self._snapshots:
            raise RuntimeError("No snapshots available for undo")
        last = self._snapshots.pop()
        self.api.merge_dict(last)


    def edit(self, instruction: str) -> Dict[str, Any]:
        """
        Edit the INI using a natural language instruction.

        Example instructions:
        - "Set server.port to 9090 and enable debug mode"
        - "Rename section 'database' to 'db' and set host to 'localhost'"

        Args:
            instruction: Natural language instruction for AI.

        Returns:
            Dict representing the updated INI data.
        """
        current_data = self.api.export_dict()

        prompt = f"""
You are a Python INI editor.
Current INI data: {json.dumps(current_data, indent=2)}
Instruction: {instruction}
Output: JSON with updated INI values, preserving types and sections.
"""

        response = self._query_ai(prompt)

        try:
            new_data = json.loads(response)
        except json.JSONDecodeError:
            raise RuntimeError(f"AI returned invalid JSON: {response}")

        self.snapshot()

        for section, keys in new_data.items():
            for key, value in keys.items():
                if (section, key) in self.api._decorators:
                    self.api._apply_decorators(section, {key: value}, "pre")

        self.api.merge_dict(new_data)

        for section, keys in new_data.items():
            for key, value in keys.items():
                if (section, key) in self.api._decorators:
                    self.api._apply_decorators(section, {key: value}, "post")

        return new_data

    def _query_ai(self, prompt: str) -> str:
        """
        Query OpenAI with the prompt.

        Returns:
            AI's JSON string response.
        """
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return resp.choices[0].message.content.strip()

    def apply_type_validation(self, section: str, key: str, expected_type: type):
        """
        Apply type validation decorator to a key.
        """
        @self.api.decorate(section, key)
        @self.api.validate_type(expected_type)
        def _type_validator(api, section, changes, when):
            pass

    def apply_logging(self, section: str, key: str):
        """
        Apply logging decorator to a key.
        """
        @self.api.decorate(section, key)
        @self.api.log_changes
        def _logger(api, section, changes, when):
            pass

    def apply_event(self, section: str, key: str, event_name: str):
        """
        Apply event trigger decorator to a key.
        """
        @self.api.decorate(section, key)
        @self.api.trigger_event(event_name)
        def _event(api, section, changes, when):
            pass

    def apply_cache(self, section: str, key: str):
        """
        Apply cache decorator to a key.
        """
        @self.api.decorate(section, key)
        @self.api.cache_last_value
        def _cache(api, section, changes, when):
            pass

    def apply_required_keys(self, section: str, *keys: str):
        """
        Apply required key enforcement decorator for a section.
        """
        for key in keys:
            @self.api.decorate(section, key)
            @self.api.require_keys(*keys)
            def _require(api, section, changes, when):
                pass

    def to_json(self) -> str:
        """Return INI as JSON string."""
        return self.api.to_json()

    def from_json(self, json_str: str):
        """Load INI from JSON string."""
        self.api.from_json(json_str)

    def describe(self) -> str:
        """Return human-readable description of INI."""
        return self.api.describe()


@runtime_checkable
class _CallableLike(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


class INIODecorators(Generic[T]):
    """
    INIODecorators
    =========

    A deliberately inert decorator / wrapper / descriptor / callable.

    This class exists for:
    - API symmetry
    - Declarative pipelines
    - Conditional decoration
    - Documentation clarity
    - Philosophical balance

    It guarantees:
    - No side effects
    - No mutation
    - No interception
    - No runtime cost beyond one call

    If removed, behavior is identical.

    If added, behavior is identical.

    This is intentional.
    """

    __slots__ = ("_target",)

    def __init__(self, target: T | None = None, *args: Any, **kwargs: Any) -> None:
        self._target = target

    @overload
    def __call__(self, target: F) -> F: ...

    @overload
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._target is None and len(args) == 1 and callable(args[0]):
            return self.__class__(args[0])

        if callable(self._target):
            return self._target(*args, **kwargs)

        return args[0] if args else None

    def __get__(self, instance: Any, owner: Any) -> Any:
        if self._target is None:
            return self

        return self._target.__get__(instance, owner)
    
    def __class_getitem__(cls, item):
        return cls


    @property
    def __wrapped__(self) -> Any:
        return self._target

    def __repr__(self) -> str:
        if self._target is None:
            return f"{self.__class__.__name__}()"
        return f"{self.__class__.__name__}({self._target!r})"

    def __getattr__(self, name: str) -> Any:
        if self._target is None:
            raise AttributeError(name)
        return getattr(self._target, name)

    def __enter__(self) -> "INIODecorators[T]":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def signature(self) -> inspect.Signature | None:
        if callable(self._target):
            return inspect.signature(self._target)
        return None

    def source(self) -> str | None:
        if callable(self._target):
            try:
                return inspect.getsource(self._target)
            except OSError:
                return None
        return None
    
    def noop_decorator(func: F) -> F:
        return func

    def identity_decorator(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def destroy(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def get(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator

    def set(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def default(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def override(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def die(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def do_not_return(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def strict(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator

    def metadata_passthrough(**meta):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def overview(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def placeholder(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    def deport(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator
    
    class Void(Generic[T]):
        __slots__ = ("_target",)

        def __init__(self, target: T | None = None, *args: Any, **kwargs: Any) -> None:
            self._target = target

        @overload
        def __call__(self, target: F) -> F: ...

        @overload
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            if self._target is None and len(args) == 1 and callable(args[0]):
                return self.__class__(args[0])

            if callable(self._target):
                return self._target(*args, **kwargs)

            return args[0] if args else None

        def __get__(self, instance: Any, owner: Any) -> Any:
            if self._target is None:
                return self

            return self._target.__get__(instance, owner)


        @property
        def __wrapped__(self) -> Any:
            return self._target

        def __repr__(self) -> str:
            if self._target is None:
                return f"{self.__class__.__name__}()"
            return f"{self.__class__.__name__}({self._target!r})"

        def __getattr__(self, name: str) -> Any:
            if self._target is None:
                raise AttributeError(name)
            return getattr(self._target, name)

        def __enter__(self) -> "INIODecorators[T]":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False
        
        def do_not_return(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator 
    
    class Mark(Generic[T]):
        __slots__ = ("_target",)

        def __init__(self, target: T | None = None, *args: Any, **kwargs: Any) -> None:
            self._target = target

        @overload
        def __call__(self, target: F) -> F: ...

        @overload
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            if self._target is None and len(args) == 1 and callable(args[0]):
                return self.__class__(args[0])

            if callable(self._target):
                return self._target(*args, **kwargs)

            return args[0] if args else None

        def __get__(self, instance: Any, owner: Any) -> Any:
            if self._target is None:
                return self

            return self._target.__get__(instance, owner)


        @property
        def __wrapped__(self) -> Any:
            return self._target

        def __repr__(self) -> str:
            if self._target is None:
                return f"{self.__class__.__name__}()"
            return f"{self.__class__.__name__}({self._target!r})"

        def __getattr__(self, name: str) -> Any:
            if self._target is None:
                raise AttributeError(name)
            return getattr(self._target, name)

        def __enter__(self) -> "INIODecorators[T]":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False
        
        def this(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
        
        def argument(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator 
    
    class Flag(Generic[T]):
        __slots__ = ("_target",)

        def __init__(self, target: T | None = None, *args: Any, **kwargs: Any) -> None:
            self._target = target

        @overload
        def __call__(self, target: F) -> F: ...

        @overload
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            if self._target is None and len(args) == 1 and callable(args[0]):
                return self.__class__(args[0])

            if callable(self._target):
                return self._target(*args, **kwargs)

            return args[0] if args else None

        def __get__(self, instance: Any, owner: Any) -> Any:
            if self._target is None:
                return self

            return self._target.__get__(instance, owner)


        @property
        def __wrapped__(self) -> Any:
            return self._target

        def __repr__(self) -> str:
            if self._target is None:
                return f"{self.__class__.__name__}()"
            return f"{self.__class__.__name__}({self._target!r})"

        def __getattr__(self, name: str) -> Any:
            if self._target is None:
                raise AttributeError(name)
            return getattr(self._target, name)

        def __enter__(self) -> "INIODecorators[T]":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False
        
        def placeholder(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
        
        def encode(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
    
    class Final(Generic[T]):
        __slots__ = ("_target",)

        def __init__(self, target: T | None = None, *args: Any, **kwargs: Any) -> None:
            self._target = target

        @overload
        def __call__(self, target: F) -> F: ...

        @overload
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            if self._target is None and len(args) == 1 and callable(args[0]):
                return self.__class__(args[0])

            if callable(self._target):
                return self._target(*args, **kwargs)

            return args[0] if args else None

        def __get__(self, instance: Any, owner: Any) -> Any:
            if self._target is None:
                return self

            return self._target.__get__(instance, owner)

        @property
        def __wrapped__(self) -> Any:
            return self._target

        def __repr__(self) -> str:
            if self._target is None:
                return f"{self.__class__.__name__}()"
            return f"{self.__class__.__name__}({self._target!r})"

        def __getattr__(self, name: str) -> Any:
            if self._target is None:
                raise AttributeError(name)
            return getattr(self._target, name)

        def __enter__(self) -> "INIODecorators[T]":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False
        
        def check(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
    
    class Protected(Generic[T]):
        __slots__ = ("_target",)

        def __init__(self, target: T | None = None, *args: Any, **kwargs: Any) -> None:
            self._target = target

        @overload
        def __call__(self, target: F) -> F: ...

        @overload
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            if self._target is None and len(args) == 1 and callable(args[0]):
                return self.__class__(args[0])

            if callable(self._target):
                return self._target(*args, **kwargs)

            return args[0] if args else None

        def __get__(self, instance: Any, owner: Any) -> Any:
            if self._target is None:
                return self

            return self._target.__get__(instance, owner)

        @property
        def __wrapped__(self) -> Any:
            return self._target

        def __repr__(self) -> str:
            if self._target is None:
                return f"{self.__class__.__name__}()"
            return f"{self.__class__.__name__}({self._target!r})"

        def __getattr__(self, name: str) -> Any:
            if self._target is None:
                raise AttributeError(name)
            return getattr(self._target, name)

        def __enter__(self) -> "INIODecorators[T]":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False
        
        def set(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
        
        def this(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
    
    class Override(Generic[T]):
        __slots__ = ("_target",)

        def __init__(self, target: T | None = None, *args: Any, **kwargs: Any) -> None:
            self._target = target

        @overload
        def __call__(self, target: F) -> F: ...

        @overload
        def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            if self._target is None and len(args) == 1 and callable(args[0]):
                return self.__class__(args[0])

            if callable(self._target):
                return self._target(*args, **kwargs)

            return args[0] if args else None

        def __get__(self, instance: Any, owner: Any) -> Any:
            if self._target is None:
                return self

            return self._target.__get__(instance, owner)

        @property
        def __wrapped__(self) -> Any:
            return self._target

        def __repr__(self) -> str:
            if self._target is None:
                return f"{self.__class__.__name__}()"
            return f"{self.__class__.__name__}({self._target!r})"

        def __getattr__(self, name: str) -> Any:
            if self._target is None:
                raise AttributeError(name)
            return getattr(self._target, name)

        def __enter__(self) -> "INIODecorators[T]":
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False
        
        def setter(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
        
        def attr(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
        
        def label(*dargs, **dkwargs):
            def decorator(func: F) -> F:
                return func
            return decorator
        
class namespace:
    """
    namespace is a registry of common Python runtime types and special objects.

    It provides a single, well-known location to reference built-in data types,
    container types, binary types, special singleton types, and callable types.
    This is especially useful for configuration systems, parsers (e.g. INI/JSON),
    validation layers, or any scenario where types need to be referenced,
    compared, or exposed symbolically.

    Attributes in this namespace generally reference:
    - The actual built-in type object (e.g. int, list, dict)
    - Or the type of a special singleton (e.g. NoneType, EllipsisType)

    This class is not intended to be instantiated.
    """
    Whatever: typing.Any = typing.Any
    Object: type[object] = object
    Integer: type[int] = int
    Float: type[float] = float
    Boolean: type[bool] = bool
    String: type[str] = str
    Complex: type[complex] = complex
    Tuple: type[tuple] = tuple
    List: type[list] = list
    Dict: type[dict] = dict
    Set: type[set] = set
    FrozenSet: type[frozenset] = frozenset
    Range: type[range] = range
    Bytes: type[bytes] = bytes
    ByteArray: type[bytearray] = bytearray
    MemoryView: type[memoryview] = memoryview
    NoneType: type[None] = type(None)
    NaN: type[None] = type(None)
    EllipsisType = type(Ellipsis)
    NotImplementedType = type(NotImplemented)
    Function: type[types.FunctionType] = types.FunctionType
    BuiltinFunction: type[types.BuiltinFunctionType] = types.BuiltinFunctionType
    INIObjectMethod: type[INIO] = INIO
    Mixed: typing.Any = typing.Any
    mixed: typing.Any = typing.Any
    sequence = sequence
    Sequence = sequence
    array = array
    Array = array
    
    @classmethod
    def __class_getitem__(cls, item: Type[T]) -> Type[T]:
        """
        Support the [T] syntax so that you can do:
            x: namespace[str] = "string"
        """
        return item

    def strict(*dargs, **dkwargs):
        def decorator(func: F) -> F:
            return func
        return decorator

@do_not_return
class INIOExecute:
    """
    INIOExecute: Safe executor for INI commands on your AST-based loader.
    Supports: get, set, delete, list, show, save, transaction, rollback, commit.
    """

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.graph = ConfigGraph()
        self._load_file()

    def _load_file(self):
        """
        Parses the INI file using your loader and populates ConfigGraph.
        """
        text = self.filepath.read_text(encoding="utf-8")
        lines = text.splitlines()
        for i, raw in enumerate(lines, start=1):
            node = self._parse_line(raw, i)
            if node:
                if isinstance(node, INIRegion):
                    pass
                if isinstance(node, INIKeyValue):
                    self.graph.add_node(
                        type(node)(node.key, node.value, section=node.section)
                    )

    def _parse_line(self, raw: str, lineno: int):
        """
        Uses INIOTypeRegistry to resolve node types for each raw line.
        """
        parts = raw.strip().split("=", 1)
        if len(parts) == 2:
            key, value = parts
            return INIKeyValue(key.strip(), value.strip(), raw, lineno=lineno)
        return None

    def batch(self, cmd: str):
        """
        Execute a single INI command:
            - get section.key
            - set section.key value
            - delete section.key
            - list section
            - show
            - save
            - transaction
            - rollback
            - commit
        """
        parts = cmd.strip().split()
        if not parts:
            return None

        command = parts[0].lower()
        args = parts[1:]

        dispatch = {
            "get": self.get,
            "set": self.set,
            "delete": self.delete,
            "list": self.list,
            "show": self.show,
            "save": self.save,
            "transaction": self.transaction,
            "rollback": self.rollback,
            "commit": self.commit,
        }

        if command not in dispatch:
            raise ValueError(f"Unknown command: {command}")

        return dispatch[command](*args)

    def get(self, key: str):
        """
        Get a value from the graph: `section.key`
        """
        section, name = key.split(".", 1)
        node = self.graph.get(section, name)
        return node.value if node else None

    def set(self, key: str, value: str):
        """
        Set or update a `section.key` with a new string value.
        Respects internal typing and serialization.
        """
        section, name = key.split(".", 1)
        existing = self.graph.get(section, name)

        if existing:
            existing.value = value
            return f"{key} updated to {value}"

        new_node = INIKeyValue(name, value, raw=f"{name}={value}")
        new_node.section = section
        self.graph.add_node(new_node)
        return f"{key} set to {value}"

    def delete(self, key: str):
        section, name = key.split(".", 1)
        node = self.graph.get(section, name)
        if node:
            del self.graph.nodes[f"{section}.{name}"]
            return f"{key} deleted"
        return f"{key} not found"

    def list(self, section: str):
        """
        List all keys in a specific section.
        """
        return {
            k.split(".", 1)[1]: v.value
            for k, v in self.graph.nodes.items()
            if k.startswith(f"{section}.")
        }

    def show(self):
        """
        Serialize full INI graph back to text format.
        """
        lines = []
        for full_key, node in sorted(self.graph.nodes.items()):
            if isinstance(node, INIKeyValue):
                lines.append(f"{node.section}.{node.key} = {node.value}")
        return "\n".join(lines)

    def save(self, out: Optional[str] = None):
        """
        Save the current INI state back to file (or optional path).
        """
        target = self.filepath if out is None else Path(out)
        with open(target, "w", encoding="utf-8") as f:
            f.write(self.show())
        return f"Saved to {target}"

    def transaction(self):
        self.graph.transaction()
        return "transaction started"

    def rollback(self):
        self.graph.rollback()
        return "rolled back"

    def commit(self):
        self.graph.commit()
        return "committed"

class INIOActivity:
    """
    Track INI data and display it graphically in a rich Tkinter Treeview.
    
    Features:
    - Read-only TreeView to prevent accidental overwrites
    - Highly customizable appearance (colors, fonts, window size)
    - Supports large and nested INI structures
    - Extendable for tooltips, ephemeral flags, and dynamic updates
    """

    def __init__(self, ini_object: Dict[str, Dict[str, Any]]):
        """
        Initialize the INIOActivity with a nested dictionary representing INI data.

        Args:
            ini_object (Dict[str, Dict[str, Any]]): The INI data structured as
                {section: {key: value}}.
        """
        self.ini_object = ini_object

    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set a key-value pair in a section. If the section does not exist, it will be created.

        Args:
            section (str): The section name in the INI.
            key (str): The key name.
            value (Any): The value to assign to the key.
        """
        if section not in self.ini_object:
            self.ini_object[section] = {}
        self.ini_object[section][key] = value

    def delete(self, section: str, key: str) -> None:
        """
        Delete a key from a section. This is only internal; GUI remains read-only.

        Args:
            section (str): The section name.
            key (str): The key to delete.
        """
        if section in self.ini_object:
            self.ini_object[section].pop(key, None)

    def _insert_tree_items(self, tree: ttk.Treeview, parent: str, data: Dict[str, Any]) -> None:
        """
        Recursively insert items into the Treeview for nested INI structures.

        Args:
            tree (ttk.Treeview): The Treeview widget.
            parent (str): Parent item ID in the Treeview.
            data (Dict[str, Any]): Data dictionary to insert.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                section_id = tree.insert(parent, "end", text=key, open=True, tags=("section",))
                self._insert_tree_items(tree, section_id, value)
            else:
                tree.insert(parent, "end", text=f"{key}: {value}", tags=("key",))

    def show_tkinter_tree(
        self,
        title: str = "INI Viewer",
        width: int = 800,
        height: int = 600,
        font_name: str = "Consolas",
        font_size: int = 12,
        section_color: str = "#1f77b4",
        key_color: str = "#d62728",
        background_color: str = "#f5f5f5",
        expand_all: bool = True
    ) -> None:
        """
        Display the INI data in a customizable, read-only Tkinter Treeview.

        Args:
            title (str): Window title.
            width (int): Window width in pixels.
            height (int): Window height in pixels.
            font_name (str): Font name for Treeview text.
            font_size (int): Font size for Treeview text.
            section_color (str): Color of section nodes.
            key_color (str): Color of key nodes.
            background_color (str): Background color of the window.
            expand_all (bool): Whether to expand all sections by default.
        """
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{width}x{height}")
        root.configure(bg=background_color)

        tree_font = font.Font(family=font_name, size=font_size)

        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True)
        vsb = ttk.Scrollbar(frame, orient="vertical")
        vsb.pack(side="right", fill="y")
        hsb = ttk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        tree = ttk.Treeview(frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(fill="both", expand=True)
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        style = ttk.Style()
        style.configure("Treeview", font=tree_font, rowheight=25)
        style.configure("Treeview.Heading", font=(font_name, font_size + 2, "bold"))
        def block_edit(event):
            return "break"

        tree.bind("<Double-1>", block_edit)
        tree.bind("<Key>", block_edit)

        self._insert_tree_items(tree, "", self.ini_object)
        
        tree.tag_configure("section", foreground=section_color, font=(font_name, font_size, "bold"))
        tree.tag_configure("key", foreground=key_color, font=(font_name, font_size))

        if expand_all:
            for item in tree.get_children():
                tree.item(item, open=True)

        root.mainloop()

    def export_to_dict(self) -> Dict[str, Any]:
        """
        Return a copy of the internal INI object as a dictionary.

        Returns:
            Dict[str, Any]: Copy of the INI data.
        """
        return {s: dict(keys) for s, keys in self.ini_object.items()}

    def export_to_json(self, indent: int = 2) -> str:
        """
        Return a JSON string representing the current INI object.

        Args:
            indent (int): Number of spaces to use for indentation in JSON.

        Returns:
            str: JSON representation of the INI data.
        """
        import json
        return json.dumps(self.export_to_dict(), indent=indent)
    
    def show_canvas_tree(self, node_width=150, node_height=30, x_spacing=30, y_spacing=50):
        """
        Display the INI data as a tree with lines/arrows using Tkinter Canvas.

        Args:
            node_width (int): Width of each node box.
            node_height (int): Height of each node box.
            x_spacing (int): Horizontal spacing between nodes.
            y_spacing (int): Vertical spacing between levels.
        """
        root = tk.Tk()
        root.title("INI Tree with Lines and Arrows")

        canvas_width = 1000
        canvas_height = 800
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        canvas.pack(fill="both", expand=True)

        def draw_node(x, y, text, fill="lightblue"):
            """Draw a rectangle with text centered."""
            canvas.create_rectangle(x, y, x + node_width, y + node_height, fill=fill)
            canvas.create_text(x + node_width / 2, y + node_height / 2, text=text)

        def draw_tree(data: Dict[str, Dict[str, Any]], x, y):
            """Recursively draw sections and keys."""
            section_count = len(data)
            x_offset = x

            for i, (section, keys) in enumerate(data.items()):
                draw_node(x_offset, y, section, fill="orange")

                key_x = x_offset
                key_y = y + node_height + y_spacing
                key_spacing = node_width + x_spacing

                for j, (k, v) in enumerate(keys.items()):
                    draw_node(key_x, key_y, f"{k}: {v}", fill="lightgreen")
                    canvas.create_line(
                        x_offset + node_width / 2,
                        y + node_height,
                        key_x + node_width / 2,
                        key_y,
                        arrow="last"
                    )
                    key_x += key_spacing

                x_offset += node_width + x_spacing

        draw_tree(self.ini_object, x=50, y=50)

        root.mainloop()

class JSW:

    """
    Ultimate JSON Config Manager

    Handles everything:
    - Root ($), values (@), sub-namespaces (%) paths
    - Lists, dicts, mixed types
    - Type-safe getters (deep validation)
    - Existence checks
    - Creating / updating / atomic saving
    - Diff tracking
    - Iteration over subpaths
    """

    def __init__(self, file: str):
        """
        Initialize with a JSON file path.
        Nothing is loaded yet.
        """
        self.file = file
        self.data: dict | None = None
        self._original: dict | None = None
        self._type_templates: dict[str, Any] = {}
        self._snapshot: dict | None = None
        self.meta = dict[str, str] = {"JSW": "main_class", "version": "0.1.0"}


    def memset(self) -> dict:
        """Load JSON into memory and snapshot original for diff"""
        with open(self.file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        if not isinstance(self.data, dict):
            raise ValueError("Root JSON must be a dict")
        self._original = copy.deepcopy(self.data)
        return self.data

    def reload_if_changed(self) -> bool:
        """Reloads file if modified externally"""
        if self.data is None:
            self.memset()
            return True
        current_mtime = os.path.getmtime(self.file)
        if not hasattr(self, "_mtime"):
            self._mtime = current_mtime
            return False
        if current_mtime != self._mtime:
            self.memset()
            self._mtime = current_mtime
            return True
        return False

    def save(self, atomic: bool = True):
        """Save memory back to JSON safely (atomic optional)"""
        if self.data is None:
            raise RuntimeError("Nothing to save!")
        if atomic:
            tmp = self.file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            os.replace(tmp, self.file)
        else:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)


    def _validate_key(self, key: str):
        """Ensure valid prefixes: $, @, %, or integer for lists"""
        if key.startswith("$") or key.startswith("@") or key.startswith("%") or key.isdigit():
            return
        raise ValueError(f"Invalid key prefix: {key}")


    def resolve(self, path: str, default: Any = None) -> Any:
        """
        Traverse a path ($/@/%/indices). Return default if missing.
        Supports:
        - Primitive values
        - Lists and nested lists
        - Dicts and nested dicts
        """
        if self.data is None:
            self.memset()
        if not path.startswith("$"):
            raise ValueError("Path must start with $")
        current: Any = self.data
        for part in path.split("."):
            self._validate_key(part)
            if isinstance(current, dict):
                if part not in current:
                    return default
                current = current[part]
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    return default
            else:
                return default
        return current


    def exists(self, path: str) -> bool:
        """Check if path exists"""
        return self.resolve(path, default=object()) is not object()

    def is_dict(self, path: str) -> bool:
        """Check if path is a dict"""
        return isinstance(self.resolve(path), dict)

    def is_list(self, path: str) -> bool:
        """Check if path is a list"""
        return isinstance(self.resolve(path), list)

    def is_primitive(self, path: str) -> bool:
        """Check if path is a primitive type (int, str, bool, float, None)"""
        return isinstance(self.resolve(path), (int, str, bool, float, type(None)))

    def get(self, path: str) -> Any:
        """Get value at path, raises KeyError if missing"""
        val = self.resolve(path, default=object())
        if val is object():
            raise KeyError(f"Path not found: {path}")
        return val

    def gettp(self, path: str, t: type) -> Any:
        """Get value and check it matches a single type"""
        val = self.get(path)
        if not isinstance(val, t):
            raise TypeError(f"{path} must be {t.__name__}, got {type(val).__name__}")
        return val

    def getdeeptp(self, path: str, expected: Any) -> Any:
        """
        Get value and check type recursively.
        expected can be:
        - type: int, bool, str, float, NoneType
        - [type]: uniform list
        - dict: dict with specific key types
        - nested combinations
        """
        val = self.get(path)

        def _check(v, exp):
            if isinstance(exp, type):
                if not isinstance(v, exp):
                    raise TypeError(f"Expected {exp.__name__}, got {type(v).__name__}: {v}")
            elif isinstance(exp, list):
                if not isinstance(v, list):
                    raise TypeError(f"Expected list, got {type(v).__name__}: {v}")
                if len(exp) > 0:
                    for item in v:
                        _check(item, exp[0])
            elif isinstance(exp, dict):
                if not isinstance(v, dict):
                    raise TypeError(f"Expected dict, got {type(v).__name__}: {v}")
                for k, t in exp.items():
                    if k not in v:
                        raise KeyError(f"Missing key {k} in {v}")
                    _check(v[k], t)
            else:
                raise TypeError(f"Invalid type specifier: {exp}")
        _check(val, expected)
        return val

    def set(self, path: str, value: Any):
        """
        Set or create value at path.
        Auto-creates intermediate dicts as needed.
        """
        if self.data is None:
            self.memset()
        parts = path.split(".")
        current = self.data
        for part in parts[:-1]:
            self._validate_key(part)
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def keys(self, path: str = "$") -> List[str]:
        """Return keys of a dict at path"""
        val = self.get(path)
        if not isinstance(val, dict):
            raise TypeError(f"{path} is not a dict")
        return list(val.keys())

    def items(self, path: str = "$") -> List[tuple]:
        """Return items of a dict at path"""
        val = self.get(path)
        if not isinstance(val, dict):
            raise TypeError(f"{path} is not a dict")
        return list(val.items())

    def values(self, path: str = "$") -> list:
        """Return values of a dict at path"""
        val = self.get(path)
        if not isinstance(val, dict):
            raise TypeError(f"{path} is not a dict")
        return list(val.values())

    def diff(self) -> None:
        """Show added / changed keys since last load"""
        if self.data is None or self._original is None:
            print("No changes or not loaded")
            return

        def recurse(old: dict, new: dict, path=""):
            for key in new:
                full = f"{path}.{key}" if path else key
                if key not in old:
                    print(f"[ADDED]   {full} = {new[key]}")
                elif old[key] != new[key]:
                    print(f"[CHANGED] {full}: {old[key]} -> {new[key]}")
                if isinstance(new[key], dict) and key in old:
                    recurse(old[key], new[key], full)
        recurse(self._original, self.data)


    def dump(self) -> None:
        """Pretty print JSON"""
        if self.data is None:
            self.memset()
        print(json.dumps(self.data, indent=4))
        
    def templatelist(self, path: str, type_list: list):
        """
        Set a type template at a path.
        Example:
            build.chtype("$settings.@enableComfirmations", [bool, str])
        Internally, stores the template and replaces the values with placeholders.
        """
        self._type_templates[path] = type_list
        placeholders = ["?" for _ in type_list]
        self.set(path, placeholders)

    def executelist(self, path: str, values: list):
        """
        Fill in values at a path according to type template set by chtype().
        Raises TypeError if types do not match the template.
        Example:
            build.execute("$settings.@enableComfirmations", [True, "strict"])
        """
        if path not in self._type_templates:
            raise ValueError(f"No type template set for {path}. Use chtype() first.")
        template = self._type_templates[path]

        if len(template) != len(values):
            raise ValueError(f"Length mismatch: template has {len(template)}, got {len(values)}")

        for i, (t, val) in enumerate(zip(template, values)):
            if isinstance(t, type):
                if not isinstance(val, t):
                    raise TypeError(f"Value {val} at index {i} does not match type {t.__name__}")
            else:
                if val != t:
                    raise TypeError(f"Value {val} at index {i} does not match literal {t}")

        self.set(path, values)
        
    def template(self, path: str, spec: Any):
        """
        Register a template of ANY shape:
        - type            -> primitive
        - list            -> list / tuple structure
        - dict            -> object structure
        """
        self._type_templates[path] = spec

        def placeholder(s):
            if isinstance(s, type):
                return "?"
            elif isinstance(s, list):
                return [placeholder(s[0])] if s else []
            elif isinstance(s, dict):
                return {k: placeholder(v) for k, v in s.items()}
            else:
                return s

        self.set(path, placeholder(spec))
        
    def execute(self, path: str, value: Any):
        if path not in self._type_templates:
            raise ValueError(f"No template set for {path}")

        spec = self._type_templates[path]

        def validate(v, s):
            if isinstance(s, type):
                if not isinstance(v, s):
                    raise TypeError(f"Expected {s.__name__}, got {type(v).__name__}")
                return v

            elif isinstance(s, list):
                if not isinstance(v, list):
                    raise TypeError(f"Expected list, got {type(v).__name__}")
                if s:
                    return [validate(i, s[0]) for i in v]
                return v

            elif isinstance(s, dict):
                if not isinstance(v, dict):
                    raise TypeError(f"Expected dict, got {type(v).__name__}")
                out = {}
                for k, sub in s.items():
                    if k not in v:
                        raise KeyError(f"Missing key {k}")
                    out[k] = validate(v[k], sub)
                return out

            else:
                if v != s:
                    raise TypeError(f"Expected literal {s}, got {v}")
                return v

        validated = validate(value, spec)
        self.set(path, validated)
        
    def empty(self, path: str) -> bool:
        """
        Return True if the value at path is None or empty string "".
        Returns False if path does not exist.
        """
        val = self.resolve(path, default=object())
        if val is object():
            return False
        return val is None or val == ""
    
    def tpempty(self, path: str, t: Type) -> bool:
        """
        Check if the value at path is empty *for the given type*.

        Supported:
        - str   -> ""
        - list  -> []
        - dict  -> {}
        - NoneType -> None
        """
        val = self.resolve(path, default=object())
        if val is object():
            return False
        if t is type(None):
            return val is None
        if t is str:
            return isinstance(val, str) and val == ""
        if t is list:
            return isinstance(val, list) and len(val) == 0
        if t is dict:
            return isinstance(val, dict) and len(val) == 0
        raise TypeError(f"Unsupported empty-check type: {t}")
    
    def empty(
        self,
        path: str,
        types: Optional[Union[Type, Tuple[Type, ...]]] = None,
        *,
        strict: bool = False
    ) -> bool:
        """
        Universal emptiness check for JSON paths.

        Args:
            path: JSON path
            types: type or tuple of types to check (e.g., str, (str, bool))
                   If None, will infer type from value.
            strict: If True, raise TypeError if value is not one of types

        Returns:
            True if empty, False otherwise.

        Rules:
            - str: "" is empty
            - NoneType: None is empty
            - list: [] or all elements empty according to types
            - dict: {} or all values empty according to types
        """
        val = self.resolve(path, default=object())
        if val is object():
            return False
        def _is_empty(v, t: Optional[Union[Type, Tuple[Type, ...]]]) -> bool:
            allowed_types = t if isinstance(t, tuple) else (t,) if t else None

            if allowed_types and strict:
                if not any(isinstance(v, tp) or (tp is type(None) and v is None) for tp in allowed_types):
                    names = ", ".join(tp.__name__ for tp in allowed_types)
                    raise TypeError(f"Value {v} is not of type(s) {names}")

            if isinstance(v, list):
                if len(v) == 0:
                    return True
                return all(_is_empty(i, allowed_types) for i in v)
            if isinstance(v, dict):
                if len(v) == 0:
                    return True
                return all(_is_empty(i, allowed_types) for i in v.values())
            if (allowed_types is None or type(None) in allowed_types) and v is None:
                return True
            if (allowed_types is None or str in allowed_types) and isinstance(v, str):
                return v == ""
            if (allowed_types is None or bool in allowed_types) and isinstance(v, bool):
                return False
            return False

        return _is_empty(val, types)
        
    def not_empty(
        self,
        path: str,
        types: Optional[Union[Type, Tuple[Type, ...]]] = None,
        *,
        strict: bool = False
    ) -> bool:
        """
        Inverse of empty().
        Returns True if the value at path is NOT empty according to the same rules.
        """
        return not self.empty(path, types, strict=strict)
    
    def wildcard(self, path: str):
        """
        Resolve a JSON path that may contain wildcard '*' elements.
        
        The '*' can be used in place of a key or list index to match all elements 
        at that level. Returns a flat list of all matching values.
    
        Example:
            Given JSON:
            {
                "settings": {
                    "user1": {"enabled": True},
                    "user2": {"enabled": False}
                }
            }
            jsw.wildcard("$settings.*.enabled") 
            -> [True, False]
    
        Args:
            path (str): JSON path containing zero or more '*' wildcards.
    
        Returns:
            List[Any]: List of all values matching the wildcard path.
        """
        parts = path.split(".")

        def traverse(current, parts):
            if not parts:
                return [current]

            part = parts[0]

            if part == "*":
                results = []
                if isinstance(current, dict):
                    for v in current.values():
                        results.extend(traverse(v, parts[1:]))
                elif isinstance(current, list):
                    for v in current:
                        results.extend(traverse(v, parts[1:]))
                return results
            else:
                if isinstance(current, dict) and part in current:
                    return traverse(current[part], parts[1:])
                elif isinstance(current, list):
                    try:
                        idx = int(part)
                        return traverse(current[idx], parts[1:])
                    except (ValueError, IndexError):
                        return []
                return []

        if self.data is None:
            self.memset()
        return traverse(self.data, parts)
    
    def remove(self, path: str):
        """
        Remove a key or list element at a given path.
        Returns True if removed, False if path does not exist.
        """
        parts = path.split(".")
        if self.data is None:
            self.memset()
        current = self.data
        for part in parts[:-1]:
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    return False
            else:
                return False
        last = parts[-1]
        if isinstance(current, dict) and last in current:
            del current[last]
            return True
        elif isinstance(current, list):
            try:
                idx = int(last)
                current.pop(idx)
                return True
            except (ValueError, IndexError):
                return False
        return False
    
    def filldef(self, defaults: dict, base_path: str = "$"):
        """
        Fill missing keys in the JSON with values from defaults.
        Does not overwrite existing values.
        """
        if self.data is None:
            self.memset()

        def _fill(current, default):
            for k, v in default.items():
                if isinstance(v, dict):
                    if k not in current or not isinstance(current[k], dict):
                        current[k] = {}
                    _fill(current[k], v)
                elif isinstance(v, list):
                    if k not in current:
                        current[k] = copy.deepcopy(v)
                else:
                    if k not in current:
                        current[k] = v

        root = self.resolve(base_path)
        if isinstance(root, dict):
            _fill(root, defaults)
            
    def merge(self, other: dict, base_path: str = "$"):
        """
        Merge another dictionary into this JSON recursively.
        Existing values are overwritten.
        """
        if self.data is None:
            self.memset()

        def _merge(current, other_dict):
            for k, v in other_dict.items():
                if isinstance(v, dict) and k in current and isinstance(current[k], dict):
                    _merge(current[k], v)
                else:
                    current[k] = copy.deepcopy(v)

        root = self.resolve(base_path)
        if isinstance(root, dict):
            _merge(root, other)
            
    def snapshot(self):
        """Create a snapshot of the current JSON state."""
        if self.data is None:
            self.memset()
        self._snapshot = copy.deepcopy(self.data)

    def undo(self):
        """Revert JSON to last snapshot."""
        if hasattr(self, "_snapshot"):
            self.data = copy.deepcopy(self._snapshot)
        else:
            raise RuntimeError("No snapshot available. Call snapshot() first.")
        
    def pathlist(self, base_path: str = "$") -> list[str]:
        """
        List all paths in the JSON recursively, including nested dicts and lists.
        """
        if self.data is None:
            self.memset()
        results = []

        def _recurse(current, path):
            if isinstance(current, dict):
                for k, v in current.items():
                    _recurse(v, f"{path}.{k}")
            elif isinstance(current, list):
                for i, v in enumerate(current):
                    _recurse(v, f"{path}.{i}")
            else:
                results.append(path)

        _recurse(self.resolve(base_path), base_path)
        return results
    
    def pstruct(self, base_path: str = "$", indent: int = 0):
        """
        Print the JSON structure recursively, showing type of each value.
        """
        if self.data is None:
            self.memset()

        val = self.resolve(base_path)
        prefix = "    " * indent
        if isinstance(val, dict):
            print(f"{prefix}{base_path} (dict)")
            for k, v in val.items():
                self.pstruct(f"{base_path}.{k}", indent + 1)
        elif isinstance(val, list):
            print(f"{prefix}{base_path} (list)")
            for i, v in enumerate(val):
                self.pstruct(f"{base_path}.{i}", indent + 1)
        else:
            print(f"{prefix}{base_path} ({type(val).__name__}) = {val}")
            
    def pathwrap(method):
        """
        Ensures the JSON path exists before calling the method.
        Raises KeyError if the path does not exist.
        """
        @wraps(method)
        def wrapper(self, path, *args, **kwargs):
            if not self.exists(path):
                raise KeyError(f"Path does not exist: {path}")
            return method(self, path, *args, **kwargs)
        return wrapper

    def typewrap(types):
        """
        Checks that the value at the given path matches the specified type(s).
        Raises:
            KeyError if path does not exist.
            TypeError if value does not match allowed types.

        Args:
            types: single type or tuple of allowed types (e.g., int, (int, str))
        """
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                val = self.resolve(path, default=object())
                if val is object():
                    raise KeyError(f"Path does not exist: {path}")
                allowed_types = types if isinstance(types, tuple) else (types,)
                if not any(isinstance(val, t) for t in allowed_types):
                    names = ", ".join(t.__name__ for t in allowed_types)
                    raise TypeError(f"Value at {path} must be of type(s) {names}, got {type(val).__name__}")
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator

    def emptywrap(method):
        """
        Ensures the value at the path is not empty.
        Empty values include: None, "", empty list, or empty dict.
        Raises ValueError if the value is empty.
        """
        @wraps(method)
        def wrapper(self, path, *args, **kwargs):
            if self.empty(path):
                raise ValueError(f"Value at path {path} is empty")
            return method(self, path, *args, **kwargs)
        return wrapper

    def makesnapshot(method):
        """
        Takes a snapshot of the current JSON state before executing the method.
        Useful for undo/rollback functionality.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self.snapshot()
            return method(self, *args, **kwargs)
        return wrapper
    
    def auto_undo(method):
        """Automatically revert JSON to last snapshot if exception occurs."""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            snapshot = copy.deepcopy(self.data)
            try:
                return method(self, *args, **kwargs)
            except Exception as e:
                self.data = snapshot
                raise e
        return wrapper

    def log_changes(method):
        """Prints value before and after method runs."""
        @wraps(method)
        def wrapper(self, path, *args, **kwargs):
            before = copy.deepcopy(self.resolve(path, default=None))
            result = method(self, path, *args, **kwargs)
            after = self.resolve(path, default=None)
            print(f"[LOG] {path}: {before} -> {after}")
            return result
        return wrapper

    def diffwrap(method):
        """Print diff automatically after method completes."""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            snapshot = copy.deepcopy(self.data)
            result = method(self, *args, **kwargs)
            self.diff_changes(snapshot, self.data)
            return result
        return wrapper

    def auditwrap(user="system"):
        """Attach meta info for audit purposes."""
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                result = method(self, path, *args, **kwargs)
                if hasattr(self, "meta"):
                    self.meta["last_changed_by"] = user
                return result
            return wrapper
        return decorator

    def rangewrap(min_val=None, max_val=None):
        """Check numeric range before method runs."""
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                val = self.resolve(path, default=None)
                if val is not None:
                    if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                        raise ValueError(f"Value at {path} = {val} is outside range [{min_val}, {max_val}]")
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator

    def lengthwrap(min_len=None, max_len=None):
        """Check length of string/list before method runs."""
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                val = self.resolve(path, default=None)
                if val is not None:
                    length = len(val)
                    if (min_len is not None and length < min_len) or (max_len is not None and length > max_len):
                        raise ValueError(f"Length of {path} = {length} outside [{min_len}, {max_len}]")
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator

    def patternwrap(regex):
        """Check string matches regex."""
        pattern = re.compile(regex)
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                val = self.resolve(path, default=None)
                if val is not None and not pattern.fullmatch(str(val)):
                    raise ValueError(f"Value at {path} = {val} does not match pattern {regex}")
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator

    def enumwrap(*allowed_values):
        """Check value is in a set of allowed values."""
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                val = self.resolve(path, default=None)
                if val is not None and val not in allowed_values:
                    raise ValueError(f"Value at {path} = {val} not in allowed set {allowed_values}")
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator

    def wildcardwrap(method):
        """Apply method to every path matching a wildcard *."""
        @wraps(method)
        def wrapper(self, path, *args, **kwargs):
            if "*" in path:
                results = []
                for val in self.wildcard(path):
                    results.append(method(self, path, *args, **kwargs))
                return results
            return method(self, path, *args, **kwargs)
        return wrapper

    def listwrap(method):
        """Automatically loops over a list of paths."""
        @wraps(method)
        def wrapper(self, paths, *args, **kwargs):
            if isinstance(paths, list):
                return [method(self, p, *args, **kwargs) for p in paths]
            return method(self, paths, *args, **kwargs)
        return wrapper

    def autofill(default_value):
        """Fill missing or empty values automatically."""
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                if self.empty(path):
                    self.set(path, default_value)
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator

    def convert_to(target_type):
        """Convert value to a type before method runs."""
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                val = self.resolve(path, default=None)
                if val is not None and not isinstance(val, target_type):
                    try:
                        self.set(path, target_type(val))
                    except Exception:
                        raise TypeError(f"Cannot convert value at {path} = {val} to {target_type}")
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator

    def atomic(method):
        """Wraps method in temporary copy, only writes if no error occurs."""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            backup = copy.deepcopy(self.data)
            result = method(self, *args, **kwargs)
            return result
        return wrapper

    def readonly(method):
        """Prevents any changes to JSON during method."""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            backup = copy.deepcopy(self.data)
            result = method(self, *args, **kwargs)
            self.data = backup
            return result
        return wrapper

    def diff_changes(self, old, new):
        """Show diff between old and new data (used by @diffwrap)."""
        def recurse(o, n, path=""):
            for k in n:
                full = f"{path}.{k}" if path else k
                if k not in o:
                    print(f"[ADDED] {full} = {n[k]}")
                elif o[k] != n[k]:
                    print(f"[CHANGED] {full}: {o[k]} -> {n[k]}")
                if isinstance(n[k], dict) and k in o:
                    recurse(o[k], n[k], full)
        recurse(old, new)
        
    def validate(path=False, types: Union[Type, Tuple[Type, ...]] = None, not_empty=False, snapshot=False):
        """
        General-purpose validation decorator for JSON paths.

        Args:
            path: bool → check if path exists
            types: type or tuple → check value type
            not_empty: bool → check value is not empty
            snapshot: bool → take snapshot before method

        Usage:
            @validate(path=True, types=int, not_empty=True, snapshot=True)
            def set_value(self, path, value):
                self.set(path, value)
        """
        def decorator(method):
            @wraps(method)
            def wrapper(self, path, *args, **kwargs):
                if snapshot:
                    self.makesnapshot()
                if path and not self.exists(path):
                    raise KeyError(f"Path does not exist: {path}")
                if types is not None:
                    val = self.resolve(path, default=object())
                    if val is object():
                        raise KeyError(f"Path does not exist: {path}")
                    allowed_types = types if isinstance(types, tuple) else (types,)
                    if not any(isinstance(val, t) for t in allowed_types):
                        names = ", ".join(t.__name__ for t in allowed_types)
                        raise TypeError(f"Value at {path} must be of type(s) {names}, got {type(val).__name__}")
                if not_empty:
                    if self.empty(path):
                        raise ValueError(f"Value at path {path} is empty")
                return method(self, path, *args, **kwargs)
            return wrapper
        return decorator
    
    def restrict(self, path: str):
        """
        Replace the value at `path` with a list containing that value.

        Example:
            "setting": true  ->  "setting": [true]
        """
        if self.data is None:
            self.memset()

        val = self.get(path)
        self.set(path, [val])

class CSV:
    def __init__(
        self, 
        path: str,
        extension: str | None = None, 
        autostrip: bool = True
    ) -> None:
        self.path: str = path
        self.extension: str | None = extension
        self.autostrip: bool = True
        self.data: list[str] = []
    
    def memset(
        self, 
        r: bool | None = None, 
        mod: Literal["r", "w", "r+"] | None = None, 
        errors: bool | None = None,
        encoding: Literal["utf-8"] | None = None
    ) -> dict[str, int] | list[int]:
        if not self.path or not os.path.exists(self.path) or not os.path.isfile(self.path):
            if r:
                raise Exception("Invalid path passed. Please check and try valid one.")
            else:
                return { "_error": -1 }
        
        try:
            with open(self.path, "r") as file:
                rawdata = file.readlines()
                for line in rawdata:
                    if self.autostrip:
                        self.data.append(line.strip())
                    else:
                        self.data.append(line)
            return { "_ok": 0 }
        except (Exception, FileNotFoundError) as e:
            if r:
                raise Exception(e)
            else:
                return { "_error": -1 }
    
    def load(self) -> list[str]: return self.data if self.data else []
    
    def append(self, content: str) -> bool:
        if not self.data or len(self.data) == 0:
            self.memset(r=False)
        
        if not isinstance(content, str):
            raise TypeError(f"Invalid data type for content: got {type(content).__name__}")    
        
        try:
            with open(self.path, "r") as file:
                file.write(f"\n{content}\n")
            return True
        except Exception as e:
            return False
        
    def lenght(self, hint: int = -1, skip: bool = True) -> int | None:
        if not self.data or len(self.data) == 0:
            self.memset(r=False)
        try:
            with open(self.path, "r") as file:
                rawlines: list[str] = file.readlines()
                lines: list[str] = []
                count: int = 0 
                
                if not self.autostrip:
                    for l in rawlines:
                        lines.append(l.strip())
                
                if skip and self.autostrip:
                    for i in rawlines:
                        if not i or i.isspace() or i.startswith(("#", ";")):
                            continue
                        count += 1
                elif skip and not self.autostrip:
                    for line in lines:
                        if not line or line.isspace() or line.startswith(("#", ";")):
                            continue
                        count += 1
                else:
                    for i in rawlines:
                        count += 1
        except Exception as e:
            return None
    
    def size(self) -> int:
        if not self.data or len(self.data) == 0:
            self.memset(r=False)        
        if self.path and os.path.exists(self.path):
            return os.path.getsize(self.path)
        else:
            return 0

XMLNode = Dict[str, Dict[str, Union[str, List["XMLNode"]]]]

class XML:
    def __init__(self, path: str = ""):
        self.path: str = path
        self.data: XMLNode = {}
        if path:
            self.load_file(path)

    def load_file(self, path: str):
        self.path = path
        with open(path, "r", encoding="utf-8") as f:
            xml_string = f.read()
        self.data = self.parse(xml_string)

    def save_file(self, path: str = None):
        path = path or self.path
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_string())

    def parse(self, xml: str) -> XMLNode:
        xml = xml.strip()
        pos = 0
        def parse_node() -> XMLNode:
            nonlocal pos
            assert xml[pos] == "<"
            pos += 1
            tag = ""
            while xml[pos] not in (">", " "):
                tag += xml[pos]
                pos += 1
            while xml[pos] != ">":
                pos += 1
            pos += 1
            children = []
            text = ""
            while not xml[pos:pos+len(tag)+3] == f"</{tag}>":
                if xml[pos] == "<":
                    children.append(parse_node())
                else:
                    text += xml[pos]
                    pos += 1
            pos += len(tag)+3
            return {tag: {"_text": text.strip(), "_children": children}}
        return parse_node()

    def to_string(self, node: XMLNode = None, level=0) -> str:
        node = node or self.data
        xml_str = ""
        for tag, content in node.items():
            indent = "  " * level
            xml_str += f"{indent}<{tag}>"
            if content["_text"]:
                xml_str += content["_text"]
            if content["_children"]:
                xml_str += "\n"
                for child in content["_children"]:
                    xml_str += self.to_string(child, level + 1)
                xml_str += f"{indent}"
            xml_str += f"</{tag}>\n"
        return xml_str

    def print_data(self, node: XMLNode = None, level=0):
        node = node or self.data
        for tag, content in node.items():
            print("  " * level + tag + ": " + content["_text"])
            for child in content["_children"]:
                self.print_data(child, level + 1)

    def search(self, keyword: str, node: XMLNode = None, results=None):
        node = node or self.data
        results = results or []
        for tag, content in node.items():
            if keyword.lower() in tag.lower() or keyword.lower() in content["_text"].lower():
                results.append({tag: content})
            for child in content["_children"]:
                self.search(keyword, child, results)
        return results

    def add_element(self, parent_tag: str, new_tag: str, new_text: str = "", node: XMLNode = None):
        node = node or self.data
        for tag, content in node.items():
            if tag == parent_tag:
                content["_children"].append({new_tag: {"_text": new_text, "_children": []}})
                return True
            for child in content["_children"]:
                if self.add_element(parent_tag, new_tag, new_text, child):
                    return True
        return False

    def edit_element(self, target_tag: str, new_text: str, node: XMLNode = None):
        node = node or self.data
        for tag, content in node.items():
            if tag == target_tag:
                content["_text"] = new_text
                return True
            for child in content["_children"]:
                if self.edit_element(target_tag, new_text, child):
                    return True
        return False

    def delete_element(self, target_tag: str, node: XMLNode = None):
        node = node or self.data
        for tag, content in list(node.items()):
            children = content["_children"]
            for i, child in enumerate(children):
                if target_tag in child:
                    del children[i]
                    return True
                else:
                    if self.delete_element(target_tag, child):
                        return True
        return False

class Batch:
    """Holds the result of a batch execution and allows chaining filters."""

    def __init__(self, stdout: str, stderr: str, returncode: int):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


    def grep(self, pattern: str, ignore_case: bool = False) -> "Batch":
        """Filter lines containing a pattern (like grep)."""
        if ignore_case:
            pattern = pattern.lower()
            lines = [l for l in self.stdout.splitlines() if pattern in l.lower()]
        else:
            lines = [l for l in self.stdout.splitlines() if pattern in l]

        return Batch("\n".join(lines), self.stderr, self.returncode)

    def awk(self, column: int, sep: str | None = None) -> "Batch":
        """
        Extract a column from each line (like awk '{print $N}').

        column is 1-based index.
        """
        result_lines: List[str] = []

        for line in self.stdout.splitlines():
            parts = line.split(sep) if sep else line.split()
            if 0 < column <= len(parts):
                result_lines.append(parts[column - 1])

        return Batch("\n".join(result_lines), self.stderr, self.returncode)

    def lines(self) -> list[str]:
        """Return stdout as a list of lines."""
        return self.stdout.splitlines()

    def text(self) -> str:
        """Return raw stdout."""
        return self.stdout

    def ok(self) -> bool:
        """Return True if return code is 0."""
        return self.returncode == 0

    def __str__(self) -> str:
        return self.stdout

_COMMAND_REGISTRY: Dict[str, Callable[..., Batch]] = {}

def register_command(name: str, func: Callable[..., Batch]) -> None:
    """Register a custom batch command."""
    _COMMAND_REGISTRY[name] = func


def _run_command(
    command: str | list[str],
    cwd: str | None = None,
) -> subprocess.CompletedProcess:
    """Internal command runner."""
    return subprocess.run(
        command,
        shell=isinstance(command, str),
        cwd=Path(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )


def batch(
    t: str,
    command: str | list[str] | None = None,
    path: str | None = None,
    stdout: bool = True,
) -> Batch:
    """
    Execute a command and return a chainable BatchResult.

    Parameters
    ----------
    t : str
        Execution type:
            "raw"  -> run command exactly as given (shell if str)
            "cmd"  -> Windows cmd execution
            "sh"   -> POSIX shell execution
    command : str | list[str] | None
        Command to execute.
        - str  -> executed via shell
        - list -> executed without shell
    path : str | None
        Working directory.
    stdout : bool
        If True, print stdout to console.

    Returns
    -------
    BatchResult
        Contains stdout, stderr, returncode and supports chaining.
    """

    if command is None:
        raise ValueError("command cannot be None")
    
    if t in _COMMAND_REGISTRY:
        result = _COMMAND_REGISTRY[t](command, path=path)

        if stdout and result.stdout:
            print(result.stdout, end="")

        return result

    if t == "cmd":
        if isinstance(command, list):
            command = ["cmd", "/c", *command]
        else:
            command = f"cmd /c {command}"

    elif t == "sh":
        if isinstance(command, list):
            command = ["sh", "-c", " ".join(command)]
        else:
            command = ["sh", "-c", command]

    elif t == "raw":
        pass

    else:
        raise ValueError(f"Unknown execution type: {t}")

    proc = _run_command(command, cwd=path)

    result = Batch(proc.stdout, proc.stderr, proc.returncode)

    if stdout and result.stdout:
        print(result.stdout, end="")

    return result

def _inio_batch(command: Any, path: str | None = None) -> Batch:
    """
    Custom batch adapter for INIO.
    Accepts:
        str  -> path to ini file
        dict -> arguments for INIO
    """

    try:
        if isinstance(command, str):
            cfg = INIO(command)
            output = f"INI loaded: {command}"

        elif isinstance(command, dict):
            cfg = INIO(**command)
            output = f"INI loaded with args: {command}"

        else:
            raise ValueError("Unsupported INIO command format")

        return Batch(output, "", 0)

    except Exception as e:
        return Batch("", str(e), 1)

class wrapio:
    @staticmethod
    def do_not_return(func):
        """
        Ensures the decorated function returns None.
        If it returns anything else, an error is raised.
        """
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is not None:
                raise TypeError(
                    f"{func.__name__} is marked do_not_return but returned a value"
                )
            return None
        return wrapper

    @staticmethod
    def inline(func):
        """
        Enforces that the function body is a single return statement.
        (Best-effort check using bytecode.)
        """
        import dis

        instructions = list(dis.get_instructions(func))

        return_ops = [i for i in instructions if i.opname == "RETURN_VALUE"]

        if len(return_ops) != 1:
            raise SyntaxError(
                f"{func.__name__} must contain exactly one return statement for @inline"
            )

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def destroy(func):
        """
        Makes the function callable only once.
        After first call, it is 'destroyed'.
        """
        called = False

        def wrapper(*args, **kwargs):
            nonlocal called
            if called:
                raise RuntimeError(f"{func.__name__} has been destroyed after first call")
            called = True
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def pure(func):
        """
        Best-effort detector for side effects.
        Blocks usage of print, global writes, and nonlocal writes.
        (Not bulletproof, but useful.)
        """
        import dis

        forbidden = {"STORE_GLOBAL", "STORE_DEREF", "DELETE_GLOBAL", "PRINT_EXPR"}

        instructions = list(dis.get_instructions(func))
        for ins in instructions:
            if ins.opname in forbidden:
                raise RuntimeError(
                    f"{func.__name__} is marked @pure but contains side effects"
                )

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    
    @staticmethod
    def type_strict(func):
        """
        Enforces type hints on arguments and return value at runtime.
        """
        from inspect import signature

        sig = signature(func)
        annotations = func.__annotations__

        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            # Check argument types
            for name, value in bound.arguments.items():
                if name in annotations:
                    expected = annotations[name]
                    if not isinstance(value, expected):
                        raise TypeError(
                            f"{name} must be {expected}, got {type(value)}"
                        )

            result = func(*args, **kwargs)

            # Check return type
            if "return" in annotations:
                expected = annotations["return"]
                if not isinstance(result, expected):
                    raise TypeError(
                        f"Return must be {expected}, got {type(result)}"
                    )

            return result

        return wrapper
    
    @staticmethod
    def timeit(func):
        """
        Measures execution time of the function.
        """
        import time

        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{func.__name__} took {end - start:.6f}s")
            return result

        return wrapper
    
    @staticmethod
    def detatch(func):
        """
        Executes function once and memoizes the result.
        Subsequent calls return cached value.
        """
        called = False
        cache = None

        def wrapper(*args, **kwargs):
            nonlocal called, cache
            if not called:
                cache = func(*args, **kwargs)
                called = True
            return cache

        return wrapper
    
    @staticmethod
    def immutable_args(func):
        """
        Makes all mutable arguments immutable inside the function by deep copying them.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_copy = tuple(copy.deepcopy(a) for a in args)
            kwargs_copy = {k: copy.deepcopy(v) for k, v in kwargs.items()}
            return func(*args_copy, **kwargs_copy)
        return wrapper
    
    @staticmethod
    def no_exceptions(func):
        """
        Catches all exceptions, logs them, and returns None.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Caught exception in {func.__name__}: {e}")
                return None
        return wrapper
    
    @staticmethod
    def retry(times=3, delay=0):
        """
        Retries a function on exception up to `times` with optional `delay` in seconds.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for _ in range(times):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if delay:
                            time.sleep(delay)
                raise last_exception
            return wrapper
        return decorator
    
    @staticmethod
    def cached(ttl=None):
        """
        Caches function results. Optional TTL in seconds.
        """
        def decorator(func):
            cache = {}
            cache_time = {}
            lock = threading.Lock()

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (args, frozenset(kwargs.items()))
                with lock:
                    if key in cache:
                        if ttl is None or (time.time() - cache_time[key]) < ttl:
                            return cache[key]
                    result = func(*args, **kwargs)
                    cache[key] = result
                    cache_time[key] = time.time()
                    return result
            return wrapper
        return decorator
    
    @staticmethod
    def const(func):
        """
        Freezes function attributes to make them read-only.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        class ConstWrapper:
            __slots__ = ('_func',)
            def __init__(self, f):
                object.__setattr__(self, '_func', f)
            def __call__(self, *args, **kwargs):
                return self._func(*args, **kwargs)
            def __getattr__(self, item):
                return getattr(self._func, item)
            def __setattr__(self, key, value):
                raise AttributeError(f"Cannot modify attribute '{key}' of const function")
        return ConstWrapper(wrapper)
  
    @staticmethod
    def log_calls(func):
        """Logs arguments and return value of a function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"{func.__name__} returned {result}")
            return result
        return wrapper

    @staticmethod
    def memoize(func):
        """Caches function results based on arguments."""
        cache = {}
        lock = threading.Lock()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            with lock:
                if key in cache:
                    return cache[key]
                result = func(*args, **kwargs)
                cache[key] = result
                return result
        return wrapper

    @staticmethod
    def validate_types(func):
        """Enforces argument and return type hints at runtime."""
        from inspect import signature
        sig = signature(func)
        annotations = func.__annotations__
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name, val in bound.arguments.items():
                if name in annotations and not isinstance(val, annotations[name]):
                    raise TypeError(f"{name} must be {annotations[name]}, got {type(val)}")
            result = func(*args, **kwargs)
            if "return" in annotations and not isinstance(result, annotations["return"]):
                raise TypeError(f"Return must be {annotations['return']}, got {type(result)}")
            return result
        return wrapper

    @staticmethod
    def timeout(seconds):
        """Raises TimeoutError if function takes longer than `seconds`."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = [None]
                exc = [None]
                def target():
                    try:
                        result[0] = func(*args, **kwargs)
                    except Exception as e:
                        exc[0] = e
                thread = threading.Thread(target=target)
                thread.daemon = True
                thread.start()
                thread.join(seconds)
                if thread.is_alive():
                    raise TimeoutError(f"{func.__name__} timed out after {seconds} seconds")
                if exc[0]:
                    raise exc[0]
                return result[0]
            return wrapper
        return decorator

    @staticmethod
    def retry(times=3, delay=0):
        """Retries function on exception `times` times with optional `delay`."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exc = None
                for i in range(times):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exc = e
                        if delay > 0:
                            time.sleep(delay)
                raise last_exc
            return wrapper
        return decorator

    @staticmethod
    def profile(func):
        """Prints execution time of the function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{func.__name__} executed in {end - start:.6f}s")
            return result
        return wrapper

    @staticmethod
    def deprecated(reason=""):
        """Marks function as deprecated and warns when used."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warnings.warn(f"{func.__name__} is deprecated. {reason}", DeprecationWarning)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def thread_safe(func):
        """Makes function thread-safe using a lock."""
        lock = threading.Lock()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def singleton(cls):
        """Ensures a class has only one instance."""
        instances = {}
        lock = threading.Lock()
        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
                return instances[cls]
        return wrapper

    @staticmethod
    def once(func):
        """Runs function only once; caches result for subsequent calls."""
        called = False
        cache = None
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal called, cache
            if not called:
                cache = func(*args, **kwargs)
                called = True
            return cache
        return wrapper

    @staticmethod
    def cached_property(func):
        """Lazy-evaluated property cached on first access."""
        attr_name = f"_{func.__name__}_cached"
        @property
        @functools.wraps(func)
        def wrapper(self):
            if not hasattr(self, attr_name):
                setattr(self, attr_name, func(self))
            return getattr(self, attr_name)
        return wrapper

    @staticmethod
    def retry_on_exception(exceptions, times=3, delay=0):
        """Retries function only on specific exceptions."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exc = None
                for _ in range(times):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exc = e
                        if delay > 0:
                            time.sleep(delay)
                raise last_exc
            return wrapper
        return decorator

    @staticmethod
    def log_exceptions(re_raise=False):
        """Logs exceptions; optionally re-raises."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Exception in {func.__name__}: {e}")
                    if re_raise:
                        raise
            return wrapper
        return decorator

    @staticmethod
    def auto_repr(cls):
        """Generates __repr__ automatically from __dict__."""
        orig_init = cls.__init__
        @functools.wraps(orig_init)
        def __init__(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)
        def __repr__(self):
            attrs = ", ".join(f"{k}={v!r}" for k,v in self.__dict__.items())
            return f"{self.__class__.__name__}({attrs})"
        cls.__init__ = __init__
        cls.__repr__ = __repr__
        return cls

    @staticmethod
    def timed_cache(ttl=None):
        """Caches function results with optional TTL (seconds)."""
        def decorator(func):
            cache = {}
            cache_time = {}
            lock = threading.Lock()
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (args, frozenset(kwargs.items()))
                with lock:
                    if key in cache:
                        if ttl is None or (time.time() - cache_time[key]) < ttl:
                            return cache[key]
                    result = func(*args, **kwargs)
                    cache[key] = result
                    cache_time[key] = time.time()
                    return result
            return wrapper
        return decorator

    @staticmethod
    def synchronized(func):
        """Thread-safe function lock decorator."""
        lock = threading.Lock()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def lockstep(func):
        """Thread-safe lock decorator for multi-threaded execution."""
        lock = threading.Lock()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def once_and_only(func):
        """Runs function exactly once; further calls raise RuntimeError."""
        called = False
        cache = None
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal called, cache
            if called:
                raise RuntimeError(f"{func.__name__} can only be called once")
            cache = func(*args, **kwargs)
            called = True
            return cache
        return wrapper

    @staticmethod
    def snapshot(func):
        """Deep-copies all mutable arguments to avoid side effects."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_copy = tuple(copy.deepcopy(a) for a in args)
            kwargs_copy = {k: copy.deepcopy(v) for k, v in kwargs.items()}
            return func(*args_copy, **kwargs_copy)
        return wrapper

    @staticmethod
    def echo_call(func):
        """Prints function name, args, and return value for tracing."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"→ {func.__name__}({args}, {kwargs})")
            result = func(*args, **kwargs)
            print(f"← {func.__name__} → {result}")
            return result
        return wrapper

    @staticmethod
    def retry_loop(times=3, delay=1, backoff=2, exceptions=(Exception,)):
        """Retries function on exception with exponential backoff."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                current_delay = delay
                for _ in range(times):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        print(f"Retry due to {e}, waiting {current_delay}s")
                        time.sleep(current_delay)
                        current_delay *= backoff
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def frozen_class(cls):
        """Makes class attributes immutable after creation."""
        orig_setattr = cls.__setattr__
        def locked_setattr(self, name, value):
            if hasattr(self, name):
                raise AttributeError(f"Cannot modify {name}, class is frozen")
            orig_setattr(self, name, value)
        cls.__setattr__ = locked_setattr
        return cls

    @staticmethod
    def lazy_load(func):
        """Lazy-evaluates and caches property or method result."""
        attr_name = f"_lazy_{func.__name__}"
        @property
        @functools.wraps(func)
        def wrapper(self):
            if not hasattr(self, attr_name):
                setattr(self, attr_name, func(self))
            return getattr(self, attr_name)
        return wrapper

    @staticmethod
    def exception_guard(default=None):
        """Catches exceptions and returns default value."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Exception in {func.__name__}: {e}")
                    return default
            return wrapper
        return decorator

    @staticmethod
    def type_enforce(func):
        """Runtime type enforcement for arguments and return value."""
        from inspect import signature
        sig = signature(func)
        ann = func.__annotations__
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for k, v in bound.arguments.items():
                if k in ann and not isinstance(v, ann[k]):
                    raise TypeError(f"{k} must be {ann[k]}, got {type(v)}")
            res = func(*args, **kwargs)
            if "return" in ann and not isinstance(res, ann["return"]):
                raise TypeError(f"Return must be {ann['return']}, got {type(res)}")
            return res
        return wrapper

    @staticmethod
    def benchmark_it(func):
        """Measures execution time of function in seconds."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{func.__name__} executed in {end-start:.6f}s")
            return result
        return wrapper

    @staticmethod
    def call_limit(n):
        """Function can be called at most n times."""
        def decorator(func):
            calls = 0
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal calls
                if calls >= n:
                    raise RuntimeError(f"{func.__name__} can only be called {n} times")
                calls += 1
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def retry_forever(delay=1, exceptions=(Exception,)):
        """Retries function forever until success."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                while True:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        print(f"Retry forever due to {e}, waiting {delay}s")
                        time.sleep(delay)
            return wrapper
        return decorator

    @staticmethod
    def auto_cache(ttl=None):
        """Automatically caches function results with optional TTL."""
        def decorator(func):
            cache = {}
            cache_time = {}
            lock = threading.Lock()
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (args, frozenset(kwargs.items()))
                with lock:
                    if key in cache:
                        if ttl is None or (time.time() - cache_time[key]) < ttl:
                            return cache[key]
                    result = func(*args, **kwargs)
                    cache[key] = result
                    cache_time[key] = time.time()
                    return result
            return wrapper
        return decorator

    @staticmethod
    def memoize_deep(func):
        """Caches function results, supports mutable arguments safely."""
        cache = {}
        lock = threading.Lock()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (tuple(copy.deepcopy(args)), frozenset((k, copy.deepcopy(v)) for k,v in kwargs.items()))
            with lock:
                if key in cache:
                    return cache[key]
                result = func(*args, **kwargs)
                cache[key] = result
                return result
        return wrapper

    @staticmethod
    def traceflow(func):
        """Prints call stack flow for decorated function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("Traceflow call stack:")
            traceback.print_stack(limit=3)
            return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def auto_retry(times=3, delay=1):
        """Retries a function automatically on any exception."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exc = None
                for _ in range(times):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exc = e
                        time.sleep(delay)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def thread_safe_cache(func):
        """Thread-safe memoization for heavy functions."""
        cache = {}
        lock = threading.Lock()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            with lock:
                if key in cache:
                    return cache[key]
                result = func(*args, **kwargs)
                cache[key] = result
                return result
        return wrapper

    @staticmethod
    def assert_output(assertion_func):
        """Asserts function output meets a condition."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                assert assertion_func(result), f"{func.__name__} output failed assertion"
                return result
            return wrapper
        return decorator

    @staticmethod
    def profile_memory(func):
        """Profiles approximate memory usage of a function call."""
        import tracemalloc
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            result = func(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            print(f"{func.__name__} memory: current={current/1024:.2f}KB, peak={peak/1024:.2f}KB")
            return result
        return wrapper

    @staticmethod
    def event_hook(before=None, after=None):
        """Executes callbacks before and/or after function execution."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if callable(before):
                    before(*args, **kwargs)
                result = func(*args, **kwargs)
                if callable(after):
                    after(result, *args, **kwargs)
                return result
            return wrapper
        return decorator

    @staticmethod
    def debounce(ms=300):
        """Prevents function from being called more than once within `ms` milliseconds."""
        def decorator(func):
            last_call = [0]
            lock = threading.Lock()
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with lock:
                    now = time.time() * 1000
                    if now - last_call[0] >= ms:
                        last_call[0] = now
                        return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def throttle(ms=300):
        """Ensures function runs at most once per interval."""
        def decorator(func):
            last_call = [0]
            lock = threading.Lock()
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with lock:
                    now = time.time() * 1000
                    if now - last_call[0] >= ms:
                        last_call[0] = now
                        return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def trace_args(func):
        """Logs the types of arguments passed to a function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{func.__name__} args types: {[type(a).__name__ for a in args]}, kwargs types: {{k:type(v).__name__ for k,v in kwargs.items()}}")
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def trace_return(func):
        """Logs the type of the return value."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"{func.__name__} return type: {type(result).__name__}")
            return result
        return wrapper

    @staticmethod
    def inject_logger(func):
        """Injects `logger` argument if not provided."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'logger' not in kwargs:
                import logging
                kwargs['logger'] = logging.getLogger(func.__name__)
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def default_on_exception(default=None):
        """Returns default value if any exception occurs."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    return default
            return wrapper
        return decorator

    @staticmethod
    def auto_invoke(func):
        """Automatically executes function at definition time."""
        func()
        return func

    @staticmethod
    def suppress_output(func):
        """Suppresses stdout during function execution."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with contextlib.redirect_stdout(io.StringIO()):
                return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def monitor_calls(func):
        """Counts the number of times a function is called."""
        calls = [0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            calls[0] += 1
            wrapper.calls = calls[0]
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def retry_until(condition, times=5, delay=1):
        """Retries function until output satisfies a condition."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for _ in range(times):
                    result = func(*args, **kwargs)
                    if condition(result):
                        return result
                    time.sleep(delay)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def lazy_class_property(func):
        """Lazy property at class level, shared across instances."""
        attr_name = f"_lazy_class_{func.__name__}"
        @property
        @functools.wraps(func)
        def wrapper(cls):
            if not hasattr(cls, attr_name):
                setattr(cls, attr_name, func(cls))
            return getattr(cls, attr_name)
        return wrapper

    @staticmethod
    def clone_args(func):
        """Deep-copies mutable arguments before function execution."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_copy = tuple(copy.deepcopy(a) for a in args)
            kwargs_copy = {k: copy.deepcopy(v) for k,v in kwargs.items()}
            return func(*args_copy, **kwargs_copy)
        return wrapper

    @staticmethod
    def stack_limit(limit=100):
        """Limits recursion depth for a function."""
        def decorator(func):
            depth = [0]
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if depth[0] >= limit:
                    raise RecursionError(f"{func.__name__} exceeded recursion limit of {limit}")
                depth[0] += 1
                result = func(*args, **kwargs)
                depth[0] -= 1
                return result
            return wrapper
        return decorator

    @staticmethod
    def dynamic_dispatch(func_map):
        """Dispatches function based on type of first argument."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(first_arg, *args, **kwargs):
                func_to_call = func_map.get(type(first_arg), func)
                return func_to_call(first_arg, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def benchmark_loop(n=10):
        """Measures average execution time over N iterations."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                total = 0
                for _ in range(n):
                    start = time.perf_counter()
                    func(*args, **kwargs)
                    total += time.perf_counter() - start
                avg = total/n
                print(f"{func.__name__} avg execution over {n} runs: {avg:.6f}s")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
def const(obj):
    """
    Makes functions, classes, objects, or values immutable.
    """

    if isinstance(obj, types.FunctionType):
        class ConstFunc:
            __slots__ = ('_func',)
            def __init__(self, f):
                object.__setattr__(self, '_func', f)
            def __call__(self, *args, **kwargs):
                return self._func(*args, **kwargs)
            def __getattr__(self, name):
                return getattr(self._func, name)
            def __setattr__(self, key, value):
                raise AttributeError(f"Cannot modify attribute '{key}' of const function")
        return ConstFunc(obj)

    elif isinstance(obj, type):
        class ConstClass(obj):
            def __setattr__(self, key, value):
                raise AttributeError(f"Cannot modify attribute '{key}' of const class instance")
            def __delattr__(self, key):
                raise AttributeError(f"Cannot delete attribute '{key}' of const class instance")
        ConstClass.__name__ = obj.__name__
        return ConstClass

    elif isinstance(obj, object):
        class ConstObj:
            __slots__ = ('_obj',)
            def __init__(self, o):
                object.__setattr__(self, '_obj', o)
            def __getattr__(self, name):
                return getattr(self._obj, name)
            def __setattr__(self, key, value):
                raise AttributeError(f"Cannot modify attribute '{key}' of const object")
            def __delattr__(self, key):
                raise AttributeError(f"Cannot delete attribute '{key}' of const object")
        return ConstObj(obj)

    else:
        class ConstValue:
            __slots__ = ('_value',)
            def __init__(self, val):
                object.__setattr__(self, '_value', val)
            @property
            def value(self):
                return self._value
            def __setattr__(self, key, value):
                raise AttributeError("Cannot modify const value")
            def __repr__(self):
                return repr(self._value)
            def __str__(self):
                return str(self._value)
        return ConstValue(obj)
    
class FrozenVar:
    """
    Wrapper for a variable to make it immutable.
    Supports primitives, lists, dicts, sets, and objects.
    """
    __slots__ = ('_value',)

    def __init__(self, value):
        if isinstance(value, (list, dict, set)):
            self._value = copy.deepcopy(value)
        else:
            self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _):
        raise AttributeError("Cannot reassign a frozen variable")

    def __repr__(self):
        return repr(self._value)
    
    def __str__(self):
        return str(self._value)
    
    def __getitem__(self, key):
        return self._value[key]
    
    def __len__(self):
        return len(self._value)
    
    def __iter__(self):
        return iter(self._value)

    def __contains__(self, item):
        return item in self._value

    def __add__(self, other):
        return self._value + other
    def __sub__(self, other):
        return self._value - other
    def __mul__(self, other):
        return self._value * other
    def __truediv__(self, other):
        return self._value / other

    def __getattr__(self, name):
        if isinstance(self._value, (list, dict, set)):
            if name in ('append', 'extend', 'pop', 'remove', 'clear', 'update', 'add', 'discard', 'setdefault'):
                raise AttributeError(f"Cannot mutate frozen variable via '{name}'")
            return getattr(self._value, name)
        return getattr(self._value, name)

def freeze(var) -> FrozenVar:
    """
    Wraps a variable into a FrozenVar to make it immutable.
    Usage: 
    ```
    x = freeze(10)
    ```
    """
    return FrozenVar(var)



"""
    pynmap components — Python Nmap Wrapper and Scan Utilities
    ===============================================

    This module provides a high-level, type-safe Python interface to Nmap-style
    network scanning. It includes classes for managing hosts, ports, scan switches,
    and OS detection, along with utilities for parsing, validating, and rendering
    scan targets and options into a fully formed Nmap CLI command.

    Purpose
    -------
    The `pynmap` library is designed to make Nmap scanning programmatically
    accessible in Python while maintaining strict type safety, validation, and
    chainable, human-readable APIs. It allows the construction of complex scans
    with hosts, ports, exclusions, timing templates, and protocol-specific options
    without manually assembling command-line strings.

    Core Components
    ---------------
    1. **NmapComponent**
       - Provides standardized port types (single, range, sequence) with validation
         and parsing utilities.
       - Helps safely represent ports in Nmap-style scanning.

    2. **OSDetection**
       - Detects the operating system of the current environment.
       - Supports short/raw (`win`, `linux`, `darwin`) and full names
         (`windows`, `linux`, `mac`).

    3. **NmapPackage**
       - Helper to install Python packages from files or lists.
       - Supports multiple overloads and selective package installation.

    4. **Ports**
       - Comprehensive representation of ports:
         - Single ports, sequences, ranges, exclusions, known service ports.
       - Parsing strings like `"22,80-90,!23,http"`.
       - Normalization to included/excluded port lists.
       - Charting ports to CLI-ready strings.

    5. **Hosts**
       - Type-safe host representation:
         - Single host/IP, sequence, IP range, CIDR subnet, exclusions, file-based hosts.
       - Parsing and normalization of host strings.
       - Converts to Nmap-compatible CLI formats.

    6. **Switches**
       - Chainable controller for all Nmap scan and discovery switches.
       - Enforces required values, mutual exclusions, and correct CLI rendering.
       - Pre-defined common switches: SYN, UDP, FIN, XMAS, OS detection, version detection, etc.

    7. **Nmap**
       - High-level Nmap command builder combining Hosts, Ports, and Switches.
       - Chainable API for hosts, ports, scan types, timing templates, and max packet rate.
       - Generates fully valid Nmap CLI commands with `.build()` or `str()`.

    Usage Examples
    --------------

    **Build a basic Nmap scan:**
    ```python
    from pynmap import Nmap

    cmd = (
        Nmap()
        .hosts("192.168.1.1", "scanme.nmap.org")
        .ports(22, 80, "8000-8100", exclude=23)
        .timing(3)
        .max_rate(1000)
        .scan.syn()
    )

    print(cmd)
    # Example Output:
    # nmap -sS -T3 --max-rate 1000 -p 22,80,8000-8100 192.168.1.1,scanme.nmap.org
    """

class NmapComponent:
    """
    Standardized types and helpers for Nmap-style port scanning.

    Provides type aliases, specialized port types, and validation methods
    to safely represent single ports, port ranges, and sequences of ports.

    Type Aliases:
        integer: Alias for int.
        sequence: Alias for str.
        array: Alias for list.
        noreturn: Alias for None.

    Nested Classes:
        port:
            Defines specialized Nmap port types and utility methods.

            Attributes:
                singleport:
                    NewType representing a single integer port (1-65535).
                rangeport:
                    NewType representing a port range string (e.g., "80-443").
                sequenceport:
                    NewType representing a list of integer ports.

            Class Methods:
                single() -> singleport:
                    Returns the type object for a single port.
                buffer() -> int:
                    Returns the maximum valid port number (65535).

            Static Methods:
                validate_single(port: int) -> singleport:
                    Validates that a single port is between 1 and 65535.

                validate_range(port_range: str) -> rangeport:
                    Validates that a port range string is in the format "start-end"
                    with each port between 1 and 65535 and start < end.

                validate_sequence(ports: list[int]) -> sequenceport:
                    Validates that a list of ports contains only integers 1-65535.

                parse(port_str: str) -> list[int]:
                    Parses a string like "22,80-90,443" into a list of integer ports,
                    supporting both individual ports and ranges.

            Usage Examples:
                # Single port
                sp = nmaptype.port.validate_single(80)
                print(sp)  # singleport(80)

                # Port range
                rp = nmaptype.port.validate_range("8000-8100")
                print(rp)  # rangeport('8000-8100')

                # Sequence of ports
                seq = nmaptype.port.validate_sequence([22, 80, 443])
                print(seq)  # sequenceport([22, 80, 443])

                # Parsing a string
                parsed = nmaptype.port.parse("22,80-82,443")
                print(parsed)  # [22, 80, 81, 82, 443]

                # Maximum allowed port
                max_port = nmaptype.port.buffer()
                print(max_port)  # 65535
    """
    integer: typing.TypeAlias = int
    sequence: typing.TypeAlias = str
    array: typing.TypeAlias = list
    noreturn: typing.TypeAlias = None

    class port:
        """Defines specialized Nmap port types and utilities."""
        singleport = NewType("singleport", int)
        rangeport = NewType("rangeport", str)
        sequenceport = NewType("sequenceport", list[int])

        @classmethod
        def single(cls) -> NewType:
            """Return the singleport type (int)."""
            return cls.singleport

        @classmethod
        @final
        def buffer(cls) -> int:
            """Maximum valid TCP/UDP port number."""
            return 65535

        @staticmethod
        def validate_single(port: int) -> singleport:
            """Validate a single port is in range 1-65535."""
            if not (1 <= port <= 65535):
                raise ValueError(f"Port {port} out of range (1-65535)")
            return NmapComponent.port.singleport(port)

        @staticmethod
        def validate_range(port_range: str) -> rangeport:
            """Validate a port range string like '80-443'."""
            if not isinstance(port_range, str):
                raise TypeError("Port range must be a string")
            parts = port_range.split("-")
            if len(parts) != 2:
                raise ValueError(f"Invalid range format: {port_range}")
            start, end = map(int, parts)
            if not (1 <= start <= 65535 and 1 <= end <= 65535 and start < end):
                raise ValueError(f"Port range out of bounds: {port_range}")
            return NmapComponent.port.rangeport(port_range)

        @staticmethod
        def validate_sequence(ports: list[int]) -> sequenceport:
            """Validate a list of ports."""
            if not all(1 <= p <= 65535 for p in ports):
                raise ValueError(f"All ports must be in range 1-65535: {ports}")
            return NmapComponent.port.sequenceport(ports)

        @staticmethod
        def parse(port_str: str) -> list[int]:
            """
            Parse a string like '22,80-90,443' into a list of port integers.
            Handles single ports and ranges.
            """

            ports: list[int] = []
            items = [s.strip() for s in port_str.split(",")]
            for item in items:
                if re.fullmatch(r"\d+", item):
                    ports.append(int(item))
                elif re.fullmatch(r"\d+-\d+", item):
                    start, end = map(int, item.split("-"))
                    if not (1 <= start <= 65535 and 1 <= end <= 65535):
                        raise ValueError(f"Port range out of bounds: {item}")
                    ports.extend(range(start, end + 1))
                else:
                    raise ValueError(f"Invalid port entry: {item}")
            return ports

class OSDetection:
    """
    A class to detect the operating system of the current environment.

    Attributes
    ----------
    raw : bool
        Determines the format of the returned OS name.
        - If True, returns a short/raw version: 'win', 'linux', 'darwin'.
        - If False, returns a more readable version: 'windows', 'linux', 'mac'.

    Methods
    -------
    detect
        Returns the name of the operating system based on the `raw` flag.
    """

    def __init__(self, raw: bool = True) -> str | None:
        """
        Initialize OSDetection instance.

        Parameters
        ----------
        raw : bool, optional
            Flag to specify if the returned OS name should be raw/short or readable.
            Default is True (raw/short format).
        """
        self.raw = raw

    @final
    def detect(self) -> str | None:
        """
        Detect the operating system.

        Returns
        -------
        str | None
            The name of the operating system:
            - If `raw` is True: 'win', 'linux', 'darwin'
            - If `raw` is False: 'windows', 'linux', 'mac'

        Notes
        -----
        Uses `sys.platform` to determine the OS.
        Returns `None` if the platform is unrecognized.
        """
        os_name: str
        if sys.platform.startswith("win"):
            os_name = "windows" if not self.raw else "win"
        elif sys.platform.startswith("linux"):
            os_name = "linux" if not self.raw else "linux"
        elif sys.platform == "darwin":
            os_name = "mac" if not self.raw else "darwin"
        else:
            os_name = None
        
        return os_name

    @property
    def platform(self) -> str | None:
        return sys.platform
    
__os_platform__ = OSDetection(raw=False)

@final
class NmapPackage:
    def __init__(
        self,
        path: str | list,
        *,
        r: bool = True
    ) -> None:
        self.path = path
        self.r = r

    @overload
    def install(self) -> bool: ...
    @overload
    def install(self, path: str, /) -> bool | dict: ...
    @overload
    def install(self, c: bool, /) -> str | bool: ...
    @overload
    def install(self, c: bool, specific: str | list[str], /) -> str | list | bool: ...
    @overload
    def install(self, path: str, specific: str | list[str], /) -> str | list | bool: ...
    @overload
    def install(self, path: str, c: bool, specific: str | list[str], /) -> str | list | bool: ...
    def install(
        self,
        arg1: str | bool | None = None,
        arg2: bool | str | list[str] | None = None,
        arg3: str | list[str] | None = None,
        /
    ) -> bool | dict | str | list:

        path: str | None = None
        c: bool = False
        specific: str | list[str] | None = None

        if arg1 is None:
            path = self.path

        elif isinstance(arg1, str):
            path = arg1

            if isinstance(arg2, (str, list)):
                specific = arg2
            elif isinstance(arg2, bool):
                c = arg2
                specific = arg3

        elif isinstance(arg1, bool):
            c = arg1

            if isinstance(arg2, (str, list)):
                specific = arg2
        else:
            raise TypeError("Invalid arguments")

        if not path:
            raise ValueError("No path provided")

        try:
            with open(path, "r") as file:
                lines = [
                    line.strip().lower()
                    for line in file
                    if line.strip()
                    and not line.lstrip().startswith(("#", "//", "/*", ";"))
                ]

            if specific:
                if isinstance(specific, str):
                    lines = [pkg for pkg in lines if pkg == specific]
                else:
                    lines = [pkg for pkg in lines if pkg in specific]

            for pkg in lines:
                os.system(f"python3 -m pip install {pkg}")

            return True if not c else lines

        except FileNotFoundError:
            return False
   
class Ports:
    """
    A comprehensive representation of network ports for Nmap-style scanning.

    This class provides types, validation, parsing, and utility methods
    for single ports, sequences of ports, port ranges, exclusions, and services.

    Nested Classes:
        Single:
            Represents a single TCP/UDP port. Valid values are 1-65535.
        Sequence:
            Represents a list of individual ports. Each port must be 1-65535.
        Range:
            Represents a range of ports as a string, e.g., "80-443".
        ExclusionRange:
            Represents a set of ports with an optional list of exclusions.
        ServicePort:
            Represents a known service and its corresponding port number.
        TopPortsExtendable:
            Base class for extendable top ports definitions.
        TopPorts:
            Example implementation of the top ports list (_TOP1000).

    Attributes:
        port:
            Can hold a Single, Sequence, or Range object.
        SingleClass:
            Reference to the inner Single class for convenience.
        SequenceClass:
            Reference to the inner Sequence class for convenience.
        RangeClass:
            Reference to the inner Range class for convenience.

    Class Methods:
        parse(port_string: str) -> list[Port] | ExclusionRange:
            Converts a string like "22,80,443,8000-8100,!23,http" into
            a list of Ports objects or an ExclusionRange object.
        normalize(parsed) -> tuple[list[int], list[int]]:
            Converts the result of parse() into two lists:
            the included ports and the excluded ports.
        service_to_port(service: str) -> int:
            Maps a known service name (e.g., "http") to its default port number.

    Static Methods:
        chart(sequence: Single | Sequence | Range) -> str:
            Converts a port object into its string representation.

    Instance Methods:
        __init__(port=None):
            Initializes a Ports object with an optional port object.
        construct(strict: bool) -> int | list[int] | str:
            Returns the value of the port object.
            Raises an exception if strict mode is enabled and no port is set.

    Port Type:
        Port = Union[Single, Sequence, Range, ServicePort]
        Represents any valid type of port that this class can handle.

    Example Usage:
        p1 = Ports.Single(22)
        p2 = Ports.Sequence([80, 443])
        p3 = Ports.Range("8000-8100")
        ports = Ports(p1)
        value = ports.construct(strict=True)
        parsed_ports = Ports.parse("22,80-90,!23,http")
        include, exclude = Ports.normalize(parsed_ports)
        charted = Ports.chart(p2)
    """    
    @dataclass(frozen=True)
    class Single:
        """
        Represents a single TCP/UDP port.

        Attributes:
            value (int): Port number between 1 and 65535.

        Raises:
            ValueError: If port number is out of valid range.
        """
        value: int
        def __post_init__(self):
            if not (1 <= self.value <= 65535):
                raise ValueError("Port must be 1-65535")
    
    @dataclass(frozen=True)
    class NoReturn:
        """
        Represents a No Return Type

        Attributes:
            value (None): No return 
        """
        value: None
            
    @dataclass(frozen=True)
    class Sequence:
        """
        Represents a sequence (list) of individual ports.

        Attributes:
            value (List[int]): List of ports, each between 1 and 65535.

        Raises:
            ValueError: If any port in the sequence is out of range.
        """
        value: List[int]
        def __post_init__(self):
            if not all(1 <= p <= 65535 for p in self.value):
                raise ValueError("All ports must be 1-65535")
            
    @dataclass(frozen=True)
    class Range:
        """
        Represents a range of ports.

        Attributes:
            value (str): Range in format "start-end", e.g., "80-443".

        Raises:
            ValueError: If range format is invalid or ports are out of bounds.
        """
        value: str
        def __post_init__(self):
            parts = self.value.split('-')
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                raise ValueError(f"Invalid range: {self.value}")
            start, end = map(int, parts)
            if not (1 <= start <= 65535 and 1 <= end <= 65535 and start < end):
                raise ValueError(f"Range out of bounds: {self.value}")
    
    @dataclass(frozen=True)
    class ExclusionRange:
        """
        Represents included ports with optional exclusions.

        Attributes:
            include (List[int]): Ports to include.
            exclude (List[int]): Ports to exclude.
        """
        include: List[int]
        exclude: List[int]
        
    @dataclass(frozen=True)
    class ServicePort:
        """
        Represents a known service and its port.

        Attributes:
            service (str): Name of the service (e.g., "http").
            port (int): Corresponding port number.
        """
        service: str
        port: int
    
    @disjoint_base
    class TopPortsExtendable:
        """
        Base class for defining extendable lists of top ports.
        """
        ...
    class TopPorts(TopPortsExtendable):
        """
        Example top ports implementation.

        Attributes:
            _TOP1000 (List[int]): List of the 1000 most commonly used ports.
        """
        _TOP1000: list[int] = [80, 443, 22, 21, 23, ...]
        
    
    Port = Union["Ports.Single", "Ports.Sequence", "Ports.Range", "Ports.ServicePort", "Ports.ExclusionRange"]
    
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, port: Port) -> None: ...
    def __init__(self, port: Port | None = None) -> None:
        """
        Initialize a Ports object with an optional port value.

        The Ports object can hold a single port, a sequence of ports, 
        a port range, or a service port. If no port is provided, the object 
        can be used later to assign or parse ports.

        Args:
            port (Single | Sequence | Range | ServicePort | None, optional):
                The port object to initialize this Ports instance with.
                - Single: Represents a single port number (1-65535).
                - Sequence: Represents a list of ports, e.g., [22, 80, 443].
                - Range: Represents a port range as a string, e.g., "8000-8100".
                - ServicePort: Represents a known service and its port number.
                - None: Creates an empty Ports object, which can be assigned or 
                  parsed later.

        Attributes Initialized:
            self.port: Stores the assigned port object or None if no port is given.
            self.SingleClass: Convenience reference to the inner Single class.
            self.SequenceClass: Convenience reference to the inner Sequence class.
            self.RangeClass: Convenience reference to the inner Range class.

        Behavior:
            - If a valid port object is provided, it is stored in `self.port`.
            - If None is provided, `self.port` is set to None.
            - The class-level references to Single, Sequence, and Range are 
              stored in instance attributes for easy access.

        Usage Examples:
            # Initialize with a single port
            sp = Ports.Single(22)
            ports = Ports(sp)
            print(ports.port.value)  # 22

            # Initialize with a sequence of ports
            seq = Ports.Sequence([80, 443])
            ports_seq = Ports(seq)
            print(ports_seq.port.value)  # [80, 443]

            # Initialize with a port range
            rng = Ports.Range("8000-8100")
            ports_range = Ports(rng)
            print(ports_range.port.value)  # "8000-8100"

            # Initialize an empty Ports object
            empty_ports = Ports()
            print(empty_ports.port)  # None
        """
        self.port = port
        self.SingleClass = self.Single
        self.SequenceClass = self.Sequence
        self.RangeClass = self.Range

    def construct(self, strict: bool, /) -> int | list[int] | str:
        """
        Return the value of the assigned port object.

        Args:
            strict (bool): If True, raises an exception if no port is set.

        Returns:
            int | List[int] | str: Value of Single, Sequence, or Range.

        Raises:
            Exception: If strict is True and no port is assigned.
            TypeError: If the port type is unsupported.
        """
        if not strict:
            raise Exception("Strict mode required")

        if self.port is None:
            raise ValueError("No port set")

        if isinstance(self.port, self.Single):
            return self.port.value
        elif isinstance(self.port, self.Sequence):
            return self.port.value
        elif isinstance(self.port, self.Range):
            return self.port.value
        else:
            raise TypeError(f"Unsupported port type: {type(self.port)}")

    @classmethod
    def parse(cls, port_string: str) -> list[Port] | "Ports.ExclusionRange":
        """
        Parse a string into Ports objects or an ExclusionRange.

        Args:
            port_string (str): Port string like "22,80-90,!23,http".

        Returns:
            list[Port] | ExclusionRange: Parsed port objects or exclusions.

        Raises:
            ValueError: For invalid port strings or formats.
        """
        include: List[int] = []
        exclude: List[int] = []
        result: List[Ports.Port] = []
        items = [s.strip() for s in port_string.split(",")]
        for item in items:
            if item.startswith("!"):
                port_str = item[1:]
                if port_str.isdigit():
                    exclude.append(int(port_str))
                else:
                    raise ValueError(f"Invalid exclusion port: {item}")
                continue
            if re.fullmatch(r"\d+-\d+", item):
                r = Ports.Range(item)
                result.append(r)
                start, end = map(int, item.split("-"))
                include.extend(range(start, end + 1))
                continue
            if item.isdigit():
                val = int(item)
                s = Ports.Single(val)
                result.append(s)
                include.append(val)
                continue
            result.append(Ports.ServicePort(service=item, port=cls.service_to_port(item)))
        if exclude:
            return Ports.ExclusionRange(include=include, exclude=exclude)
        return result
    
    @staticmethod
    def normalize(parsed) -> tuple[list[int], list[int]]:
        """
        Convert parsed Ports objects into include and exclude lists.

        Args:
            parsed (list[Port] | ExclusionRange): Parsed port objects.

        Returns:
            tuple[List[int], List[int]]: Included and excluded ports.
        """
        if isinstance(parsed, Ports.ExclusionRange):
            return parsed.include, parsed.exclude
        include: list[int] = []
        exclude: list[int] = []
        for p in parsed:
            if isinstance(p, Ports.Single):
                include.append(p.value)
            elif isinstance(p, Ports.Sequence):
                include.extend(p.value)
            elif isinstance(p, Ports.Range):
                start, end = map(int, p.value.split("-"))
                include.extend(range(start, end + 1))
            elif isinstance(p, Ports.ServicePort):
                include.append(p.port)
        return include, exclude
    
    @staticmethod
    def chart(sequence: Ports.Single | Ports.Sequence | Ports.Range) -> str:
        """
        Convert a port object into a string representation.

        Args:
            sequence (Single | Sequence | Range): Port object to chart.

        Returns:
            str: String representation of the port(s).

        Raises:
            TypeError: If the port type is unsupported.
        """
        if isinstance(sequence, Ports.Single):
            return str(sequence.value)
        elif isinstance(sequence, Ports.Sequence):
            return ",".join(str(p) for p in sequence.value)
        elif isinstance(sequence, Ports.Range):
            return sequence.value
        else:
            raise TypeError(f"Unsupported port type: {type(sequence)}")
        
    @property
    def flag(self) -> "Ports.NoReturn": return Ports.NoReturn.value

class Hosts:
    """
    Represents and manages scan targets (hosts).
    """

    @dataclass(frozen=True)
    class Single:
        """
        Represents a single host or IP address.

        Example:
            "192.168.1.1"
            "example.com"
        """
        value: str
        
        def __post_init__(self):
            Hosts.validate_single(self.value)

    @dataclass(frozen=True)
    class Sequence:
        """
        Represents multiple hosts separated logically.

        Example:
            ["192.168.1.1", "example.com"]
        """
        value: list[str]
        
        def __post_init__(self):
            for h in self.value:
                Hosts.validate_single(h)

    @dataclass(frozen=True)
    class Range:
        """
        Represents an IP range.

        Example:
            "192.168.1.1-20"
        """
        value: str
        
        def __post_init__(self):
            Hosts.validate_range(self.value)

    @dataclass(frozen=True)
    class CIDR:
        """
        Represents a CIDR subnet.

        Example:
            "192.168.1.0/24"
        """
        value: str
        
        def __post_init__(self):
            Hosts.validate_cidr(self.value)

    @dataclass(frozen=True)
    class Exclusion:
        """
        Represents excluded hosts.

        Example:
            ["192.168.1.5"]
        """
        value: list[str]

    @dataclass(frozen=True)
    class File:
        """
        Represents hosts loaded from a file.

        Example:
            "@hosts.txt"
        """
        path: str

    Host: typing.TypeAlias = (
        Literal[
            "Hosts.Single",
            "Hosts.Sequence",
            "Hosts.Range",
            "Hosts.CIDR",
            "Hosts.Exclusion",
            "Hosts.File",
        ]
    )

    def __init__(self, host: Host | None = None) -> None:
        """
        Initialize a Hosts object with an optional host definition.

        Args:
            host:
                One of the Hosts nested types or None.
        """
        self.host = host

    @staticmethod
    def chart(host) -> str:
        """
        Convert a host object into its string representation.
        """
        if isinstance(host, Hosts.Single):
            return host.value
        if isinstance(host, Hosts.Sequence):
            return ",".join(host.value)
        if isinstance(host, Hosts.Range):
            return host.value
        if isinstance(host, Hosts.CIDR):
            return host.value
        if isinstance(host, Hosts.Exclusion):
            return ",".join(f"!{h}" for h in host.value)
        if isinstance(host, Hosts.File):
            return f"@{host.path}"

        raise TypeError(f"Unsupported host type: {type(host)}")

    @staticmethod
    def validate_single(value: str) -> None:
        """
        Validate a single host value.

        Accepts:
        - IPv4 / IPv6
        - Hostnames
        """
        try:
            ipaddress.ip_address(value)
            return
        except ValueError:
            pass

        hostname_re = re.compile(
            r"^(?=.{1,253}$)([a-zA-Z0-9-]{1,63}\.)*[a-zA-Z]{2,63}$"
        )
        if not hostname_re.match(value):
            raise ValueError(f"Invalid host: {value}")
        
    @staticmethod
    def validate_cidr(value: str) -> None:
        try:
            ipaddress.ip_network(value, strict=False)
        except ValueError:
            raise ValueError(f"Invalid CIDR: {value}")

    @staticmethod
    def validate_range(value: str) -> None:
        if "-" not in value:
            raise ValueError(f"Invalid range: {value}")
    
        base, end = value.rsplit(".", 1)
        if not end.isdigit():
            raise ValueError(f"Invalid range end: {value}")
    
        start_ip = f"{base}.0"
        ipaddress.ip_address(start_ip)
    
    @classmethod
    def parse(cls, host_string: str) -> list[Host]:
        """
        Parse a host string into Host objects.

        Example:
            "192.168.1.1,example.com,!192.168.1.5,192.168.1.0/24"
        """
        result: list[Hosts.Host] = []

        for item in map(str.strip, host_string.split(",")):
            if item.startswith("!"):
                result.append(cls.Exclusion([item[1:]]))
                continue

            if item.startswith("@"):
                result.append(cls.File(item[1:]))
                continue

            if "/" in item:
                result.append(cls.CIDR(item))
                continue

            if "-" in item:
                result.append(cls.Range(item))
                continue

            result.append(cls.Single(item))

        return result

    @staticmethod
    def normalize(parsed: list[Host]) -> tuple[list[str], list[str]]:
        """
        Normalize parsed hosts into include / exclude lists.
        """
        include: list[str] = []
        exclude: list[str] = []

        for h in parsed:
            if isinstance(h, Hosts.Single):
                include.append(h.value)

            elif isinstance(h, Hosts.Sequence):
                include.extend(h.value)

            elif isinstance(h, Hosts.Range):
                include.append(h.value)

            elif isinstance(h, Hosts.CIDR):
                include.append(h.value)

            elif isinstance(h, Hosts.Exclusion):
                exclude.extend(h.value)

            elif isinstance(h, Hosts.File):
                include.append(f"@{h.path}")

        return include, exclude

    def chart_self(self) -> str:
        """
        Chart the instance host.
        """
        if self.host is None:
            raise ValueError("No host set")
        return self.chart(self.host)
    
    @staticmethod
    def expand_cidr(value: str) -> list[str]:
        net = ipaddress.ip_network(value, strict=False)
        return [str(ip) for ip in net.hosts()]

class Switches:
    """
    Authoritative controller for ALL Nmap scan and discovery switches.

    Enforces:
    - Valid scan names
    - Required values
    - Mutual exclusion rules
    - Correct CLI rendering
    """

    SCANS: dict[str, dict] = {
        "SYN":        {"flag": "-sS", "group": "PORT_SCAN"},
        "CONNECT":    {"flag": "-sT", "group": "PORT_SCAN"},
        "ACK":        {"flag": "-sA", "group": "PORT_SCAN"},
        "WINDOW":     {"flag": "-sW", "group": "PORT_SCAN"},
        "MAIMON":     {"flag": "-sM", "group": "PORT_SCAN"},
        "FIN":        {"flag": "-sF", "group": "PORT_SCAN"},
        "NULL":       {"flag": "-sN", "group": "PORT_SCAN"},
        "XMAS":       {"flag": "-sX", "group": "PORT_SCAN"},
        "UDP":        {"flag": "-sU", "group": "PORT_SCAN"},
        "SCTP_INIT":  {"flag": "-sY", "group": "PORT_SCAN"},
        "SCTP_COOKIE":{"flag": "-sZ", "group": "PORT_SCAN"},
        "IP_PROTO":   {"flag": "-sO", "group": "PORT_SCAN"},

        "IDLE": {
            "flag": "-sI",
            "group": "PORT_SCAN",
            "value_required": True
        },

        "PING_ONLY":  {"flag": "-sn", "group": "DISCOVERY"},
        "LIST":       {"flag": "-sL", "group": "DISCOVERY"},
        "NO_PING":    {"flag": "-Pn", "group": "DISCOVERY"},

        "VERSION":    {"flag": "-sV", "group": "DETECTION"},
        "OS":         {"flag": "-O",  "group": "DETECTION"},
        "AGGRESSIVE": {"flag": "-A",  "group": "DETECTION"},

        "TCP_SYN_PING": {
            "flag": "-PS",
            "group": "DISCOVERY_PROBE",
            "value_optional": True
        },
        "TCP_ACK_PING": {
            "flag": "-PA",
            "group": "DISCOVERY_PROBE",
            "value_optional": True
        },
        "UDP_PING": {
            "flag": "-PU",
            "group": "DISCOVERY_PROBE",
            "value_optional": True
        },
        "ARP_PING": {
            "flag": "-PR",
            "group": "DISCOVERY_PROBE"
        },
    }
    EXCLUSIVE_GROUPS = {
        "PORT_SCAN",
        "DISCOVERY",
    }

    def __init__(self) -> None:
        self._enabled: dict[str, str] = {}
        self._order: list[str] = []

    def add(self, scan: str, value: str | None = None) -> "Switches":
        scan = scan.upper()

        if scan not in self.SCANS:
            raise ValueError(f"Unknown scan type: {scan}")

        meta = self.SCANS[scan]
        group = meta["group"]

        self._validate_conflicts(scan, group)

        if meta.get("value_required") and not value:
            raise ValueError(f"Scan '{scan}' requires a value")

        if meta.get("value_optional") and value:
            rendered = f"{meta['flag']}{value}"
        elif value:
            rendered = f"{meta['flag']} {value}"
        else:
            rendered = meta["flag"]

        self._enabled[scan] = rendered
        if scan not in self._order:
            self._order.append(scan)

        return self

    def remove(self, scan: str) -> "Switches":
        scan = scan.upper()
        self._enabled.pop(scan, None)
        if scan in self._order:
            self._order.remove(scan)
        return self

    def clear(self) -> None:
        self._enabled.clear()
        self._order.clear()

    def _validate_conflicts(self, scan: str, group: str) -> None:
        if group not in self.EXCLUSIVE_GROUPS:
            return

        for existing in self._enabled:
            if self.SCANS[existing]["group"] == group:
                raise ValueError(
                    f"Scan '{scan}' conflicts with already enabled '{existing}'"
                )
                
    def render(self) -> str:
        return " ".join(self._enabled[s] for s in self._order)

    def __str__(self) -> str:
        return self.render()

    def syn(self): return self.add("SYN")
    def connect(self): return self.add("CONNECT")
    def udp(self): return self.add("UDP")
    def fin(self): return self.add("FIN")
    def null(self): return self.add("NULL")
    def xmas(self): return self.add("XMAS")
    def idle(self, zombie: str): return self.add("IDLE", zombie)
    def ping_only(self): return self.add("PING_ONLY")
    def no_ping(self): return self.add("NO_PING")
    def list(self): return self.add("LIST")
    def version(self): return self.add("VERSION")
    def os(self): return self.add("OS")
    def aggressive(self): return self.add("AGGRESSIVE")


class Nmap:
    """
    pynmap — Python Nmap Wrapper and Scan Utilities
    ===============================================

    This module provides a high-level, type-safe Python interface to Nmap-style
    network scanning. It includes classes for managing hosts, ports, scan switches,
    and OS detection, along with utilities for parsing, validating, and rendering
    scan targets and options into a fully formed Nmap CLI command.

    Purpose
    -------
    The `pynmap` library is designed to make Nmap scanning programmatically
    accessible in Python while maintaining strict type safety, validation, and
    chainable, human-readable APIs. It allows the construction of complex scans
    with hosts, ports, exclusions, timing templates, and protocol-specific options
    without manually assembling command-line strings.

    Core Components
    ---------------
    1. **NmapComponent**
       - Provides standardized port types (single, range, sequence) with validation
         and parsing utilities.
       - Helps safely represent ports in Nmap-style scanning.

    2. **OSDetection**
       - Detects the operating system of the current environment.
       - Supports short/raw (`win`, `linux`, `darwin`) and full names
         (`windows`, `linux`, `mac`).

    3. **NmapPackage**
       - Helper to install Python packages from files or lists.
       - Supports multiple overloads and selective package installation.

    4. **Ports**
       - Comprehensive representation of ports:
         - Single ports, sequences, ranges, exclusions, known service ports.
       - Parsing strings like `"22,80-90,!23,http"`.
       - Normalization to included/excluded port lists.
       - Charting ports to CLI-ready strings.

    5. **Hosts**
       - Type-safe host representation:
         - Single host/IP, sequence, IP range, CIDR subnet, exclusions, file-based hosts.
       - Parsing and normalization of host strings.
       - Converts to Nmap-compatible CLI formats.

    6. **Switches**
       - Chainable controller for all Nmap scan and discovery switches.
       - Enforces required values, mutual exclusions, and correct CLI rendering.
       - Pre-defined common switches: SYN, UDP, FIN, XMAS, OS detection, version detection, etc.

    7. **Nmap**
       - High-level Nmap command builder combining Hosts, Ports, and Switches.
       - Chainable API for hosts, ports, scan types, timing templates, and max packet rate.
       - Generates fully valid Nmap CLI commands with `.build()` or `str()`.

    Usage Examples
    --------------

    **Build a basic Nmap scan:**
    ```python
    from pynmap import Nmap

    cmd = (
        Nmap()
        .hosts("192.168.1.1", "scanme.nmap.org")
        .ports(22, 80, "8000-8100", exclude=23)
        .timing(3)
        .max_rate(1000)
        .scan.syn()
    )

    print(cmd)
    # Example Output:
    # nmap -sS -T3 --max-rate 1000 -p 22,80,8000-8100 192.168.1.1,scanme.nmap.org
    """

    def __init__(self) -> None:
        self._hosts: Hosts | None = None
        self._ports: Ports | None = None
        self._switches = Switches()
        self._options: list[str] = []


    def hosts(self, *targets: str) -> "Nmap":
        """
        Define scan targets.

        Example:
            .hosts("192.168.1.1", "scanme.nmap.org")
        """
        if not targets:
            raise ValueError("At least one host is required")

        if len(targets) == 1:
            self._hosts = Hosts(Hosts.Single(targets[0]))
        else:
            self._hosts = Hosts(Hosts.Sequence(list(targets)))

        return self

    def ports(self, *ports, exclude=None) -> "Nmap":
        """
        Define target ports.

        Example:
            .ports(22, 80, "8000-8100", exclude=23)
        """
        if not ports:
            raise ValueError("At least one port must be specified")

        base = Ports.parse(",".join(map(str, ports)))

        if exclude is not None:
            exclusion = Ports.parse(f"!{exclude}")
            base = Ports.merge(base, exclusion)

        self._ports = base
        return self

    @property
    def scan(self) -> Switches:
        """
        Access scan-type switches.

        Example:
            .scan.syn().scan.version()
        """
        return self._switches

    def timing(self, template: int) -> "Nmap":
        """
        Set timing template (0-5).

        Maps to: -T<template>
        """
        if not 0 <= template <= 5:
            raise ValueError("Timing template must be between 0 and 5")

        self._options.append(f"-T{template}")
        return self

    def max_rate(self, rate: int) -> "Nmap":
        """
        Set max packet rate.

        Maps to: --max-rate <rate>
        """
        if rate <= 0:
            raise ValueError("Rate must be positive")

        self._options.append(f"--max-rate {rate}")
        return self

    def build(self) -> str:
        """
        Build the final nmap command.
        """
        parts: list[str] = ["nmap"]

        if self._switches:
            rendered = str(self._switches)
            if rendered:
                parts.append(rendered)

        parts.extend(self._options)

        if self._ports:
            parts.append(f"-p {Ports.chart(self._ports.port)}")

        if self._hosts:
            parts.append(Hosts.chart(self._hosts.host))

        return " ".join(parts)

    def __str__(self) -> str:
        return self.build()
    
    
class CSVConfigError(Exception):
    """Base exception for CSV configuration errors."""

class CSVSchemaError(CSVConfigError):
    """Raised when schema validation fails."""

class CSVTransactionError(CSVConfigError):
    """Raised when transaction handling fails."""


class CSVIO:
    """
    Advanced CSV configuration manager with transactional updates, schema enforcement,
    version snapshots, diffing, uniqueness constraints, computed columns, hooks,
    import/export, pagination, and conflict-aware upserts.

    Supports both single and composite keys and maintains a change history for auditing.
    """

    def __init__(
        self,
        path: str,
        key_field: Optional[str] = None,
        composite_key: Optional[Tuple[str, ...]] = None,
        schema: Optional[Dict[str, type]] = None,
        required: Optional[List[str]] = None,
        defaults: Optional[Dict[str, Any]] = None,
        unique: Optional[List[str]] = None,
        computed: Optional[Dict[str, Callable[[Dict[str, Any]], Any]]] = None,
        validators: Optional[List[Callable[[Dict[str, Any]], None]]] = None,
        auto_cast: bool = True,
    ):
        self.path = Path(path)
        self.key_field = key_field
        self.composite_key = composite_key
        self.schema = schema or {}
        self.required = required or []
        self.defaults = defaults or {}
        self.unique = unique or []
        self.computed = computed or {}
        self.validators = validators or []
        self.auto_cast = auto_cast

        self.rows: List[Dict[str, Any]] = []
        self._headers: List[str] = []
        self._index: Dict[Any, Dict[str, Any]] = {}
        self._dirty = False
        self._history: List[Dict[str, Any]] = []
        self._snapshots: List[List[Dict[str, Any]]] = []
        self._in_transaction = False

        self._hooks = {
            "before_load": [],
            "after_load": [],
            "before_save": [],
            "after_save": [],
        }

        if self.path.exists():
            self.load()

    def _run_hooks(self, name: str) -> None:
        for hook in self._hooks.get(name, []):
            hook(self)

    def register_hook(self, event: str, func: Callable[["CSVIO"], None]) -> None:
        """
        Register a lifecycle hook. Supported events:
        before_load, after_load, before_save, after_save.
        """
        if event not in self._hooks:
            raise CSVConfigError(f"Unsupported hook: {event}")
        self._hooks[event].append(func)

    def _cast(self, value: Any) -> Any:
        """
        Coerce values into native Python types.
        """
        if not self.auto_cast or value is None:
            return value

        if isinstance(value, (bool, int, float, list, dict)):
            return value

        v = str(value).strip()

        if v.lower() in ("true", "false"):
            return v.lower() == "true"

        try:
            if v.startswith("[") or v.startswith("{"):
                return json.loads(v)
        except Exception:
            pass

        try:
            if "." in v:
                return float(v)
            return int(v)
        except ValueError:
            pass

        if "," in v:
            return [self._cast(x) for x in v.split(",")]

        return v

    def _row_key(self, row: Dict[str, Any]) -> Any:
        """
        Compute the key for a row based on key_field or composite_key.
        """
        if self.composite_key:
            return tuple(row.get(k) for k in self.composite_key)
        if self.key_field:
            return row.get(self.key_field)
        return None

    def _hash_row(self, row: Dict[str, Any]) -> str:
        """
        Generate a stable hash for a row for change detection.
        """
        data = json.dumps(row, sort_keys=True, default=str)
        return hashlib.sha256(data.encode()).hexdigest()

    def _apply_defaults(self, row: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in self.defaults.items():
            row.setdefault(k, v)
        return row

    def _apply_computed(self, row: Dict[str, Any]) -> None:
        for k, func in self.computed.items():
            row[k] = func(row)

    def _validate_row(self, row: Dict[str, Any]) -> None:
        for field in self.required:
            if field not in row or row[field] in (None, ""):
                raise CSVSchemaError(f"Missing required field: {field}")

        for field, expected_type in self.schema.items():
            if field in row and row[field] is not None:
                if not isinstance(row[field], expected_type):
                    raise CSVSchemaError(
                        f"Field '{field}' expected {expected_type.__name__}, "
                        f"got {type(row[field]).__name__}"
                    )

        for validator in self.validators:
            validator(row)

    def _check_unique(self, row: Dict[str, Any]) -> None:
        for field in self.unique:
            value = row.get(field)
            for existing in self.rows:
                if existing is not row and existing.get(field) == value:
                    raise CSVSchemaError(f"Unique constraint failed for field: {field}")

    def _rebuild_index(self) -> None:
        self._index.clear()
        for row in self.rows:
            key = self._row_key(row)
            if key is not None:
                self._index[key] = row

    def load(self) -> None:
        """
        Load CSV into memory with validation, computed columns, and hooks.
        """
        self._run_hooks("before_load")

        with self.path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self._headers = reader.fieldnames or []
            self.rows = []

            for raw in reader:
                row = {k: self._cast(v) for k, v in raw.items()}
                row = self._apply_defaults(row)
                self._apply_computed(row)
                self._validate_row(row)
                self.rows.append(row)

        self._rebuild_index()
        self._dirty = False
        self._run_hooks("after_load")

    def save(self, atomic: bool = True) -> None:
        """
        Persist to disk with optional atomic write and hooks.
        """
        self._run_hooks("before_save")

        if not self._headers and self.rows:
            self._headers = list(self.rows[0].keys())

        target = self.path
        temp = target.with_suffix(".tmp")

        def _write(p: Path):
            with p.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self._headers)
                writer.writeheader()
                writer.writerows(self.rows)

        if atomic:
            _write(temp)
            shutil.move(temp, target)
        else:
            _write(target)

        self._dirty = False
        self._run_hooks("after_save")

    def transaction(self):
        """
        Context manager for transactional updates with automatic rollback on error.
        """
        manager = self

        class _Txn:
            def __enter__(self_inner):
                if manager._in_transaction:
                    raise CSVTransactionError("Nested transactions not supported")
                manager._snapshots.append(json.loads(json.dumps(manager.rows)))
                manager._in_transaction = True
                return manager

            def __exit__(self_inner, exc_type, exc, tb):
                if exc:
                    manager.rows = manager._snapshots.pop()
                    manager._rebuild_index()
                else:
                    manager._snapshots.pop()
                    manager._dirty = True
                manager._in_transaction = False

        return _Txn()

    def snapshot(self) -> None:
        """
        Store a version snapshot of the current state.
        """
        self._snapshots.append(json.loads(json.dumps(self.rows)))

    def rollback(self) -> None:
        """
        Roll back to the most recent snapshot.
        """
        if not self._snapshots:
            raise CSVTransactionError("No snapshot available")
        self.rows = self._snapshots.pop()
        self._rebuild_index()
        self._dirty = True

    def diff(self, other: Iterable[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Compute diff between current rows and another iterable of rows.
        """
        current = {self._hash_row(r): r for r in self.rows}
        other_map = {self._hash_row(r): r for r in other}

        added = [other_map[h] for h in other_map.keys() - current.keys()]
        removed = [current[h] for h in current.keys() - other_map.keys()]
        unchanged = [current[h] for h in current.keys() & other_map.keys()]

        return {"added": added, "removed": removed, "unchanged": unchanged}

    def upsert(self, row: Dict[str, Any], strategy: str = "replace") -> None:
        """
        Insert or update a row with conflict strategies: replace, merge, ignore.
        """
        row = {k: self._cast(v) for k, v in row.items()}
        row = self._apply_defaults(row)
        self._apply_computed(row)
        self._validate_row(row)

        key = self._row_key(row)

        if key in self._index:
            if strategy == "replace":
                self._index[key].update(row)
            elif strategy == "merge":
                for k, v in row.items():
                    if v is not None:
                        self._index[key][k] = v
            elif strategy == "ignore":
                return
            else:
                raise CSVConfigError(f"Unknown strategy: {strategy}")
        else:
            self.rows.append(row)

        self._check_unique(row)
        self._rebuild_index()
        self._dirty = True

    def query(self, expression: str) -> List[Dict[str, Any]]:
        """
        Evaluate a simple boolean expression against rows.
        Example: "enabled == True and port > 8000"
        """
        results = []
        for row in self.rows:
            try:
                if eval(expression, {}, row):
                    results.append(row)
            except Exception:
                continue
        return results

    def paginate(self, page: int, per_page: int) -> List[Dict[str, Any]]:
        """
        Return a slice of rows for pagination.
        """
        start = (page - 1) * per_page
        end = start + per_page
        return self.rows[start:end]

    def export_json(self, path: str) -> None:
        """
        Export rows to a JSON file.
        """
        with Path(path).open("w", encoding="utf-8") as f:
            json.dump(self.rows, f, indent=2, default=str)

    def import_json(self, path: str, strategy: str = "replace") -> None:
        """
        Import rows from JSON with upsert strategy.
        """
        with Path(path).open(encoding="utf-8") as f:
            data = json.load(f)
        for row in data:
            self.upsert(row, strategy=strategy)

    def history(self) -> List[Dict[str, Any]]:
        """
        Return the change history log.
        """
        return list(self._history)

    def log_change(self, action: str, row: Dict[str, Any]) -> None:
        """
        Append a change record to the history log.
        """
        self._history.append(
            {
                "action": action,
                "row": json.loads(json.dumps(row)),
                "hash": self._hash_row(row),
            }
        )

    def to_list(self) -> List[Dict[str, Any]]:
        """
        Return a shallow copy of all rows.
        """
        return list(self.rows)

    def __len__(self) -> int:
        """
        Return number of rows.
        """
        return len(self.rows)

def classhasattr(obj: object, att: str) -> bool:
    """
        classhasattr checks if passed object has str() attribute inside its structure

        Args:
            _obj_: type object
            _att_: type str
            object is passed to check if it has its family attribute

        Returns:
            **bool**
    """
    return hasattr(obj, att)


def resolvedotpath(path: str) -> str:
    dot = "@"

    if dot not in path:
        return ""

    if path.startswith(dot):
        path = path[1:]

    return path.replace(dot, "/")

def resolvepath(haystack: str, niddle: str, repl: str):
    if not all(isinstance(argu, str) for argu in [haystack, niddle, repl]):
        raise TypeError
    
    if niddle not in haystack:
        return ""
    
    return haystack.replace(niddle, repl)

class KeySignal:
    """
    Signal class to track keyboard keys.
    Stores the last key pressed and allows action triggers.
    """
    
    def __init__(self):
        self._last_key = None
        self._running = False
        self._lock = threading.Lock()
        self._thread = None

    @property
    def last_key(self):
        """Return the last pressed key."""
        with self._lock:
            return self._last_key

    def _on_key(self, event):
        with self._lock:
            self._last_key = event.name
        if event.name == "esc":
            self.stop()

    def start(self):
        """Start listening to keyboard in a background thread."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._listen, daemon=True)
            self._thread.start()

    def _listen(self):
        keyboard.on_press(self._on_key)
        while self._running:
            pass
        keyboard.unhook_all()

    def stop(self):
        """Stop listening."""
        self._running = False
        
class SIGINT(IntEnum):
    SUCCESS              = 0
    ERROR                = 1
    FAIL                 = 2
    ABORT                = -1
    WARN                 = -2
    FATAL                = -6
    FORCE                = -10
    """"""
    NETWORK_ERROR        = 3
    TIMEOUT              = 4
    INVALID_INPUT        = 5
    NOT_FOUND            = 6
    PERMISSION_DENIED    = 7
    AUTH_FAILED          = 8
    CONNECTION_LOST      = 9
    PARSE_ERROR          = 10
    CONFIG_MISSING       = 11
    CONFIG_INVALID       = 12
    DATABASE_ERROR       = 13
    IO_ERROR             = 14
    FILE_NOT_FOUND       = 15
    FILE_CORRUPT         = 16
    UNAUTHORIZED         = 17
    DEPRECATED           = 18
    RATE_LIMITED         = 19
    CONFLICT             = 20
    NOT_SUPPORTED        = 21
    ALREADY_EXISTS       = 22
    SERVICE_UNAVAILABLE  = 23
    PARTIAL_SUCCESS      = 24
    OVERFLOW             = 25
    UNDERFLOW            = 26
    MEMORY_ERROR         = 27
    CPU_OVERLOAD         = 28
    SECURITY_BREACH      = 29
    DATA_CORRUPTION      = 30
    INVALID_STATE        = 31
    TIME_TRAVEL          = 32
    UNKNOWN_ERROR        = 33
    INTERRUPTED          = 34
    UNSUPPORTED_FORMAT   = 35
    INVALID_TYPE         = 36
    RESOURCE_EXHAUSTED   = 37
    CONNECTION_REFUSED   = 38
    DEADLOCK             = 39
    QUOTA_EXCEEDED       = 40
    SERVICE_DEGRADED     = 41
    TEST_FLAG            = 42
    
class Result(Generic[T, E]):
    """
    A typed result container representing SUCCESS, WARN, ERROR, FAIL, or ABORT states.

    This is similar to Rust's `Result` type but supports multiple severity levels.

    Features:
        - Generic payload typing: Signal[int], Signal[str], etc.
        - Truthy on success (`if signal:`)
        - `unwrap()` to extract data or raise
        - `expect()` with custom message
        - `map()` to transform successful data
        - `to_exception()` for exception-based flows
        
        Represents a structured result signal.

    A Signal can be returned from functions to indicate success, failure,
    warning, or abort states without immediately raising exceptions.
    It can also be inspected and converted into an exception by higher-level code.

    This pattern is useful for:
        - validation pipelines
        - parsers
        - config loaders
        - non-exception control flow

    Args:
        code (SIGINT): Status code indicating the result type.
            Defaults to SIGINT.SUCCESS.
        message (str): Optional human-readable message.
        data (Any): Optional payload associated with the result.

    Attributes:
        code (SIGINT): The signal status code.
        message (str): Informational message.
        data (Any): Optional result data.

    Properties:
        ok (bool): True if the signal represents success.
        is_error (bool): True if the signal represents an error, failure, or abort.
        is_warn (bool): True if the signal represents a warning.

    Example:
        result = Result.success("Loaded config", data=config)

        if result.ok:
            use(result.data)
        elif result.is_warn:
            log_warning(result.message)
        else:
            raise RuntimeError(result.message)
    """

    __slots__ = ("code", "message", "data", "_warnings", "_context", "_time_ms", "_value", "_error")

    def __init__(self, code: SIGINT = SIGINT.SUCCESS, message: str = "", data: Optional[T] = None):
        """
        Initialize a Result object.

        Args:
            code (SIGINT, optional): Status code of the result. Defaults to SIGINT.SUCCESS.
            message (str, optional): Human-readable message. Defaults to empty string.
            data (Optional[T], optional): Payload of the result. Defaults to None.
        """
        if isinstance(code, int):
            code = SIGINT(code)
        elif not isinstance(code, SIGINT):
            raise TypeError(f"code must be SIGINT enum, got {type(code)}")
        self.code: SIGINT = code
        self.message: str = message or ""
        self.data: Optional[T] = data
        self._warnings: list[str] = []
        self._context: list[str] = []
        self._time_ms: Optional[float] = None
        self._value: Optional[T] = data
        self._error: Optional[str] = self.message if self.is_error else None

    @property
    def ok(self) -> bool:
        """Return True if the result represents success."""
        return self.code == SIGINT.SUCCESS

    @property
    def is_warn(self) -> bool:
        """Return True if the result represents a warning."""
        return self.code == SIGINT.WARN

    @property
    def is_error(self) -> bool:
        """Return True if the result represents an error, failure, or abort."""
        return self.code in {SIGINT.ERROR, SIGINT.FAIL, SIGINT.ABORT}

    def __bool__(self) -> bool:
        """Allow the Result to be truthy if it is successful."""
        return self.ok

    @classmethod
    def success(cls, message: str = "", data: Optional[T] = None) -> "Result[T]":
        """Create a successful Result."""
        return cls(SIGINT.SUCCESS, message, data)

    @classmethod
    def warn(cls, message: str = "", data: Optional[T] = None) -> "Result[T]":
        """Create a warning Result."""
        return cls(SIGINT.WARN, message, data)

    @classmethod
    def error(cls, message: str = "", data: Optional[T] = None) -> "Result[T]":
        """Create an error Result."""
        return cls(SIGINT.ERROR, message, data)

    @classmethod
    def fail(cls, message: str = "", data: Optional[T] = None) -> "Result[T]":
        """Create a fail Result."""
        return cls(SIGINT.FAIL, message, data)

    @classmethod
    def abort(cls, message: str = "", data: Optional[T] = None) -> "Result[T]":
        """Create an abort Result."""
        return cls(SIGINT.ABORT, message, data)

    def unwrap(self) -> T:
        """
        Return the contained successful value.

        Raises:
            RuntimeError: If the result is not successful.

        Returns:
            T: The value contained in a successful result.
        """
        if not self.ok:
            raise RuntimeError(self.message or f"Result {self.code.name} has no value")
        return self.data

    def expect(self, message: str) -> T:
        """
        Return the contained value, or raise an error with a custom message.

        Args:
            message (str): Custom error message if the result is not successful.

        Raises:
            RuntimeError: With the provided message if the result is not successful.

        Returns:
            T: The value contained in a successful result.
        """
        if not self.ok:
            raise RuntimeError(message)
        return self.data

    def unwrap_err(self) -> str:
        """
        Return the error message if the result is a failure.

        Raises:
            RuntimeError: If called on a successful result.

        Returns:
            str: The error message associated with the result.
        """
        if self.ok:
            raise RuntimeError("Called unwrap_err on SUCCESS result")
        return self.message

    def expect_err(self, message: str) -> str:
        """
        Return the error message, or raise an error with a custom message.

        Args:
            message (str): Custom error message if the result is successful.

        Raises:
            RuntimeError: With the provided message if the result is successful.

        Returns:
            str: The error message associated with the result.
        """
        if self.ok:
            raise RuntimeError(message)
        return self.message

    def unwrap_or(self, default: T) -> T:
        """
        Return the contained value if successful, or a default value otherwise.

        Args:
            default (T): Value to return if the result is not successful.

        Returns:
            T: The result value or the provided default.
        """
        return self.data if self.ok else default

    def map(self, func: Callable[[T], U]) -> "Result[U]":
        """
        Apply a function to the successful value, returning a new Result.

        Args:
            func (Callable[[T], U]): Function to transform the successful value.

        Returns:
            Result[U]: A new Result with the transformed value, or the original error.
        """
        if self.ok:
            try:
                return Result.success(self.message, func(self.data))
            except Exception as e:
                return Result.error(str(e))
        return Result(self.code, self.message, self.data)

    def map_err(self, func: Callable[[str], str]) -> "Result[T]":
        """
        Apply a function to the error message if the result is a failure.

        Args:
            func (Callable[[str], str]): Function to transform the error message.

        Returns:
            Result[T]: A new Result with the transformed error, or the original success.
        """
        if self.is_error:
            return Result(self.code, func(self.message), self.data)
        return self

    def and_then(self, func: Callable[[T], "Result[U]"]) -> "Result[U]":
        """
        Chain another computation that returns a Result if this result is successful.

        Args:
            func (Callable[[T], Result[U]]): Function to run on the successful value.

        Returns:
            Result[U]: The Result returned by the function, or the original error.
        """
        if self.ok:
            try:
                return func(self.data)
            except Exception as e:
                return Result.error(str(e))
        return Result(self.code, self.message, self.data)

    def or_else(self, func: Callable[[str], "Result[T]"]) -> "Result[T]":
        """
        Recover from an error by applying a function to the error message.

        Args:
            func (Callable[[str], Result[T]]): Function to produce a new Result from an error.

        Returns:
            Result[T]: The new Result returned by the function, or the original success.
        """
        if self.ok:
            return self
        return func(self.message)

    def inspect(self, func: Callable[[T], Any]) -> "Result[T]":
        """
        Run a side-effect function on the successful value without modifying it.

        Args:
            func (Callable[[T], Any]): Function to run on the successful value.

        Returns:
            Result[T]: The same Result unchanged.
        """
        if self.ok:
            func(self.data)
        return self

    def inspect_err(self, func: Callable[[str], Any]) -> "Result[T]":
        """
        Run a side-effect function on the error message without modifying it.

        Args:
            func (Callable[[str], Any]): Function to run on the error message.

        Returns:
            Result[T]: The same Result unchanged.
        """
        if self.is_error:
            func(self.message)
        return self

    def to_exception(self) -> None:
        """
        Raise a RuntimeError if the result is not successful.

        Raises:
            RuntimeError: With the result message if it is an error.
        """
        if not self.ok:
            raise RuntimeError(self.message or f"Result {self.code.name}")

    @staticmethod
    def capture(func: Callable[..., T], *args, **kwargs) -> "Result[T]":
        """
        Execute a function and capture its result, returning a Result object.

        Args:
            func (Callable[..., T]): Function to execute.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Result[T]: A successful Result if the function returns without exception,
                       otherwise an error Result with the exception message.
        """
        try:
            return Result.success(data=func(*args, **kwargs))
        except Exception as e:
            return Result.error(str(e))

    def __iter__(self) -> Iterator[T]:
        """
        Iterate over the contained value if successful.

        Yields:
            T: The contained value if the result is successful.
        """
        if self.ok:
            yield self.data

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another Result object.

        Args:
            other (object): Object to compare with.

        Returns:
            bool: True if the code, message, and data are all equal, False otherwise.
        """
        if not isinstance(other, Result):
            return False
        return (
            self.code == other.code
            and self.message == other.message
            and self.data == other.data
        )

    def __repr__(self) -> str:
        """
        Return the official string representation of the Result.

        Returns:
            str: String representation showing code, message, and data.
        """
        return (
            f"Result(code={self.code.name}, "
            f"message={self.message!r}, "
            f"data={self.data!r})"
        )
        
    def contains(self, value: T) -> bool:
        """Return True if SUCCESS and data equals the given value."""
        return self.ok and self.data == value

    def is_ok_and(self, predicate: Callable[[T], bool]) -> bool:
        """Return True if SUCCESS and predicate(data) is True."""
        return self.ok and predicate(self.data)  # type: ignore

    def is_err_and(self, predicate: Callable[[str], bool]) -> bool:
        """Return True if error and predicate(message) is True."""
        return self.is_error and predicate(self.message)

    def ok_value(self) -> Optional[T]:
        """Return data if SUCCESS else None."""
        return self.data if self.ok else None

    def err_value(self) -> Optional[str]:
        """Return message if error else None."""
        return self.message if self.is_error else None

    def unwrap_or_else(self, func: Callable[[str], T]) -> T:
        """Return data if SUCCESS else compute default from error message."""
        return self.data if self.ok else func(self.message)

    def unwrap_or_raise(self, exc_type: type[Exception]) -> T:
        """Raise a custom exception type if not SUCCESS."""
        if not self.ok:
            raise exc_type(self.message)
        return self.data

    def filter(self, predicate: Callable[[T], bool], err_msg: str) -> "Result[T]":
        """
        Keep SUCCESS only if predicate(data) is True, otherwise convert to ERROR.
        """
        if self.ok:
            try:
                if predicate(self.data):
                    return self
                return Result.error(err_msg)
            except Exception as e:
                return Result.error(str(e))
        return self

    def flatten(self) -> "Result[T]":
        """Flatten nested Result[Result[T]] into Result[T]."""
        if self.ok and isinstance(self.data, Result):
            return self.data
        return self

    def zip(self, other: "Result[U]") -> "Result[tuple[T, U]]":
        """
        Combine two SUCCESS results into a tuple.
        Propagates the first error encountered.
        """
        if not self.ok:
            return Result(self.code, self.message)
        if not other.ok:
            return Result(other.code, other.message)
        return Result.success(data=(self.data, other.data))

    def zip_with(self, other: "Result[U]", func: Callable[[T, U], Any]) -> "Result[Any]":
        """Zip two results and apply a function to their values."""
        return self.zip(other).map(lambda pair: func(pair[0], pair[1]))

    @staticmethod
    def combine(results: list["Result[T]"]) -> "Result[list[T]]":
        """
        Collect all SUCCESS values.
        If any ERROR/FAIL/ABORT occurs, return the first error.
        WARN values are included but preserved.
        """
        values: list[T] = []
        for r in results:
            if r.is_error:
                return Result(r.code, r.message)
            if r.ok or r.is_warn:
                values.append(r.data)
        return Result.success(data=values)

    @staticmethod
    def collect(results: list["Result[T]"]) -> "Result[list[T]]":
        """
        Rust-style collect:
        - All SUCCESS → SUCCESS[list]
        - First error → ERROR
        """
        values: list[T] = []
        for r in results:
            if not r.ok:
                return Result(r.code, r.message)
            values.append(r.data)
        return Result.success(data=values)

    def tap(self, func: Callable[[T], Any]) -> "Result[T]":
        """Run side-effect on SUCCESS without changing the value."""
        if self.ok:
            func(self.data)
        return self

    def tap_err(self, func: Callable[[str], Any]) -> "Result[T]":
        """Run side-effect on error without changing the result."""
        if self.is_error:
            func(self.message)
        return self

    def promote_warn_to_error(self) -> "Result[T]":
        """Convert WARN into ERROR."""
        if self.is_warn:
            return Result.error(self.message, self.data)
        return self

    def ignore_warn(self) -> "Result[T]":
        """Convert WARN into SUCCESS."""
        if self.is_warn:
            return Result.success(self.message, self.data)
        return self
    
    def __len__(self) -> int:
        if self.ok and hasattr(self.data, "__len__"):
            return len(self.data)
        return 0

    def __getitem__(self, key):
        if not self.ok:
            raise RuntimeError(self.message)
        return self.data[key]

    def __contains__(self, item) -> bool:
        return self.ok and hasattr(self.data, "__contains__") and item in self.data

    def __getattr__(self, name: str):
        if self.ok and hasattr(self.data, name):
            return getattr(self.data, name)
        raise AttributeError(name)

    def __call__(self, *args, **kwargs):
        if not self.ok:
            raise RuntimeError(self.message)
        if callable(self.data):
            return self.data(*args, **kwargs)
        raise TypeError("Result data is not callable")

    def __enter__(self) -> T:
        if not self.ok:
            raise RuntimeError(self.message)
        return self.data

    def __exit__(self, exc_type, exc, tb):
        return False

    def __or__(self, other: "Result[T]") -> "Result[T]":
        """Fallback if self is error."""
        return self if self.ok else other

    def __and__(self, other: "Result[U]") -> "Result[tuple[T, U]]":
        """Zip operator."""
        return self.zip(other)

    def __rshift__(self, func: Callable[[T], "Result[U]"]) -> "Result[U]":
        """Chain operator (and_then)."""
        return self.and_then(func)

    def __invert__(self) -> T:
        """~result → unwrap()"""
        return self.unwrap()

    def match(
        self,
        ok: Optional[Callable[[T], U]] = None,
        err: Optional[Callable[[str], U]] = None,
        warn: Optional[Callable[[T], U]] = None,
    ) -> Optional[U]:
        """
        Pattern-match on the result state and execute a corresponding function.

        This allows handling success, warning, and error cases in a single call.

        Args:
            ok (Optional[Callable[[T], U]]): Function to call if the result is successful.
                Receives the contained value as an argument.
            err (Optional[Callable[[str], U]]): Function to call if the result is an error, fail, or abort.
                Receives the error message as an argument.
            warn (Optional[Callable[[T], U]]): Function to call if the result is a warning.
                Receives the contained value as an argument.

        Returns:
            Optional[U]: The return value of the called function, or None if no function matches the result state.
        """
        if self.ok and ok:
            return ok(self.data)
        if self.is_warn and warn:
            return warn(self.data)
        if self.is_error and err:
            return err(self.message)
        return None

    def recover(self, func: Callable[[str], T]) -> "Result[T]":
        """Convert error into success using a recovery function."""
        if self.ok:
            return self
        try:
            return Result.success(data=func(self.message))
        except Exception as e:
            return Result.error(str(e))

    def ensure(self, predicate: Callable[[T], bool], msg: str) -> "Result[T]":
        """Ensure a condition on SUCCESS value."""
        if self.ok and not predicate(self.data):
            return Result.error(msg)
        return self

    def to_optional(self) -> Optional[T]:
        return self.data if self.ok else None

    def to_list(self) -> list[T]:
        return [self.data] if self.ok else []
    
    def push_context(self, ctx: str) -> "Result[T]":
        """Attach contextual information (e.g., 'database.host')."""
        self._context.append(ctx)
        return self

    def context_str(self) -> str:
        """Return joined context path."""
        return ".".join(self._context)
        
    def add_warning(self, message: str) -> "Result[T]":
        """Attach a warning without failing the result."""
        self._warnings.append(message)
        if self.code == SIGINT.SUCCESS:
            self.code = SIGINT.WARN
        return self

    @property
    def warnings(self) -> list[str]:
        """
        Convert the Result into an optional value.

        Returns:
            Optional[T]: The contained value if successful, otherwise None.
        """
        return list(self._warnings)

    def has_warnings(self) -> bool:
        """
        Convert the Result into a list containing the value if successful.

        Returns:
            list[T]: A single-element list with the contained value if successful, otherwise an empty list.
        """
        return bool(self._warnings)
    
    def promote_warnings(self) -> "Result[T]":
        """Convert WARN state into ERROR."""
        if self._warnings and not self.is_error:
            self.code = SIGINT.ERROR
        return self

    def clear_warnings(self) -> "Result[T]":
        """Remove all warnings."""
        self._warnings.clear()
        if self.code == SIGINT.WARN:
            self.code = SIGINT.SUCCESS
        return self


    def timeit(self, func: Callable[[], U]) -> "Result[U]":
        """Measure execution time and store in result."""
        start = time.perf_counter()
        try:
            value = func()
            elapsed = (time.perf_counter() - start) * 1000
            r = Result.success(data=value)
            r._time_ms = elapsed
            return r
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            r = Result.error(str(e))
            r._time_ms = elapsed
            return r

    @property
    def time_ms(self) -> float | None:
        """
        Get the elapsed time associated with this Result in milliseconds.

        Returns:
            float | None: The elapsed time in milliseconds, or None if not set.
        """
        return self._time_ms
    
    @staticmethod
    def validate_all(validators: list[Callable[[], "Result[Any]"]]) -> "Result[list[Any]]":
        """
        Run multiple validators.
        Collect all SUCCESS/WARN values.
        Fail on first ERROR/FAIL/ABORT.
        """
        values = []
        for v in validators:
            r = v()
            if r.is_error:
                return r
            values.append(r.data)
        return Result.success(data=values)
    
    @staticmethod
    def collect_all(results: list["Result[T]"]) -> "Result[list[T]]":
        """
        Collect values even if WARN.
        Fail only on ERROR/FAIL/ABORT.
        """
        values: list[T] = []
        out = Result.success(data=values)

        for r in results:
            if r.is_error:
                return r
            if r.has_warnings():
                out._warnings.extend(r._warnings)
                out.code = SIGINT.WARN
            values.append(r.data)

        return out
    
    def profile(self, label: str = "") -> "Result[T]":
        """Print execution time if available."""
        if self._time_ms is not None:
            print(f"[Result] {label} took {self._time_ms:.2f} ms")
        return self
    
    def cast(self, type_: type[U]) -> "Result[U]":
        """
        Ensure the contained value is of a given type, returning a new Result.

        If the Result is successful and the data is of the specified type, a
        new successful Result is returned.  
        If the data is of a different type, an error Result is returned.  
        If the original Result is not successful, it is returned unchanged.

        Args:
            type_ (type[U]): The expected type for the contained value.

        Returns:
            Result[U]: 
                - Success with the data if it matches the type.
                - Error if the data type does not match.
                - Original Result if it was not successful.
        """
        if not self.ok:
            return self
        if not isinstance(self.data, type_):
            return Result.error(
                f"Type mismatch: expected {type_.__name__}, got {type(self.data).__name__}"
            )
        return Result.success(data=self.data)
    
    def schema(self, rules: dict[str, Callable[[Any], bool]]) -> "Result":
        """
        Validate the contained value (expected to be a dictionary) against a schema of rules.

        Each key in the `rules` dictionary corresponds to a key in the value dictionary, and
        each rule is a function that should return `True` if the value is valid and `False` otherwise.  

        This method:
            - Skips validation if the Result is already an error.
            - Ensures the contained value is a dictionary.
            - Applies each validation function to the corresponding value.
            - Collects all failures into a single error message.
            - Returns a new error Result if any validation fails, or the original Result if all pass.

        Args:
            rules (dict[str, Callable[[Any], bool]]): Mapping of keys to validator functions.

        Returns:
            Result: 
                - Original Result if all validations succeed.
                - Error Result containing a concatenated message of all failed validations.

        Example:
            rules = {
                "age": lambda x: isinstance(x, int) and x >= 0,
                "name": lambda x: isinstance(x, str) and len(x) > 0
            }
            r = Result.success(data={"age": 25, "name": "Alice"})
            r_validated = r.schema(rules)
        """
        if self.is_err:
            return self
        data = self._value
        if not isinstance(data, dict):
            return Result.err(TypeError("Value must be a dict for schema validation"))

        errors = []
        for key, validator in rules.items():
            try:
                if not validator(data.get(key)):
                    errors.append(f"Invalid value for key '{key}': {data.get(key)!r}")
            except Exception as e:
                errors.append(f"Exception for key '{key}': {e}")
        if errors:
            return Result.err(ValueError("; ".join(errors)))
        return self

    def recover(self, fn: Callable[[E], T]) -> "Result[T]":
        """
        Attempt to recover from an error by converting it into a successful value.

        If the Result is already successful, it is returned unchanged.  
        If the Result contains an error, the recovery function `fn` is applied to the error
        value to produce a new successful value.  

        If the recovery function itself raises an exception, the Result is returned as an error
        containing that exception.

        Args:
            fn (Callable[[E], T]): Function to transform the error into a success value.

        Returns:
            Result[T]:
                - Success Result if recovery succeeds.
                - Original Result if already successful.
                - Error Result if recovery function raises an exception.

        Example:
            r = Result.error("File not found")
            r_recovered = r.recover(lambda e: default_config())
        """
        if self.is_ok:
            return self
        try:
            return Result.ok(fn(self._error))
        except Exception as e:
            return Result.err(e)

    def ensure(self, predicate: Callable[[T], bool], msg: str) -> "Result[T]":
        """
        Validate the successful value using a predicate function, keeping SUCCESS only if it passes.

        - If the Result is successful and the predicate returns True for the contained value,
          the Result is returned unchanged.
        - If the predicate returns False, a new error Result is returned with the provided message.
        - If the Result is already an error, it is returned unchanged.
        - If the predicate raises an exception, the Result becomes an error containing that exception.

        Args:
            predicate (Callable[[T], bool]): Function that returns True if the value is valid.
            msg (str): Error message used if the predicate returns False.

        Returns:
            Result[T]:
                - Original Result if predicate passes or if Result is not successful.
                - Error Result with `msg` if predicate fails.
                - Error Result if predicate raises an exception.

        Example:
            r = Result.success(10)
            r_validated = r.ensure(lambda x: x > 0, "Value must be positive")
        """
        if self.is_ok:
            try:
                if predicate(self._value):
                    return self
                return Result.err(ValueError(msg))
            except Exception as e:
                return Result.err(e)
        return self

    def iter_value(self) -> Iterator[T]:
        """
        Yield value if success, otherwise do nothing.
        Useful in generator pipelines with `yield from`.
        """
        if self.is_ok:
            yield self._value

    @staticmethod
    def multicombine(results: list["Result[T]"]) -> "Result[list[T]]":
        """
        Aggregate multiple Result objects into one.
        - Fails if any is error
        - Collects warnings or successful values
        """
        values = []
        for r in results:
            if r.is_err:
                return r
            values.append(r._value)
        return Result.ok(values)

    def map_errors(self, fn: Callable[[E], Any]) -> "Result[T]":
        """
        Transform error into another error or message.
        """
        if self.is_ok:
            return self
        return Result.err(fn(self._error))

    def tap(self, fn: Callable[[T], Any]) -> "Result[T]":
        """
        Execute a side-effect function on the success value without changing it.
        """
        if self.is_ok:
            fn(self._value)
        return self

    def tap_err(self, fn: Callable[[E], Any]) -> "Result[T]":
        """
        Execute a side-effect function on the error without changing it.
        """
        if self.is_err:
            fn(self._error)
        return self

    def or_default(self, default: T) -> T:
        """
        Return value if success, otherwise return default.
        """
        return self._value if self.is_ok else default

    def assert_ok(self, msg: str = "Result is error") -> "Result[T]":
        """
        Raise AssertionError if result is error.
        Can be used for assert keyword integration.
        """
        assert self.is_ok, msg
        return self

    def raise_if_err(self) -> T:
        """
        Raise the error if present, using Python's `from` chaining.
        """
        if self.is_err:
            raise self._error
        return self._value
    
class Signal:
    """
    Represents a structured result signal.

    A Signal can be returned from functions to indicate success, failure,
    warning, or abort states without immediately raising exceptions.
    It can also be inspected and converted into an exception by higher-level code.

    This pattern is useful for:
        - validation pipelines
        - parsers
        - config loaders
        - non-exception control flow

    Args:
        code (SIGINT): Status code indicating the result type.
            Defaults to SIGINT.SUCCESS.
        message (str): Optional human-readable message.
        data (Any): Optional payload associated with the result.

    Attributes:
        code (SIGINT): The signal status code.
        message (str): Informational message.
        data (Any): Optional result data.

    Properties:
        ok (bool): True if the signal represents success.
        is_error (bool): True if the signal represents an error, failure, or abort.
        is_warn (bool): True if the signal represents a warning.

    Example:
        result = Signal.success("Loaded config", data=config)

        if result.ok:
            use(result.data)
        elif result.is_warn:
            log_warning(result.message)
        else:
            raise RuntimeError(result.message)
    """

    __slots__ = ("code", "message", "data")

    def __init__(self, code: SIGINT = SIGINT.SUCCESS, message: str = "", data=None):
        self.code = code
        self.message = message
        self.data = data

    @property
    def ok(self) -> bool:
        """Return True if the signal represents a SUCCESS state."""
        return self.code == SIGINT.SUCCESS

    @property
    def is_error(self) -> bool:
        """
        Return True if the signal represents an error-like state
        (ERROR, FAIL, or ABORT).
        """
        return self.code in {SIGINT.ERROR, SIGINT.FAIL, SIGINT.ABORT}

    @property
    def is_warn(self) -> bool:
        """Return True if the signal represents a WARN state."""
        return self.code == SIGINT.WARN

    @classmethod
    def success(cls, message: str = "", data=None):
        """Create a SUCCESS signal."""
        return cls(SIGINT.SUCCESS, message, data)

    @classmethod
    def error(cls, message: str = "", data=None):
        """Create an ERROR signal."""
        return cls(SIGINT.ERROR, message, data)

    @classmethod
    def fail(cls, message: str = "", data=None):
        """Create a FAIL signal."""
        return cls(SIGINT.FAIL, message, data)

    @classmethod
    def abort(cls, message: str = "", data=None):
        """Create an ABORT signal."""
        return cls(SIGINT.ABORT, message, data)

    @classmethod
    def warn(cls, message: str = "", data=None):
        """Create a WARN signal."""
        return cls(SIGINT.WARN, message, data)

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the Signal."""
        return f"Signal(code={self.code.name}, message={self.message!r}, data={self.data!r})"

def as_(value: object) -> T:
    """
    Return the given value while preserving a generic type for static type checkers.

    This is a zero-cost helper used purely for typing purposes.
    It performs no runtime validation or conversion.

    Useful when you *know* the type but the type checker cannot infer it.

    Args:
        value (object): The value to treat as type T.

    Returns:
        T: The same value, typed as T for static analysis.

    Example:
        raw = config["port"].value  # type: object
        port = as_(raw)             # type: int (for the type checker)
    """
    return value

def trust(t: object) -> T:
    """
    Mark a value as trusted and treat it as type T without runtime checks.

    This function is identical to `as_` at runtime but semantically indicates
    that the caller guarantees the correctness of the type.

    Intended for:
        - internal library code
        - validated parser outputs
        - performance-sensitive paths

    Warning:
        No runtime validation is performed. Misuse may cause type errors later.

    Args:
        t (object): The trusted value.

    Returns:
        T: The same value, typed as T for static analysis.

    Example:
        token = trust(parsed_token)  # already validated earlier
    """
    return t

@overload
def std_typed(value: T) -> T: ...
@overload
def std_typed(cls: Type[T], value: object) -> T: ...
def std_typed(arg1, arg2=None):
    """
    Smart type helper for both static typing and optional runtime checks.

    Usage:
    1. Preserve type for static analysis:
        x: int = typed(123)

    2. Optional runtime type checking:
        y = typed(int, some_value)  # ensures some_value is int at runtime

    3. Works for generics and any type hints.
    """
    if arg2 is None:
        return arg1
    else:
        cls, value = arg1, arg2
        if not isinstance(value, cls):
            raise TypeError(f"Expected value of type {cls.__name__}, got {type(value).__name__}")
        return value
    
def typed(value: object, type_: Type[T] = None) -> T:
    """
    Returns the value with type information preserved for type checkers.
    If type_ is provided, optionally check runtime type.
    """
    if type_ is not None and not isinstance(value, type_):
        raise TypeError(f"Expected value of type {type_.__name__}, got {type(value).__name__}")
    return cast(T, value)

def restrict(f: Callable):
    """
    Decorator that wraps a function and converts any raised exception
    into a RuntimeError with a standardized error message.

    The original exception is preserved as the cause using exception chaining.

    Args:
        f (Callable): The function to wrap.

    Returns:
        Callable: The wrapped function that raises RuntimeError on failure.

    Example:
        @restrict
        def divide(a, b):
            return a / b
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Function {f.__name__} failed") from e
    return wrapper


class Protected:
    """
    Wrapper class for creating a read-only value.

    Once initialized, the stored value cannot be modified.
    Any attempt to assign to `.value` will raise an AttributeError.

    Args:
        value (Any): The value to protect from modification.

    Attributes:
        value (Any): Read-only access to the protected value.

    Example:
        host = Protected("localhost")
        print(host.value)      # OK
        host.value = "127.0.0.1"  # Raises AttributeError
    """

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        """Return the protected value (read-only)."""
        return self._value

    @value.setter
    def value(self, new):
        """
        Prevent reassignment of the protected value.

        Raises:
            AttributeError: Always raised to enforce immutability.
        """
        raise AttributeError("Cannot modify this value")


def protectedclass(cls):
    """
    Class decorator that locks down a class to prevent subclassing
    and instance attribute modification.

    Effects:
        - Subclassing the decorated class raises TypeError.
        - Setting attributes on instances raises AttributeError.

    Args:
        cls (type): The class to protect.

    Returns:
        type: The same class with restrictions applied.

    Example:
        @protectclass
        class Config:
            HOST = "localhost"

        class Child(Config):  # Raises TypeError
            pass

        c = Config()
        c.HOST = "127.0.0.1"  # Raises AttributeError
    """
    original_init_subclass = cls.__init_subclass__

    def locked_subclass(*args, **kwargs):
        raise TypeError(f"Cannot subclass {cls.__name__}")

    cls.__init_subclass__ = classmethod(locked_subclass)

    original_setattr = cls.__setattr__

    def locked_setattr(self, name, value):
        raise AttributeError(f"Cannot modify attributes of {cls.__name__}")

    cls.__setattr__ = locked_setattr

    return cls

@final
class Meta:
    def __init__(
        self,
        *,
        author: _MetaType = None,
        version: _MetaType = None,
        github_clone: _MetaType = None,
        github: _MetaType = None,
        license: _MetaType = None,
    ) -> None:
        object.__setattr__(self, '_author', author)
        object.__setattr__(self, '_version', version)
        object.__setattr__(self, '_github_clone', github_clone)
        object.__setattr__(self, '_github', github)
        object.__setattr__(self, '_license', license)

    @property
    def author(self) -> str: return str(self._author)

    @property
    def version(self) -> str: return str(self._version)

    @property
    def github_clone(self) -> str: return str(self._github_clone)

    @property
    def github(self) -> str: return str(self._github)

    @property
    def license(self) -> str: return str(self._license)

    @author.setter
    def author(self, value: _MetaType) -> None:
        raise TypeError(f"Author: cannot be assigned.")
    
    @version.setter
    def version(self, value: _MetaType) -> None:
        raise TypeError(f"Version: cannot be assigned.")
    
    @github_clone.setter
    def github_clone(self, value: _MetaType) -> None:
        raise TypeError(f"Github_clone: cannot be assigned.")
    
    @license.setter
    def license(self, value: _MetaType) -> None:
        raise TypeError(f"License: cannot be assigned.")


META = Meta(
    author="Matija", 
    version=1.0, 
    github="https://github.com/n11kol11c",
    github_clone="https://github.com/n11kol11c/dopamine.git",
    license="MIT"
)

class include:
    """Unified dynamic import with support for modules, files, and relative paths.

    Provides a single call interface for all Python import scenarios while
    remaining readable and explicit at the call site.

    Parameters
    ----------
    name : str
        One of:
        - A standard module or package name, e.g. ``"sys"``, ``"os.path"``.
        - A ``.py`` file path, e.g. ``"utils.py"``, ``"../config.py"``.
        - A dotted file path, e.g. ``"subdir/tools.py"``.
        - A relative Python import, e.g. ``".sibling"``, ``"..parent_mod"``.

    Returns
    -------
    types.ModuleType
        The imported module object.

    Raises
    ------
    ImportError
        If the module cannot be found or loaded.

    Examples
    --------
    Standard library:

    >>> sys = include("sys")
    >>> re = include("re")

    Dotted package:

    >>> ospath = include("os.path")

    Local file path:

    >>> helpers = include("helpers.py")

    Relative file path:

    >>> cfg = include("../config/app.py")

    Relative Python import (inside a package):

    >>> sibling = include(".submodule")
    >>> parent_mod = include("..module")
    """
    __slots__ = ()

    def __new__(cls, module):
        """Dispatch import based on the format of *name*."""
        if module.endswith('.py') or '/' in module or '\\' in module:
            return cls._import_file(module)
        if module.startswith('.'):
            return cls._relative_import(module)
        return importlib.import_module(module)

    @classmethod
    def _import_file(cls, path):
        """Import a Python file from an absolute or relative filesystem path.

        Parameters
        ----------
        path : str
            Path to a ``.py`` file.  Relative paths are resolved from the
            current working directory.

        Returns
        -------
        types.ModuleType
            The module compiled from *path*.

        Raises
        ------
        ImportError
            If the file does not exist or cannot be loaded as a module.
        """
        abs_path = os.path.abspath(path)
        if not os.path.isfile(abs_path):
            raise ImportError(f"No module file: {abs_path}")
        mod_name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(mod_name, abs_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec: {abs_path}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
        return mod

    @classmethod
    def _relative_import(cls, name):
        """Perform a relative Python import by inspecting the caller's package.

        Resolves the caller's ``__package__`` (with ``__name__`` fallback) so
        that relative import expressions such as ``.sibling`` or ``..parent``
        work correctly regardless of whether the module is run directly or
        loaded as part of a package.

        Parameters
        ----------
        name : str
            Relative import expression, e.g. ``".module"``, ``"..other"``.

        Returns
        -------
        types.ModuleType
            The target module.

        Raises
        ------
        ImportError
            If the relative name cannot be resolved.
        """
        frame = inspect.currentframe()
        try:
            caller = frame.f_back.f_back 
            pkg = caller.f_globals.get('__package__', '')
            if not pkg:
                pkg = caller.f_globals.get('__name__', '').rpartition('.')[0]
            return importlib.import_module(name, package=pkg)
        finally:
            del frame

class include_once:
    """Unified dynamic import with support for modules, files, and relative paths.

    Provides a single call interface for all Python import scenarios while
    remaining readable and explicit at the call site.

    Parameters
    ----------
    module : str
        One of:
        - A standard module or package name, e.g. ``"sys"``, ``"os.path"``.
        - A ``.py`` file path, e.g. ``"utils.py"``, ``"../config.py"``.
        - A dotted file path, e.g. ``"subdir/tools.py"``.
        - A relative Python import, e.g. ``".sibling"``, ``"..parent_mod"``.

    Returns
    -------
    types.ModuleType
        The imported module object.

    Raises
    ------
    ImportError
        If the module cannot be found or loaded.

    Examples
    --------
    Standard library:

    >>> sys = include_once("sys")
    >>> re = include_once("re")

    Dotted package:

    >>> ospath = include_once("os.path")

    Local file path:

    >>> helpers = include_once("helpers.py")

    Relative file path:

    >>> cfg = include_once("../config/app.py")

    Relative Python import (inside a package):

    >>> sibling = include_once(".submodule")
    >>> parent_mod = include_once("..module")
    """
    __slots__ = ()

    def __new__(cls, module):
        """Dispatch import based on the format of *name*."""
        if module.endswith('.py') or '/' in module or '\\' in module:
            return cls._import_file(module)
        if module.startswith('.'):
            return cls._relative_import(module)
        return importlib.import_module(module)

    @classmethod
    def _import_file(cls, path):
        """Import a Python file from an absolute or relative filesystem path.

        Parameters
        ----------
        path : str
            Path to a ``.py`` file.  Relative paths are resolved from the
            current working directory.

        Returns
        -------
        types.ModuleType
            The module compiled from *path*.

        Raises
        ------
        ImportError
            If the file does not exist or cannot be loaded as a module.
        """
        abs_path = os.path.abspath(path)
        if not os.path.isfile(abs_path):
            raise ImportError(f"No module file: {abs_path}")
        mod_name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(mod_name, abs_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec: {abs_path}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
        return mod

    @classmethod
    def _relative_import(cls, name):
        """Perform a relative Python import by inspecting the caller's package.

        Resolves the caller's ``__package__`` (with ``__name__`` fallback) so
        that relative import expressions such as ``.sibling`` or ``..parent``
        work correctly regardless of whether the module is run directly or
        loaded as part of a package.

        Parameters
        ----------
        name : str
            Relative import expression, e.g. ``".module"``, ``"..other"``.

        Returns
        -------
        types.ModuleType
            The target module.

        Raises
        ------
        ImportError
            If the relative name cannot be resolved.
        """
        frame = inspect.currentframe()
        try:
            caller = frame.f_back.f_back 
            pkg = caller.f_globals.get('__package__', '')
            if not pkg:
                pkg = caller.f_globals.get('__name__', '').rpartition('.')[0]
            return importlib.import_module(name, package=pkg)
        finally:
            del frame

@final
class define:
    """Transparent type alias — ``define[T]`` is exactly ``T``.

    This class is a **runtime-only shim** that makes the expression
    ``define[str]`` evaluate to ``str``.  A ``.pyi`` stub overrides
    this with a ``type define[T] = T`` declaration so that every
    modern type-checker treats ``define[str]`` identically to ``str``.

    .. rubric:: Annotation use

    .. code-block:: python

        x: define[int]            # type-checker sees ``int``
        items: define[list[str]]  # type-checker sees ``list[str]``

    .. rubric:: Runtime identity

    .. code-block:: python

        define[str] is str    # True
        define[int]  is int   # True

    Notes
    -----
    This class is **not** meant to be instantiated.  Use :class:`Define`
    when you need a runtime definition container.

    See Also
    --------
    Define : Runtime definition container for pairing a type with a default
        value and metadata.
    """

    __type__: type[T] | None
    __default__: T | None

    @classmethod
    def __class_getitem__(cls, item: T) -> T:
        """Return *item* unchanged, making ``define[T]`` identical to ``T``.

        This method is invoked when the class is subscripted (e.g.
        ``define[int]``).  It simply returns the argument so that the
        subscript expression evaluates to the inner type at runtime.

        Parameters
        ----------
        item : T
            The type placed inside the brackets (e.g. ``int`` in
            ``define[int]``).

        Returns
        -------
        T
            The same *item*, unchanged.

        Examples
        --------
        >>> define[int] is int
        True
        >>> isinstance("hello", define[str])
        True
        """
        return item

    def __init_subclass__(cls, **kwargs: Any) -> None:
        raise TypeError(f"{cls.__name__} cannot be subclassed")

class Define:
    """Container that pairs a runtime type with a default value and metadata.

    Use this class to capture configuration metadata — the expected
    type, a default value, and arbitrary extra information::

        PORT    = Define(int, 8080, description="HTTP listen port")
        TIMEOUT = Define(float, 30.0, env="APP_TIMEOUT")

    The resulting object stores its arguments in the :attr:`__type__`,
    :attr:`__default__` and :attr:`__metadata__` attributes.

    For type annotations, use the lower-case :func:`define` alias::

        def configure(p: define[int]) -> None: ...   # ``p`` seen as ``int``

    Parameters
    ----------
    type_ : type[T]
        The expected runtime type of the defined value.
    default : T | None, optional
        Default value for the definition.  ``None`` when omitted.
    **kwargs : Any
        Extra metadata attached to this definition.  Stored verbatim
        in :attr:`__metadata__`.

    Attributes
    ----------
    __type__ : type[T]
        The type passed at construction time.
    __default__ : T | None
        The default value (``None`` if not supplied).
    __metadata__ : dict[str, Any]
        Dictionary of extra keyword arguments provided at construction.

    Examples
    --------
    >>> timeout = Define(int, 30)
    >>> timeout.__type__
    <class 'int'>
    >>> timeout.__default__
    30
    >>> timeout
    Define(int, 30)

    >>> with_meta = Define(str, "admin", description="Default role")
    >>> with_meta.__metadata__
    {'description': 'Default role'}

    See Also
    --------
    define : Transparent generic type alias for use in annotations.
    """

    __type__: type[T]
    __default__: T | None
    __metadata__: Dict[str, Any]

    def __init__(
        self,
        type_: type[T],
        default: T | None = None,
        **kwargs: Any,
    ) -> None:
        """Bind *type_* and *default* to a new definition.

        Parameters
        ----------
        type_ : type[T]
            Runtime type of the defined value.
        default : T | None, optional
            Default value (``None`` if not provided).
        **kwargs : Any
            Extra metadata stored verbatim in :attr:`__metadata__`.
        """
        self.__type__ = type_
        self.__default__ = default
        self.__metadata__ = kwargs

    @classmethod
    def __class_getitem__(cls, item: T) -> T:
        """Return *item* directly — ``Define[str]`` is ``str`` at runtime.

        This provides backward compatibility for code that subscripts
        ``Define`` directly.  For new code, prefer the :class:`define`
        alias in annotations and :class:`Define` for runtime construction.

        Parameters
        ----------
        item : T
            The type placed inside brackets.

        Returns
        -------
        T
            The same *item* unchanged.
        """
        return item

    def __repr__(self) -> str:
        """Return a readable string representation of this definition.

        Includes the type name, default value, and any extra metadata.

        Returns
        -------
        str
            ``Define(type, default, key=value, ...)``

        Examples
        --------
        >>> repr(Define(int, 30))
        'Define(int, 30)'
        >>> repr(Define(str, "", description="name"))
        "Define(str, '', description='name')"
        """
        metadata = ""
        if self.__metadata__:
            parts = [f"{k}={v!r}" for k, v in self.__metadata__.items()]
            metadata = ", " + ", ".join(parts)
        return f"Define({self.__type__.__name__}, {self.__default__!r}{metadata})"

    def __eq__(self, other: object) -> bool:
        """Compare two definitions by type and default.

        Two ``Define`` instances are equal when their ``__type__`` and
        ``__default__`` match.  Extra metadata is **not** compared.

        Parameters
        ----------
        other : object
            The object to compare against.

        Returns
        -------
        bool
            ``True`` if *other* is a ``Define`` with the same type and
            default.

        Examples
        --------
        >>> Define(int, 10) == Define(int, 10)
        True
        >>> Define(int, 10) == Define(int, 20)
        False
        """
        if not isinstance(other, Define):
            return NotImplemented
        return (self.__type__, self.__default__) == (
            other.__type__,
            other.__default__,
        )

    def __hash__(self) -> int:
        """Hash based on type and default.

        Ensures ``Define`` instances can be used in sets and as
        dictionary keys when they share the same ``(type, default)``
        pair.

        Returns
        -------
        int
            Hash of ``(type, default)``.
        """
        return hash((self.__type__, self.__default__))
    

@final
class define_once:
    """Transparent type alias — ``define[T]`` is exactly ``T``.

    This class is a **runtime-only shim** that makes the expression
    ``define[str]`` evaluate to ``str``.  A ``.pyi`` stub overrides
    this with a ``type define[T] = T`` declaration so that every
    modern type-checker treats ``define[str]`` identically to ``str``.

    .. rubric:: Annotation use

    .. code-block:: python

        x: define[int]            # type-checker sees ``int``
        items: define[list[str]]  # type-checker sees ``list[str]``

    .. rubric:: Runtime identity

    .. code-block:: python

        define[str] is str    # True
        define[int]  is int   # True

    Notes
    -----
    This class is **not** meant to be instantiated.  Use :class:`Define`
    when you need a runtime definition container.

    See Also
    --------
    Define : Runtime definition container for pairing a type with a default
        value and metadata.
    """

    __type__: type[T] | None
    __default__: T | None

    @classmethod
    def __class_getitem__(cls, item: T) -> T:
        """Return *item* unchanged, making ``define[T]`` identical to ``T``.

        This method is invoked when the class is subscripted (e.g.
        ``define[int]``).  It simply returns the argument so that the
        subscript expression evaluates to the inner type at runtime.

        Parameters
        ----------
        item : T
            The type placed inside the brackets (e.g. ``int`` in
            ``define[int]``).

        Returns
        -------
        T
            The same *item*, unchanged.

        Examples
        --------
        >>> define[int] is int
        True
        >>> isinstance("hello", define[str])
        True
        """
        return item

    def __init_subclass__(cls, **kwargs: Any) -> None:
        raise TypeError(f"{cls.__name__} cannot be subclassed")

@final
class pragma:
    """C-style ``#pragma`` directives for Python.

    Provides module-level directives that mirror the most common uses
    of the C preprocessor ``#pragma``: include guards, compile-time
    messages, deprecation markers, identifier poisoning, and region
    folding hints.

    Usage
    -----
    Module-level directives (executed at import time)::

        pragma.once                         # ``#pragma once``
        pragma.message("Building v2 …")     # ``#pragma message("…")``
        pragma.warning("Use new API")       # ``#pragma warning(…)``
        pragma.todo("Refactor me")          # custom – TODO reminder
        pragma.poison("eval", "exec")       # ``#pragma GCC poison``

    Decorator::

        @pragma.deprecated("use ``bar`` instead")
        def foo(): ...

    Notes
    -----
    All members are ``@staticmethod`` so the class is never instantiated.
    The atomic sentinel ``pragma.once`` (no parentheses) is a valid usage
    that evaluates to ``True``.
    """

    __slots__ = ()

    @staticmethod
    def once() -> bool:
        """Include guard — skip module-level code on re-import.

        Call at module level so that re-importing the module prints a
        message and returns ``False``::

            pragma.once()
            if not pragma.once():
                ...  # already loaded

        The bare attribute ``pragma.once`` (without parentheses) is
        also supported as a truthy sentinel.
        """
        frame = inspect.currentframe()
        try:
            caller = frame.f_back
            mod_name = caller.f_globals.get('__name__', '')
            spec = caller.f_globals.get('__spec__', None)
            loaded = mod_name in sys.modules
            origin = getattr(spec, 'origin', mod_name) if spec else mod_name
            if loaded:
                print(f"[pragma once] {origin} already loaded, skipping")
                return False
            return True
        finally:
            del frame

    @staticmethod
    def message(text: str) -> None:
        """Emit a user-defined message at import time.

        Parameters
        ----------
        text : str
            The message string to display.
        """
        print(f"[pragma message] {text}")

    @staticmethod
    def message_once(text: str) -> None:
        """Emit a message at import time, deduplicated by *text*.

        Subsequent calls with the same string in the same process are
        silently ignored.
        """
        if not hasattr(pragma, '_dedup'):
            pragma._dedup = set()
        if text not in pragma._dedup:
            pragma._dedup.add(text)
            print(f"[pragma message] {text}")


    @staticmethod
    def warning(
        text: str,
        category: type[Warning] = UserWarning,
    ) -> None:
        """Issue a warning at import time.

        Parameters
        ----------
        text : str
            Warning message body.
        category : type[Warning]
            Warning subclass (default ``UserWarning``).
        """
        warnings.warn(text, category, stacklevel=2)

    @staticmethod
    def todo(text: str) -> None:
        """Print a TODO reminder at import time.

        Parameters
        ----------
        text : str
            TODO description.
        """
        print(f"[pragma TODO] {text}")

    @staticmethod
    def deprecated(reason: str = "") -> Callable[[F], F]:
        """Decorator that marks a callable as deprecated.

        Wraps *reason* in a :class:`DeprecationWarning` that is emitted
        when the decorated object is defined (not when it is called).

        Parameters
        ----------
        reason : str
            Explanation or migration hint.

        Returns
        -------
        Callable[[F], F]
            The same object, unchanged at runtime.
        """
        def decorator(obj: F) -> F:
            msg = f"{obj.__qualname__} is deprecated"
            if reason:
                msg += f": {reason}"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return obj
        return decorator

    @staticmethod
    def poison(*names: str) -> None:
        """Forbid access to one or more names in the caller's module.

        Every *name* is replaced in the module's global namespace with
        a sentinel that raises :class:`NameError` on any access.

        Parameters
        ----------
        *names : str
            Identifiers to poison.

        Raises
        ------
        NameError
            When any of *names* is subsequently read or written.

        Examples
        --------
        .. code-block:: python

            pragma.poison("eval", "exec")
            eval("1 + 1")   # NameError: 'eval' is poisoned
        """
        frame = inspect.currentframe()
        try:
            globs = frame.f_back.f_globals
            sentinel = _PoisonSentinel()
            for name in names:
                globs[name] = sentinel
        finally:
            del frame

    @staticmethod
    def region(name: str = "") -> None:
        """Open a foldable region.

        Parameters
        ----------
        name : str
            Optional label for the region.
        """
        if name:
            print(f"[pragma region] {name}")

    @staticmethod
    def endregion() -> None:
        """Close last-opened foldable region."""
        pass

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def optimize(level: int = 1) -> bool:
        """Hint that the module is safe for aggressive optimisation.

        This is purely informational (the interpreter is free to
        ignore it).  Calling ``pragma.optimize(0)`` requests no
        optimisation.

        Parameters
        ----------
        level : int
            Optimisation level (0, 1, or 2).

        Returns
        -------
        bool
            ``True`` when *level* is non-zero.
        """
        if level < 0 or level > 2:
            raise ValueError(f"optimize level must be 0, 1 or 2, got {level}")
        return bool(level)


class _PoisonSentinel:
    """Sentinel that raises ``NameError`` on any attribute access.

    Instances replace the original value in the module namespace when
    :meth:`pragma.poison` is called.
    """
    __slots__ = ()
    _name: str | None = None

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return "<poisoned>"

    def __bool__(self) -> bool:
        raise NameError("cannot access poisoned name")

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        raise NameError("cannot access poisoned name")

    def __getattr__(self, name: str) -> Any:
        raise NameError(f"cannot access poisoned name")

    def __setattr__(self, name: str, value: Any) -> None:
        raise NameError(f"cannot assign to poisoned name")

    def __delattr__(self, name: str) -> None:
        raise NameError(f"cannot delete poisoned name")


_UNSET = object()


class _ExportMeta(type):
    """Metaclass enabling attribute syntax on ``export`` and ``extern``."""

    def __getattr__(cls, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return cls._registry[name]
        except KeyError:
            raise AttributeError(f"{cls.__name__} has no attribute '{name!r}'")

    def __setattr__(cls, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            cls._registry[name] = value

    def __delattr__(cls, name: str) -> None:
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            cls._registry.pop(name, None)

    def __contains__(cls, name: object) -> bool:
        return name in cls._registry

    def __len__(cls) -> int:
        return len(cls._registry)

    def __iter__(cls) -> typing.Iterator[str]:
        return iter(cls._registry)

    def __repr__(cls) -> str:
        items = ", ".join(f"{k}={v!r}" for k, v in cls._registry.items())
        return f"{cls.__name__}({items})"


@final
class export(metaclass=_ExportMeta):
    """``export`` — define and share values across all Python modules (like C's ``__declspec(dllexport)``).

    Usage
    -----
        export.db = create_engine(...)
        export("api_key", "sk-…")
        export.db
        export("api_key")
        export("missing", default="fallback")
        export.list()
        export.clear()
        "key" in export
        len(export)
        list(export)
    """

    _registry: dict[str, Any] = {}

    def __new__(cls, name: str, value: Any = _UNSET, *, default: Any = None) -> Any:
        if value is _UNSET:
            return cls._registry.get(name, default)
        cls._registry[name] = value
        return value

    @classmethod
    def list(cls) -> dict[str, Any]:
        return dict(cls._registry)

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()


class _ExternMeta(type):
    """Metaclass enabling read-only attribute syntax on ``extern``."""

    def __getattr__(cls, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return export._registry[name]
        except KeyError:
            raise AttributeError(f"extern has no attribute '{name!r}'")

    def __setattr__(cls, name: str, value: Any) -> None:
        raise TypeError("extern is read-only — use export to define values")

    def __delattr__(cls, name: str) -> None:
        raise TypeError("extern is read-only — cannot delete")

    def __contains__(cls, name: object) -> bool:
        return name in export._registry

    def __len__(cls) -> int:
        return len(export._registry)

    def __iter__(cls) -> typing.Iterator[str]:
        return iter(export._registry)

    def __repr__(cls) -> str:
        items = ", ".join(f"{k}={v!r}" for k, v in export._registry.items())
        return f"extern({items})"


@final
class extern(metaclass=_ExternMeta):
    """``extern`` — access values exported by other modules (like C's ``extern`` keyword).

    Usage
    -----
        extern.db
        extern("api_key")
        extern("missing", default="fallback")
        "key" in extern
        len(extern)
        list(extern)
    """

    def __new__(cls, name: str, *, default: Any = None) -> Any:
        return export._registry.get(name, default)


@final
class default:
    """Transparent default-value marker for function parameters.

    ``default(x)`` wraps *x* so it can be detected later via
    ``default.is_marked(val)`` or ``isinstance(val, default)``.
    The wrapper proxies all attribute access, operators, and calls
    to the inner value, so it works transparently in most contexts.

    ``default(None)`` returns bare ``None`` so it can be used in
    union annotations: ``int | default(None)`` → ``int | None``.

    For type annotations ``default[T]`` is transparent via the
    ``.pyi`` stub: ``type default[T] = T``.

    Usage
    -----
        def connect(host: str = default("localhost")):
            if default.is_marked(host):
                print("using default host")
            return f"connect to {host}"

        def lookup(key: str | default(None)):
            print(key or "no key")

    Introspection
    -------------
        default.is_marked(obj)  → bool
        default.unwrap(obj)     → inner value (or obj if unmarked)
    """

    __slots__ = ('_value',)

    def __new__(cls, value: Any = _UNSET) -> Any:
        if value is _UNSET:
            return cls
        if value is None:
            return None
        instance = super().__new__(cls)
        instance._value = value
        return instance

    @classmethod
    def __class_getitem__(cls, item: Any) -> Any:
        return item

    @classmethod
    def is_marked(cls, obj: Any) -> bool:
        return isinstance(obj, cls)

    @classmethod
    def unwrap(cls, obj: Any) -> Any:
        return obj._value if isinstance(obj, cls) else obj

    def __repr__(self) -> str:
        return f"default({self._value!r})"

    def __str__(self) -> str:
        return str(self._value)

    def __bool__(self) -> bool:
        return bool(self._value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, default):
            return self._value == other._value
        return self._value == other

    def __hash__(self) -> int:
        return hash(self._value)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._value(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._value, name)

def _proxy_binary(name: str) -> Callable:
    def _op(self, other: Any) -> Any:
        return getattr(self._value, name)(other)
    _op.__name__ = name
    _op.__qualname__ = f"default.{name}"
    return _op

def _proxy_unary(name: str) -> Callable:
    def _op(self) -> Any:
        return getattr(self._value, name)()
    _op.__name__ = name
    _op.__qualname__ = f"default.{name}"
    return _op

def _proxy_getset(name: str) -> Callable:
    def _op(self, key: Any) -> Any:
        return getattr(self._value, name)(key)
    _op.__name__ = name
    _op.__qualname__ = f"default.{name}"
    return _op

def _proxy_setitem(name: str) -> Callable:
    def _op(self, key: Any, value: Any) -> Any:
        return getattr(self._value, name)(key, value)
    _op.__name__ = name
    _op.__qualname__ = f"default.{name}"
    return _op

def _proxy_delitem(name: str) -> Callable:
    def _op(self, key: Any) -> Any:
        return getattr(self._value, name)(key)
    _op.__name__ = name
    _op.__qualname__ = f"default.{name}"
    return _op

def _proxy_contains(name: str) -> Callable:
    def _op(self, item: Any) -> Any:
        return getattr(self._value, name)(item)
    _op.__name__ = name
    _op.__qualname__ = f"default.{name}"
    return _op

_binary = (
    '__add__', '__sub__', '__mul__', '__matmul__', '__truediv__',
    '__floordiv__', '__mod__', '__divmod__', '__pow__', '__lshift__',
    '__rshift__', '__and__', '__xor__', '__or__',
    '__radd__', '__rsub__', '__rmul__', '__rmatmul__', '__rtruediv__',
    '__rfloordiv__', '__rmod__', '__rdivmod__', '__rpow__', '__rlshift__',
    '__rrshift__', '__rand__', '__rxor__', '__ror__',
    '__iadd__', '__isub__', '__imul__', '__imatmul__', '__itruediv__',
    '__ifloordiv__', '__imod__', '__ipow__', '__ilshift__',
    '__irshift__', '__iand__', '__ixor__', '__ior__',
    '__lt__', '__le__', '__gt__', '__ge__', '__ne__',
)
_unary = (
    '__neg__', '__pos__', '__invert__',
    '__int__', '__float__', '__complex__', '__index__',
    '__len__', '__iter__', '__reversed__',
)
_getset = ('__getitem__',)
_setitem = ('__setitem__',)
_delitem = ('__delitem__',)
_contains = ('__contains__',)

for _name in _binary:
    setattr(default, _name, _proxy_binary(_name))
for _name in _unary:
    setattr(default, _name, _proxy_unary(_name))
for _name in _getset:
    setattr(default, _name, _proxy_getset(_name))
for _name in _setitem:
    setattr(default, _name, _proxy_setitem(_name))
for _name in _delitem:
    setattr(default, _name, _proxy_delitem(_name))
for _name in _contains:
    setattr(default, _name, _proxy_contains(_name))


@final
class empty:
    """Check whether a value is "empty" — returns a ``bool``.

    ``empty(x)`` returns ``True`` when *x* is any of:

        ``None``, ``False``, ``0`` / ``0.0`` / ``0j``, ``""``,
        ``[]``, ``()``, ``{}``, ``set()``, ``range(0)``,
        ``b""``, ``bytearray()``,
        or any object whose ``__bool__`` returns ``False``
        or ``__len__`` returns ``0``.

    Usage
    -----
        empty([])       → True
        empty("text")   → False
        empty(None)     → True
        empty(0)        → True
    """

    def __new__(cls, value: Any) -> bool:
        return not value


class _FILTERS:
    """Internal filter registry — maps filter IDs to callables."""

    @staticmethod
    def validate_int(value: Any) -> int | None:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_float(value: Any) -> float | None:
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_bool(value: Any) -> bool | None:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return {"true": True, "false": False, "1": True, "0": False}.get(value.lower(), None)
        if isinstance(value, (int, float)):
            return bool(value)
        return None

    _email_re = re.compile(
        r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+'
        r'@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
        r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    )

    @staticmethod
    def validate_email(value: Any) -> str | None:
        if not isinstance(value, str):
            return None
        if _FILTERS._email_re.match(value):
            return value
        return None

    @staticmethod
    def validate_url(value: Any) -> str | None:
        if not isinstance(value, str):
            return None
        return value if value.startswith(("http://", "https://", "ftp://")) else None

    @staticmethod
    def validate_ip(value: Any) -> str | None:
        if not isinstance(value, str):
            return None
        parts = value.split(".")
        if len(parts) != 4:
            return None
        for p in parts:
            if not p.isdigit() or not 0 <= int(p) <= 255:
                return None
        return value

    @staticmethod
    def validate_regex(value: Any, pattern: str) -> str | None:
        if not isinstance(value, str):
            return None
        m = re.match(pattern, value)
        return m.group() if m else None

    @staticmethod
    def sanitize_string(value: Any) -> str:
        s = str(value) if not isinstance(value, str) else value
        return "".join(c for c in s if c.isprintable() or c in "\n\r\t")

    @staticmethod
    def sanitize_email(value: Any) -> str:
        s = str(value) if not isinstance(value, str) else value
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._+-")
        return "".join(c for c in s if c in allowed)

    @staticmethod
    def sanitize_url(value: Any) -> str:
        s = str(value) if not isinstance(value, str) else value
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:/?#[]@!$&'()*+,;=-._~%")
        return "".join(c for c in s if c in allowed)

    @staticmethod
    def sanitize_number_int(value: Any) -> str:
        s = str(value) if not isinstance(value, str) else value
        return "".join(c for c in s if c.isdigit() or c in "+-")

    @staticmethod
    def sanitize_number_float(value: Any) -> str:
        s = str(value) if not isinstance(value, str) else value
        return "".join(c for c in s if c.isdigit() or c in "+-.eE")

    @staticmethod
    def callback(value: Any, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        return func(value, *args, **kwargs)


class filter_flags:
    """Bitmask-like options for ``filter_var``."""
    NONE = 0
    STRIP_LOW = 1  
    STRIP_HIGH = 2    
    ENCODE_LOW = 4    
    ENCODE_HIGH = 8   
    STRIP_BACKTICK = 16


@final
class filter_var:
    """PHP-style ``filter_var`` — validate and sanitize values.

    Usage
    -----
        filter_var("123", filter_var.VALIDATE_INT)       → 123
        filter_var("abc", filter_var.VALIDATE_INT)       → None
        filter_var("user@site.com", filter_var.VALIDATE_EMAIL) → "user@site.com"
        filter_var(42, filter_var.SANITIZE_STRING)       → "42"
    """

    VALIDATE_INT       = "validate_int"
    VALIDATE_FLOAT     = "validate_float"
    VALIDATE_BOOLEAN   = "validate_bool"
    VALIDATE_EMAIL     = "validate_email"
    VALIDATE_URL       = "validate_url"
    VALIDATE_IP        = "validate_ip"
    VALIDATE_REGEX     = "validate_regex"
    SANITIZE_STRING    = "sanitize_string"
    SANITIZE_EMAIL     = "sanitize_email"
    SANITIZE_URL       = "sanitize_url"
    SANITIZE_NUMBER_INT = "sanitize_number_int"
    SANITIZE_NUMBER_FLOAT = "sanitize_number_float"
    CALLBACK           = "callback"

    def __new__(
        cls,
        value: Any,
        filter_id: str | None = None,
        options: Any = None,
        *,
        default: Any = None,
        flags: int = 0,
        min: int | float | None = None,
        max: int | float | None = None,
        regex: str | None = None,
        callback: Callable[..., Any] | None = None,
    ) -> Any:
        if filter_id is None:
            filter_id = filter_var.SANITIZE_STRING

        result = cls._run(value, filter_id, options, min=min, max=max, regex=regex, callback=callback)

        if result is None:
            return default

        return cls._apply_flags(result, flags)

    @classmethod
    def _run(cls, value: Any, filter_id: str, options: Any, **kwargs: Any) -> Any:
        match filter_id:
            case filter_var.VALIDATE_INT:
                v = _FILTERS.validate_int(value)
                if v is not None:
                    lo = kwargs.get("min")
                    if lo is None and isinstance(options, dict):
                        lo = options.get("min")
                    hi = kwargs.get("max")
                    if hi is None and isinstance(options, dict):
                        hi = options.get("max")
                    if lo is not None and v < lo:
                        return None
                    if hi is not None and v > hi:
                        return None
                return v
            case filter_var.VALIDATE_FLOAT:
                v = _FILTERS.validate_float(value)
                if v is not None:
                    lo = kwargs.get("min")
                    if lo is None and isinstance(options, dict):
                        lo = options.get("min")
                    hi = kwargs.get("max")
                    if hi is None and isinstance(options, dict):
                        hi = options.get("max")
                    if lo is not None and v < lo:
                        return None
                    if hi is not None and v > hi:
                        return None
                return v
            case filter_var.VALIDATE_BOOLEAN:
                return _FILTERS.validate_bool(value)
            case filter_var.VALIDATE_EMAIL:
                return _FILTERS.validate_email(value)
            case filter_var.VALIDATE_URL:
                return _FILTERS.validate_url(value)
            case filter_var.VALIDATE_IP:
                return _FILTERS.validate_ip(value)
            case filter_var.VALIDATE_REGEX:
                pattern = kwargs.get("regex") or (options.get("regex") if isinstance(options, dict) else None)
                if pattern is None:
                    raise ValueError("VALIDATE_REGEX requires a regex pattern")
                return _FILTERS.validate_regex(value, pattern)
            case filter_var.SANITIZE_STRING:
                return _FILTERS.sanitize_string(value)
            case filter_var.SANITIZE_EMAIL:
                return _FILTERS.sanitize_email(value)
            case filter_var.SANITIZE_URL:
                return _FILTERS.sanitize_url(value)
            case filter_var.SANITIZE_NUMBER_INT:
                return _FILTERS.sanitize_number_int(value)
            case filter_var.SANITIZE_NUMBER_FLOAT:
                return _FILTERS.sanitize_number_float(value)
            case filter_var.CALLBACK:
                func = kwargs.get("callback") or (options if callable(options) else None)
                if func is None:
                    raise ValueError("CALLBACK filter requires a callable")
                return _FILTERS.callback(value, func)
            case _:
                raise ValueError(f"Unknown filter: {filter_id!r}")

    @classmethod
    def _apply_flags(cls, value: Any, flags: int) -> Any:
        if not isinstance(value, str) or flags == filter_flags.NONE:
            return value
        chars = []
        for c in value:
            code = ord(c)
            if flags & filter_flags.STRIP_LOW and code < 32 and c not in "\n\r\t":
                continue
            if flags & filter_flags.STRIP_HIGH and code > 127:
                continue
            if flags & filter_flags.ENCODE_LOW and code < 32 and c not in "\n\r\t":
                chars.append(f"&#x{code:02X};")
                continue
            if flags & filter_flags.ENCODE_HIGH and code > 127:
                chars.append(f"&#x{code:04X};")
                continue
            if flags & filter_flags.STRIP_BACKTICK and c == "`":
                continue
            chars.append(c)
        return "".join(chars)


class ENT:
    """PHP-style ``htmlspecialchars`` bitmask flags."""
    COMPAT      = 2
    QUOTES      = 3
    NOQUOTES    = 0
    SUBSTITUTE  = 8
    IGNORE      = 4
    DISALLOWED  = 128
    HTML401     = 0
    XML1        = 16
    XHTML       = 32
    HTML5       = 48


@final
class htmlspecialchars:
    """PHP-style ``htmlspecialchars`` — convert special HTML chars to entities.

    ``&``, ``<``, ``>``, ``"``, ``'`` → ``&amp;``, ``&lt;``, ``&gt;``, ``&quot;``, ``&#039;``

    Usage
    -----
        htmlspecialchars('<a href="x"> &')           → "&lt;a href=&quot;x&quot;&gt; &amp;amp;"
        htmlspecialchars("it's", ENT.QUOTES)         → "it&#039;s"
        htmlspecialchars("it's", ENT.COMPAT)         → "it's"
        htmlspecialchars("it's", ENT.NOQUOTES)       → "it's"
    """

    _table: dict[str, str] = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
    }

    _entities: frozenset[str] = frozenset(_table.values())

    def __new__(cls, string: str, flags: int = ENT.QUOTES, encoding: str = "UTF-8", double_encode: bool = True) -> str:
        if not isinstance(string, str):
            string = str(string)

        act = dict(cls._table)

        if not (flags & 1):
            act.pop("'", None)
        if not (flags & 2):
            act.pop('"', None)

        if double_encode:
            return "".join(act.get(c, c) for c in string)
        return cls._replace_no_double(string, act)

    @classmethod
    def _replace_no_double(cls, string: str, table: dict[str, str]) -> str:
        out: list[str] = []
        i = 0
        while i < len(string):
            amp = string.find("&", i)
            if amp == -1:
                out.append(string[i:])
                break
            out.append(string[i:amp])
            semi = string.find(";", amp)
            if semi != -1:
                entity = string[amp:semi + 1]
                if entity in cls._entities:
                    out.append(entity)
                    i = semi + 1
                    continue
                out.append("&amp;")
            i = amp + 1
        return "".join(out)


@final
class foreach:
    """PHP-style ``foreach`` iteration — works with ``for``, ``with``, and unpacking.

    ``foreach`` returns a reusable iterator wrapper.  Use it in any
    Python iteration context: ``for`` loops, ``with`` statements, list
    comprehensions, and sequence unpacking.

    Usage
    -----
        for val in foreach([10, 20, 30]):
            ...

        for key, val in foreach([10, 20, 30], key=True):
            ...

        for key, val in foreach({"a": 1, "b": 2}, key=True):
            ...

        with foreach([10, 20, 30]) as items:
            for val in items:
                ...

        first, *rest = foreach([1, 2, 3])
    """

    __slots__ = ('_it', '_key')

    def __new__(cls, iterable: Any, *, key: bool = False) -> foreach:
        instance = super().__new__(cls)
        instance._it = iterable
        instance._key = key
        return instance

    def __iter__(self) -> Any:
        if self._key:
            if isinstance(self._it, dict):
                return iter(self._it.items())
            return enumerate(self._it)
        return iter(self._it)

    def __enter__(self) -> Any:
        return self.__iter__()

    def __exit__(self, *args: Any) -> None:
        pass

_TickId: int = 0
_TickRegistry: dict[int, threading.Timer] = {}

@final
class settick:
    """JS-style ``setTimeout`` / ``setInterval`` — schedule callbacks.

    ``settick(fn, ms)`` runs *fn* once after *ms* milliseconds.
    ``settick.interval(fn, ms)`` runs *fn* every *ms* milliseconds.
    Both return a numeric id that can be passed to ``settick.clear(id)``.

    Usage
    -----
        def hello():
            print("hello")

        tid = settick(hello, 1000)            # runs once after 1s
        iid = settick.interval(hello, 500)    # runs every 500ms
        settick.clear(iid)                    # cancel
    """

    __slots__ = ()

    def __new__(cls, fn: Callable[..., Any], ms: float, /, *args: Any) -> int:
        global _TickId, _TickRegistry
        _TickId += 1
        tid = _TickId
        t = threading.Timer(ms / 1000, fn, args)
        t.daemon = True
        t.start()
        _TickRegistry[tid] = t
        return tid

    @classmethod
    def interval(cls, fn: Callable[..., Any], ms: float, /, *args: Any) -> int:
        def _loop() -> None:
            fn(*args)
            t = threading.Timer(ms / 1000, _loop)
            t.daemon = True
            t.start()
            _TickRegistry[tid] = t

        global _TickId, _TickRegistry
        _TickId += 1
        tid = _TickId
        t = threading.Timer(ms / 1000, _loop)
        t.daemon = True
        t.start()
        _TickRegistry[tid] = t
        return tid

    @classmethod
    def clear(cls, tid: int) -> None:
        t = _TickRegistry.pop(tid, None)
        if t:
            t.cancel()


@final
class flush:
    """Delete variables from the caller's scope — like ``del x``.

    ``flush("x")`` removes *x*.  ``flush("x", "y")`` removes multiple.
    ``flush()`` removes all non-underscored local variables.

    Usage
    -----
        x = 42
        flush("x")       # same as ``del x``
        print(x)         # NameError
    """

    __slots__ = ()

    def __new__(cls, *names: str) -> None:
        frame = inspect.currentframe()
        try:
            caller = frame.f_back
            if names:
                for name in names:
                    caller.f_globals.pop(name, None)
                    caller.f_locals.pop(name, None)
            else:
                locals_ = caller.f_locals
                for name in list(locals_):
                    if name.startswith('_'):
                        continue
                    del locals_[name]
        finally:
            del frame


@final
class findpath:
    """Search upward from *start* (default: current dir) for a folder named *name*.

    Usage
    -----
        findpath("src")                # "/home/user/project/src"
        findpath("src", start="..")    # search from parent dir
    """

    __slots__ = ()

    def __new__(cls, name: str, *, start: str | None = None) -> str | None:
        path = pathlib.Path(start or os.getcwd()).resolve()
        for parent in [path] + list(path.parents):
            candidate = parent / name
            if candidate.is_dir():
                return str(candidate)
        return None


@final
class globalize:
    """Find a folder by name upward from the current dir and insert it to ``sys.path[0]``.

    Usage
    -----
        globalize("src")    # /abs/path/to/src is now in sys.path[0]
    """

    __slots__ = ()

    def __new__(cls, name: str, *, start: str | None = None) -> str | None:
        p = findpath(name, start=start)
        if p and p not in sys.path:
            sys.path.insert(0, p)
        return p


@final
class free:
    """Delete variables from the caller's scope — like ``del x``.

    ``free("x")`` removes *x*.  ``free("x", "y")`` removes multiple.
    ``free()`` removes all non-underscored local variables.

    Usage
    -----
        x = 42
        free("x")       # same as ``del x``
        print(x)         # NameError
    """

    __slots__ = ()

    def __new__(cls, *names: str) -> None:
        frame = inspect.currentframe()
        try:
            caller = frame.f_back
            if names:
                for name in names:
                    caller.f_globals.pop(name, None)
                    caller.f_locals.pop(name, None)
            else:
                locals_ = caller.f_locals
                for name in list(locals_):
                    if name.startswith('_'):
                        continue
                    del locals_[name]
        finally:
            del frame

# @final
# class private:
#     __slots__ = ('_func', '_owner')
# 
#     def __new__(cls, func: Callable[..., Any]) -> private:
#         instance = super().__new__(cls)
#         instance._func = func
#         instance._owner = None
#         return instance
# 
#     def __set_name__(self, owner: type, name: str) -> None:
#         self._owner = owner
# 
#     def __get__(self, obj: Any, objtype: type | None = None) -> Any:
#         if obj is None:
#             return self
#         return _BoundPrivate(self._func, obj, self._owner)
    
@final
def private(f):
    """Decorator to indicate final methods and final classes.

    Use this decorator to indicate to type checkers that the decorated
    method cannot be overridden, and decorated class cannot be subclassed.

    For example::

        class Base:
            @private
            def done(self) -> None:
                ...
        class Sub(Base):
            def done(self) -> None:  # Error reported by type checker
                ...

        @private
        class Leaf:
            ...
        class Other(Leaf):  # Error reported by type checker
            ...

    There is no runtime checking of these properties. The decorator
    attempts to set the ``__final__`` attribute to ``True`` on the decorated
    object to allow runtime introspection.
    """
    try:
        f.__final__ = True
    except (AttributeError, TypeError):
        # Skip the attribute silently if it is not writable.
        # AttributeError happens if the object has __slots__ or a
        # read-only property, TypeError if it's a builtin class.
        pass
    return f


class _BoundPrivate:
    __slots__ = ('_func', '_self', '_owner')

    def __init__(self, func: Callable[..., Any], self_: Any, owner: type) -> None:
        self._func = func
        self._self = self_
        self._owner = owner

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        frame = inspect.currentframe()
        try:
            caller = frame.f_back
            while caller:
                cself = caller.f_locals.get('self')
                if isinstance(cself, self._owner):
                    return self._func(self._self, *args, **kwargs)
                ccls = caller.f_locals.get('cls')
                if ccls is self._owner:
                    return self._func(self._self, *args, **kwargs)
                caller = caller.f_back
            raise TypeError(
                f"private method '{self._func.__name__}' cannot be "
                f"accessed outside {self._owner.__name__}"
            )
        finally:
            del frame

def die(message: str = "", /) -> NoReturn:
    if message:
        print(message, file=sys.stderr)
    sys.exit(1)

@final
def sealed(f):
    """Decorator to indicate final methods and final classes.

    Use this decorator to indicate to type checkers that the decorated
    method cannot be overridden, and decorated class cannot be subclassed.

    For example::

        class Base:
            @sealed
            def done(self) -> None:
                ...
        class Sub(Base):
            def done(self) -> None:  # Error reported by type checker
                ...

        @sealed
        class Leaf:
            ...
        class Other(Leaf):  # Error reported by type checker
            ...

    There is no runtime checking of these properties. The decorator
    attempts to set the ``__final__`` attribute to ``True`` on the decorated
    object to allow runtime introspection.
    """
    try:
        f.__final__ = True
    except (AttributeError, TypeError):
        # Skip the attribute silently if it is not writable.
        # AttributeError happens if the object has __slots__ or a
        # read-only property, TypeError if it's a builtin class.
        pass
    return f

class VK(IntEnum):
    LBUTTON = 0x01
    RBUTTON = 0x02
    CANCEL = 0x03
    MBUTTON = 0x04
    XBUTTON1 = 0x05
    XBUTTON2 = 0x06
    BACK = 0x08
    TAB = 0x09
    CLEAR = 0x0C
    RETURN = 0x0D
    SHIFT = 0x10
    CONTROL = 0x11
    MENU = 0x12
    PAUSE = 0x13
    CAPITAL = 0x14
    ESCAPE = 0x1B
    SPACE = 0x20
    PRIOR = 0x21
    NEXT = 0x22
    END = 0x23
    HOME = 0x24
    LEFT = 0x25
    UP = 0x26
    RIGHT = 0x27
    DOWN = 0x28
    SELECT = 0x29
    PRINT = 0x2A
    EXECUTE = 0x2B
    SNAPSHOT = 0x2C
    INSERT = 0x2D
    DELETE = 0x2E
    HELP = 0x2F
    VK_0 = 0x30
    VK_1 = 0x31
    VK_2 = 0x32
    VK_3 = 0x33
    VK_4 = 0x34
    VK_5 = 0x35
    VK_6 = 0x36
    VK_7 = 0x37
    VK_8 = 0x38
    VK_9 = 0x39
    VK_A = 0x41
    VK_B = 0x42
    VK_C = 0x43
    VK_D = 0x44
    VK_E = 0x45
    VK_F = 0x46
    VK_G = 0x47
    VK_H = 0x48
    VK_I = 0x49
    VK_J = 0x4A
    VK_K = 0x4B
    VK_L = 0x4C
    VK_M = 0x4D
    VK_N = 0x4E
    VK_O = 0x4F
    VK_P = 0x50
    VK_Q = 0x51
    VK_R = 0x52
    VK_S = 0x53
    VK_T = 0x54
    VK_U = 0x55
    VK_V = 0x56
    VK_W = 0x57
    VK_X = 0x58
    VK_Y = 0x59
    VK_Z = 0x5A
    LWIN = 0x5B
    RWIN = 0x5C
    APPS = 0x5D
    NUMPAD0 = 0x60
    NUMPAD1 = 0x61
    NUMPAD2 = 0x62
    NUMPAD3 = 0x63
    NUMPAD4 = 0x64
    NUMPAD5 = 0x65
    NUMPAD6 = 0x66
    NUMPAD7 = 0x67
    NUMPAD8 = 0x68
    NUMPAD9 = 0x69
    MULTIPLY = 0x6A
    ADD = 0x6B
    SEPARATOR = 0x6C
    SUBTRACT = 0x6D
    DECIMAL = 0x6E
    DIVIDE = 0x6F
    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    F5 = 0x74
    F6 = 0x75
    F7 = 0x76
    F8 = 0x77
    F9 = 0x78
    F10 = 0x79
    F11 = 0x7A
    F12 = 0x7B
    F13 = 0x7C
    F14 = 0x7D
    F15 = 0x7E
    F16 = 0x7F
    F17 = 0x80
    F18 = 0x81
    F19 = 0x82
    F20 = 0x83
    F21 = 0x84
    F22 = 0x85
    F23 = 0x86
    F24 = 0x87
    NUMLOCK = 0x90
    SCROLL = 0x91
    LSHIFT = 0xA0
    RSHIFT = 0xA1
    LCONTROL = 0xA2
    RCONTROL = 0xA3
    LMENU = 0xA4
    RMENU = 0xA5
    OEM_1 = 0xBA
    OEM_PLUS = 0xBB
    OEM_COMMA = 0xBC
    OEM_MINUS = 0xBD
    OEM_PERIOD = 0xBE
    OEM_2 = 0xBF
    OEM_3 = 0xC0
    OEM_4 = 0xDB
    OEM_5 = 0xDC
    OEM_6 = 0xDD
    OEM_7 = 0xDE
    OEM_8 = 0xDF
    OEM_102 = 0xE2
    PROCESSKEY = 0xE5
    PACKET = 0xE7
    ATTN = 0xF6
    CRSEL = 0xF7
    EXSEL = 0xF8
    EREOF = 0xF9
    PLAY = 0xFA
    ZOOM = 0xFB
    NONAME = 0xFC
    PA1 = 0xFD
    OEM_CLEAR = 0xFE

class Namespace(Generic[_T]):
    Whatever: typing.Any = typing.Any
    Object: type[object] = object
    Integer: type[int] = int
    Float: type[float] = float
    Boolean: type[bool] = bool
    String: type[str] = str
    Complex: type[complex] = complex
    Tuple: type[tuple] = tuple
    List: type[list] = list
    Dict: type[dict] = dict
    Set: type[set] = set
    FrozenSet: type[frozenset] = frozenset
    Range: type[range] = range
    Bytes: type[bytes] = bytes
    ByteArray: type[bytearray] = bytearray
    MemoryView: type[memoryview] = memoryview
    NoneType: type[None] = type(None)
    EllipsisType = type(Ellipsis)
    NotImplementedType = type(NotImplemented)
    Function: type[types.FunctionType] = types.FunctionType
    BuiltinFunction: type[types.BuiltinFunctionType] = types.BuiltinFunctionType
    VirtualCode: type[str] = str
    VirtualCodeValue: type[int] = int
    VirtualCodeIOValue: type[float] = float
    
    @classmethod
    def __class_getitem__(cls, item: Type[_T]) -> Type[_T]:
        """
        Support the [_T] syntax so that you can do:
            x: Namespace[str] = "string"
        """
        return item

    def strict(*dargs, **dkwargs):
        def dc(fun: _F) -> _F:
            return fun
        return dc

    
def noop_decor_callback(func: _F) -> _F:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return cast(_F, wrapper)

def inline(func: _F) -> _F:
    return noop_decor_callback(func)

@final
def export(identifier: str, value: Any, *, ephemeral: Type[Any]):
    """
    No-op decorator that accepts:
    - identifier: str ("self" or "function_name")
    - value: any variable (for annotation)
    """
    def decorator(func: _F) -> _F:
        func._export_identifier = identifier
        func._export_value_type = type(value)
        func._export_ephemeral = ephemeral
        return cast(_F, func)
    return decorator

def critical(func: _F) -> _F:
    return noop_decor_callback(func)

def pure(func: _F) -> _F:
    return noop_decor_callback(func)

def memoize(func: _F) -> _F:
    return noop_decor_callback(func)


class VirtualMachineCode(Generic[_T]):
    _user32 = ctypes.windll.user32

    def __init__(self):
        self.bindings: Dict[str, VK] = {}

    @staticmethod
    def fname(name: str) -> VK:
        return VK[name]

    @staticmethod
    def fcode(code: int) -> VK:
        return VK(code)

    @staticmethod
    def name(vk: VK) -> str:
        return vk.name

    @staticmethod
    def code(vk: VK) -> int:
        return int(vk)

    @staticmethod
    def index(vk: VK) -> int:
        return list(VK).index(vk)

    @staticmethod
    def get_all() -> list[VK]:
        return list(VK)

    @staticmethod
    def pall():
        for vk in VK:
            print(f"{vk.name:<15} = 0x{vk.value:02X}")

    def bind(self, action: str, key: str | VK):
        if isinstance(key, str):
            key = VK[key]
        self.bindings[action] = key

    def get_binding(self, action: str) -> VK | None:
        return self.bindings.get(action)

    @classmethod
    def is_pressed(cls, key: str | VK) -> bool:
        if isinstance(key, str):
            key = VK[key]
        return bool(cls._user32.GetAsyncKeyState(key) & 0x8000)

def guard(value: object | Any | None = None):
    """
    A conditional class decorator factory.

    Enforces integrity constraints or metadata injection on the decorated 
    class based on the provided predicate value.
    """
    if callable(value):
        return value
    def wrapper(cls):
        return cls
    return wrapper

def mark_as_property(flag: object | None = None):
    """
    A class decorator used to mark a class as a specific property type.

    This decorator serves as a metadata marker for classes, allowing other 
    components or registry systems to identify and filter classes based 
    on the provided flag. It does not modify the class structure itself.

    Args:
        flag (object | None, optional): A unique identifier or flag used 
            to categorize the decorated class. Defaults to None.

    Returns:
        Callable[[type], type]: A wrapper function that returns the 
            original class unchanged.

    Example:
        >>> @mark_as_property(flag="UI_COMPONENT")
        >>> class MyButton:
        ...     pass
    """
    def wrapper(cls: Any):
        return cls
    return wrapper

def namespace(cls: Type[T]) -> Type[T]:
    """
    Ensures a class is treated as a semantic namespace for static analysis.

    This decorator acts as a zero-overhead identity function. It is primarily 
    used to explicitly categorize a class as a container for related constants 
    or utility methods, while preserving full type information and preventing 
    type erasure in IDEs like PyCharm or VS Code.

    Args:
        cls: The class to be used as a namespace.

    Returns:
        The original class with its type signature fully intact.

    Note:
        Use this to improve code discoverability and to signal intent that 
        the decorated class should not be instantiated.
    """
    return cls

def tag(value: str, name: str | None = "tag_name"):
    """
    Enforces a contract between a Python class and its HTML tag representation.

    This decorator acts as a guardian of structural integrity during the class 
    definition phase (import-time). It validates that the decorated class 
    correctly defines its target HTML tag, preventing runtime bugs caused by 
    mismatched or missing tag identifiers.

    Args:
        value (str): The mandatory HTML tag string (e.g., 'div', 'section').
        name (str, optional): The attribute name to check within the class. 
            Defaults to "tag_name".

    Returns:
        Callable[[type], type]: A class decorator that validates the target class.

    Raises:
        TypeError: If the provided `value` argument is not a string.
        AttributeError: If the class does not define the attribute specified by `name`.
        ValueError: If the class attribute value does not match the expected `value`.

    Example:
        >>> @tag("div")
        >>> class Div(Element):
        ...     tag_name = "div"  # Passes validation
        
        >>> @tag("p")
        >>> class Paragraph(Element):
        ...     tag_name = "div"  # Raises ValueError: Tag mismatch
    """
    def wrapper(cls):
        if not isinstance(value, str):
            raise TypeError(f"Value must be str, got {type(value).__name__}")
        
        class_attr_value = getattr(cls, name, None)
        
        if class_attr_value is None:
            raise AttributeError(f"Class {cls.__name__} is missing required attribute: '{name}'")  
        
        if class_attr_value != value:
            raise ValueError(
                f"Tag mismatch in {cls.__name__}: "
                f"Expected '{value}', but found '{class_attr_value}'."
            )
            
        return cls
    return wrapper

def distrait_check(slots: bool | None = None):
    """
    Enforces the presence of essential metadata containers on a class.

    This decorator acts as a structural gatekeeper, ensuring that the decorated 
    class explicitly defines a '__traits__' attribute. It is used to prevent 
    the initialization of components that do not comply with the framework's 
    metadata and trait-tracking standards.

    Args:
        slots (bool | None, optional): Reserved for future use to enforce 
            __slots__ alongside traits. Defaults to None.

    Returns:
        Callable[[type], type]: A decorator that validates class attributes.

    Raises:
        AttributeError: If the mandatory '__traits__' attribute is missing 
            from the class definition.
    """
    def wrapper(cls):
        if not hasattr(cls, '__traits__'):
            raise AttributeError(f"Class \'{cls.__name__}\' does not contain attribute: __traits__")
        
        return cls
    return wrapper

def trait(t: str | list | int, attribute: str = "__traits__"):
    """
    Validates that a class adheres to specific functional or behavioral contracts.

    This decorator inspects the class's metadata registry (defaulting to '__traits__') 
    to verify the existence of required markers. It supports singular validation 
    (str, int) or bulk validation (list), ensuring the class is equipped for 
    specific framework operations.

    Args:
        t (str | list | int): The required trait or list of traits to check for.
        attribute (str): The class attribute to inspect for traits. 
            Defaults to "__traits__".

    Returns:
        Callable[[type], type]: A decorator that performs membership validation.

    Raises:
        TypeError: If the 'attribute' argument is not a string.
        AttributeError: If an unauthorized attribute name is provided for inspection.
        ValueError: If one or more required traits are missing from the class registry.
    """
    def wrapper(cls):
        if not isinstance(attribute, str):
            raise TypeError(f"Invalid data type passed for param \'attribute\', got: {type(attribute).__name__}")
        
        if attribute != "__traits__":
            raise AttributeError(f"STD attribute: __traits__, found: {str(attribute)}")
        
        if not t: return cls
        
        if isinstance(t, str):
            slots = getattr(cls, attribute)
            
            if t not in slots:
                raise ValueError(f"Attribute \'{attribute}\' does not contain value \'{str(t)}\'")
            
            return cls
        
        elif isinstance(t, list):
            slots = getattr(cls, attribute)
            
            for item in range(0, len(slots)):
                if t[item] not in slots:
                    raise ValueError(f"Attribute \'{attribute}\' does not contain value \'{str(t[item])}\'")
            
            return cls
        
        elif isinstance(t, int):
            slots = getattr(cls, attribute)
            
            if t not in slots:
                raise ValueError(f"Attribute \'{attribute}\' does not contain value \'{str(t)}\'")
            
            return cls
    return wrapper

def void(cls: Type[T]) -> Type[T]:
    """
    Transforms a class into a strictly defined HTML void element.

    This decorator enforces the structural constraints of void elements (e.g., <img>, <br>). 
    It automatically sets the 'is_void' flag to True and overrides the class 
    constructor to prevent the attachment of child elements, ensuring compliance 
    with HTML5 specification for self-closing tags.

    Args:
        cls (Type[T]): The element class to be transformed into a void type.

    Returns:
        Type[T]: The modified class with restricted initialization logic.

    Raises:
        ValueError: If an attempt is made to instantiate the decorated class 
            with positional arguments (children).

    Example:
        >>> @void
        >>> class Br(Element):
        ...     tag_name = "br"
        >>> br = Br()  # Works
        >>> br = Br("text")  # Raises ValueError: VoidElementError
    """
    cls.is_void = True
    
    original_init = cls.__init__
    
    def locked_init(self, *children, **kwargs):
        if children:
            raise ValueError(
                f"VoidElementError: Tag '<{cls.tag_name} />' cannot have children. "
                f"Attempted to add: {children}"
            )
            
        original_init(self, **kwargs)
        
    cls.__init__ = locked_init
    
    return cls

class CSSFunctions:
    @staticmethod
    def url(path: str) -> str:
        return str(f"url({path})")
    
    @staticmethod
    def var(vname: str) -> str:
        return str(f"var({vname})")
    
    @staticmethod
    def calc(compl: str) -> str:
        return str(f"calc({compl})")
    
    @staticmethod
    def min(m: str) -> str:
        return str(f"min({m})")
    
    @staticmethod
    def max(m: str) -> str:
        return str(f"max({m})")
    
    @staticmethod
    def clamp(i: str) -> str:
        return str(f"clamp({i})")
    
    @staticmethod
    def rgb(rng: str) -> str:
        return str(f"rgb({rng})")
    
    @staticmethod
    def rgba(rng: str) -> str:
        return str(f"rgba({rng})")
    
    @staticmethod
    def hex(rng: str) -> str:
        return str(f"hex({rng})")
    
    @staticmethod
    def hsl(rng: str) -> str:
        return str(f"hsl({rng})")
    
    @staticmethod
    def hsla(rng: str) -> str:
        return str(f"hsla({rng})")
    
    @staticmethod
    def use(f: str, params: str | list[str]) -> str | None:
        if not isinstance(f, str):
            raise TypeError(f"Invalid data type passed for \'f\', got: {type(f).__name__}")
        
        final_str: str | None = None
        
        if isinstance(params, str):
            final_str = f"{f}({params})"
            return final_str
        elif isinstance(params, list):
            final_str = f"{f}(" + " ".join(params) + ")"
            return final_str
        else:
            raise TypeError(f"Invalid or unsupported data type passed for \'params\', got: {type(params).__name__}")
        
    @staticmethod
    def raw(content: str | list[str]):
        if not isinstance(content, str) or not isinstance(content, list):
            raise TypeError(f"Invalid data type passed for \'content\', neither str nor list.")
        
        if isinstance(content, str):
            return f"{content}"
        elif isinstance(content, list):
            return " ".join(content)
        else:
            raise TypeError(f"Invalid data type passed for \'content\', neither str nor list.")

class CSSImport:
    def __init__(self, url: str, layer: Optional[str] = None, supports: Optional[str] = None):
        self.url = url
        self.layer = layer
        self.supports = supports

    def render(self) -> str:
        path = f"url('{self.url}')" if not self.url.startswith(("url(", "'", '"')) else self.url
        
        parts = [f"@import {path}"]
        
        if self.layer:
            parts.append(f"layer({self.layer})")
            
        if self.supports:
            parts.append(f"supports({self.supports})")
            
        return " ".join(parts) + ";"

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return f"Import(url='{self.url}')"

class CSSKeyframes:
    def __init__(self, name: str):
        self.name = name
        self.steps: Dict[str, Dict[str, Any]] = {}

    def add_step(self, offset: Union[str, int], **kwargs: Unpack[CSSStyleScema]) -> 'CSSKeyframes':
        if isinstance(offset, int):
            key = f"{offset}%"
        else:
            key = offset
        rules = {k.replace("_", "-"): v for k, v in kwargs.items()}
        self.steps[key] = rules
        return self

    def render(self) -> str:
        output = [f"@keyframes {self.name} {{"]
        
        for step, rules in self.steps.items():
            content = "\n    ".join([f"{k}: {v};" for k, v in rules.items()])
            output.append(f"  {step} {{\n    {content}\n  }}")
            
        output.append("}")
        return "\n".join(output)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Keyframes(name={self.name}, steps={list(self.steps.keys())})"

class CSSMediaQuery:
    def __init__(self, query: str):
        self.query = query
        self.styles: List[Any] = []

    def add(self, *styles: Any) -> 'CSSMediaQuery':
        for s in styles:
            self.styles.append(s)
        return self

    def render(self) -> str:
        if not self.styles:
            return ""
        
        inner_content = "\n\n".join([s.render_block() for s in self.styles])
        indented_content = "\n  ".join(inner_content.split("\n"))
        
        return f"@media {self.query} {{\n  {indented_content}\n}}"

class CSSMedia:
    @staticmethod
    def custom(query_string: str) -> CSSMediaQuery:
        """Korisnik piše npr. 'max-width: 600px' bez zagrada."""
        return CSSMediaQuery(f"({query_string})")

    @staticmethod
    def max_width(px: Union[int, str]) -> CSSMediaQuery:
        val = f"{px}px" if isinstance(px, int) else px
        return CSSMediaQuery(f"(max-width: {val})")

    @staticmethod
    def min_width(px: Union[int, str]) -> CSSMediaQuery:
        val = f"{px}px" if isinstance(px, int) else px
        return CSSMediaQuery(f"(min-width: {val})")

    @staticmethod
    def range(min_px: Union[int, str], max_px: Union[int, str]) -> CSSMediaQuery:
        min_v = f"{min_px}px" if isinstance(min_px, int) else min_px
        max_v = f"{max_px}px" if isinstance(max_px, int) else max_px
        return CSSMediaQuery(f"(min-width: {min_v}) and (max-width: {max_v})")

    @staticmethod
    def dark() -> CSSMediaQuery:
        return CSSMediaQuery("(prefers-color-scheme: dark)")

    @staticmethod
    def light() -> CSSMediaQuery:
        return CSSMediaQuery("(prefers-color-scheme: light)")

class CSSStyleScema(TypedDict):
    color: NotRequired[Optional[Union[str, Any]]]
    background_color: NotRequired[Optional[Union[str, Any]]]
    background: NotRequired[Optional[Union[str, Any]]]
    background_image: NotRequired[Optional[Union[str, Any]]]
    border: NotRequired[Optional[Union[str, Any]]]
    border_color: NotRequired[Optional[Union[str, Any]]]
    border_radius: NotRequired[Optional[Union[str, Any]]]
    border_width: NotRequired[Optional[Union[str, Any]]]
    border_style: NotRequired[Optional[Union[str, Any]]]
    width: NotRequired[Optional[Union[str, Any]]]
    height: NotRequired[Optional[Union[str, Any]]]
    min_width: NotRequired[Optional[Union[str, Any]]]
    max_width: NotRequired[Optional[Union[str, Any]]]
    min_height: NotRequired[Optional[Union[str, Any]]]
    max_height: NotRequired[Optional[Union[str, Any]]]
    padding: NotRequired[Optional[Union[str, Any]]]
    padding_top: NotRequired[Optional[Union[str, Any]]]
    padding_bottom: NotRequired[Optional[Union[str, Any]]]
    padding_left: NotRequired[Optional[Union[str, Any]]]
    padding_right: NotRequired[Optional[Union[str, Any]]]
    margin: NotRequired[Optional[Union[str, Any]]]
    inset: NotRequired[Optional[Union[str, Any]]]
    margin_top: NotRequired[Optional[Union[str, Any]]]
    margin_bottom: NotRequired[Optional[Union[str, Any]]]
    margin_left: NotRequired[Optional[Union[str, Any]]]
    margin_right: NotRequired[Optional[Union[str, Any]]]
    font_family: NotRequired[Optional[Union[str, Any]]]
    font_size: NotRequired[Optional[Union[str, Any]]]
    font_weight: NotRequired[Optional[Union[str, Any]]]
    text_align: NotRequired[Optional[Union[str, Any]]]
    text_decoration: NotRequired[Optional[Union[str, Any]]]
    line_height: NotRequired[Optional[Union[str, Any]]]
    letter_spacing: NotRequired[Optional[Union[str, Any]]]
    text_transform: NotRequired[Optional[Union[str, Any]]]
    display: NotRequired[Optional[Union[str, Any]]]
    position: NotRequired[Optional[Union[str, Any]]]
    top: NotRequired[Optional[Union[str, Any]]]
    right: NotRequired[Optional[Union[str, Any]]]
    bottom: NotRequired[Optional[Union[str, Any]]]
    left: NotRequired[Optional[Union[str, Any]]]
    z_index: NotRequired[Optional[Union[str, Any]]]
    overflow: NotRequired[Optional[Union[str, Any]]]
    opacity: NotRequired[Optional[Union[str, Any]]]
    visibility: NotRequired[Optional[Union[str, Any]]]
    flex: NotRequired[Optional[Union[str, Any]]]
    flex_direction: NotRequired[Optional[Union[str, Any]]]
    justify_content: NotRequired[Optional[Union[str, Any]]]
    align_items: NotRequired[Optional[Union[str, Any]]]
    flex_wrap: NotRequired[Optional[Union[str, Any]]]
    gap: NotRequired[Optional[Union[str, Any]]]
    flex_grow: NotRequired[Optional[Union[str, Any]]]
    grid_template_columns: NotRequired[Optional[Union[str, Any]]]
    grid_template_rows: NotRequired[Optional[Union[str, Any]]]
    grid_area: NotRequired[Optional[Union[str, Any]]]
    box_shadow: NotRequired[Optional[Union[str, Any]]]
    text_shadow: NotRequired[Optional[Union[str, Any]]]
    cursor: NotRequired[Optional[Union[str, Any]]]
    transition: NotRequired[Optional[Union[str, Any]]]
    transform: NotRequired[Optional[Union[str, Any]]]
    filter: NotRequired[Optional[Union[str, Any]]]
    outline: NotRequired[Optional[Union[str, Any]]]

class CSSRule:
    @staticmethod
    def _parse(obj: Any) -> str:
        return str(obj)

    @staticmethod
    def _hover(obj: Any) -> str: return f"{CSSRule._parse(obj)}:hover"

    @staticmethod
    def _active(obj: Any) -> str: return f"{CSSRule._parse(obj)}:active"

    @staticmethod
    def _focus(obj: Any) -> str: return f"{CSSRule}:focus"

    @staticmethod
    def _first_child(obj: Any) -> str: return f"{CSSRule._parse(obj)}:first-child"

    @staticmethod
    def _last_child(obj: Any) -> str: return f"{CSSRule._parse(obj)}:last-child"

    @staticmethod
    def _nth_child(obj: Any, n: Union[int, str]) -> str: return f"{CSSRule._parse(obj)}:nth-child({n})"

    @staticmethod
    def _not(obj: Any, selector: str) -> str: return f"{CSSRule._parse(obj)}:not({selector})"

    @staticmethod
    def _checked(obj: Any) -> str: return f"{CSSRule._parse(obj)}:checked"

    @staticmethod
    def _disabled(obj: Any) -> str: return f"{CSSRule._parse(obj)}:disabled"

    @staticmethod
    def __after(obj: Any) -> str: return f"{CSSRule._parse(obj)}::after"

    @staticmethod
    def __before(obj: Any) -> str: return f"{CSSRule._parse(obj)}::before"

    @staticmethod
    def __placeholder(obj: Any) -> str: return f"{CSSRule._parse(obj)}::placeholder"

    @staticmethod
    def __selection(obj: Any) -> str: return f"{CSSRule._parse(obj)}::selection"

    @staticmethod
    def __first_line(obj: Any) -> str: return f"{CSSRule._parse(obj)}::first-line"

    @staticmethod
    def __first_letter(obj: Any) -> str: return f"{CSSRule._parse(obj)}::first-letter"

    @staticmethod
    def attr(obj: Any, name: str, value: Optional[str] = None, op: str = "=") -> str:
        t = CSSRule._parse(obj)
        return f"{t}[{name}]" if value is None else f"{t}[{name}{op}\"{value}\"]"

    @staticmethod
    def combine(first: Any, second: Any, separator: str = " ") -> str:
        return f"{CSSRule._parse(first)}{separator}{CSSRule._parse(second)}"

    class global_:
        def __init__(self, iden: str): self.iden = iden
        def __str__(self) -> str: return self.iden

    class class_:
        def __init__(self, iden: str): self.iden = iden
        def __str__(self) -> str: return f".{self.iden}"

    class id:
        def __init__(self, iden: str): self.iden = iden
        def __str__(self) -> str: return f"#{self.iden}"

class CSSStyle:
    def __init__(self, target: Optional[Union[Any, List[Any]]] = None, **kwargs: Unpack[CSSStyleScema]):
        self.targets = target if isinstance(target, list) else ([target] if target else [])
        self.rules = {k.replace("_", "-"): v for k, v in kwargs.items()}
        self.sub_styles: List['CSSStyle'] = []

    def _compile_selector(self) -> str:
        res = []
        for t in self.targets:
            if isinstance(t, str) and not t.startswith((".", "#", ":", "@")):
                res.append(f".{t}")
            else:
                res.append(str(t))
        return ", ".join(res)

    def hover(self, **kwargs: Unpack[CSSStyleScema]) -> 'CSSStyle':
        new_targets = [t.hover() if hasattr(t, 'hover') else f"{str(t)}:hover" for t in self.targets]
        s = CSSStyle(target=new_targets, **kwargs)
        self.sub_styles.append(s)
        return self

    def active(self, **kwargs: Unpack[CSSStyleScema]) -> 'CSSStyle':
        new_targets = [t.active() if hasattr(t, 'active') else f"{str(t)}:active" for t in self.targets]
        s = CSSStyle(target=new_targets, **kwargs)
        self.sub_styles.append(s)
        return self

    def focus(self, **kwargs: Unpack[CSSStyleScema]) -> 'CSSStyle':
        new_targets = [t.focus() if hasattr(t, 'focus') else f"{str(t)}:focus" for t in self.targets]
        s = CSSStyle(target=new_targets, **kwargs)
        self.sub_styles.append(s)
        return self

    def sibling(self, other: Any, direct: bool = False, **kwargs: Unpack[CSSStyleScema]) -> 'CSSStyle':
        symbol = "+" if direct else "~"
        new_targets = [f"{str(t)} {symbol} {str(other)}" for t in self.targets]
        s = CSSStyle(target=new_targets, **kwargs)
        self.sub_styles.append(s)
        return self

    def child(self, other: Any, direct: bool = False, **kwargs: Unpack[CSSStyleScema]) -> 'CSSStyle':
        symbol = ">" if direct else ""
        new_targets = [f"{str(t)} {symbol} {str(other)}".replace("  ", " ") for t in self.targets]
        s = CSSStyle(target=new_targets, **kwargs)
        self.sub_styles.append(s)
        return self

    def render_inline(self) -> str:
        return "; ".join([f"{k}: {v}" for k, v in self.rules.items()]) + (";" if self.rules else "")

    def render_block(self) -> str:
        output = []
        if self.targets and self.rules:
            selector = self._compile_selector()
            body = "\n  ".join([f"{k}: {v};" for k, v in self.rules.items()])
            output.append(f"{selector} {{\n  {body}\n}}")
        for sub in self.sub_styles:
            output.append(sub.render_block())
        return "\n\n".join(output)

    def __str__(self) -> str:
        return self.render_inline()

    def __repr__(self) -> str:
        return f"Style(targets={self._compile_selector()})"
    
class CSSStyleSheet:
    def __init__(self):
        self.imports: List[CSSImport] = []
        self.keyframes: List[CSSKeyframes] = []
        self.styles: List[CSSStyle] = []
        self.media_queries: List[CSSMediaQuery] = []

    def add(self, item: Union[CSSImport, CSSStyle, CSSKeyframes, CSSMediaQuery]):
        if isinstance(item, CSSImport):
            self.imports.append(item)
        elif isinstance(item, CSSKeyframes):
            self.keyframes.append(item)
        elif isinstance(item, CSSMediaQuery):
            self.media_queries.append(item)
        else:
            self.styles.append(item)
        return item

    def render(self) -> str:
        sections = [
            "\n".join([i.render() for i in self.imports]),
            "\n\n".join([s.render_block() for s in self.styles]),
            "\n\n".join([k.render() for k in self.keyframes]),
            "\n\n".join([m.render() for m in self.media_queries])
        ]
        return "\n\n".join([section for section in sections if section.strip()])

    def save(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.render())

class JSEvents(TypedDict):
    on_click: NotRequired[Optional[str]]
    on_dblclick: NotRequired[Optional[str]]
    on_mousedown: NotRequired[Optional[str]]
    on_mouseup: NotRequired[Optional[str]]
    on_mouseover: NotRequired[Optional[str]]
    on_mouseout: NotRequired[Optional[str]]
    on_mousemove: NotRequired[Optional[str]]
    on_keydown: NotRequired[Optional[str]]
    on_keyup: NotRequired[Optional[str]]
    on_keypress: NotRequired[Optional[str]]
    on_change: NotRequired[Optional[str]]
    on_input: NotRequired[Optional[str]]
    on_submit: NotRequired[Optional[str]]
    on_focus: NotRequired[Optional[str]]
    on_blur: NotRequired[Optional[str]]
    on_load: NotRequired[Optional[str]]
    on_resize: NotRequired[Optional[str]]
    on_scroll: NotRequired[Optional[str]]

class HTMLSchema(TypedDict):
    id: NotRequired[Optional[str]]
    class_: NotRequired[Optional[str]]
    style: NotRequired[Optional[Any]]
    title: NotRequired[Optional[str]]
    lang: NotRequired[Optional[str]]
    dir: NotRequired[Optional[str]]
    hidden: NotRequired[Optional[bool]]
    tabindex: NotRequired[Optional[int]]
    role: NotRequired[Optional[str]]
    src: NotRequired[Optional[str]]
    alt: NotRequired[Optional[str]]
    href: NotRequired[Optional[str]]
    target: NotRequired[Optional[str]]
    rel: NotRequired[Optional[str]]
    download: NotRequired[Optional[Any]]
    type: NotRequired[Optional[str]]
    value: NotRequired[Optional[Any]]
    placeholder: NotRequired[Optional[str]]
    name: NotRequired[Optional[str]]
    required: NotRequired[Optional[bool]]
    disabled: NotRequired[Optional[bool]]
    checked: NotRequired[Optional[bool]]
    readonly: NotRequired[Optional[bool]]
    action: NotRequired[Optional[str]]
    method: NotRequired[Optional[str]]
    on_click: NotRequired[Optional[str]]
    on_submit: NotRequired[Optional[str]]
    on_change: NotRequired[Optional[str]]
    on_mouseover: NotRequired[Optional[str]]
    on_keydown: NotRequired[Optional[str]]
    on_load: NotRequired[Optional[str]]

class HTMLElement:
    tag_name: str = "div"
    is_void: bool = False
    is_raw: bool = False

    def __init__(self, *children: Any, **kwargs: Unpack[HTMLSchema]):
        self.children = [] if self.is_void else list(children)
        self.attributes = {}
        for k, v in kwargs.items():
            if k.startswith("on_"):
                clean_key = k.replace("_", "")
            else:
                clean_key = k.rstrip('_').replace('_', '-')
            self.attributes[clean_key] = v

    def _render_attributes(self) -> str:
        res = []
        for k, v in self.attributes.items():
            if v is None or v is False: continue
            if v is True:
                res.append(k)
                continue
            if k == "style" and hasattr(v, 'render_inline'):
                val = v.render_inline()
            else:
                val = str(v)
            
            res.append(f'{k}="{val}"')
        
        return " " + " ".join(res) if res else ""

    def render(self, indent: int = 0) -> str:
        tab = "  " * indent
        attrs = self._render_attributes()
        if self.is_void:
            return f"{tab}<{self.tag_name}{attrs} />"
        if self.is_raw:
            content = "\n".join([str(c) for c in self.children])
            if self.tag_name == "php":
                return f"{tab}<?php\n{content}\n{tab}?>"
            return f"{tab}<{self.tag_name}{attrs}>\n{content}\n{tab}</{self.tag_name}>"
        if not self.children:
            return f"{tab}<{self.tag_name}{attrs}></{self.tag_name}>"

        opening = f"{tab}<{self.tag_name}{attrs}>"
        closing = f"{tab}</{self.tag_name}>"
        
        rendered_children = []
        for child in self.children:
            if isinstance(child, HTMLElement):
                rendered_children.append(child.render(indent + 1))
            else:
                rendered_children.append(f"{tab}  {str(child)}")

        return "\n".join([opening] + rendered_children + [closing])

    def __str__(self) -> str:
        return self.render()

class HTMLDocument:
    def __init__(self, title: str = "My Framework Page", lang: str = "en"):
        self.title = title
        self.lang = lang
        self.stylesheets: List[CSSStyleSheet] = []
        self.body_elements: List[HTMLElement] = []
        self.meta_tags: List[HTMLElement] = []
        self.scripts: List[HTMLElement] = []

    def add_style(self, sheet: CSSStyleSheet):
        self.stylesheets.append(sheet)
        return sheet

    def add_body(self, *elements: HTMLElement):
        self.body_elements.extend(elements)
        return elements

    def add_script(self, script_element: HTMLElement):
        self.scripts.append(script_element)
        return script_element

    def render(self) -> str:
        full_css = "\n".join([s.render() for s in self.stylesheets])
        html = [
            f'<!DOCTYPE html>',
            f'<html lang="{self.lang}">',
            '  <head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>{self.title}</title>',
            '    <style>',
            f'      {self._indent_text(full_css, 3)}',
            '    </style>',
            '  </head>',
            '  <body>',
        ]

        for el in self.body_elements:
            html.append(el.render(indent=2))

        for script in self.scripts:
            html.append(script.render(indent=2))

        html.append('  </body>')
        html.append('</html>')

        return "\n".join(html)

    def _indent_text(self, text: str, levels: int) -> str:
        lines = text.split("\n")
        indent = "  " * levels
        return f"\n{indent}".join(lines)

    def save(self, filename: str = "index.html"):
        if not filename.endswith(".html"):
            filename += ".html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.render())
        print(f"Document created: {filename}")

@guard
class DomProperties:
    @staticmethod
    def id(parse: str) -> str: return str(parse)
    
    @staticmethod
    def class_(parse: str) -> str: return str(parse)
    
    @staticmethod
    def style(parse: str) -> str: return str(parse)
    
    @staticmethod
    @void
    def html() -> bool: return True
    
    @staticmethod
    def lang(parse: str) -> str: return str(parse)
    

"""
HTML5 Element Library
=====================

This module serves as the primary registry for HTML elements within the framework. 
Each class is strategically enhanced with decorators to enforce web standards:

- Standard Elements: Inherit basic nesting and rendering capabilities.
- @void: Enforces self-closing tag structures and prevents child injection.
- @guard: Protects sensitive or raw elements (Meta, Script, PHP) from 
  unintended structural modifications or escaping.

Usage:
    >>> div = Div(P("Hello World"), class_="container")
    >>> img = Img(src="logo.png")  # Protected by @void
"""


class Div(HTMLElement): tag_name = "div"
class Span(HTMLElement): tag_name = "span"
class P(HTMLElement): tag_name = "p"
class H1(HTMLElement): tag_name = "h1"
class H2(HTMLElement): tag_name = "h2"
class H3(HTMLElement): tag_name = "h3"
class A(HTMLElement): tag_name = "a"
class Button(HTMLElement): tag_name = "button"
class Ul(HTMLElement): tag_name = "ul"
class Li(HTMLElement): tag_name = "li"
class Form(HTMLElement): tag_name = "form"
class Label(HTMLElement): tag_name = "label"
class Section(HTMLElement): tag_name = "section"
class Nav(HTMLElement): tag_name = "nav"
class Header(HTMLElement): tag_name = "header"
class Footer(HTMLElement): tag_name = "footer"
@void
class Img(HTMLElement): tag_name = "img"; is_void = True
@void
class Input(HTMLElement): tag_name = "input"; is_void = True
@void
class Br(HTMLElement): tag_name = "br"; is_void = True
@void
class Hr(HTMLElement): tag_name = "hr"; is_void = True
@void
class Link(HTMLElement): tag_name = "link"; is_void = True
@void
@guard
class Meta(HTMLElement): tag_name = "meta"; is_void = True
@guard
class Script(HTMLElement): tag_name = "script"; is_raw = True
@guard
class PHP(HTMLElement): tag_name = "php"; is_raw = True
@guard
class StyleTag(HTMLElement): tag_name = "style"; is_raw = True

class TagSchema(str):
    tag_name = ""

    def __new__(cls, content: str):
        target = cls.tag_name if cls.tag_name else cls.__name__.lower()
        if f"<{target}" not in content.lower():
            raise TypeError(f"ValidationError: Passed tag does not contain <{target}> tag.")
        return super().__new__(cls, content)

@distrait_check
@trait(["PEP", "T"])
class DomType:
    __traits__ = ("PEP", "T")
    
    @tag("doctype")
    @guard
    class DOCTYPE(TagSchema):
        tag_name = "doctype"
    
    @tag("html")
    @guard
    class HTML(TagSchema):
        tag_name = "html"
    
    @tag("head")
    @guard
    class HEAD(TagSchema):
        tag_name = "head"
    
    @tag("meta")
    @guard
    class META(TagSchema):
        tag_name = "meta"
    
    @tag("title")
    @guard
    class TITLE(TagSchema):
        tag_name = "title"
    
    @tag("link")
    @guard
    class LINK(TagSchema):
        tag_name = "link"
    
    @tag("style")
    @guard
    class STYLE(TagSchema):
        tag_name = "style"
        
    @tag("body")
    @guard
    class BODY(TagSchema):
        tag_name = "body"

class PyenvFileHandler:
    def __init__(
        self,
        path: str,
        *,
        origins: bool = True,
        autoclose=True,
        slots=True
    ):
        self.path: str = path
        self.autoclose: bool = autoclose
        self.slots: bool = slots
        self.data: list[str] = []
        self.origins: bool = origins
        
    def file_open(self):
        if not self.data or len(self.data):
            if self.origins:
                error_msg = PyenvText("No origins found.").apply_color(colorama.Fore.RED)
                print(error_msg)
                return None
            else:
                return None
            
        if not self.autoclose: return
        
        try:
            with open(self.path, "r") as file:
                items = file.readlines()
                
                for item in items:
                    item = item.strip()
                    
                    if not item:
                        continue
                    
                    if item.startswith((";", "/", "*", "#")):
                        continue
                    
                    self.data.append(item)
                    
                return True
            return False
        except FileNotFoundError as error:
            raise FileNotFoundError(str(error))
        
        
    @property.getter
    def getPath(self) -> str: return str(self.path)
    
    @property.setter
    def setPath(self) -> None:
        raise ValueError(f"Cant modify already loaded relative path.")  

class PyenvText:
    def __init__(self, content: str, autoreset=False) -> None:
        self.content: str = content
        self.autoreset: bool = autoreset
        colorama.init(autoreset=self.autoreset)
        
    def apply_color(self, color: str) -> str:
        if not color:
            raise AttributeError(f"Invalid color provided to the function.")
        
        if not isinstance(color, str):
            raise TypeError(f"Invalid data type passed for \'color\', got {type(color).__name__}")
        
        return f"{color}{self.content}"
    
    def pprint(self, obj: str | None = None) -> None:
        if not obj:
            print(self.content)
            return None
        else:
            if not isinstance(obj, str):
                raise TypeError(f"Invalid data type passed for \'obj\', got {type(obj).__name__}")
            print(obj)
            return None

class PyEnv:
    def __init__(
        self,
        path: str,
        origins=True
    ):
        self.path = path
        self.origins = origins
        self.buffer: list[str] = []
        self.data: list[str] | None = None
        
    def assign(self):
        if not isinstance(self.path, str):
            raise TypeError(f"Invalid data type provided for \'path\', got {type(self.path).__name__}")
        
        if not isinstance(self.origins, bool):
            raise TypeError(f"Invalid data type provided for \'origins\', got {type(self.origins).__name__}")
        
        self.data = PyenvFileHandler(self.path, origins=self.origins, autoclose=True, slots=True).file_open()
        
        if not self.data or len(self.data) == 0:
            if self.origins:
                raise ValueError(f"Data cant be resolved.")
            else:
                return None
        

    @property.setter
    def data(self):
        raise ValueError(f"Can't manually assign value to the file buffer.")
    
    @property.getter
    def data(self):
        raise ValueError(f"Can't manually get value from the file buffer.")
    
    def append_key(self, key: dict[str, str] | str, value: str | None = None) -> bool | None:
        if not self.data or len(self.data) == 0:
            return None
        
        if not isinstance(key, (dict, str)):
            raise TypeError(f"Invalid data type passed for \'key\', got {type(key).__name__}")
        
        if isinstance(key, str) and value is None:
            raise ValueError(f"Key pair dismatch.")
        
        self.buffer = self.data
        
        if isinstance(key, dict) and value is None:
            for k, v in key.items():
                self.buffer.append(f"{k.strip()}={v.strip()}")
                
        elif isinstance(key, str) and value is not None:
            key = key.strip()
            self.buffer.append(key)
            
        try:
            with open(self.path, "w") as file:
                for item in range(0, len(self.buffer)):
                    file.write(self.buffer[item].strip())
                return True
            return False
        except (FileNotFoundError, Exception) as error:
            raise FileNotFoundError(str(error))
        
def sloted(attribute: str = "__slots__"):
    def wrapper(cls):
        if not hasattr(cls, attribute):
            raise AttributeError(
                f"Class \'{cls.__name__}\' is missing the requred argument: \'{attribute}\'"
            )
        return cls
    return wrapper

def has_sloted_value(attribute: str, value: str):
    def wrapper(cls):
        if not hasattr(cls, attribute):
            raise AttributeError(
                f"Class '{cls.__name__}' does not have attribute '{attribute}'"
            )
        
        slots_content = getattr(cls, attribute)
        if value not in slots_content:
            raise ValueError(
                f"Class '{cls.__name__}' u '{attribute}' does not contain value: '{value}'"
            )

        return cls
    return wrapper

@sloted
@has_sloted_value("__slots__", "type")
@trait('type')
class PyEnvType(typing.Generic[T]):
    __slots__ = ("type",)
    __trait__ = ('type',)

    def __init__(self, cout: typing.Type[T]):
        self.cout = cout
        pass

def compare(str1: str, str2: str, /) -> bool:
    return str1.strip() == str2.strip()

class const:
    def __init__(self, value: Any, /) -> None:
        self.value = value

    @property
    def value(self) -> Any: return self.value

    @value.getter
    def value(self) -> Any: return self.value

    @value.setter
    def value(self) -> None:
        raise TypeError(f"Cannot change value to a const variable.")
    
    def __repr__(self) -> Any:
        f"""{self.__repr__.__name__}-r"""
        return self.value

def default(obj: object, val: Any | None = None, /) -> Any:
    if val is None or empty(val):
        return None
    
    if empty(obj):
        return val
    
def invoke(module: str, scope: str, /) -> bool:
    """Check if the current module was executed as the entry point script.

    Returns True when `module` (typically ``__name__``) matches `scope`
    (typically the string ``"__main__"``), meaning the file was run
    directly by the interpreter rather than imported by another module.

    Intended usage at the bottom of a script:

        if invoke(__name__, "__main__"):
            main_entry()

    Parameters
    ----------
    module : str
        The module's name, always pass ``__name__`` here.
    scope : str
        The target identifier, always pass ``"__main__"`` here.

    Returns
    -------
    bool
        True if the module is the program's entry point, False otherwise.
    """

    return module == scope

class mastermethod:
    """Descriptor that transforms a method into one receiving both ``cls`` and ``self``.

    A ``mastermethod`` combines aspects of :func:`classmethod` and
    :class:`~object.__get__` descriptor semantics. The decorated method is
    called with ``(cls, self, *args, **kwargs)``, where *cls* is the owning
    class and *self* is the instance (or ``None`` when accessed on the class
    directly).

    This is useful when a utility method needs access to both instance state
    and class-level configuration without requiring the caller to explicitly
    pass either.

    .. code-block:: python

        class Service:
            timeout = 30

            def __init__(self, url: str) -> None:
                self.url = url

            @mastermethod
            def connect(cls, self, retries: int = 3) -> str:
                if self is not None:
                    print(f"Connecting to {self.url}")
                print(f"  timeout={cls.timeout}s, retries={retries}")
                return "ok"

        # Called on an instance — both ``cls`` and ``self`` are populated:
        >>> svc = Service("https://example.com")
        >>> svc.connect()
        Connecting to https://example.com
          timeout=30s, retries=3
        'ok'

        # Called on the class — ``self`` is ``None``:
        >>> Service.connect()
          timeout=30s, retries=3
        'ok'
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        @functools.wraps(self.func)
        def wrapper(*args, **kwargs):
            return self.func(owner, instance, *args, **kwargs)
        return wrapper

def new[T](obj: T, /) -> T:
    """Return ``obj`` unchanged after inferring its type parameter *T*.

    Unlike a bare reference or identity function, ``new()`` forces the type
    checker to resolve *T* at the call site, making it useful for narrowing
    union types or providing an explicit type anchor without a runtime cast.

    This pairs naturally with generic contexts where a constructor or factory
    returns a broad type but the caller knows the precise subtype:

    Examples
    --------
    Basic usage – type checker narrows a union:

        >>> x: int | str = "hello"
        >>> y = new(x)          # revealed type is str, not int | str

    With generic containers:

        >>> items: list[object] = [1, "two", 3.0]
        >>> nums = new[list[int]](items)  # lights-out cast, no runtime check
    """
    return obj

@final
def private(f):
    """Decorator to indicate final methods and final classes.

    Use this decorator to indicate to type checkers that the decorated
    method cannot be overridden, and decorated class cannot be subclassed.

    For example::

        class Base:
            @private
            def done(self) -> None:
                ...
        class Sub(Base):
            def done(self) -> None:  # Error reported by type checker
                ...

        @private
        class Leaf:
            ...
        class Other(Leaf):  # Error reported by type checker
            ...

    There is no runtime checking of these properties. The decorator
    attempts to set the ``__final__`` attribute to ``True`` on the decorated
    object to allow runtime introspection.
    """
    try:
        f.__final__ = True
    except (AttributeError, TypeError):
        # Skip the attribute silently if it is not writable.
        # AttributeError happens if the object has __slots__ or a
        # read-only property, TypeError if it's a builtin class.
        pass
    return f

def public[T](f: T) -> T:
    """Mark a method or class as part of the public API.

    Purpose
    -------
    Python has no language-level access control, so this decorator
    serves as a visible contract: decorated methods are **intended**
    to be overridden in subclasses and decorated classes are **intended**
    to be subclassed.  Everything else should be treated as internal
    and may change between releases without notice.

    Usage
    -----
        class Base:
            @public
            def hook(self):
                ...

        @public
        class Extensible:
            ...

    Parameter
    ---------
    f
        The function or class being marked as public.

    Returns
    -------
    object
    """
    return f

@final
def sealed(f):
    """Decorator to indicate final methods and final classes.

    Use this decorator to indicate to type checkers that the decorated
    method cannot be overridden, and decorated class cannot be subclassed.

    For example::

        class Base:
            @sealed
            def done(self) -> None:
                ...
        class Sub(Base):
            def done(self) -> None:  # Error reported by type checker
                ...

        @sealed
        class Leaf:
            ...
        class Other(Leaf):  # Error reported by type checker
            ...

    There is no runtime checking of these properties. The decorator
    attempts to set the ``__final__`` attribute to ``True`` on the decorated
    object to allow runtime introspection.
    """
    try:
        f.__final__ = True
    except (AttributeError, TypeError):
        # Skip the attribute silently if it is not writable.
        # AttributeError happens if the object has __slots__ or a
        # read-only property, TypeError if it's a builtin class.
        pass
    return f

def standalone(module: str, /) -> bool | NoReturn:
    """Harden a module against accidental import execution.

    Call at module level in any script that must ***only*** be run directly:

        standalone(__name__)
        # ... rest of script ...

    If the module IS the entry point (``__name__ == "__main__"``),
    returns True and execution continues normally.

    If the module is being imported, immediately exits with code 1,
    preventing the rest of the module body from running in an
    unintended context. This is a safety belt — it catches the
    case where someone writes ``import myscript`` and avoids
    silent side effects.

    Parameters
    ----------
    module : str
        Always pass ``__name__`` here.  The function checks
        whether it equals ``"__main__"``.

    Returns
    -------
    bool
        ``True`` when the module is the entry point.

    Raises
    ------
    SystemExit
        When ``module != "__main__"`` — exits the process with
        code 1 to prevent execution as an import.
    """
    if module == "__main__":
        return True
    sys.exit(1)

@final
class Vector(Generic[T]):
    _type_arg: type = object

    def __class_getitem__(cls, item):
        name = f"{cls.__name__}[{getattr(item, '__name__', str(item))}]"
        return type(name, (cls,), {'_type_arg': item})

    @overload
    def __init__(self, x: T, y: T, /) -> None: ...
    @overload
    def __init__(self, x: T, y: T, z: T, /) -> None: ...
    def __init__(self, *points: T) -> None:
        expected = self._type_arg
        for p in points:
            if not isinstance(p, expected):
                raise TypeError(
                    f"Expected {expected.__name__}, got {type(p).__name__}"
                )
        if len(points) not in (2, 3):
            raise ValueError("Vector must have 2 or 3 elements.")
        self._points = points

    @property
    def x(self) -> T: return self._points[0]
    @property
    def y(self) -> T: return self._points[1]

    @property
    def z(self) -> T | None:
        return self._points[2] if len(self._points) == 3 else None

    def __iter__(self):
        return iter(self._points)

    def __len__(self) -> int:
        return len(self._points)

    def __repr__(self) -> str:
        return f"Vector({', '.join(map(repr, self._points))})"