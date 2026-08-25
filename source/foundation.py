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
import datetime as _dt_module
import logging
import dataclasses
import tempfile
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
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from copy import deepcopy

logging.basicConfig(level=logging.INFO)
colorama.init(autoreset=True)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])
U = TypeVar("U")
E = TypeVar("E", bound=BaseException)
P = ParamSpec("P")
R = TypeVar("R")
K = TypeVar("K")
V = TypeVar("V")

@dataclass(frozen=True, slots=True)
class Cow(Generic[T]):
    _Borrowed: ClassVar[type]
    _Owned: ClassVar[type]

    def is_borrowed(self) -> bool:
        return isinstance(self, _CowBorrowed)

    def is_owned(self) -> bool:
        return isinstance(self, _CowOwned)

    def as_ref(self) -> T:
        if isinstance(self, _CowBorrowed):
            return self._data
        return self._data

    def into_owned(self) -> T:
        if isinstance(self, _CowOwned):
            return self._data
        return copy.deepcopy(self._data)

    def to_owned(self) -> T:
        if isinstance(self, _CowOwned):
            return self._data
        return copy.deepcopy(self._data)

    def map(self, fn: Callable[[T], U]) -> Cow[U]:
        if isinstance(self, _CowOwned):
            return CowOwned(fn(self._data))
        return CowBorrowed(fn(self._data))

    def unwrap(self) -> T:
        if isinstance(self, _CowOwned):
            return self._data
        return self._data

    def __repr__(self) -> str:
        if isinstance(self, _CowBorrowed):
            return f"Cow::Borrowed({self._data!r})"
        return f"Cow::Owned({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cow):
            return self.as_ref() == other.as_ref()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.as_ref())


@dataclass(frozen=True, slots=True)
class _CowBorrowed(Cow[T]):
    _data: T


@dataclass(frozen=True, slots=True)
class _CowOwned(Cow[T]):
    _data: T


Cow._Borrowed = _CowBorrowed
Cow._Owned = _CowOwned


def CowBorrowed(value: T) -> Cow[T]:
    return _CowBorrowed(value)


def CowOwned(value: T) -> Cow[T]:
    return _CowOwned(value)


class Lazy(Generic[T]):
    __slots__ = ("_fn", "_value", "_computed", "_lock")

    def __init__(self, fn: Callable[[], T]) -> None:
        self._fn = fn
        self._value: T = None  # type: ignore[assignment]
        self._computed = False
        self._lock = threading.Lock()

    def force(self) -> T:
        if self._computed:
            return self._value
        with self._lock:
            if not self._computed:
                self._value = self._fn()
                self._computed = True
        return self._value

    def is_forced(self) -> bool:
        return self._computed

    def try_into_inner(self) -> T | None:
        if not self._computed:
            return None
        return self._value

    def __repr__(self) -> str:
        if self._computed:
            return f"Lazy({self._value!r})"
        return "Lazy(<not initialized>)"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Lazy):
            return self.force() == other.force()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.force())

    def __bool__(self) -> bool:
        return bool(self.force())

    def __iter__(self) -> Iterator[T]:
        return iter(self.force())


class Box(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    @classmethod
    def new(cls, value: T) -> Box[T]:
        return cls(value)

    @classmethod
    def from_fn(cls, fn: Callable[[], T]) -> Box[T]:
        return cls(fn())

    def into_inner(self) -> T:
        return self._value

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def leak(self) -> T:
        return self._value

    def pin(self) -> Pin[T]:
        return Pin(self._value)

    def __enter__(self) -> Box[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        return f"Box({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Box):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return True

    def __del__(self) -> None:
        self._value = None


class Rc(Generic[T]):
    __slots__ = ("_value", "_ref_count", "_weak_count")

    def __init__(self, value: T) -> None:
        self._value = value
        self._ref_count = 1
        self._weak_count = 0

    @classmethod
    def new(cls, value: T) -> Rc[T]:
        return cls(value)

    def clone(self) -> Rc[T]:
        self._ref_count += 1
        return Rc._from_raw(self._value, self._ref_count, self._weak_count)

    @classmethod
    def _from_raw(cls, value: T, ref_count: int, weak_count: int) -> Rc[T]:
        rc = cls.__new__(cls)
        rc._value = value
        rc._ref_count = ref_count
        rc._weak_count = weak_count
        return rc

    def downgrade(self) -> Weak[T]:
        self._weak_count += 1
        return Weak._from_raw(self._value, self._ref_count, self._weak_count)

    def strong_count(self) -> int:
        return self._ref_count

    def weak_count(self) -> int:
        return self._weak_count

    def try_unwrap(self) -> T | None:
        if self._ref_count == 1:
            return self._value
        return None

    def as_ptr(self) -> int:
        return id(self._value)

    def into_inner(self) -> T:
        return self._value

    def __enter__(self) -> Rc[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __del__(self) -> None:
        self._ref_count -= 1

    def __repr__(self) -> str:
        return f"Rc({self._value!r}, strong={self._ref_count}, weak={self._weak_count})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Rc):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return True


class Weak(Generic[T]):
    __slots__ = ("_value", "_ref_count", "_weak_count")

    def __init__(self, value: T) -> None:
        self._value = value
        self._ref_count = 0
        self._weak_count = 1

    @classmethod
    def _from_raw(cls, value: T, ref_count: int, weak_count: int) -> Weak[T]:
        w = cls.__new__(cls)
        w._value = value
        w._ref_count = ref_count
        w._weak_count = weak_count
        return w

    def upgrade(self) -> Rc[T] | None:
        if self._ref_count > 0:
            self._ref_count += 1
            return Rc._from_raw(self._value, self._ref_count, self._weak_count)
        return None

    def strong_count(self) -> int:
        return self._ref_count

    def weak_count(self) -> int:
        return self._weak_count

    def as_ptr(self) -> int:
        return id(self._value)

    def is_alive(self) -> bool:
        return self._ref_count > 0

    def __repr__(self) -> str:
        return f"Weak(strong={self._ref_count}, weak={self._weak_count})"

    def __bool__(self) -> bool:
        return self._ref_count > 0

    def __del__(self) -> None:
        self._weak_count -= 1


class Pin(Generic[T]):
    __slots__ = ("_value", "_pinned")

    def __init__(self, value: T) -> None:
        self._value = value
        self._pinned = True

    @classmethod
    def new(cls, value: T) -> Pin[T]:
        return cls(value)

    @classmethod
    def into_pin(cls, value: T) -> Pin[T]:
        return cls(value)

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def into_inner(self) -> T:
        self._pinned = False
        return self._value

    def is_pinned(self) -> bool:
        return self._pinned

    def __repr__(self) -> str:
        return f"Pin({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pin):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __enter__(self) -> Pin[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass


class ManuallyDrop(Generic[T]):
    __slots__ = ("_value", "_dropped")

    def __init__(self, value: T) -> None:
        self._value = value
        self._dropped = False

    @classmethod
    def new(cls, value: T) -> ManuallyDrop[T]:
        return cls(value)

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def into_inner(self) -> T:
        self._dropped = True
        return self._value

    def drop(self) -> None:
        self._dropped = True
        self._value = None  # type: ignore[assignment]

    def is_dropped(self) -> bool:
        return self._dropped

    def __repr__(self) -> str:
        return f"ManuallyDrop({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ManuallyDrop):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __del__(self) -> None:
        if not self._dropped:
            self._dropped = True


class MaybeUninit(Generic[T]):
    __slots__ = ("_value", "_initialized")

    def __init__(self) -> None:
        self._value: T = None  # type: ignore[assignment]
        self._initialized = False

    @classmethod
    def new(cls) -> MaybeUninit[T]:
        return cls()

    @classmethod
    def uninit(cls) -> MaybeUninit[T]:
        return cls()

    @classmethod
    def init(cls, value: T) -> MaybeUninit[T]:
        cell = cls()
        cell._value = value
        cell._initialized = True
        return cell

    def assume_init(self) -> T:
        if not self._initialized:
            raise ValueError("MaybeUninit is not initialized")
        return self._value

    def write(self, value: T) -> T:
        self._value = value
        self._initialized = True
        return value

    def as_ptr(self) -> int:
        return id(self._value)

    def is_initialized(self) -> bool:
        return self._initialized

    def __repr__(self) -> str:
        if self._initialized:
            return f"MaybeUninit({self._value!r})"
        return "MaybeUninit(<uninitialized>)"

    def __bool__(self) -> bool:
        return self._initialized

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MaybeUninit):
            if not self._initialized or not other._initialized:
                return False
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        if self._initialized:
            return hash(self._value)
        return hash(None)


class NonNull(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        if value is None:
            raise ValueError("NonNull cannot hold None")
        self._value = value

    @classmethod
    def new(cls, value: T) -> NonNull[T]:
        return cls(value)

    def as_ref(self) -> T:
        return self._value

    def as_mut(self) -> T:
        return self._value

    def replace(self, value: T) -> T:
        if value is None:
            raise ValueError("NonNull cannot hold None")
        old = self._value
        self._value = value
        return old

    def into_inner(self) -> T:
        return self._value

    def is_null(self) -> bool:
        return False

    def as_ptr(self) -> int:
        return id(self._value)

    def __repr__(self) -> str:
        return f"NonNull({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NonNull):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return True


class PhantomData(Generic[T]):
    __slots__ = ()

    def __init__(self) -> None:
        pass

    @classmethod
    def new(cls) -> PhantomData[T]:
        return cls()

    def __repr__(self) -> str:
        return "PhantomData"

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PhantomData)

    def __hash__(self) -> int:
        return 0


class Borrow(Generic[T]):
    __slots__ = ("_value", "_owner")

    def __init__(self, value: T, owner: Any = None) -> None:
        self._value = value
        self._owner = owner

    @classmethod
    def new(cls, value: T, owner: Any = None) -> Borrow[T]:
        return cls(value, owner)

    def as_ref(self) -> T:
        return self._value

    def into_inner(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"Borrow({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Borrow):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __enter__(self) -> Borrow[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass


class BorrowMut(Generic[T]):
    __slots__ = ("_value", "_owner", "_released")

    def __init__(self, value: T, owner: Any = None) -> None:
        self._value = value
        self._owner = owner
        self._released = False

    @classmethod
    def new(cls, value: T, owner: Any = None) -> BorrowMut[T]:
        return cls(value, owner)

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, v: T) -> None:
        self._value = v

    def replace(self, v: T) -> T:
        old = self._value
        self._value = v
        return old

    def into_inner(self) -> T:
        self._released = True
        return self._value

    def release(self) -> None:
        self._released = True

    def is_released(self) -> bool:
        return self._released

    def __enter__(self) -> BorrowMut[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"BorrowMut({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BorrowMut):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)


class Drain(Generic[T]):
    __slots__ = ("_source", "_index")

    def __init__(self, source: list[T]) -> None:
        self._source = source
        self._index = 0

    def __iter__(self) -> Iterator[T]:
        while self._index < len(self._source):
            yield self._source[self._index]
            self._index += 1
        self._source.clear()

    def __next__(self) -> T:
        if self._index >= len(self._source):
            raise StopIteration
        value = self._source[self._index]
        self._index += 1
        return value

    def __repr__(self) -> str:
        return f"Drain(remaining={len(self._source) - self._index})"


class IntoIter(Generic[T]):
    __slots__ = ("_iter",)

    def __init__(self, source: Iterable[T]) -> None:
        self._iter = iter(source)

    def __iter__(self) -> Iterator[T]:
        return self._iter

    def __next__(self) -> T:
        return next(self._iter)

    def __repr__(self) -> str:
        return "IntoIter(...)"


class Slice(Generic[T]):
    __slots__ = ("_data", "_start", "_end")

    def __init__(self, data: Sequence[T], start: int = 0, end: int | None = None) -> None:
        self._data = data
        self._start = start
        self._end = end if end is not None else len(data)

    @classmethod
    def from_list(cls, data: Sequence[T]) -> Slice[T]:
        return cls(data)

    def get(self, index: int) -> T:
        return self._data[self._start + index]

    def first(self) -> T | None:
        if self._start >= self._end:
            return None
        return self._data[self._start]

    def last(self) -> T | None:
        if self._start >= self._end:
            return None
        return self._data[self._end - 1]

    def len(self) -> int:
        return self._end - self._start

    def is_empty(self) -> bool:
        return self._start >= self._end

    def contains(self, value: T) -> bool:
        for i in range(self._start, self._end):
            if self._data[i] == value:
                return True
        return False

    def split_at(self, mid: int) -> tuple[Slice[T], Slice[T]]:
        return (
            Slice(self._data, self._start, self._start + mid),
            Slice(self._data, self._start + mid, self._end),
        )

    def iter(self) -> Iterator[T]:
        for i in range(self._start, self._end):
            yield self._data[i]

    def to_list(self) -> list[T]:
        return list(self._data[self._start:self._end])

    def __len__(self) -> int:
        return self.len()

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def __contains__(self, value: object) -> bool:
        return self.contains(value)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        return f"Slice({self.to_list()})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Slice):
            return self.to_list() == other.to_list()
        if isinstance(other, (list, tuple)):
            return self.to_list() == list(other)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self._data[self._start:self._end]))


class HashSet(Generic[T]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._data: set[T] = set()
        if values is not None:
            for v in values:
                self._data.add(v)

    @classmethod
    def new(cls) -> HashSet[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> HashSet[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> HashSet[T]:
        return cls(values)

    def insert(self, value: T) -> bool:
        existed = value in self._data
        self._data.add(value)
        return not existed

    def remove(self, value: T) -> T | None:
        return self._data.discard(value) or None if value in self._data else None

    def take(self, value: T) -> T | None:
        if value in self._data:
            self._data.remove(value)
            return value
        return None

    def contains(self, value: T) -> bool:
        return value in self._data

    def get(self, value: T) -> T | None:
        if value in self._data:
            return value
        return None

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def iter(self) -> Iterator[T]:
        return iter(self._data)

    def drain(self) -> Iterator[T]:
        items = list(self._data)
        self._data.clear()
        return iter(items)

    def extend(self, values: Iterable[T]) -> None:
        for v in values:
            self._data.add(v)

    def intersection(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data & other._data)

    def union(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data | other._data)

    def difference(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data - other._data)

    def symmetric_difference(self, other: HashSet[T]) -> HashSet[T]:
        return HashSet(self._data ^ other._data)

    def is_disjoint(self, other: HashSet[T]) -> bool:
        return self._data.isdisjoint(other._data)

    def is_subset(self, other: HashSet[T]) -> bool:
        return self._data.issubset(other._data)

    def is_superset(self, other: HashSet[T]) -> bool:
        return self._data.issuperset(other._data)

    def to_list(self) -> list[T]:
        return list(self._data)

    def to_set(self) -> set[T]:
        return self._data.copy()

    def into_iter(self) -> Iterator[T]:
        items = list(self._data)
        self._data.clear()
        return iter(items)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"HashSet({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashSet):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(frozenset(self._data))

    def __bool__(self) -> bool:
        return bool(self._data)


class BTreeMap(Generic[K, V]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[tuple[K, V]] | dict[K, V] | None = None) -> None:
        self._data: dict[K, V] = {}
        if values is not None:
            if isinstance(values, dict):
                self._data = dict(sorted(values.items()))
            else:
                self._data = dict(sorted(values, key=lambda x: x[0]))

    @classmethod
    def new(cls) -> BTreeMap[K, V]:
        return cls()

    @classmethod
    def from_dict(cls, values: dict[K, V]) -> BTreeMap[K, V]:
        return cls(values)

    def insert(self, key: K, value: V) -> V | None:
        old = self._data.get(key)
        self._data[key] = value
        return old

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def get_key_value(self, key: K) -> tuple[K, V] | None:
        if key in self._data:
            return (key, self._data[key])
        return None

    def remove(self, key: K) -> V | None:
        return self._data.pop(key, None)

    def contains_key(self, key: K) -> bool:
        return key in self._data

    def first_key_value(self) -> tuple[K, V] | None:
        if not self._data:
            return None
        key = min(self._data.keys())
        return (key, self._data[key])

    def last_key_value(self) -> tuple[K, V] | None:
        if not self._data:
            return None
        key = max(self._data.keys())
        return (key, self._data[key])

    def clear(self) -> None:
        self._data.clear()

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def keys(self) -> Iterator[K]:
        return iter(sorted(self._data.keys()))

    def values(self) -> Iterator[V]:
        for k in sorted(self._data.keys()):
            yield self._data[k]

    def iter(self) -> Iterator[tuple[K, V]]:
        for k in sorted(self._data.keys()):
            yield (k, self._data[k])

    def drain(self) -> Iterator[tuple[K, V]]:
        items = sorted(self._data.items())
        self._data.clear()
        return iter(items)

    def range_(self, start: K, end: K) -> Iterator[tuple[K, V]]:
        for k in sorted(self._data.keys()):
            if start <= k < end:
                yield (k, self._data[k])

    def to_dict(self) -> dict[K, V]:
        return dict(sorted(self._data.items()))

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[K]:
        return self.keys()

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __setitem__(self, key: K, value: V) -> None:
        self._data[key] = value

    def __delitem__(self, key: K) -> None:
        del self._data[key]

    def __repr__(self) -> str:
        return f"BTreeMap({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BTreeMap):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(sorted(self._data.items())))

    def __bool__(self) -> bool:
        return bool(self._data)


class BTreeSet(Generic[T]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._data: set[T] = set()
        if values is not None:
            for v in values:
                self._data.add(v)

    @classmethod
    def new(cls) -> BTreeSet[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> BTreeSet[T]:
        return cls(values)

    def insert(self, value: T) -> bool:
        existed = value in self._data
        self._data.add(value)
        return not existed

    def remove(self, value: T) -> bool:
        if value in self._data:
            self._data.remove(value)
            return True
        return False

    def contains(self, value: T) -> bool:
        return value in self._data

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def first(self) -> T | None:
        if not self._data:
            return None
        return min(self._data)

    def last(self) -> T | None:
        if not self._data:
            return None
        return max(self._data)

    def iter(self) -> Iterator[T]:
        return iter(sorted(self._data))

    def range_(self, start: T, end: T) -> Iterator[T]:
        for v in sorted(self._data):
            if start <= v < end:
                yield v

    def intersection(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data & other._data)

    def union(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data | other._data)

    def difference(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data - other._data)

    def symmetric_difference(self, other: BTreeSet[T]) -> BTreeSet[T]:
        return BTreeSet(self._data ^ other._data)

    def is_disjoint(self, other: BTreeSet[T]) -> bool:
        return self._data.isdisjoint(other._data)

    def is_subset(self, other: BTreeSet[T]) -> bool:
        return self._data.issubset(other._data)

    def is_superset(self, other: BTreeSet[T]) -> bool:
        return self._data.issuperset(other._data)

    def to_list(self) -> list[T]:
        return sorted(self._data)

    def to_set(self) -> set[T]:
        return self._data.copy()

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"BTreeSet({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BTreeSet):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(frozenset(self._data))

    def __bool__(self) -> bool:
        return bool(self._data)


class VecDeque(Generic[T]):
    __slots__ = ("_data",)

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._data: list[T] = list(values) if values else []

    @classmethod
    def new(cls) -> VecDeque[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> VecDeque[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> VecDeque[T]:
        return cls(values)

    def push_back(self, value: T) -> None:
        self._data.append(value)

    def push_front(self, value: T) -> None:
        self._data.insert(0, value)

    def pop_back(self) -> T | None:
        if self._data:
            return self._data.pop()
        return None

    def pop_front(self) -> T | None:
        if self._data:
            return self._data.pop(0)
        return None

    def front(self) -> T | None:
        return self._data[0] if self._data else None

    def back(self) -> T | None:
        return self._data[-1] if self._data else None

    def get(self, index: int) -> T | None:
        if 0 <= index < len(self._data):
            return self._data[index]
        return None

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def insert(self, index: int, value: T) -> None:
        self._data.insert(index, value)

    def remove(self, index: int) -> T | None:
        if 0 <= index < len(self._data):
            return self._data.pop(index)
        return None

    def contains(self, value: T) -> bool:
        return value in self._data

    def rotate_left(self, k: int) -> None:
        if self._data:
            k = k % len(self._data)
            self._data = self._data[k:] + self._data[:k]

    def rotate_right(self, k: int) -> None:
        if self._data:
            k = k % len(self._data)
            self._data = self._data[-k:] + self._data[:-k]

    def truncate(self, length: int) -> None:
        del self._data[length:]

    def drain(self) -> Drain[T]:
        return Drain(self._data)

    def iter(self) -> Iterator[T]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._data[index] = value

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"VecDeque({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, VecDeque):
            return self._data == other._data
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self._data))

    def __bool__(self) -> bool:
        return bool(self._data)


class BinaryHeap(Generic[T]):
    __slots__ = ("_data", "_reverse")

    def __init__(self, values: Iterable[T] | None = None, *, reverse: bool = False) -> None:
        self._data: list[T] = list(values) if values else []
        self._reverse = reverse
        self._data.sort(reverse=not reverse)

    @classmethod
    def new(cls) -> BinaryHeap[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> BinaryHeap[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T], *, reverse: bool = False) -> BinaryHeap[T]:
        return cls(values, reverse=reverse)

    def push(self, value: T) -> None:
        self._data.append(value)
        self._data.sort(reverse=not self._reverse)

    def pop(self) -> T | None:
        if self._data:
            return self._data.pop(0)
        return None

    def peek(self) -> T | None:
        return self._data[0] if self._data else None

    def push_pop(self, push_value: T) -> T:
        self.push(push_value)
        return self.pop()  # type: ignore

    def peek_mut(self) -> T | None:
        return self.peek()

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def contains(self, value: T) -> bool:
        return value in self._data

    def drain(self) -> Iterator[T]:
        items = sorted(self._data, reverse=not self._reverse)
        self._data.clear()
        return iter(items)

    def iter(self) -> Iterator[T]:
        return iter(sorted(self._data, reverse=not self._reverse))

    def to_list(self) -> list[T]:
        return sorted(self._data, reverse=not self._reverse)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"BinaryHeap({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BinaryHeap):
            return sorted(self._data) == sorted(other._data)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(sorted(self._data)))

    def __bool__(self) -> bool:
        return bool(self._data)


class LinkedListNode(Generic[T]):
    __slots__ = ("value", "next", "prev")

    def __init__(self, value: T) -> None:
        self.value = value
        self.next: LinkedListNode[T] | None = None
        self.prev: LinkedListNode[T] | None = None


class LinkedList(Generic[T]):
    __slots__ = ("_head", "_tail", "_len")

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._head: LinkedListNode[T] | None = None
        self._tail: LinkedListNode[T] | None = None
        self._len = 0
        if values is not None:
            for v in values:
                self.push_back(v)

    @classmethod
    def new(cls) -> LinkedList[T]:
        return cls()

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> LinkedList[T]:
        return cls(values)

    def push_front(self, value: T) -> None:
        node = LinkedListNode(value)
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._len += 1

    def push_back(self, value: T) -> None:
        node = LinkedListNode(value)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._len += 1

    def pop_front(self) -> T | None:
        if self._head is None:
            return None
        value = self._head.value
        if self._head == self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
            if self._head:
                self._head.prev = None
        self._len -= 1
        return value

    def pop_back(self) -> T | None:
        if self._tail is None:
            return None
        value = self._tail.value
        if self._head == self._tail:
            self._head = None
            self._tail = None
        else:
            self._tail = self._tail.prev
            if self._tail:
                self._tail.next = None
        self._len -= 1
        return value

    def front(self) -> T | None:
        return self._head.value if self._head else None

    def back(self) -> T | None:
        return self._tail.value if self._tail else None

    def len(self) -> int:
        return self._len

    def is_empty(self) -> bool:
        return self._len == 0

    def clear(self) -> None:
        self._head = None
        self._tail = None
        self._len = 0

    def contains(self, value: T) -> bool:
        node = self._head
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def reverse(self) -> None:
        node = self._head
        while node:
            node.next, node.prev = node.prev, node.next
            node = node.prev
        self._head, self._tail = self._tail, self._head

    def iter(self) -> Iterator[T]:
        node = self._head
        while node:
            yield node.value
            node = node.next

    def iter_rev(self) -> Iterator[T]:
        node = self._tail
        while node:
            yield node.value
            node = node.prev

    def drain(self) -> Drain[T]:
        items = list(self.iter())
        self.clear()
        return Drain(items)

    def to_list(self) -> list[T]:
        return list(self.iter())

    def __len__(self) -> int:
        return self._len

    def __iter__(self) -> Iterator[T]:
        return self.iter()

    def __contains__(self, value: object) -> bool:
        return self.contains(value)  # type: ignore[arg-type]

    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LinkedList):
            return self.to_list() == other.to_list()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(self.iter()))

    def __bool__(self) -> bool:
        return self._len > 0


class CloneTrait(Protocol[T]):
    def clone(self) -> T: ...


class CopyTrait(Protocol[T]):
    def copy(self) -> T: ...


class DebugTrait(Protocol):
    def debug(self) -> str: ...


class DisplayTrait(Protocol):
    def fmt(self) -> str: ...


class DefaultTrait(Protocol[T]):
    @classmethod
    def default(cls) -> T: ...


class EqTrait(Protocol):
    def eq(self, other: object) -> bool: ...
    def ne(self, other: object) -> bool: ...


class OrdTrait(Protocol):
    def cmp(self, other: object) -> int: ...
    def lt(self, other: object) -> bool: ...
    def le(self, other: object) -> bool: ...
    def gt(self, other: object) -> bool: ...
    def ge(self, other: object) -> bool: ...


class HashTrait(Protocol):
    def hash(self) -> int: ...


class FromTrait(Protocol[T]):
    @classmethod
    def from_(cls, value: Any) -> T: ...


class IntoTrait(Protocol[T]):
    def into(self) -> T: ...


class TryFromTrait(Protocol[T]):
    @classmethod
    def try_from(cls, value: Any) -> Result[T, str]: ...


class TryIntoTrait(Protocol[T]):
    def try_into(self) -> Result[T, str]: ...


class AsRefTrait(Protocol[T]):
    def as_ref(self) -> T: ...


class AsMutTrait(Protocol[T]):
    def as_mut(self) -> T: ...


class DerefTrait(Protocol[T]):
    def deref(self) -> T: ...


class DerefMutTrait(Protocol[T]):
    def deref_mut(self) -> T: ...


class DropTrait(Protocol):
    def drop(self) -> None: ...


def clone(value: T) -> T:
    if hasattr(value, 'clone'):
        return value.clone()
    return copy.deepcopy(value)


def debug(value: Any) -> str:
    if hasattr(value, 'debug'):
        return value.debug()
    return repr(value)


def display(value: Any) -> str:
    if hasattr(value, 'fmt'):
        return value.fmt()
    return str(value)


def default_of(cls: type[T]) -> T:
    if hasattr(cls, 'default'):
        try:
            return cls.default()
        except TypeError:
            return cls.default(cls)
    return cls()


def from_(cls: type[T], value: Any) -> T:
    if hasattr(cls, 'from_'):
        return cls.from_(value)
    return cls(value)


def into(value: Any, target_type: type[T]) -> T:
    if hasattr(value, 'into'):
        return value.into()
    return target_type(value)


def try_from(cls: type[T], value: Any) -> Result[T, str]:
    if hasattr(cls, 'try_from'):
        return cls.try_from(value)
    try:
        return Ok(cls(value))
    except Exception as e:
        return Err(str(e))


def try_into(value: Any, target_type: type[T]) -> Result[T, str]:
    if hasattr(value, 'try_into'):
        return value.try_into()
    try:
        return Ok(target_type(value))
    except Exception as e:
        return Err(str(e))


def as_ref(value: T) -> T:
    if hasattr(value, 'as_ref'):
        return value.as_ref()
    return value


def as_mut(value: T) -> T:
    if hasattr(value, 'as_mut'):
        return value.as_mut()
    return value


def deref(value: T) -> T:
    if hasattr(value, 'deref'):
        return value.deref()
    return value


def deref_mut(value: T) -> T:
    if hasattr(value, 'deref_mut'):
        return value.deref_mut()
    return value


def drop(value: Any) -> None:
    if hasattr(value, 'drop'):
        value.drop()


class Cell(Generic[T]):
    __slots__ = ("_value", "_copy")

    def __init__(self, value: T, *, deep: bool = False) -> None:
        self._value = value
        self._copy = deep

    @classmethod
    def new(cls, value: T) -> Cell[T]:
        return cls(value)

    def get(self) -> T:
        if self._copy:
            return copy.deepcopy(self._value)
        return self._value

    def set(self, value: T) -> None:
        self._value = value

    def replace(self, value: T) -> T:
        old = self._value
        self._value = value
        return old

    def swap(self, other: Cell[T]) -> None:
        self._value, other._value = other._value, self._value

    def take(self) -> T:
        old = self._value
        self._value = None  # type: ignore[assignment]
        return old

    def into_inner(self) -> T:
        return self._value

    def as_ptr(self) -> int:
        return id(self._value)

    def __repr__(self) -> str:
        return f"Cell({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __bool__(self) -> bool:
        return bool(self._value)


class Range(Generic[T]):
    __slots__ = ("start", "end")

    def __init__(self, start: T, end: T) -> None:
        self.start = start
        self.end = end

    def contains(self, value: T) -> bool:
        return self.start <= value < self.end

    def contains_inclusive(self, value: T) -> bool:
        return self.start <= value <= self.end

    def is_empty(self) -> bool:
        return self.start >= self.end

    def iter(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end))

    def __iter__(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end))

    def __len__(self) -> int:
        return max(0, int(self.end) - int(self.start))

    def __contains__(self, value: T) -> bool:
        return self.start <= value < self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Range):
            return self.start == other.start and self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        return f"{self.start}..{self.end}"


class RangeInclusive(Generic[T]):
    __slots__ = ("start", "end")

    def __init__(self, start: T, end: T) -> None:
        self.start = start
        self.end = end

    def contains(self, value: T) -> bool:
        return self.start <= value <= self.end

    def is_empty(self) -> bool:
        return self.start > self.end

    def iter(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end) + 1)

    def __iter__(self) -> Iterator[T]:
        yield from range(int(self.start), int(self.end) + 1)

    def __len__(self) -> int:
        return max(0, int(self.end) - int(self.start) + 1)

    def __contains__(self, value: T) -> bool:
        return self.start <= value <= self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeInclusive):
            return self.start == other.start and self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        return f"{self.start}..={self.end}"


class RangeFrom(Generic[T]):
    __slots__ = ("start",)

    def __init__(self, start: T) -> None:
        self.start = start

    def contains(self, value: T) -> bool:
        return value >= self.start

    def iter(self, end: T) -> Iterator[T]:
        yield from range(int(self.start), int(end))

    def __contains__(self, value: T) -> bool:
        return value >= self.start

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeFrom):
            return self.start == other.start
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.start)

    def __repr__(self) -> str:
        return f"{self.start}.."


class RangeTo(Generic[T]):
    __slots__ = ("end",)

    def __init__(self, end: T) -> None:
        self.end = end

    def contains(self, value: T) -> bool:
        return value < self.end

    def iter(self, start: T = 0) -> Iterator[T]:
        yield from range(int(start), int(self.end))

    def __contains__(self, value: T) -> bool:
        return value < self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeTo):
            return self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.end)

    def __repr__(self) -> str:
        return f"..{self.end}"


class RangeToInclusive(Generic[T]):
    __slots__ = ("end",)

    def __init__(self, end: T) -> None:
        self.end = end

    def contains(self, value: T) -> bool:
        return value <= self.end

    def iter(self, start: T = 0) -> Iterator[T]:
        yield from range(int(start), int(self.end) + 1)

    def __contains__(self, value: T) -> bool:
        return value <= self.end

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeToInclusive):
            return self.end == other.end
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.end)

    def __repr__(self) -> str:
        return f"..={self.end}"


class RangeFull:
    __slots__ = ()

    def contains(self, value: object) -> bool:
        return True

    def __contains__(self, value: object) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RangeFull):
            return True
        return NotImplemented

    def __hash__(self) -> int:
        return hash(None)

    def __repr__(self) -> str:
        return ".."


def range_(start: T, end: T) -> Range[T]:
    return Range(start, end)


def range_inclusive(start: T, end: T) -> RangeInclusive[T]:
    return RangeInclusive(start, end)


def range_from(start: T) -> RangeFrom[T]:
    return RangeFrom(start)


def range_to(end: T) -> RangeTo[T]:
    return RangeTo(end)


def range_to_inclusive(end: T) -> RangeToInclusive[T]:
    return RangeToInclusive(end)


class MatchError(Exception):
    pass


class _Case(Generic[T, R]):
    __slots__ = ("pattern", "handler", "guard")

    def __init__(
        self,
        pattern: T | type | tuple[type, ...] | None,
        handler: Callable[[T], R] | R,
        guard: Callable[[T], bool] | None,
    ) -> None:
        self.pattern = pattern
        self.handler = handler
        self.guard = guard

    def matches(self, value: object) -> bool:
        if self.pattern is _:
            return True
        if self.pattern is None:
            return value is None
        if isinstance(self.pattern, type):
            if not isinstance(value, self.pattern):
                return False
        elif isinstance(self.pattern, tuple):
            if not isinstance(value, self.pattern):
                return False
        elif self.pattern != value:
            return False
        if self.guard is not None and not self.guard(value):
            return False
        return True

    def execute(self, value: T) -> R:
        if callable(self.handler) and not isinstance(self.handler, type):
            return self.handler(value)
        return self.handler  # type: ignore[return-value]


class Match(Generic[T, R]):
    __slots__ = ("_value", "_cases", "_executed", "_result")

    def __init__(self, value: T) -> None:
        self._value = value
        self._cases: list[_Case] = []
        self._executed = False
        self._result: R = None  # type: ignore[assignment]

    def case(
        self,
        pattern: object | type | tuple[type, ...] | None,
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        self._cases.append(_Case(pattern, handler, guard))
        return self

    def case_type(
        self,
        typ: type | tuple[type, ...],
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        self._cases.append(_Case(typ, handler, guard))
        return self

    def case_eq(
        self,
        value: object,
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        self._cases.append(_Case(value, handler, guard))
        return self

    def case_range(
        self,
        start: int,
        end: int,
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        class _RangePattern:
            def __init__(self, s: int, e: int) -> None:
                self.start = s
                self.end = e
            def __eq__(self, other: object) -> bool:
                if isinstance(other, (int, float)):
                    return self.start <= other < self.end
                return NotImplemented
        self._cases.append(_Case(_RangePattern(start, end), handler, guard))
        return self

    def case_pred(
        self,
        predicate: Callable[[T], bool],
        handler: Callable[[T], R] | R | None = None,
    ) -> Match[T, R]:
        class _PredPattern:
            def __init__(self, pred: Callable[[T], bool]) -> None:
                self.pred = pred
            def __eq__(self, other: object) -> bool:
                return self.pred(other)  # type: ignore[arg-type]
        self._cases.append(_Case(_PredPattern(predicate), handler, None))
        return self

    def case_in(
        self,
        collection: Iterable[object],
        handler: Callable[[T], R] | R | None = None,
        *,
        guard: Callable[[T], bool] | None = None,
    ) -> Match[T, R]:
        class _InPattern:
            def __init__(self, coll: Iterable[object]) -> None:
                self.coll = coll
            def __eq__(self, other: object) -> bool:
                return other in self.coll
        self._cases.append(_Case(_InPattern(collection), handler, guard))
        return self

    def otherwise(self, handler: Callable[[T], R] | R) -> R:
        self._cases.append(_Case(_, handler, None))
        return self.execute()

    def execute(self) -> R:
        if self._executed:
            return self._result
        for case in self._cases:
            if case.matches(self._value):
                self._result = case.execute(self._value)
                self._executed = True
                return self._result
        raise MatchError(
            f"no match found for {self._value!r}"
        )

    def __repr__(self) -> str:
        if self._executed:
            return f"Match({self._value!r} => {self._result!r})"
        return f"Match({self._value!r}, {len(self._cases)} cases)"


class _MatchWildcard:
    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return True

    def __hash__(self) -> int:
        return hash("_")

    def __repr__(self) -> str:
        return "_"


class _:
    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return True

    def __hash__(self) -> int:
        return hash("_")

    def __repr__(self) -> str:
        return "_"


_ = _MatchWildcard()


def match(value: T) -> Match[T, Any]:
    return Match(value)


class PropagateError(Exception):
    __slots__ = ("_result",)

    def __init__(self, result: Result) -> None:
        self._result = result

    @property
    def result(self) -> Result:
        return self._result


class Propagate:
    __slots__ = ("_fn",)

    def __init__(self, fn: F) -> None:
        self._fn = fn

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return self._fn(*args, **kwargs)
        except PropagateError as e:
            return e.result

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        return Propagate(lambda *a, **kw: self._fn(obj, *a, **kw))


def propagate(fn: F) -> F:
    return Propagate(fn)  # type: ignore[return-value]


def ask(result: Result) -> Any:
    if isinstance(result, Err):
        raise PropagateError(result)
    return result.value


def try_ask(fn: F) -> F:
    def wrapper(*args: Any, **kwargs: Any) -> Result:
        try:
            return Ok(fn(*args, **kwargs))
        except Exception as e:
            return Err(e)
    return wrapper  # type: ignore[return-value]


class UnimplementedError(Exception):
    __slots__ = ("_message",)

    def __init__(self, message: str | None = None) -> None:
        self._message = message or "not yet implemented"
        super().__init__(self._message)


def unimplemented(message: str | None = None) -> NoReturn:
    raise UnimplementedError(message)


def todo(message: str | None = None) -> NoReturn:
    raise UnimplementedError(message or "not yet implemented")


class PanicError(Exception):
    __slots__ = ("_message", "_backtrace")

    def __init__(self, message: str | None = None) -> None:
        self._message = message or "explicit panic"
        self._backtrace = traceback.format_stack()
        super().__init__(self._message)

    @property
    def backtrace(self) -> list[str]:
        return self._backtrace

    def __str__(self) -> str:
        tb = "".join(self._backtrace[:-1])
        return f"panicked at '{self._message}'\n{tb}"


def panic(message: str | None = None) -> NoReturn:
    raise PanicError(message)


def panic_fmt(*args: Any, **kwargs: Any) -> NoReturn:
    msg = " ".join(str(a) for a in args)
    for k, v in kwargs.items():
        msg += f" {k}={v!r}"
    raise PanicError(msg)


class MutexPoisoned(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("mutex is poisoned")


class MutexLock:
    __slots__ = ("_mutex", "_guard")

    def __init__(self, mutex: Mutex) -> None:
        self._mutex = mutex
        self._guard = None

    def __enter__(self) -> Any:
        self._guard = self._mutex.lock()
        return self._guard

    def __exit__(self, *_: Any) -> None:
        if self._guard is not None:
            self._guard.release()
            self._guard = None


class MutexGuard:
    __slots__ = ("_mutex",)

    def __init__(self, mutex: Mutex) -> None:
        self._mutex = mutex

    @property
    def value(self) -> Any:
        return self._mutex._value

    @value.setter
    def value(self, v: Any) -> None:
        self._mutex._value = v

    def replace(self, v: Any) -> Any:
        old = self._mutex._value
        self._mutex._value = v
        return old

    def swap(self, other: Mutex) -> None:
        self._mutex._value, other._value = other._value, self._mutex._value

    def into_inner(self) -> Any:
        return self._mutex._value

    def release(self) -> None:
        self._mutex._lock.release()

    def __repr__(self) -> str:
        return f"MutexGuard({self._mutex._value!r})"


class Mutex(Generic[T]):
    __slots__ = ("_value", "_lock", "_poisoned")

    def __init__(self, value: T) -> None:
        self._value = value
        self._lock = threading.Lock()
        self._poisoned = False

    @classmethod
    def new(cls, value: T) -> Mutex[T]:
        return cls(value)

    def lock(self) -> MutexGuard:
        if self._poisoned:
            raise MutexPoisoned()
        self._lock.acquire()
        return MutexGuard(self)

    def try_lock(self) -> MutexGuard | None:
        if self._poisoned:
            raise MutexPoisoned()
        acquired = self._lock.acquire(blocking=False)
        if acquired:
            return MutexGuard(self)
        return None

    def into_inner(self) -> T:
        return self._value

    def is_poisoned(self) -> bool:
        return self._poisoned

    def poison(self) -> None:
        self._poisoned = True

    def clear_poison(self) -> None:
        self._poisoned = False

    def __enter__(self) -> MutexGuard:
        return self.lock()

    def __exit__(self, *_: Any) -> None:
        self._lock.release()

    def __repr__(self) -> str:
        return f"Mutex({self._value!r})"


class Arc(Generic[T]):
    __slots__ = ("_inner", "_ref_count", "_lock")

    def __init__(self, value: T) -> None:
        self._inner = value
        self._ref_count = 1
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: T) -> Arc[T]:
        return cls(value)

    def clone(self) -> Arc[T]:
        with self._lock:
            self._ref_count += 1
        return Arc._from_raw(self._inner, self._ref_count, self._lock)

    @classmethod
    def _from_raw(cls, value: T, ref_count: int, lock: threading.Lock) -> Arc[T]:
        arc = cls.__new__(cls)
        arc._inner = value
        arc._ref_count = ref_count
        arc._lock = lock
        return arc

    def strong_count(self) -> int:
        with self._lock:
            return self._ref_count

    def try_unwrap(self) -> T | None:
        with self._lock:
            if self._ref_count == 1:
                return self._inner
        return None

    def as_ptr(self) -> int:
        return id(self._inner)

    def into_inner(self) -> T:
        return self._inner

    def make_mut(self) -> T:
        return self._inner

    def __enter__(self) -> Arc[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __del__(self) -> None:
        with self._lock:
            self._ref_count -= 1

    def __repr__(self) -> str:
        return f"Arc({self._inner!r}, strong={self._ref_count})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Arc):
            return self._inner == other._inner
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._inner)

    def __bool__(self) -> bool:
        return True


class RwLockReadGuard(Generic[T]):
    __slots__ = ("_lock",)

    def __init__(self, lock: RwLock) -> None:
        self._lock = lock

    @property
    def value(self) -> Any:
        return self._lock._value

    def release(self) -> None:
        self._lock._readers -= 1

    def __enter__(self) -> RwLockReadGuard[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"RwLockReadGuard({self._lock._value!r})"


class RwLockWriteGuard(Generic[T]):
    __slots__ = ("_lock",)

    def __init__(self, lock: RwLock) -> None:
        self._lock = lock

    @property
    def value(self) -> Any:
        return self._lock._value

    @value.setter
    def value(self, v: Any) -> None:
        self._lock._value = v

    def replace(self, v: Any) -> Any:
        old = self._lock._value
        self._lock._value = v
        return old

    def release(self) -> None:
        self._lock._writing = False
        self._lock._write_lock.release()

    def __enter__(self) -> RwLockWriteGuard[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"RwLockWriteGuard({self._lock._value!r})"


class RwLock(Generic[T]):
    __slots__ = ("_value", "_readers", "_writing", "_read_lock", "_write_lock", "_cond")

    def __init__(self, value: T) -> None:
        self._value = value
        self._readers = 0
        self._writing = False
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._cond = threading.Condition(threading.Lock())

    @classmethod
    def new(cls, value: T) -> RwLock[T]:
        return cls(value)

    def read(self) -> RwLockReadGuard[T]:
        with self._cond:
            while self._writing:
                self._cond.wait()
            self._readers += 1
        return RwLockReadGuard(self)

    def write(self) -> RwLockWriteGuard[T]:
        self._write_lock.acquire()
        with self._cond:
            while self._writing or self._readers > 0:
                self._cond.wait()
            self._writing = True
        return RwLockWriteGuard(self)

    def try_read(self) -> RwLockReadGuard[T] | None:
        with self._cond:
            if not self._writing:
                self._readers += 1
                return RwLockReadGuard(self)
        return None

    def try_write(self) -> RwLockWriteGuard[T] | None:
        if self._write_lock.acquire(blocking=False):
            with self._cond:
                if not self._writing and self._readers == 0:
                    self._writing = True
                    return RwLockWriteGuard(self)
            self._write_lock.release()
        return None

    def into_inner(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"RwLock({self._value!r})"


class BorrowError(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("already mutably borrowed")


class BorrowMutError(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("already borrowed")


class RefCell(Generic[T]):
    __slots__ = ("_value", "_borrow_count")

    def __init__(self, value: T) -> None:
        self._value = value
        self._borrow_count = 0

    @classmethod
    def new(cls, value: T) -> RefCell[T]:
        return cls(value)

    def borrow(self) -> Ref[T]:
        if self._borrow_count < 0:
            raise BorrowError()
        self._borrow_count += 1
        return Ref(self)

    def try_borrow(self) -> Ref[T] | None:
        if self._borrow_count < 0:
            return None
        self._borrow_count += 1
        return Ref(self)

    def borrow_mut(self) -> RefMut[T]:
        if self._borrow_count != 0:
            raise BorrowMutError()
        self._borrow_count = -1
        return RefMut(self)

    def try_borrow_mut(self) -> RefMut[T] | None:
        if self._borrow_count != 0:
            return None
        self._borrow_count = -1
        return RefMut(self)

    def replace(self, value: T) -> T:
        old = self._value
        self._value = value
        return old

    def swap(self, other: RefCell[T]) -> None:
        self._value, other._value = other._value, self._value

    def into_inner(self) -> T:
        return self._value

    def _release_borrow(self) -> None:
        if self._borrow_count == -1:
            self._borrow_count = 0
        elif self._borrow_count > 0:
            self._borrow_count -= 1

    def __repr__(self) -> str:
        return f"RefCell({self._value!r})"


class Ref(Generic[T]):
    __slots__ = ("_cell",)

    def __init__(self, cell: RefCell) -> None:
        self._cell = cell

    @property
    def value(self) -> Any:
        return self._cell._value

    def release(self) -> None:
        self._cell._release_borrow()

    def __enter__(self) -> Ref[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"Ref({self._cell._value!r})"


class RefMut(Generic[T]):
    __slots__ = ("_cell",)

    def __init__(self, cell: RefCell) -> None:
        self._cell = cell

    @property
    def value(self) -> Any:
        return self._cell._value

    @value.setter
    def value(self, v: Any) -> None:
        self._cell._value = v

    def replace(self, v: Any) -> Any:
        old = self._cell._value
        self._cell._value = v
        return old

    def release(self) -> None:
        self._cell._release_borrow()

    def __enter__(self) -> RefMut[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"RefMut({self._cell._value!r})"


class ScopeGuard(Generic[T]):
    __slots__ = ("_fn", "_cancelled", "_value")

    def __init__(self, fn: Callable[[], T], value: T | None = None) -> None:
        self._fn = fn
        self._cancelled = False
        self._value = value

    def cancel(self) -> None:
        self._cancelled = True

    def is_cancelled(self) -> bool:
        return self._cancelled

    def execute(self) -> T | None:
        if not self._cancelled:
            self._cancelled = True
            return self._fn()
        return None

    def __enter__(self) -> ScopeGuard[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        if not self._cancelled:
            self._cancelled = True
            self._fn()

    def __repr__(self) -> str:
        return f"ScopeGuard(cancelled={self._cancelled})"


def defer(fn: Callable[[], Any]) -> ScopeGuard:
    return ScopeGuard(fn)


class Atomic(Generic[T]):
    __slots__ = ("_value", "_lock")

    def __init__(self, value: T) -> None:
        self._value = value
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: T) -> Atomic[T]:
        return cls(value)

    def load(self) -> T:
        with self._lock:
            return self._value

    def store(self, value: T) -> None:
        with self._lock:
            self._value = value

    def swap(self, value: T) -> T:
        with self._lock:
            old = self._value
            self._value = value
            return old

    def into_inner(self) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"Atomic({self._value!r})"


class AtomicBool:
    __slots__ = ("_value", "_lock")

    def __init__(self, value: bool = False) -> None:
        self._value = value
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: bool = False) -> AtomicBool:
        return cls(value)

    def load(self) -> bool:
        with self._lock:
            return self._value

    def store(self, value: bool) -> None:
        with self._lock:
            self._value = value

    def swap(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = value
            return old

    def compare_and_set(self, current: bool, new: bool) -> bool:
        with self._lock:
            if self._value == current:
                self._value = new
                return True
            return False

    def fetch_and(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = self._value and value
            return old

    def fetch_or(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = self._value or value
            return old

    def fetch_xor(self, value: bool) -> bool:
        with self._lock:
            old = self._value
            self._value = self._value != value
            return old

    def into_inner(self) -> bool:
        return self._value

    def __repr__(self) -> str:
        return f"AtomicBool({self._value!r})"

    def __bool__(self) -> bool:
        return self.load()


class AtomicInt:
    __slots__ = ("_value", "_lock")

    def __init__(self, value: int = 0) -> None:
        self._value = value
        self._lock = threading.Lock()

    @classmethod
    def new(cls, value: int = 0) -> AtomicInt:
        return cls(value)

    def load(self) -> int:
        with self._lock:
            return self._value

    def store(self, value: int) -> None:
        with self._lock:
            self._value = value

    def swap(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value = value
            return old

    def fetch_add(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value += value
            return old

    def fetch_sub(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value -= value
            return old

    def fetch_and(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value &= value
            return old

    def fetch_or(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value |= value
            return old

    def fetch_xor(self, value: int) -> int:
        with self._lock:
            old = self._value
            self._value ^= value
            return old

    def compare_and_set(self, current: int, new: int) -> bool:
        with self._lock:
            if self._value == current:
                self._value = new
                return True
            return False

    def into_inner(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"AtomicInt({self._value!r})"

    def __int__(self) -> int:
        return self.load()

    def __add__(self, other: int) -> int:
        return self.load() + other

    def __sub__(self, other: int) -> int:
        return self.load() - other

    def __iadd__(self, other: int) -> AtomicInt:
        self.fetch_add(other)
        return self

    def __isub__(self, other: int) -> AtomicInt:
        self.fetch_sub(other)
        return self


class Barrier:
    __slots__ = ("_count", "_threshold", "_lock", "_condition", "_generation")

    def __init__(self, count: int) -> None:
        if count == 0:
            raise ValueError("count cannot be zero")
        self._count = count
        self._threshold = count
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._generation = 0

    def wait(self) -> int:
        with self._condition:
            generation = self._generation
            self._count -= 1
            if self._count == 0:
                self._generation += 1
                self._count = self._threshold
                self._condition.notify_all()
                return 0
            while generation == self._generation:
                self._condition.wait()
            return 1


class Condvar:
    __slots__ = ("_condition", "_notify_all")

    def __init__(self, notify_all: bool = True) -> None:
        self._condition = threading.Condition()
        self._notify_all = notify_all

    @classmethod
    def new(cls) -> Condvar:
        return cls()

    def wait(self, lock: threading.Lock | None = None) -> None:
        with self._condition:
            if lock:
                lock.release()
            self._condition.wait()
            if lock:
                lock.acquire()

    def wait_while(self, predicate: Callable[[], bool], lock: threading.Lock | None = None) -> None:
        with self._condition:
            while predicate():
                if lock:
                    lock.release()
                self._condition.wait()
                if lock:
                    lock.acquire()

    def notify_one(self) -> None:
        with self._condition:
            self._condition.notify()

    def notify_all(self) -> None:
        with self._condition:
            self._condition.notify_all()

    def __enter__(self) -> Condvar:
        self._condition.acquire()
        return self

    def __exit__(self, *_: Any) -> None:
        self._condition.release()


class Sender(Generic[T]):
    __slots__ = ("_queue", "_closed")

    def __init__(self, queue: Any) -> None:
        self._queue = queue
        self._closed = False

    def send(self, value: T) -> bool:
        if self._closed:
            return False
        try:
            self._queue.put_nowait(value)
            return True
        except Exception:
            return False

    def is_closed(self) -> bool:
        return self._closed

    def close(self) -> None:
        self._closed = True

    def __enter__(self) -> Sender[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Sender(closed={self._closed})"


class Receiver(Generic[T]):
    __slots__ = ("_queue", "_closed")

    def __init__(self, queue: Any) -> None:
        self._queue = queue
        self._closed = False

    def recv(self) -> T | None:
        try:
            return self._queue.get_nowait()
        except Exception:
            return None

    def recv_blocking(self, timeout: float | None = None) -> T | None:
        try:
            return self._queue.get(timeout=timeout)
        except Exception:
            return None

    def try_recv(self) -> T | None:
        return self.recv()

    def is_empty(self) -> bool:
        return self._queue.empty()

    def is_closed(self) -> bool:
        return self._closed

    def __enter__(self) -> Receiver[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        self._closed = True

    def __iter__(self) -> Iterator[T]:
        while True:
            value = self.recv()
            if value is None:
                break
            yield value

    def __repr__(self) -> str:
        return f"Receiver(closed={self._closed})"


class Channel(Generic[T]):
    __slots__ = ("_sender", "_receiver")

    def __init__(self, capacity: int = 0) -> None:
        if capacity == 0:
            q: Any = _queue.SimpleQueue()
        else:
            q = _queue.Queue(maxsize=capacity)
        self._sender = Sender[T](q)
        self._receiver = Receiver[T](q)

    @classmethod
    def unbounded(cls) -> Channel[T]:
        return cls(0)

    @classmethod
    def bounded(cls, capacity: int) -> Channel[T]:
        return cls(capacity)

    @property
    def sender(self) -> Sender[T]:
        return self._sender

    @property
    def receiver(self) -> Receiver[T]:
        return self._receiver

    def send(self, value: T) -> bool:
        return self._sender.send(value)

    def recv(self) -> T | None:
        return self._receiver.recv()

    def __repr__(self) -> str:
        return f"Channel(sender={self._sender}, receiver={self._receiver})"


import queue as _queue


class Once:
    __slots__ = ("_executed", "_lock", "_result")

    def __init__(self) -> None:
        self._executed = False
        self._lock = threading.Lock()
        self._result: Any = None

    @classmethod
    def new(cls) -> Once:
        return cls()

    def call_once(self, fn: Callable[[], T]) -> T:
        if self._executed:
            return self._result
        with self._lock:
            if not self._executed:
                self._result = fn()
                self._executed = True
        return self._result

    def is_completed(self) -> bool:
        return self._executed

    def __repr__(self) -> str:
        return f"Once(completed={self._executed})"


class Semaphore:
    __slots__ = ("_semaphore", "_max")

    def __init__(self, max_permits: int) -> None:
        if max_permits <= 0:
            raise ValueError("max_permits must be positive")
        self._semaphore = threading.Semaphore(max_permits)
        self._max = max_permits

    @classmethod
    def new(cls, max_permits: int) -> Semaphore:
        return cls(max_permits)

    def acquire(self, blocking: bool = True, timeout: float | None = None) -> bool:
        return self._semaphore.acquire(blocking=blocking, timeout=timeout)

    def release(self) -> None:
        self._semaphore.release()

    def available(self) -> int:
        return self._semaphore._value  # type: ignore

    @property
    def max_permits(self) -> int:
        return self._max

    def __enter__(self) -> Semaphore:
        self.acquire()
        return self

    def __exit__(self, *_: Any) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"Semaphore(max={self._max})"


class Poll(Generic[T]):
    __slots__ = ("_ready", "_value")

    def __init__(self, ready: bool, value: T | None = None) -> None:
        self._ready = ready
        self._value = value

    @classmethod
    def ready(cls, value: T) -> Poll[T]:
        return cls(True, value)

    @classmethod
    def pending(cls) -> Poll[T]:
        return cls(False)

    def is_ready(self) -> bool:
        return self._ready

    def is_pending(self) -> bool:
        return not self._ready

    def unwrap(self) -> T:
        if not self._ready:
            raise RuntimeError("called unwrap on pending Poll")
        return self._value  # type: ignore

    def unwrap_or(self, default: T) -> T:
        if not self._ready:
            return default
        return self._value  # type: ignore

    def map(self, fn: Callable[[T], U]) -> Poll[U]:
        if self._ready:
            return Poll.ready(fn(self._value))  # type: ignore
        return Poll.pending()

    def and_then(self, fn: Callable[[T], Poll[U]]) -> Poll[U]:
        if self._ready:
            return fn(self._value)  # type: ignore
        return Poll.pending()

    def inspect(self, fn: Callable[[T], Any]) -> Poll[T]:
        if self._ready:
            fn(self._value)  # type: ignore
        return self

    def __repr__(self) -> str:
        if self._ready:
            return f"Poll::Ready({self._value!r})"
        return "Poll::Pending"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Poll):
            if self._ready != other._ready:
                return False
            if self._ready:
                return self._value == other._value
            return True
        return NotImplemented

    def __bool__(self) -> bool:
        return self._ready


class Waker:
    __slots__ = ("_wake_fn", "_woken")

    def __init__(self, wake_fn: Callable[[], None] | None = None) -> None:
        self._wake_fn = wake_fn
        self._woken = False

    def wake(self) -> None:
        self._woken = True
        if self._wake_fn:
            self._wake_fn()

    def wake_by_ref(self) -> None:
        self.wake()

    def clone_waker(self) -> Waker:
        return Waker(self._wake_fn)

    def is_woken(self) -> bool:
        return self._woken

    def reset(self) -> None:
        self._woken = False

    def __repr__(self) -> str:
        return f"Waker(woken={self._woken})"


class JoinHandle(Generic[T]):
    __slots__ = ("_future", "_result", "_done", "_exception", "_thread")

    def __init__(self, future: Future[T]) -> None:
        self._future = future
        self._result: T | None = None
        self._done = False
        self._exception: Exception | None = None
        self._thread: threading.Thread | None = None

    def run(self) -> None:
        try:
            loop = asyncio.new_event_loop()
            self._result = loop.run_until_complete(self._future)
            loop.close()
        except Exception as e:
            self._exception = e
        finally:
            self._done = True

    def start(self) -> None:
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def is_finished(self) -> bool:
        return self._done

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def abort(self) -> bool:
        if self._thread and self._thread.is_alive():
            return False
        return True

    def get_result(self, timeout: float | None = None) -> T | None:
        if self._thread:
            self._thread.join(timeout=timeout)
        if self._exception:
            raise self._exception
        return self._result

    def join(self, timeout: float | None = None) -> T | None:
        return self.get_result(timeout)

    def __enter__(self) -> JoinHandle[T]:
        return self

    def __exit__(self, *_: Any) -> None:
        if self._thread:
            self._thread.join()

    def __repr__(self) -> str:
        return f"JoinHandle(finished={self._done})"


class Stream(Generic[T]):
    __slots__ = ("_async_gen", "_buffer")

    def __init__(self, async_gen: Any = None) -> None:
        self._async_gen = async_gen
        self._buffer: list[T] = []

    @classmethod
    def from_iter(cls, iterable: Iterable[T]) -> Stream[T]:
        async def gen():
            for v in iterable:
                yield v
        return cls(gen())

    @classmethod
    def from_async_iter(cls, async_iter: Any) -> Stream[T]:
        return cls(async_iter)

    @classmethod
    def empty(cls) -> Stream[T]:
        async def gen():
            return
            yield  # type: ignore[misc]
        return cls(gen())

    @classmethod
    def once(cls, value: T) -> Stream[T]:
        async def gen():
            yield value
        return cls(gen())

    @classmethod
    def repeat(cls, value: T) -> Stream[T]:
        async def gen():
            while True:
                yield value
        return cls(gen())

    @classmethod
    def chain(cls, *streams: Stream[T]) -> Stream[T]:
        async def gen():
            for s in streams:
                async for item in s._async_gen:
                    yield item
        return cls(gen())

    async def next(self) -> T | None:
        try:
            return await self._async_gen.__anext__()
        except StopAsyncIteration:
            return None

    async def map(self, fn: Callable[[T], U]) -> Stream[U]:
        async def gen():
            async for item in self._async_gen:
                yield fn(item)
        return Stream(gen())

    async def filter(self, predicate: Callable[[T], bool]) -> Stream[T]:
        async def gen():
            async for item in self._async_gen:
                if predicate(item):
                    yield item
        return Stream(gen())

    async def take(self, n: int) -> Stream[T]:
        async def gen():
            count = 0
            async for item in self._async_gen:
                if count >= n:
                    break
                yield item
                count += 1
        return Stream(gen())

    async def collect(self) -> list[T]:
        result = []
        async for item in self._async_gen:
            result.append(item)
        return result

    async def fold(self, init: U, fn: Callable[[U, T], U]) -> U:
        acc = init
        async for item in self._async_gen:
            acc = fn(acc, item)
        return acc

    async def for_each(self, fn: Callable[[T], Any]) -> None:
        async for item in self._async_gen:
            fn(item)

    async def count(self) -> int:
        n = 0
        async for _ in self._async_gen:
            n += 1
        return n

    async def first(self) -> T | None:
        return await self.next()

    async def peek(self) -> T | None:
        try:
            item = await self._async_gen.__anext__()
            self._buffer.append(item)
            return item
        except StopAsyncIteration:
            return None

    def __aiter__(self) -> Any:
        return self._async_gen

    def __repr__(self) -> str:
        return "Stream(...)"


class Future(Generic[T]):
    __slots__ = ("_coro", "_done", "_result", "_exception", "_callbacks")

    def __init__(self, coro: Any = None) -> None:
        self._coro = coro
        self._done = False
        self._result: T | None = None
        self._exception: Exception | None = None
        self._callbacks: list[Callable[[Future[T]], None]] = []

    @classmethod
    def ready(cls, value: T) -> Future[T]:
        f = cls()
        f._done = True
        f._result = value
        return f

    @classmethod
    def pending(cls) -> Future[T]:
        return cls()

    def poll(self, waker: Waker | None = None) -> Poll[T]:
        if self._done:
            if self._exception:
                raise self._exception
            return Poll.ready(self._result)  # type: ignore
        return Poll.pending()

    def is_done(self) -> bool:
        return self._done

    def result(self) -> T | None:
        return self._result

    def exception(self) -> Exception | None:
        return self._exception

    def add_done_callback(self, fn: Callable[[Future[T]], None]) -> None:
        if self._done:
            fn(self)
        else:
            self._callbacks.append(fn)

    def set_result(self, value: T) -> None:
        self._result = value
        self._done = True
        for cb in self._callbacks:
            cb(self)

    def set_exception(self, exc: Exception) -> None:
        self._exception = exc
        self._done = True
        for cb in self._callbacks:
            cb(self)

    def map(self, fn: Callable[[T], U]) -> Future[U]:
        async def mapped():
            result = await self
            return fn(result)
        return Future(mapped())

    def and_then(self, fn: Callable[[T], Future[U]]) -> Future[U]:
        async def chained():
            result = await self
            return await fn(result)
        return Future(chained())

    def __await__(self) -> Any:
        if self._coro is not None:
            return self._coro.__await__()
        if self._done:
            if self._exception:
                raise self._exception
            async def _ready():
                return self._result
            return _ready().__await__()
        async def _pending():
            return None
        return _pending().__await__()

    def __repr__(self) -> str:
        if self._done:
            return f"Future::Ready({self._result!r})"
        return "Future::Pending"


def spawn(coro: Any) -> JoinHandle:
    future = Future(coro)
    handle = JoinHandle(future)
    handle.start()
    return handle


async def join_all(handles: list[JoinHandle]) -> list:
    results = []
    for h in handles:
        results.append(h.get_result())
    return results


class Elapsed(Exception):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("timer expiration error")


class Duration:
    __slots__ = ("_secs", "_nanos")

    def __init__(self, secs: int = 0, nanos: int = 0) -> None:
        if secs < 0 or nanos < 0:
            raise ValueError("duration values must be non-negative")
        self._secs = secs + nanos // 1_000_000_000
        self._nanos = nanos % 1_000_000_000

    @classmethod
    def from_secs(cls, secs: int | float) -> Duration:
        s = int(secs)
        ns = int((secs - s) * 1_000_000_000)
        return cls(s, ns)

    @classmethod
    def from_millis(cls, millis: int | float) -> Duration:
        s = int(millis) // 1000
        ns = (int(millis) % 1000) * 1_000_000
        return cls(s, ns)

    @classmethod
    def from_micros(cls, micros: int | float) -> Duration:
        s = int(micros) // 1_000_000
        ns = (int(micros) % 1_000_000) * 1_000
        return cls(s, ns)

    @classmethod
    def from_nanos(cls, nanos: int) -> Duration:
        return cls(0, nanos)

    @classmethod
    def from_minutes(cls, minutes: int | float) -> Duration:
        return cls.from_secs(minutes * 60)

    @classmethod
    def from_hours(cls, hours: int | float) -> Duration:
        return cls.from_secs(hours * 3600)

    @classmethod
    def from_days(cls, days: int | float) -> Duration:
        return cls.from_secs(days * 86400)

    @classmethod
    def zero(cls) -> Duration:
        return cls(0, 0)

    def as_secs(self) -> int:
        return self._secs

    def as_millis(self) -> int:
        return self._secs * 1000 + self._nanos // 1_000_000

    def as_micros(self) -> int:
        return self._secs * 1_000_000 + self._nanos // 1_000

    def as_nanos(self) -> int:
        return self._secs * 1_000_000_000 + self._nanos

    def secs_f64(self) -> float:
        return self._secs + self._nanos / 1_000_000_000

    def is_zero(self) -> bool:
        return self._secs == 0 and self._nanos == 0

    def checked_add(self, other: Duration) -> Duration | None:
        try:
            return Duration(self._secs + other._secs, self._nanos + other._nanos)
        except (ValueError, OverflowError):
            return None

    def checked_sub(self, other: Duration) -> Duration | None:
        total_self = self.as_nanos()
        total_other = other.as_nanos()
        if total_self < total_other:
            return None
        return Duration.from_nanos(total_self - total_other)

    def saturating_add(self, other: Duration) -> Duration:
        result = self.checked_add(other)
        return result if result else Duration.from_secs(float('inf'))

    def saturating_sub(self, other: Duration) -> Duration:
        result = self.checked_sub(other)
        return result if result else Duration.zero()

    def mul(self, rhs: int) -> Duration:
        return Duration.from_nanos(self.as_nanos() * rhs)

    def div(self, rhs: int) -> Duration:
        if rhs == 0:
            raise ZeroDivisionError("division by zero")
        return Duration.from_nanos(self.as_nanos() // rhs)

    def __add__(self, other: Duration) -> Duration:
        return Duration(self._secs + other._secs, self._nanos + other._nanos)

    def __sub__(self, other: Duration) -> Duration:
        result = self.checked_sub(other)
        if result is None:
            raise ValueError("underflow in duration subtraction")
        return result

    def __mul__(self, rhs: int) -> Duration:
        return self.mul(rhs)

    def __rmul__(self, lhs: int) -> Duration:
        return self.mul(lhs)

    def __floordiv__(self, rhs: int) -> Duration:
        return self.div(rhs)

    def __mod__(self, other: Duration) -> Duration:
        nanos = self.as_nanos() % other.as_nanos()
        return Duration.from_nanos(nanos)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Duration):
            return self._secs == other._secs and self._nanos == other._nanos
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Duration):
            return self._secs != other._secs or self._nanos != other._nanos
        return NotImplemented

    def __lt__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() < other.as_nanos()
        return NotImplemented

    def __le__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() <= other.as_nanos()
        return NotImplemented

    def __gt__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() > other.as_nanos()
        return NotImplemented

    def __ge__(self, other: Duration) -> bool:
        if isinstance(other, Duration):
            return self.as_nanos() >= other.as_nanos()
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._secs, self._nanos))

    def __repr__(self) -> str:
        if self._nanos == 0:
            return f"Duration(secs={self._secs})"
        return f"Duration(secs={self._secs}, nanos={self._nanos})"

    def __bool__(self) -> bool:
        return not self.is_zero()


UNIX_EPOCH = Duration(0, 0)


class Instant:
    __slots__ = ("_monotonic", "_wall")

    def __init__(self) -> None:
        self._monotonic = time.monotonic()
        self._wall = time.time()

    @classmethod
    def now(cls) -> Instant:
        return cls()

    @classmethod
    def from_secs(cls, secs: float) -> Instant:
        inst = cls()
        inst._wall = secs
        return inst

    def elapsed(self) -> Duration:
        return Duration.from_secs(time.monotonic() - self._monotonic)

    def checked_elapsed(self) -> Duration | None:
        diff = time.monotonic() - self._monotonic
        if diff < 0:
            return None
        return Duration.from_secs(diff)

    def checked_duration_since(self, earlier: Instant) -> Duration | None:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            return None
        return Duration.from_secs(diff)

    def duration_since(self, earlier: Instant) -> Duration:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            raise Elapsed()
        return Duration.from_secs(diff)

    def checked_since(self, earlier: Instant) -> Instant | None:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            return None
        return self

    def saturating_duration_since(self, earlier: Instant) -> Duration:
        diff = self._monotonic - earlier._monotonic
        if diff < 0:
            return Duration.zero()
        return Duration.from_secs(diff)

    def add_duration(self, duration: Duration) -> Instant:
        inst = Instant()
        inst._monotonic = self._monotonic + duration.secs_f64()
        inst._wall = self._wall + duration.secs_f64()
        return inst

    def checked_add_duration(self, duration: Duration) -> Instant | None:
        try:
            return self.add_duration(duration)
        except (ValueError, OverflowError):
            return None

    def as_secs(self) -> float:
        return self._wall

    def as_millis(self) -> int:
        return int(self._wall * 1000)

    def __sub__(self, other: Instant) -> Duration:
        return self.duration_since(other)

    def __add__(self, duration: Duration) -> Instant:
        return self.add_duration(duration)

    def __radd__(self, duration: Duration) -> Instant:
        return self.add_duration(duration)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Instant):
            return self._monotonic == other._monotonic
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Instant):
            return self._monotonic != other._monotonic
        return NotImplemented

    def __lt__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic < other._monotonic
        return NotImplemented

    def __le__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic <= other._monotonic
        return NotImplemented

    def __gt__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic > other._monotonic
        return NotImplemented

    def __ge__(self, other: Instant) -> bool:
        if isinstance(other, Instant):
            return self._monotonic >= other._monotonic
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._monotonic)

    def __repr__(self) -> str:
        return f"Instant({self._wall:.6f})"


class SystemTime:
    __slots__ = ("_seconds", "_nanos", "_tz")

    def __init__(self) -> None:
        now = _dt_module.datetime.now()
        epoch = _dt_module.datetime(1970, 1, 1)
        delta = now - epoch
        self._seconds = int(delta.total_seconds())
        self._nanos = delta.microseconds * 1000
        self._tz = now.tzinfo

    @classmethod
    def now(cls) -> SystemTime:
        return cls()

    @classmethod
    def from_secs(cls, secs: int, nanos: int = 0) -> SystemTime:
        t = cls.__new__(cls)
        t._seconds = secs
        t._nanos = nanos
        t._tz = None
        return t

    def duration_since(self, earlier: SystemTime) -> Duration:
        diff_secs = self._seconds - earlier._seconds
        diff_nanos = self._nanos - earlier._nanos
        if diff_nanos < 0:
            diff_secs -= 1
            diff_nanos += 1_000_000_000
        if diff_secs < 0:
            raise Elapsed()
        return Duration(diff_secs, diff_nanos)

    def checked_duration_since(self, earlier: SystemTime) -> Duration | None:
        diff_secs = self._seconds - earlier._seconds
        diff_nanos = self._nanos - earlier._nanos
        if diff_nanos < 0:
            diff_secs -= 1
            diff_nanos += 1_000_000_000
        if diff_secs < 0:
            return None
        return Duration(diff_secs, diff_nanos)

    def saturating_duration_since(self, earlier: SystemTime) -> Duration:
        result = self.checked_duration_since(earlier)
        return result if result else Duration.zero()

    def add_duration(self, duration: Duration) -> SystemTime:
        new_secs = self._seconds + duration._secs
        new_nanos = self._nanos + duration._nanos
        if new_nanos >= 1_000_000_000:
            new_secs += 1
            new_nanos -= 1_000_000_000
        t = SystemTime.__new__(SystemTime)
        t._seconds = new_secs
        t._nanos = new_nanos
        t._tz = None
        return t

    def checked_add_duration(self, duration: Duration) -> SystemTime | None:
        try:
            return self.add_duration(duration)
        except (ValueError, OverflowError):
            return None

    def checked_sub_duration(self, duration: Duration) -> SystemTime | None:
        new_secs = self._seconds - duration._secs
        new_nanos = self._nanos - duration._nanos
        if new_nanos < 0:
            new_secs -= 1
            new_nanos += 1_000_000_000
        if new_secs < 0:
            return None
        t = SystemTime.__new__(SystemTime)
        t._seconds = new_secs
        t._nanos = new_nanos
        t._tz = None
        return t

    def sub(self, other: SystemTime) -> Duration:
        return self.duration_since(other)

    def as_secs(self) -> int:
        return self._seconds

    def from_epoch(self) -> Duration:
        return Duration(self._seconds, self._nanos)

    def to_datetime(self) -> _dt_module.datetime:
        return _dt_module.datetime.fromtimestamp(self._seconds, tz=self._tz)

    def __sub__(self, other: SystemTime) -> Duration:
        return self.duration_since(other)

    def __add__(self, duration: Duration) -> SystemTime:
        return self.add_duration(duration)

    def __radd__(self, duration: Duration) -> SystemTime:
        return self.add_duration(duration)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SystemTime):
            return self._seconds == other._seconds and self._nanos == other._nanos
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, SystemTime):
            return self._seconds != other._seconds or self._nanos != other._nanos
        return NotImplemented

    def __lt__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) < (other._seconds, other._nanos)
        return NotImplemented

    def __le__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) <= (other._seconds, other._nanos)
        return NotImplemented

    def __gt__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) > (other._seconds, other._nanos)
        return NotImplemented

    def __ge__(self, other: SystemTime) -> bool:
        if isinstance(other, SystemTime):
            return (self._seconds, self._nanos) >= (other._seconds, other._nanos)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._seconds, self._nanos))

    def __repr__(self) -> str:
        return f"SystemTime({self._seconds}.{self._nanos:09d})"


class FileType:
    __slots__ = ("_is_file", "_is_dir", "_is_symlink")

    def __init__(self, is_file: bool = False, is_dir: bool = False, is_symlink: bool = False) -> None:
        self._is_file = is_file
        self._is_dir = is_dir
        self._is_symlink = is_symlink

    def is_file(self) -> bool:
        return self._is_file

    def is_dir(self) -> bool:
        return self._is_dir

    def is_symlink(self) -> bool:
        return self._is_symlink

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FileType):
            return (self._is_file, self._is_dir, self._is_symlink) == (other._is_file, other._is_dir, other._is_symlink)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._is_file, self._is_dir, self._is_symlink))

    def __repr__(self) -> str:
        if self._is_file:
            return "FileType::File"
        if self._is_dir:
            return "FileType::Dir"
        if self._is_symlink:
            return "FileType::Symlink"
        return "FileType::Unknown"


class Permissions:
    __slots__ = ("_readonly",)

    def __init__(self, readonly: bool = False) -> None:
        self._readonly = readonly

    def readonly(self) -> bool:
        return self._readonly

    def set_readonly(self, readonly: bool) -> None:  # type: ignore
        self._readonly = readonly

    def mode(self) -> int:
        if self._readonly:
            return 0o444
        return 0o644

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Permissions):
            return self._readonly == other._readonly
        return NotImplemented

    def __repr__(self) -> str:
        return f"Permissions(readonly={self._readonly})"


class Metadata:
    __slots__ = ("_file_type", "_permissions", "_size", "_modified", "_accessed", "_created", "_is_symlink")

    def __init__(self) -> None:
        self._file_type = FileType()
        self._permissions = Permissions()
        self._size = 0
        self._modified: float | None = None
        self._accessed: float | None = None
        self._created: float | None = None
        self._is_symlink = False

    def file_type(self) -> FileType:
        return self._file_type

    def is_dir(self) -> bool:
        return self._file_type.is_dir()

    def is_file(self) -> bool:
        return self._file_type.is_file()

    def is_symlink(self) -> bool:
        return self._is_symlink

    def len(self) -> int:  # type: ignore
        return self._size

    def size(self) -> int:
        return self._size

    def permissions(self) -> Permissions:
        return self._permissions

    def modified(self) -> SystemTime | None:
        if self._modified is None:
            return None
        t = SystemTime.__new__(SystemTime)
        t._seconds = int(self._modified)
        t._nanos = int((self._modified % 1) * 1_000_000_000)
        t._tz = None
        return t

    def accessed(self) -> SystemTime | None:
        if self._accessed is None:
            return None
        t = SystemTime.__new__(SystemTime)
        t._seconds = int(self._accessed)
        t._nanos = int((self._accessed % 1) * 1_000_000_000)
        t._tz = None
        return t

    def created(self) -> SystemTime | None:
        if self._created is None:
            return None
        t = SystemTime.__new__(SystemTime)
        t._seconds = int(self._created)
        t._nanos = int((self._created % 1) * 1_000_000_000)
        t._tz = None
        return t

    def __repr__(self) -> str:
        return f"Metadata(type={self._file_type}, size={self._size})"


class DirEntry:
    __slots__ = ("_path", "_metadata", "_name")

    def __init__(self, path: str | os.PathLike) -> None:
        self._path = os.fspath(path)
        self._name = os.path.basename(self._path)
        self._metadata: Metadata | None = None

    def path(self) -> Path:
        return Path(self._path)

    def file_name(self) -> str:
        return self._name

    def metadata(self) -> Metadata:
        if self._metadata is None:
            self._metadata = _metadata_from_os(self._path)
        return self._metadata

    def file_type(self) -> FileType:
        return self.metadata().file_type()

    def into_path(self) -> Path:  # type: ignore
        return Path(self._path)

    def __repr__(self) -> str:
        return f"DirEntry({self._name!r})"


class Path:
    __slots__ = ("_path",)

    def __init__(self, path: str | os.PathLike) -> None:
        self._path = os.fspath(path) if isinstance(path, os.PathLike) else path

    @classmethod
    def new(cls, path: str) -> Path:  # type: ignore
        return cls(path)

    def as_str(self) -> str:
        return self._path

    def to_str(self) -> str | None:
        return self._path

    def to_string_lossy(self) -> str:
        return self._path

    def to_path_buf(self) -> PathBuf:  # type: ignore
        return PathBuf(self._path)

    def as_os_str(self) -> str:  # type: ignore
        return self._path

    def is_absolute(self) -> bool:
        return os.path.isabs(self._path)

    def is_relative(self) -> bool:  # type: ignore
        return not self.is_absolute()

    def is_relative_to(self, base: str | Path) -> bool:  # type: ignore
        base_str = base.as_str() if isinstance(base, Path) else str(base)
        try:
            os.path.relpath(self._path, base_str)
            return True
        except ValueError:
            return False

    def starts_with(self, base: str | Path) -> bool:  # type: ignore
        base_str = base.as_str() if isinstance(base, Path) else str(base)
        return os.path.commonpath([self._path, base_str]) == base_str or self._path == base_str

    def ends_with(self, ext: str | Path) -> bool:  # type: ignore
        ext_str = ext.as_str() if isinstance(ext, Path) else str(ext)
        return self._path.endswith(ext_str)

    def parent(self) -> Path | None:
        parent = os.path.dirname(self._path)
        if not parent:
            return None
        return Path(parent)

    def file_name(self) -> str | None:  # type: ignore
        return os.path.basename(self._path) or None

    def extension(self) -> str | None:  # type: ignore
        _, ext = os.path.splitext(self._path)
        return ext[1:] if ext else None

    def file_stem(self) -> str | None:  # type: ignore
        stem, _ = os.path.splitext(os.path.basename(self._path))
        return stem or None

    def with_extension(self, ext: str) -> Path:  # type: ignore
        base, _ = os.path.splitext(self._path)
        if ext and not ext.startswith('.'):
            ext = '.' + ext
        return Path(base + ext)

    def join(self, other: str | Path) -> Path:
        other_str = other.as_str() if isinstance(other, Path) else other
        return Path(os.path.join(self._path, other_str))

    def __truediv__(self, other: str | Path) -> Path:
        return self.join(other)

    def __rtruediv__(self, other: str | Path) -> Path:
        other_str = other.as_str() if isinstance(other, Path) else other
        return Path(os.path.join(other_str, self._path))

    def exists(self) -> bool:
        return os.path.exists(self._path)

    def is_file(self) -> bool:  # type: ignore
        return os.path.isfile(self._path)

    def is_dir(self) -> bool:  # type: ignore
        return os.path.isdir(self._path)

    def is_symlink(self) -> bool:  # type: ignore
        return os.path.islink(self._path)

    def metadata(self) -> Metadata:  # type: ignore
        return _metadata_from_os(self._path)

    def canonicalize(self) -> Path:  # type: ignore
        return Path(os.path.realpath(self._path))

    def normalize(self) -> Path:  # type: ignore
        return Path(os.path.normpath(self._path))

    def display(self) -> str:
        return self._path

    def to_absolute(self) -> Path:  # type: ignore
        return Path(os.path.abspath(self._path))

    def read_to_string(self) -> str:  # type: ignore
        with open(self._path, 'r') as f:
            return f.read()

    def read_to_bytes(self) -> bytes:  # type: ignore
        with open(self._path, 'rb') as f:
            return f.read()

    def write_str(self, data: str) -> None:  # type: ignore
        with open(self._path, 'w') as f:
            f.write(data)

    def write_bytes(self, data: bytes) -> None:  # type: ignore
        with open(self._path, 'wb') as f:
            f.write(data)

    def create_dir(self) -> None:  # type: ignore
        os.makedirs(self._path, exist_ok=True)

    def create_dir_all(self) -> None:  # type: ignore
        os.makedirs(self._path, exist_ok=True)

    def remove_file(self) -> None:  # type: ignore
        os.remove(self._path)

    def remove_dir(self) -> None:  # type: ignore
        os.rmdir(self._path)

    def remove_dir_all(self) -> None:  # type: ignore
        import shutil
        shutil.rmtree(self._path)

    def rename(self, to: str | Path) -> None:  # type: ignore
        to_str = to.as_str() if isinstance(to, Path) else str(to)
        os.rename(self._path, to_str)

    def copy(self, to: str | Path) -> None:  # type: ignore
        import shutil
        to_str = to.as_str() if isinstance(to, Path) else str(to)
        shutil.copy2(self._path, to_str)

    def read_dir(self) -> ReadDir:
        return ReadDir(self._path)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Path):
            return os.path.normpath(self._path) == os.path.normpath(other._path)
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Path):
            return os.path.normpath(self._path) != os.path.normpath(other._path)
        return NotImplemented

    def __lt__(self, other: Path) -> bool:
        if isinstance(other, Path):
            return os.path.normpath(self._path) < os.path.normpath(other._path)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(os.path.normpath(self._path))

    def __fspath__(self) -> str:
        return self._path

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"Path({self._path!r})"


class PathBuf:
    __slots__ = ("_path",)

    def __init__(self, path: str | os.PathLike | Path = "") -> None:
        if isinstance(path, Path):
            self._path = path.as_str()
        else:
            self._path = os.fspath(path) if isinstance(path, os.PathLike) else path

    @classmethod
    def new(cls) -> PathBuf:  # type: ignore
        return cls("")

    @classmethod
    def from_str(cls, s: str) -> PathBuf:  # type: ignore
        return cls(s)

    def as_path(self) -> Path:
        return Path(self._path)

    def as_str(self) -> str:
        return self._path

    def into_string(self) -> str:  # type: ignore
        return self._path

    def push(self, path: str | Path) -> None:  # type: ignore
        if isinstance(path, Path):
            self._path = os.path.join(self._path, path.as_str())
        else:
            self._path = os.path.join(self._path, path)

    def push_str(self, s: str) -> None:  # type: ignore
        self._path = os.path.join(self._path, s)

    def pop(self) -> bool:  # type: ignore
        parent = os.path.dirname(self._path)
        if parent == self._path:
            return False
        self._path = parent
        return True

    def set_extension(self, ext: str) -> bool:  # type: ignore
        base, _ = os.path.splitext(self._path)
        if ext and not ext.startswith('.'):
            ext = '.' + ext
        self._path = base + ext
        return True

    def clear(self) -> None:  # type: ignore
        self._path = ""

    def into_boxed(self) -> Path:  # type: ignore
        return Path(self._path)

    def is_absolute(self) -> bool:  # type: ignore
        return os.path.isabs(self._path)

    def parent(self) -> Path | None:  # type: ignore
        parent = os.path.dirname(self._path)
        if not parent:
            return None
        return Path(parent)

    def file_name(self) -> str | None:  # type: ignore
        return os.path.basename(self._path) or None

    def extension(self) -> str | None:  # type: ignore
        _, ext = os.path.splitext(self._path)
        return ext[1:] if ext else None

    def join(self, other: str | Path) -> PathBuf:  # type: ignore
        other_str = other.as_str() if isinstance(other, Path) else other
        return PathBuf(os.path.join(self._path, other_str))

    def canonicalize(self) -> PathBuf:  # type: ignore
        return PathBuf(os.path.realpath(self._path))

    def normalize(self) -> PathBuf:  # type: ignore
        return PathBuf(os.path.normpath(self._path))

    def exists(self) -> bool:  # type: ignore
        return os.path.exists(self._path)

    def __truediv__(self, other: str | Path) -> PathBuf:  # type: ignore
        return self.join(other)

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"PathBuf({self._path!r})"


class OpenOptions:
    __slots__ = ("_read", "_write", "_append", "_truncate", "_create", "_create_new")

    def __init__(self) -> None:
        self._read = False
        self._write = False
        self._append = False
        self._truncate = False
        self._create = False
        self._create_new = False

    @classmethod
    def new(cls) -> OpenOptions:  # type: ignore
        return cls()

    def read(self, enable: bool = True) -> OpenOptions:
        self._read = enable
        return self

    def write(self, enable: bool = True) -> OpenOptions:
        self._write = enable
        return self

    def append(self, enable: bool = True) -> OpenOptions:
        self._append = enable
        return self

    def truncate(self, enable: bool = True) -> OpenOptions:
        self._truncate = enable
        return self

    def create(self, enable: bool = True) -> OpenOptions:
        self._create = enable
        return self

    def create_new(self, enable: bool = True) -> OpenOptions:
        self._create_new = enable
        return self

    def open(self, path: str | Path) -> File:
        path_str = path.as_str() if isinstance(path, Path) else str(path)

        if self._create_new and os.path.exists(path_str):
            raise FileExistsError(f"file already exists: {path_str}")

        mode = 'r'
        if self._create_new or (self._create and self._write):
            mode = 'w'
        elif self._write and self._append:
            mode = 'a'
        elif self._write:
            mode = 'w'
        elif self._read and self._write:
            mode = 'r+'
        elif self._read:
            mode = 'r'

        if self._truncate and mode in ('r+', 'w', 'a'):
            if mode == 'r+':
                mode = 'w'
            elif mode == 'a':
                mode = 'w'

        if 'w' in mode and not self._create and not os.path.exists(path_str):
            if not self._create:
                raise FileNotFoundError(f"no such file or directory: {path_str}")

        f = open(path_str, mode)  # type: ignore[arg-type]
        return File(f, path_str)

    def __repr__(self) -> str:  # type: ignore
        flags = []
        if self._read:
            flags.append("read")
        if self._write:
            flags.append("write")
        if self._append:
            flags.append("append")
        if self._truncate:
            flags.append("truncate")
        if self._create:
            flags.append("create")
        if self._create_new:
            flags.append("create_new")
        return f"OpenOptions({', '.join(flags)})"


class File:
    __slots__ = ("_handle", "_path", "_closed")

    def __init__(self, handle: Any, path: str = "") -> None:
        self._handle = handle
        self._path = path
        self._closed = False

    @classmethod
    def create(cls, path: str | Path) -> File:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        return cls(open(path_str, 'w'), path_str)

    @classmethod
    def create_new(cls, path: str | Path) -> File:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        if os.path.exists(path_str):
            raise FileExistsError(f"file already exists: {path_str}")
        return cls(open(path_str, 'w'), path_str)

    @classmethod
    def open(cls, path: str | Path) -> File:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        return cls(open(path_str, 'r'), path_str)

    @classmethod
    def options(cls) -> OpenOptions:  # type: ignore
        return OpenOptions()

    def read(self) -> bytes:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.read()  # type: ignore

    def read_exact(self, buf: bytearray) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        data = self._handle.read(len(buf))  # type: ignore
        n = len(data)
        buf[:n] = data
        return n

    def read_to_string(self) -> str:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.read()  # type: ignore

    def write(self, data: bytes | str) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.write(data)  # type: ignore

    def write_all(self, data: bytes | str) -> None:  # type: ignore
        self.write(data)

    def flush(self) -> None:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        self._handle.flush()  # type: ignore

    def sync_all(self) -> None:  # type: ignore
        self.flush()

    def sync_data(self) -> None:  # type: ignore
        self.flush()

    def seek(self, pos: int) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.seek(pos)  # type: ignore

    def seek_from_start(self, offset: int) -> int:  # type: ignore
        return self.seek(offset)

    def seek_from_current(self, offset: int) -> int:  # type: ignore
        return self.seek(offset)

    def seek_from_end(self, offset: int) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.seek(offset, 2)  # type: ignore

    def stream_position(self) -> int:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return self._handle.tell()  # type: ignore

    def set_len(self, size: int) -> None:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        self._handle.truncate(size)  # type: ignore

    def metadata(self) -> Metadata:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        return _metadata_from_os(self._path)

    def set_permissions(self, perm: Permissions) -> None:  # type: ignore
        os.chmod(self._path, 0o444 if perm.readonly() else 0o644)

    def path(self) -> Path:  # type: ignore
        return Path(self._path)

    def into_inner(self) -> Any:  # type: ignore
        self._closed = True
        return self._handle

    def try_clone(self) -> File:  # type: ignore
        if self._closed:
            raise ValueError("file is closed")
        import io
        new_handle = open(self._path, self._handle.mode)  # type: ignore
        return File(new_handle, self._path)

    def __enter__(self) -> File:  # type: ignore
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        self.close()

    def close(self) -> None:  # type: ignore
        if not self._closed:
            self._handle.close()  # type: ignore
            self._closed = True

    def is_closed(self) -> bool:  # type: ignore
        return self._closed

    def __repr__(self) -> str:
        return f"File({self._path!r}, closed={self._closed})"


class ReadDir:
    __slots__ = ("_path", "_entries")

    def __init__(self, path: str | os.PathLike) -> None:
        self._path = os.fspath(path)
        self._entries: list[DirEntry] | None = None

    def _ensure_entries(self) -> list[DirEntry]:
        if self._entries is None:
            self._entries = []
            if os.path.isdir(self._path):
                for name in os.listdir(self._path):
                    entry_path = os.path.join(self._path, name)
                    self._entries.append(DirEntry(entry_path))
        return self._entries

    def __iter__(self) -> Iterator[DirEntry]:
        return iter(self._ensure_entries())

    def __next__(self) -> DirEntry:
        entries = self._ensure_entries()
        return entries.__iter__().__next__()

    def len(self) -> int:  # type: ignore
        return len(self._ensure_entries())

    def is_empty(self) -> bool:  # type: ignore
        return len(self._ensure_entries()) == 0

    def __repr__(self) -> str:
        return f"ReadDir({self._path!r})"


def _metadata_from_os(path: str) -> Metadata:
    meta = Metadata()
    try:
        st = os.stat(path, follow_symlinks=False)
        meta._is_symlink = os.path.islink(path)
        if os.path.isfile(path):
            meta._file_type = FileType(is_file=True)
        elif os.path.isdir(path):
            meta._file_type = FileType(is_dir=True)
        elif meta._is_symlink:
            meta._file_type = FileType(is_symlink=True)
        meta._size = st.st_size
        meta._modified = st.st_mtime
        meta._accessed = st.st_atime
        try:
            meta._created = st.st_birthtime
        except AttributeError:
            meta._created = None
        meta._permissions = Permissions(readonly=not (st.st_mode & 0o200))
    except (OSError, ValueError):
        pass
    return meta


class SeekFrom:
    __slots__ = ("_kind", "_offset")

    START = 0
    CURRENT = 1
    END = 2

    def __init__(self, kind: int, offset: int) -> None:
        self._kind = kind
        self._offset = offset

    @classmethod
    def start(cls, offset: int = 0) -> SeekFrom:
        return cls(cls.START, offset)

    @classmethod
    def current(cls, offset: int = 0) -> SeekFrom:
        return cls(cls.CURRENT, offset)

    @classmethod
    def end(cls, offset: int = 0) -> SeekFrom:
        return cls(cls.END, offset)

    def kind(self) -> int:
        return self._kind

    def offset(self) -> int:
        return self._offset

    def __repr__(self) -> str:
        if self._kind == self.START:
            return f"SeekFrom::Start({self._offset})"
        if self._kind == self.CURRENT:
            return f"SeekFrom::Current({self._offset})"
        return f"SeekFrom::End({self._offset})"


class Read:
    def read(self, buf: bytearray) -> int:  # type: ignore
        raise NotImplementedError

    def read_exact(self, buf: bytearray) -> None:  # type: ignore
        total = 0
        needed = len(buf)
        while total < needed:
            n = self.read(buf[total:])
            if n == 0:
                raise IOError("failed to fill whole buffer")
            total += n

    def read_to_end(self) -> bytes:  # type: ignore
        chunks = []
        while True:
            chunk = self.read(8192)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)

    def read_to_string(self) -> str:  # type: ignore
        return self.read_to_end().decode("utf-8")

    def by_ref(self) -> Any:  # type: ignore
        return self


class Write:
    def write(self, data: bytes | bytearray | str) -> int:  # type: ignore
        raise NotImplementedError

    def write_all(self, data: bytes | bytearray | str) -> None:  # type: ignore
        total = 0
        if isinstance(data, str):
            data = data.encode("utf-8")
        while total < len(data):
            n = self.write(data[total:])
            total += n

    def flush(self) -> None:  # type: ignore
        pass

    def by_ref(self) -> Any:  # type: ignore
        return self


class BufRead:
    def fill_buf(self) -> bytes:  # type: ignore
        raise NotImplementedError

    def consume(self, amt: int) -> None:  # type: ignore
        pass

    def has_consumed(self) -> bool:  # type: ignore
        return False

    def read_until(self, byte: int) -> bytes:  # type: ignore
        buf = bytearray()
        while True:
            chunk = self.fill_buf()
            if not chunk:
                break
            idx = chunk.find(bytes([byte]))
            if idx >= 0:
                buf.extend(chunk[:idx + 1])
                self.consume(idx + 1)
                return bytes(buf)
            buf.extend(chunk)
            self.consume(len(chunk))
        return bytes(buf)

    def read_line(self) -> str:  # type: ignore
        return self.read_until(ord("\n")).decode("utf-8")

    def split(self, byte: int) -> BufSplitIter:  # type: ignore
        return BufSplitIter(self, byte)

    def lines(self) -> LinesIter:  # type: ignore
        return LinesIter(self)


class BufSplitIter:
    __slots__ = ("_reader", "_byte", "_done")

    def __init__(self, reader: BufRead, byte: int) -> None:
        self._reader = reader
        self._byte = byte
        self._done = False

    def __iter__(self) -> BufSplitIter:
        return self

    def __next__(self) -> bytes:
        if self._done:
            raise StopIteration
        result = self._reader.read_until(self._byte)
        if not result:
            self._done = True
            raise StopIteration
        return result


class LinesIter:
    __slots__ = ("_reader", "_done")

    def __init__(self, reader: BufRead) -> None:
        self._reader = reader
        self._done = False

    def __iter__(self) -> LinesIter:
        return self

    def __next__(self) -> str:
        if self._done:
            raise StopIteration
        line = self._reader.read_line()
        if not line:
            self._done = True
            raise StopIteration
        return line


class Cursor(Generic[T]):
    __slots__ = ("_data", "_pos")

    def __init__(self, data: T) -> None:
        if isinstance(data, (bytes, bytearray)):
            self._data = bytearray(data)
        elif isinstance(data, str):
            self._data = bytearray(data.encode("utf-8"))
        elif isinstance(data, list):
            self._data = bytearray(data)
        else:
            self._data = bytearray(data)
        self._pos = 0

    @classmethod
    def new(cls, data: T) -> Cursor[T]:  # type: ignore
        return cls(data)

    def inner(self) -> T:
        return self._data  # type: ignore

    def into_inner(self) -> T:  # type: ignore
        return self._data  # type: ignore

    def get_ref(self) -> Any:  # type: ignore
        return self._data  # type: ignore

    def get_mut(self) -> Any:  # type: ignore
        return self._data  # type: ignore

    def position(self) -> int:
        return self._pos

    def set_position(self, pos: int) -> None:  # type: ignore
        self._pos = pos

    def position_mut(self) -> int:  # type: ignore
        return self._pos  # type: ignore

    def into_inner(self) -> T:
        return self._data  # type: ignore

    def read(self, buf: bytearray) -> int:  # type: ignore
        available = len(self._data) - self._pos
        if available <= 0:
            return 0
        n = min(len(buf), available)
        buf[:n] = self._data[self._pos:self._pos + n]
        self._pos += n
        return n

    def write(self, data: bytes | bytearray | str) -> int:  # type: ignore
        if isinstance(data, str):
            data = data.encode("utf-8")
        end = self._pos + len(data)
        if end > len(self._data):
            self._data.extend(b"\x00" * (end - len(self._data)))
        self._data[self._pos:end] = data
        self._pos += len(data)
        return len(data)

    def flush(self) -> None:  # type: ignore
        pass

    def seek(self, style: SeekFrom) -> int:  # type: ignore
        if style._kind == SeekFrom.START:
            self._pos = style._offset
        elif style._kind == SeekFrom.CURRENT:
            self._pos += style._offset
        elif style._kind == SeekFrom.END:
            self._pos = len(self._data) + style._offset
        self._pos = max(0, min(self._pos, len(self._data)))
        return self._pos

    def fill_buf(self) -> bytes:  # type: ignore
        return bytes(self._data[self._pos:])

    def consume(self, amt: int) -> None:  # type: ignore
        self._pos = min(self._pos + amt, len(self._data))

    def has_consumed(self) -> bool:  # type: ignore
        return self._pos >= len(self._data)

    def read_until(self, byte: int) -> bytes:  # type: ignore
        chunk = self.fill_buf()
        idx = chunk.find(bytes([byte]))
        if idx >= 0:
            result = chunk[:idx + 1]
            self.consume(idx + 1)
            return result
        self.consume(len(chunk))
        return chunk

    def read_line(self) -> str:  # type: ignore
        return self.read_until(ord("\n")).decode("utf-8")

    def remaining(self) -> int:
        return max(0, len(self._data) - self._pos)

    def is_empty(self) -> bool:
        return self._pos >= len(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"Cursor(pos={self._pos}, len={len(self._data)})"


class BufReader:
    __slots__ = ("_inner", "_buffer", "_pos", "_capacity")

    def __init__(self, inner: Any, capacity: int = 8192) -> None:
        self._inner = inner
        self._buffer = bytearray()
        self._pos = 0
        self._capacity = capacity

    @classmethod
    def with_capacity(cls, capacity: int, inner: Any) -> BufReader:  # type: ignore
        return cls(inner, capacity)

    def inner(self) -> Any:
        return self._inner

    def into_inner(self) -> Any:  # type: ignore
        return self._inner

    def buffer(self) -> bytes:  # type: ignore
        return bytes(self._buffer[self._pos:])

    def capacity(self) -> int:
        return self._capacity

    def set_capacity(self, capacity: int) -> None:  # type: ignore
        self._capacity = capacity

    def fill_buf(self) -> bytes:  # type: ignore
        if self._pos >= len(self._buffer):
            self._buffer = bytearray()
            self._pos = 0
            read_buf = bytearray(self._capacity)
            n = self._inner.read(read_buf)
            self._buffer = bytearray(read_buf[:n])
        return bytes(self._buffer[self._pos:])

    def consume(self, amt: int) -> None:  # type: ignore
        self._pos = min(self._pos + amt, len(self._buffer))

    def has_consumed(self) -> bool:
        return self._pos >= len(self._buffer)

    def read(self, buf: bytearray) -> int:  # type: ignore
        buffered = self.fill_buf()
        if not buffered:
            return self._inner.read(buf)  # type: ignore
        n = min(len(buf), len(buffered))
        buf[:n] = buffered[:n]
        self.consume(n)
        return n

    def read_exact(self, buf: bytearray) -> None:  # type: ignore
        total = 0
        needed = len(buf)
        while total < needed:
            n = self.read(buf[total:])
            if n == 0:
                raise IOError("failed to fill whole buffer")
            total += n

    def read_to_end(self) -> bytes:  # type: ignore
        chunks = [bytes(self._buffer[self._pos:])]
        self._buffer = bytearray()
        self._pos = 0
        while True:
            read_buf = bytearray(8192)
            n = self._inner.read(read_buf)
            if n == 0:
                break
            chunks.append(bytes(read_buf[:n]))
        return b"".join(chunks)

    def read_to_string(self) -> str:  # type: ignore
        return self.read_to_end().decode("utf-8")

    def read_until(self, byte: int) -> bytes:  # type: ignore
        buf = bytearray()
        while True:
            chunk = self.fill_buf()
            if not chunk:
                rest = self._inner.read_until(byte)  # type: ignore
                buf.extend(rest)
                return bytes(buf)
            idx = chunk.find(bytes([byte]))
            if idx >= 0:
                buf.extend(chunk[:idx + 1])
                self.consume(idx + 1)
                return bytes(buf)
            buf.extend(chunk)
            self.consume(len(chunk))

    def read_line(self) -> str:  # type: ignore
        return self.read_until(ord("\n")).decode("utf-8")

    def split(self, byte: int) -> BufSplitIter:  # type: ignore
        return BufSplitIter(self, byte)

    def lines(self) -> LinesIter:  # type: ignore
        return LinesIter(self)

    def seek(self, style: SeekFrom) -> int:  # type: ignore
        if hasattr(self._inner, 'seek'):
            self._buffer = bytearray()
            self._pos = 0
            return self._inner.seek(style)  # type: ignore
        raise IOError("underlying stream is not seekable")

    def __enter__(self) -> BufReader:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        return f"BufReader(buffered={len(self._buffer) - self._pos})"


class BufWriter:
    __slots__ = ("_inner", "_buffer", "_pos", "_closed", "_capacity")

    def __init__(self, inner: Any, capacity: int = 8192) -> None:
        self._inner = inner
        self._buffer = bytearray()
        self._pos = 0
        self._capacity = capacity
        self._closed = False

    @classmethod
    def with_capacity(cls, capacity: int, inner: Any) -> BufWriter:  # type: ignore
        return cls(inner, capacity)

    def inner(self) -> Any:
        return self._inner

    def into_inner(self) -> Any:  # type: ignore
        self.flush()
        return self._inner

    def buffer(self) -> bytes:  # type: ignore
        return bytes(self._buffer[self._pos:])

    def capacity(self) -> int:
        return self._capacity

    def write(self, data: bytes | bytearray | str) -> int:  # type: ignore
        if isinstance(data, str):
            data = data.encode("utf-8")
        if len(data) > self._capacity:
            self.flush()
            return self._inner.write(data)  # type: ignore
        if len(self._buffer) + len(data) > self._capacity:
            self.flush()
        self._buffer.extend(data)
        return len(data)

    def write_all(self, data: bytes | bytearray | str) -> None:  # type: ignore
        self.write(data)

    def flush(self) -> None:  # type: ignore
        if self._buffer:
            self._inner.write(bytes(self._buffer))  # type: ignore
            if hasattr(self._inner, 'flush'):
                self._inner.flush()
            self._buffer = bytearray()
            self._pos = 0

    def write_fmt(self, args: Any) -> None:  # type: ignore
        self.write(str(args))

    def seek(self, style: SeekFrom) -> int:  # type: ignore
        self.flush()
        if hasattr(self._inner, 'seek'):
            return self._inner.seek(style)  # type: ignore
        raise IOError("underlying stream is not seekable")

    def into_raw_fd(self) -> None:  # type: ignore
        self.flush()

    def __enter__(self) -> BufWriter:
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        self.flush()

    def __del__(self) -> None:
        try:
            self.flush()
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"BufWriter(buffered={len(self._buffer)})"


class Shutdown:
    __slots__ = ("_kind",)

    READ = 0
    WRITE = 1
    BOTH = 2

    def __init__(self, kind: int) -> None:
        self._kind = kind

    @classmethod
    def read(cls) -> Shutdown:
        return cls(cls.READ)

    @classmethod
    def write(cls) -> Shutdown:
        return cls(cls.WRITE)

    @classmethod
    def both(cls) -> Shutdown:
        return cls(cls.BOTH)

    def kind(self) -> int:
        return self._kind

    def __repr__(self) -> str:
        if self._kind == self.READ:
            return "Shutdown::Read"
        if self._kind == self.WRITE:
            return "Shutdown::Write"
        return "Shutdown::Both"


class Ipv4Addr:
    __slots__ = ("_octets",)

    def __init__(self, a: int = 0, b: int = 0, c: int = 0, d: int = 0) -> None:
        self._octets = (a, b, c, d)

    @classmethod
    def new(cls, a: int, b: int, c: int, d: int) -> Ipv4Addr:  # type: ignore
        return cls(a, b, c, d)

    @classmethod
    def from_str(cls, s: str) -> Ipv4Addr:  # type: ignore
        parts = s.split(".")
        if len(parts) != 4:
            raise ValueError(f"invalid IPv4 address: {s}")
        return cls(*[int(p) for p in parts])

    @classmethod
    def from_bytes(cls, bytes: bytes | bytearray) -> Ipv4Addr:  # type: ignore
        if len(bytes) != 4:
            raise ValueError("IPv4 address must be 4 bytes")
        return cls(bytes[0], bytes[1], bytes[2], bytes[3])

    @classmethod
    def localhost(cls) -> Ipv4Addr:  # type: ignore
        return cls(127, 0, 0, 1)

    @classmethod
    def unspecified(cls) -> Ipv4Addr:  # type: ignore
        return cls(0, 0, 0, 0)

    @classmethod
    def broadcast(cls) -> Ipv4Addr:  # type: ignore
        return cls(255, 255, 255, 255)

    @classmethod
    def loopback(cls) -> Ipv4Addr:  # type: ignore
        return cls(127, 0, 0, 1)

    def octets(self) -> tuple[int, int, int, int]:
        return self._octets

    def to_str(self) -> str:  # type: ignore
        return ".".join(str(o) for o in self._octets)

    def to_bytes(self) -> bytes:  # type: ignore
        return bytes(self._octets)

    def is_loopback(self) -> bool:  # type: ignore
        return self._octets[0] == 127

    def is_unspecified(self) -> bool:  # type: ignore
        return self._octets == (0, 0, 0, 0)

    def is_broadcast(self) -> bool:  # type: ignore
        return self._octets == (255, 255, 255, 255)

    def is_multicast(self) -> bool:  # type: ignore
        return (self._octets[0] & 0xF0) == 0xE0

    def is_private(self) -> bool:  # type: ignore
        return (
            self._octets[0] == 10
            or (self._octets[0] == 172 and 16 <= self._octets[1] <= 31)
            or (self._octets[0] == 192 and self._octets[1] == 168)
        )

    def is_link_local(self) -> bool:  # type: ignore
        return self._octets[0] == 169 and self._octets[1] == 254

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ipv4Addr):
            return self._octets == other._octets
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Ipv4Addr):
            return self._octets != other._octets
        return NotImplemented

    def __lt__(self, other: Ipv4Addr) -> bool:
        if isinstance(other, Ipv4Addr):
            return self._octets < other._octets
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._octets)

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"Ipv4Addr({self.to_str()!r})"


class Ipv6Addr:
    __slots__ = ("_segments",)

    def __init__(self, *segments: int) -> None:
        if len(segments) == 0:
            self._segments = (0,) * 8
        elif len(segments) == 8:
            self._segments = tuple(segments)
        else:
            raise ValueError("IPv6 address must have 0 or 8 segments")

    @classmethod
    def new(cls, a: int, b: int, c: int, d: int, e: int, f: int, g: int, h: int) -> Ipv6Addr:  # type: ignore
        return cls(a, b, c, d, e, f, g, h)

    @classmethod
    def from_str(cls, s: str) -> Ipv6Addr:  # type: ignore
        import ipaddress
        addr = ipaddress.IPv6Address(s)
        b = addr.packed
        segments = []
        for i in range(0, 16, 2):
            segments.append((b[i] << 8) | b[i + 1])
        return cls(*segments)

    @classmethod
    def from_bytes(cls, data: bytes | bytearray) -> Ipv6Addr:  # type: ignore
        if len(data) != 16:
            raise ValueError("IPv6 address must be 16 bytes")
        segments = []
        for i in range(0, 16, 2):
            segments.append((data[i] << 8) | data[i + 1])
        return cls(*segments)

    @classmethod
    def localhost(cls) -> Ipv6Addr:  # type: ignore
        return cls(0, 0, 0, 0, 0, 0, 0, 1)

    @classmethod
    def unspecified(cls) -> Ipv6Addr:  # type: ignore
        return cls(0, 0, 0, 0, 0, 0, 0, 0)

    @classmethod
    def loopback(cls) -> Ipv6Addr:  # type: ignore
        return cls(0, 0, 0, 0, 0, 0, 0, 1)

    @classmethod
    def multicast(cls, scope: int = 2) -> Ipv6Addr:  # type: ignore
        return cls(0xFF00 | scope, 0, 0, 0, 0, 0, 0, 0)

    @classmethod
    def link_local(cls) -> Ipv6Addr:  # type: ignore
        return cls(0xFE80, 0, 0, 0, 0, 0, 0, 0x0001)

    def segments(self) -> tuple[int, ...]:
        return self._segments

    def to_str(self) -> str:  # type: ignore
        import ipaddress
        b = bytearray(16)
        for i, seg in enumerate(self._segments):
            b[i * 2] = seg >> 8
            b[i * 2 + 1] = seg & 0xFF
        return str(ipaddress.IPv6Address(bytes(b)))

    def to_bytes(self) -> bytes:  # type: ignore
        b = bytearray(16)
        for i, seg in enumerate(self._segments):
            b[i * 2] = seg >> 8
            b[i * 2 + 1] = seg & 0xFF
        return bytes(b)

    def is_loopback(self) -> bool:  # type: ignore
        return self._segments == (0, 0, 0, 0, 0, 0, 0, 1)

    def is_unspecified(self) -> bool:  # type: ignore
        return self._segments == (0, 0, 0, 0, 0, 0, 0, 0)

    def is_multicast(self) -> bool:  # type: ignore
        return (self._segments[0] & 0xFF00) == 0xFF00

    def is_unicast_link_local(self) -> bool:  # type: ignore
        return (self._segments[0] & 0xFFC0) == 0xFE80

    def to_ipv4_mapped(self) -> Ipv4Addr:  # type: ignore
        if self._segments[0] == 0 and self._segments[1] == 0 and self._segments[2] == 0 and self._segments[3] == 0 and self._segments[4] == 0:
            return Ipv4Addr(
                (self._segments[6] >> 8) & 0xFF,
                self._segments[6] & 0xFF,
                (self._segments[7] >> 8) & 0xFF,
                self._segments[7] & 0xFF,
            )
        raise ValueError("not an IPv4-mapped address")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ipv6Addr):
            return self._segments == other._segments
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Ipv6Addr):
            return self._segments != other._segments
        return NotImplemented

    def __lt__(self, other: Ipv6Addr) -> bool:
        if isinstance(other, Ipv6Addr):
            return self._segments < other._segments
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._segments)

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"Ipv6Addr({self.to_str()!r})"


class IpAddr:
    __slots__ = ("_v4", "_v6")

    def __init__(self, v4: Ipv4Addr | None = None, v6: Ipv6Addr | None = None) -> None:
        if v4 is not None and v6 is not None:
            raise ValueError("IpAddr cannot be both v4 and v6")
        self._v4 = v4
        self._v6 = v6

    @classmethod
    def v4(cls, addr: Ipv4Addr) -> IpAddr:
        return cls(v4=addr)

    @classmethod
    def v6(cls, addr: Ipv6Addr) -> IpAddr:
        return cls(v6=addr)

    @classmethod
    def from_str(cls, s: str) -> IpAddr:
        try:
            return cls.v4(Ipv4Addr.from_str(s))
        except ValueError:
            pass
        return cls.v6(Ipv6Addr.from_str(s))

    def is_ipv4(self) -> bool:  # type: ignore
        return self._v4 is not None

    def is_ipv6(self) -> bool:  # type: ignore
        return self._v6 is not None

    def as_ipv4(self) -> Ipv4Addr | None:
        return self._v4

    def as_ipv6(self) -> Ipv6Addr | None:  # type: ignore
        return self._v6

    def to_ipv4(self) -> Ipv4Addr | None:  # type: ignore
        return self._v4

    def to_ipv6(self) -> Ipv6Addr | None:  # type: ignore
        return self._v6

    def is_loopback(self) -> bool:  # type: ignore
        if self._v4:
            return self._v4.is_loopback()
        if self._v6:
            return self._v6.is_loopback()
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IpAddr):
            return self._v4 == other._v4 and self._v6 == other._v6
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, IpAddr):
            return self._v4 != other._v4 or self._v6 != other._v6
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._v4, self._v6))

    def __str__(self) -> str:
        if self._v4:
            return str(self._v4)
        return str(self._v6)

    def __repr__(self) -> str:
        if self._v4:
            return f"IpAddr::V4({self._v4!r})"
        return f"IpAddr::V6({self._v6!r})"


class SocketAddr:
    __slots__ = ("_ip", "_port")

    def __init__(self, ip: IpAddr, port: int) -> None:
        self._ip = ip
        self._port = port

    @classmethod
    def new(cls, ip: IpAddr, port: int) -> SocketAddr:
        return cls(ip, port)

    @classmethod
    def from_str(cls, s: str) -> SocketAddr:
        if s.startswith("["):
            bracket = s.find("]")
            if bracket < 0:
                raise ValueError(f"invalid socket address: {s}")
            ip_str = s[1:bracket]
            rest = s[bracket + 1:]
            if not rest.startswith(":"):
                raise ValueError(f"invalid socket address: {s}")
            port = int(rest[1:])
            return cls(IpAddr.v6(Ipv6Addr.from_str(ip_str)), port)
        colon = s.rfind(":")
        if colon < 0:
            raise ValueError(f"invalid socket address: {s}")
        ip_str = s[:colon]
        port = int(s[colon + 1:])
        return cls(IpAddr.from_str(ip_str), port)

    @classmethod
    def new_v4(cls, ip: Ipv4Addr, port: int) -> SocketAddr:
        return cls(IpAddr.v4(ip), port)

    @classmethod
    def new_v6(cls, ip: Ipv6Addr, port: int) -> SocketAddr:
        return cls(IpAddr.v6(ip), port)

    def ip(self) -> IpAddr:  # type: ignore
        return self._ip

    def port(self) -> int:
        return self._port

    def is_ipv4(self) -> bool:  # type: ignore
        return self._ip.is_ipv4()

    def is_ipv6(self) -> bool:  # type: ignore
        return self._ip.is_ipv6()

    def set_ip(self, ip: IpAddr) -> None:
        self._ip = ip

    def set_port(self, port: int) -> None:  # type: ignore
        self._port = port

    def to_socket_addr(self) -> tuple[str, int]:  # type: ignore
        return (str(self._ip), self._port)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SocketAddr):
            return self._ip == other._ip and self._port == other._port
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, SocketAddr):
            return self._ip != other._ip or self._port != other._port
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._ip, self._port))

    def __str__(self) -> str:
        if self._ip.is_ipv6():
            return f"[{self._ip}]:{self._port}"
        return f"{self._ip}:{self._port}"

    def __repr__(self) -> str:
        return f"SocketAddr({self})"


class TcpStream:
    __slots__ = ("_stream", "_addr")

    def __init__(self, stream: Any, addr: SocketAddr | None = None) -> None:
        self._stream = stream
        self._addr = addr

    @classmethod
    def connect(cls, addr: SocketAddr) -> TcpStream:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_STREAM,
        )
        sock.connect(addr.to_socket_addr())
        sock.setblocking(True)
        return TcpStream(sock, addr)

    @classmethod
    def connect_timeout(cls, addr: SocketAddr, timeout: float) -> TcpStream:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_STREAM,
        )
        sock.settimeout(timeout)
        sock.connect(addr.to_socket_addr())
        sock.setblocking(True)
        return TcpStream(sock, addr)

    @classmethod
    def from_stream(cls, stream: Any, addr: SocketAddr | None = None) -> TcpStream:
        return TcpStream(stream, addr)

    def peer_addr(self) -> SocketAddr | None:  # type: ignore
        if self._addr:
            return self._addr
        if self._stream:
            try:
                addr = self._stream.getpeername()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def local_addr(self) -> SocketAddr | None:  # type: ignore
        if self._stream:
            try:
                addr = self._stream.getsockname()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def shutdown(self, how: Shutdown) -> None:  # type: ignore
        import socket
        if not self._stream:
            return
        if how.kind() == Shutdown.READ:
            self._stream.shutdown(socket.SHUT_RD)
        elif how.kind() == Shutdown.WRITE:
            self._stream.shutdown(socket.SHUT_WR)
        else:
            self._stream.shutdown(socket.SHUT_RDWR)

    def set_nodelay(self, nodelay: bool) -> None:  # type: ignore
        if self._stream:
            self._stream.setsockopt(
                __import__('socket').IPPROTO_TCP,
                __import__('socket').TCP_NODELAY,
                1 if nodelay else 0,
            )

    def set_nonblocking(self, nonblocking: bool) -> None:  # type: ignore
        if self._stream:
            self._stream.setblocking(not nonblocking)

    def set_read_timeout(self, dur: float | None) -> None:  # type: ignore
        if self._stream:
            self._stream.settimeout(dur)

    def set_write_timeout(self, dur: float | None) -> None:  # type: ignore
        if self._stream:
            self._stream.settimeout(dur)

    def read(self, buf: bytearray) -> int:  # type: ignore
        return self._stream.recv_into(buf)  # type: ignore

    def write(self, data: bytes | bytearray) -> int:  # type: ignore
        return self._stream.send(data)  # type: ignore

    def write_all(self, data: bytes | bytearray) -> None:  # type: ignore
        total = 0
        while total < len(data):
            n = self._stream.send(data[total:])  # type: ignore
            total += n

    def try_clone(self) -> TcpStream:  # type: ignore
        import socket
        new_sock = socket.dup(self._stream)  # type: ignore
        return TcpStream(new_sock, self._addr)

    def into_inner(self) -> Any:  # type: ignore
        return self._stream

    def as_raw_fd(self) -> Any:  # type: ignore
        return self._stream

    def __enter__(self) -> TcpStream:
        return self

    def __exit__(self, *_: Any) -> None:
        try:
            self._stream.close()
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"TcpStream({self._addr})"


class TcpListener:
    __slots__ = ("_listener", "_addr")

    def __init__(self, listener: Any, addr: SocketAddr | None = None) -> None:
        self._listener = listener
        self._addr = addr

    @classmethod
    def bind(cls, addr: SocketAddr) -> TcpListener:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_STREAM,
        )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr.to_socket_addr())
        sock.listen(128)
        return TcpListener(sock, addr)

    @classmethod
    def from_std(cls, listener: Any, addr: SocketAddr | None = None) -> TcpListener:
        return TcpListener(listener, addr)

    def local_addr(self) -> SocketAddr | None:  # type: ignore
        if self._listener:
            try:
                addr = self._listener.getsockname()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def accept(self) -> tuple[TcpStream, SocketAddr]:  # type: ignore
        conn, addr = self._listener.accept()  # type: ignore
        sock_addr = SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
        return TcpStream(conn, sock_addr), sock_addr

    def accept_timeout(self, timeout: float) -> tuple[TcpStream, SocketAddr] | None:  # type: ignore
        import socket
        self._listener.settimeout(timeout)  # type: ignore
        try:
            return self.accept()
        except socket.timeout:
            return None
        finally:
            self._listener.setblocking(True)  # type: ignore

    def incoming(self) -> Incoming:  # type: ignore
        return Incoming(self)

    def set_nonblocking(self, nonblocking: bool) -> None:  # type: ignore
        if self._listener:
            self._listener.setblocking(not nonblocking)

    def into_inner(self) -> Any:  # type: ignore
        return self._listener

    def __enter__(self) -> TcpListener:
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        pass

    def __repr__(self) -> str:
        return f"TcpListener({self._addr})"


class Incoming:
    __slots__ = ("_listener", "_done")

    def __init__(self, listener: TcpListener) -> None:
        self._listener = listener
        self._done = False

    def __iter__(self) -> Incoming:
        return self

    def __next__(self) -> TcpStream:
        if self._done:
            raise StopIteration
        try:
            conn, _ = self._listener.accept()
            return conn
        except Exception:
            self._done = True
            raise StopIteration


class UdpSocket:
    __slots__ = ("_socket", "_addr")

    def __init__(self, sock: Any, addr: SocketAddr | None = None) -> None:
        self._socket = sock
        self._addr = addr

    @classmethod
    def bind(cls, addr: SocketAddr) -> UdpSocket:
        import socket
        sock = socket.socket(
            socket.AF_INET if addr.is_ipv4() else socket.AF_INET6,
            socket.SOCK_DGRAM,
        )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addr.to_socket_addr())
        return UdpSocket(sock, addr)

    @classmethod
    def from_std(cls, socket: Any, addr: SocketAddr | None = None) -> UdpSocket:
        return UdpSocket(socket, addr)

    def local_addr(self) -> SocketAddr | None:  # type: ignore
        if self._socket:
            try:
                addr = self._socket.getsockname()
                return SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
            except Exception:
                pass
        return None

    def send_to(self, buf: bytes | bytearray, target: SocketAddr) -> int:  # type: ignore
        return self._socket.sendto(buf, target.to_socket_addr())  # type: ignore

    def recv_from(self, buf_size: int) -> tuple[bytes, SocketAddr]:  # type: ignore
        data, addr = self._socket.recvfrom(buf_size)  # type: ignore
        sock_addr = SocketAddr.from_str(f"{addr[0]}:{addr[1]}")
        return data, sock_addr

    def recv(self, buf_size: int) -> bytes:  # type: ignore
        return self._socket.recv(buf_size)  # type: ignore

    def send(self, data: bytes | bytearray) -> int:  # type: ignore
        return self._socket.send(data)  # type: ignore

    def connect(self, addr: SocketAddr) -> None:  # type: ignore
        self._socket.connect(addr.to_socket_addr())  # type: ignore
        self._addr = addr

    def set_broadcast(self, on: bool) -> None:  # type: ignore
        self._socket.setsockopt(
            __import__('socket').SOL_SOCKET,
            __import__('socket').SO_BROADCAST,
            1 if on else 0,
        )

    def set_nonblocking(self, nonblocking: bool) -> None:  # type: ignore
        self._socket.setblocking(not nonblocking)

    def set_read_timeout(self, dur: float | None) -> None:  # type: ignore
        self._socket.settimeout(dur)

    def set_ttl(self, ttl: int) -> None:  # type: ignore
        import socket
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    def take_error(self) -> Exception | None:  # type: ignore
        try:
            err = self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            if err != 0:
                return OSError(err, os.strerror(err))
        except Exception:
            pass
        return None

    def into_inner(self) -> Any:  # type: ignore
        return self._socket

    def __enter__(self) -> UdpSocket:
        return self

    def __exit__(self, *_: Any) -> None:  # type: ignore
        pass

    def __repr__(self) -> str:
        return f"UdpSocket({self._addr})"


class Ordering:
    __slots__ = ("_kind",)

    LESS = -1
    EQUAL = 0
    GREATER = 1

    def __init__(self, kind: int) -> None:
        self._kind = kind

    @classmethod
    def less(cls) -> Ordering:
        return cls(cls.LESS)

    @classmethod
    def equal(cls) -> Ordering:
        return cls(cls.EQUAL)

    @classmethod
    def greater(cls) -> Ordering:
        return cls(cls.GREATER)

    @classmethod
    def from_cmp(cls, a: Any, b: Any) -> Ordering:  # type: ignore
        if a < b:
            return cls(cls.LESS)
        if a > b:
            return cls(cls.GREATER)
        return cls(cls.EQUAL)

    def reverse(self) -> Ordering:
        return Ordering(-self._kind)

    def then(self, other: Ordering) -> Ordering:  # type: ignore
        if self._kind != 0:
            return self
        return other

    def then_with(self, f: Callable[[], Ordering]) -> Ordering:  # type: ignore
        if self._kind != 0:
            return self
        return f()

    def is_less(self) -> bool:  # type: ignore
        return self._kind < 0

    def is_equal(self) -> bool:  # type: ignore
        return self._kind == 0

    def is_greater(self) -> bool:  # type: ignore
        return self._kind > 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ordering):
            return self._kind == other._kind
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Ordering):
            return self._kind != other._kind
        return NotImplemented

    def __lt__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind < other._kind
        return NotImplemented

    def __le__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind <= other._kind
        return NotImplemented

    def __gt__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind > other._kind
        return NotImplemented

    def __ge__(self, other: Ordering) -> bool:
        if isinstance(other, Ordering):
            return self._kind >= other._kind
        return NotImplemented

    def __hash__(self) -> int:
        return self._kind

    def __repr__(self) -> str:
        if self._kind < 0:
            return "Ordering::Less"
        if self._kind == 0:
            return "Ordering::Equal"
        return "Ordering::Greater"


class ControlFlow:
    __slots__ = ("_break", "_value", "_is_break")

    def __init__(self, is_break: bool = False, value: Any = None) -> None:
        self._is_break = is_break
        self._value = value

    @classmethod
    def cont(cls, value: Any = None) -> ControlFlow:
        return cls(False, value)

    @classmethod
    def brk(cls, value: Any = None) -> ControlFlow:
        return cls(True, value)

    def is_break(self) -> bool:  # type: ignore
        return self._is_break

    def is_continue(self) -> bool:  # type: ignore
        return not self._is_break

    def break_value(self) -> Any | None:  # type: ignore
        if self._is_break:
            return self._value
        return None

    def continue_value(self) -> Any | None:  # type: ignore
        if not self._is_break:
            return self._value
        return None

    def map_break(self, f: Callable[[Any], Any]) -> ControlFlow:  # type: ignore
        if self._is_break:
            return ControlFlow(True, f(self._value))
        return self

    def map_continue(self, f: Callable[[Any], Any]) -> ControlFlow:  # type: ignore
        if not self._is_break:
            return ControlFlow(False, f(self._value))
        return self

    def __repr__(self) -> str:
        if self._is_break:
            return f"ControlFlow::Break({self._value!r})"
        return f"ControlFlow::Continue({self._value!r})"


class Reverse(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def into_inner(self) -> T:  # type: ignore
        return self._value

    def as_ref(self) -> Any:  # type: ignore
        return self._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Reverse):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Reverse):
            return self._value != other._value
        return NotImplemented

    def __lt__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value < self._value
        return NotImplemented

    def __le__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value <= self._value
        return NotImplemented

    def __gt__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value > self._value
        return NotImplemented

    def __ge__(self, other: Reverse) -> bool:
        if isinstance(other, Reverse):
            return other._value >= self._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Reverse({self._value!r})"


class Wrapping(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def new(val: T) -> Wrapping[T]:
        return Wrapping(val)

    def into_inner(self) -> T:
        return self._value

    def wrapping_add(self, other: T) -> Wrapping[T]:
        return Wrapping((int(self._value) + int(other)) & 0xFFFFFFFF)

    def wrapping_sub(self, other: T) -> Wrapping[T]:
        return Wrapping((int(self._value) - int(other)) & 0xFFFFFFFF)

    def wrapping_mul(self, other: T) -> Wrapping[T]:
        return Wrapping((int(self._value) * int(other)) & 0xFFFFFFFF)

    def wrapping_div(self, other: T) -> Wrapping[T]:  # type: ignore
        if int(other) == 0:
            return Wrapping(0)
        return Wrapping((int(self._value) // int(other)) & 0xFFFFFFFF)

    def wrapping_neg(self) -> Wrapping[int]:  # type: ignore
        return Wrapping((-int(self._value)) & 0xFFFFFFFF)

    def __add__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_add(other._value)
        return self.wrapping_add(other)

    def __sub__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_sub(other._value)
        return self.wrapping_sub(other)

    def __mul__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_mul(other._value)
        return self.wrapping_mul(other)

    def __floordiv__(self, other: Wrapping | int) -> Wrapping:
        if isinstance(other, Wrapping):
            return self.wrapping_div(other._value)
        return self.wrapping_div(other)

    def __neg__(self) -> Wrapping:
        return self.wrapping_neg()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Wrapping):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Wrapping({self._value})"


class Saturating(Generic[T]):
    __slots__ = ("_value",)

    MAX = 2**31 - 1
    MIN = -(2**31)

    def __init__(self, value: T) -> None:
        self._value = value

    def new(val: T) -> Saturating[T]:
        return Saturating(val)

    def into_inner(self) -> T:
        return self._value

    def saturating_add(self, other: T) -> Saturating[T]:
        result = int(self._value) + int(other)
        return Saturating(max(self.MIN, min(self.MAX, result)))

    def saturating_sub(self, other: T) -> Saturating[T]:
        result = int(self._value) - int(other)
        return Saturating(max(self.MIN, min(self.MAX, result)))

    def saturating_mul(self, other: T) -> Saturating[T]:
        result = int(self._value) * int(other)
        return Saturating(max(self.MIN, min(self.MAX, result)))

    def __add__(self, other: Saturating | int) -> Saturating:
        if isinstance(other, Saturating):
            return self.saturating_add(other._value)
        return self.saturating_add(other)

    def __sub__(self, other: Saturating | int) -> Saturating:
        if isinstance(other, Saturating):
            return self.saturating_sub(other._value)
        return self.saturating_sub(other)

    def __mul__(self, other: Saturating | int) -> Saturating:
        if isinstance(other, Saturating):
            return self.saturating_mul(other._value)
        return self.saturating_mul(other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Saturating):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"Saturating({self._value})"


class NonZero(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        if value == 0:
            raise ValueError("NonZero cannot be zero")
        self._value = value

    @classmethod
    def new(cls, value: T) -> NonZero[T]:  # type: ignore
        return cls(value)

    @classmethod
    def try_new(cls, value: T) -> NonZero[T] | None:  # type: ignore
        if value == 0:
            return None
        return cls(value)

    @classmethod
    def from_unsigned(cls, value: int) -> NonZero[int]:  # type: ignore
        if value <= 0:
            raise ValueError("value must be positive")
        return cls(value)

    def get(self) -> T:
        return self._value

    def checked_add(self, other: int) -> NonZero[T] | None:  # type: ignore
        result = int(self._value) + other
        if result == 0:
            return None
        return NonZero(result)

    def checked_sub(self, other: int) -> NonZero[T] | None:  # type: ignore
        result = int(self._value) - other
        if result == 0:
            return None
        return NonZero(result)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NonZero):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, NonZero):
            return self._value != other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"NonZero({self._value})"


class ExitCode:
    __slots__ = ("_code",)

    def __init__(self, code: int = 0) -> None:
        self._code = code

    @classmethod
    def success(cls) -> ExitCode:
        return cls(0)

    @classmethod
    def from_raw(cls, code: int) -> ExitCode:  # type: ignore
        return cls(code)

    def code(self) -> int:  # type: ignore
        return self._code

    def is_success(self) -> bool:
        return self._code == 0

    def __repr__(self) -> str:
        return f"ExitCode({self._code})"


class Location:
    __slots__ = ("_file", "_line", "_column")

    def __init__(self, file: str = "", line: int = 0, column: int = 0) -> None:
        self._file = file
        self._line = line
        self._column = column

    def file(self) -> str:  # type: ignore
        return self._file

    def line(self) -> int:  # type: ignore
        return self._line

    def column(self) -> int:  # type: ignore
        return self._column

    def __str__(self) -> str:
        return f"{self._file}:{self._line}:{self._column}"

    def __repr__(self) -> str:
        return f"Location({self._file!r}, {self._line}, {self._column})"


class Backtrace:
    __slots__ = ("_frames", "_formatted")

    def __init__(self) -> None:
        self._frames = traceback.extract_stack()
        self._formatted = "".join(traceback.format_stack())

    def __str__(self) -> str:
        return self._formatted

    def __repr__(self) -> str:
        return f"Backtrace({len(self._frames)} frames)"

    def frames(self) -> list:  # type: ignore
        return self._frames


class Error(Exception):
    __slots__ = ("_message", "_source", "_backtrace", "_location", "_context")

    def __init__(self, message: str = "", source: Exception | None = None) -> None:
        super().__init__(message)
        self._message = message
        self._source = source
        self._backtrace: Backtrace | None = None
        self._location: Location | None = None
        self._context: str | None = None

    @classmethod
    def new(cls, message: str) -> Error:  # type: ignore
        return cls(message)

    @classmethod
    def from_source(cls, source: Exception) -> Error:  # type: ignore
        return cls(str(source), source)

    def message(self) -> str:  # type: ignore
        return self._message

    def source(self) -> Exception | None:  # type: ignore
        return self._source

    def backtrace(self) -> Backtrace:  # type: ignore
        if self._backtrace is None:
            self._backtrace = Backtrace()
        return self._backtrace

    def location(self) -> Location | None:  # type: ignore
        return self._location

    def with_context(self, ctx: str) -> Error:  # type: ignore
        self._context = ctx
        return self

    def context(self) -> str | None:  # type: ignore
        return self._context

    def with_source(self, source: Exception) -> Error:  # type: ignore
        self._source = source
        return self

    def __str__(self) -> str:
        parts = [self._message]
        if self._context:
            parts.append(f"context: {self._context}")
        if self._source:
            parts.append(f"source: {self._source}")
        return ": ".join(parts)


def context(msg: str, err: Exception) -> Error:
    e = Error(msg)
    e._source = err
    e._context = msg
    e._backtrace = Backtrace()
    return e


class Stdio:
    __slots__ = ("_kind", "_file")

    INHERIT = 0
    PIPED = 1
    NULL = 2
    FILE = 3

    def __init__(self, kind: int = INHERIT, file: str | None = None) -> None:
        self._kind = kind
        self._file = file

    @classmethod
    def inherit(cls) -> Stdio:
        return cls(cls.INHERIT)

    @classmethod
    def piped(cls) -> Stdio:
        return cls(cls.PIPED)

    @classmethod
    def null(cls) -> Stdio:
        return cls(cls.NULL)

    @classmethod
    def from_path(cls, path: str | Path) -> Stdio:  # type: ignore
        path_str = path.as_str() if isinstance(path, Path) else str(path)
        return cls(cls.FILE, path_str)

    def kind(self) -> int:
        return self._kind

    def __repr__(self) -> str:
        if self._kind == self.INHERIT:
            return "Stdio::Inherit"
        if self._kind == self.PIPED:
            return "Stdio::Piped"
        if self._kind == self.NULL:
            return "Stdio::Null"
        return f"Stdio::File({self._file!r})"


class ExitStatus:
    __slots__ = ("_code", "_success")

    def __init__(self, code: int) -> None:
        self._code = code
        self._success = code == 0

    def code(self) -> int:  # type: ignore
        return self._code

    def success(self) -> bool:  # type: ignore
        return self._success

    def signal(self) -> int | None:  # type: ignore
        if self._code < 0:
            return -self._code
        return None

    def __repr__(self) -> str:
        return f"ExitStatus(code={self._code})"

    def __bool__(self) -> bool:
        return self._success


class Output:
    __slots__ = ("_status", "_stdout", "_stderr")

    def __init__(self, status: ExitStatus, stdout: bytes = b"", stderr: bytes = b"") -> None:
        self._status = status
        self._stdout = stdout
        self._stderr = stderr

    def status(self) -> ExitStatus:  # type: ignore
        return self._status

    def stdout(self) -> bytes:  # type: ignore
        return self._stdout

    def stderr(self) -> bytes:  # type: ignore
        return self._stderr

    def stdout_str(self) -> str:  # type: ignore
        return self._stdout.decode("utf-8", errors="replace")

    def stderr_str(self) -> str:  # type: ignore
        return self._stderr.decode("utf-8", errors="replace")

    def __repr__(self) -> str:
        return f"Output(status={self._status})"


class Child:
    __slots__ = ("_process", "_pid")

    def __init__(self, process: Any) -> None:
        self._process = process
        self._pid = process.pid

    def id(self) -> int:  # type: ignore
        return self._pid

    def kill(self) -> None:  # type: ignore
        self._process.kill()

    def wait(self) -> ExitStatus:  # type: ignore
        code = self._process.wait()
        return ExitStatus(code)

    def wait_with_output(self) -> Output:  # type: ignore
        stdout, stderr = self._process.communicate()
        return Output(
            ExitStatus(self._process.returncode),
            stdout or b"",
            stderr or b"",
        )

    def try_wait(self) -> ExitStatus | None:  # type: ignore
        ret = self._process.poll()
        if ret is None:
            return None
        return ExitStatus(ret)

    def take_stdin(self) -> Any:  # type: ignore
        return self._process.stdin

    def take_stdout(self) -> Any:  # type: ignore
        return self._process.stdout

    def take_stderr(self) -> Any:  # type: ignore
        return self._process.stderr

    def wait_timeout(self, secs: float) -> ExitStatus | None:  # type: ignore
        ret = self._process.poll()
        if ret is not None:
            return ExitStatus(ret)
        try:
            self._process.wait(timeout=secs)
            return ExitStatus(self._process.returncode)
        except Exception:
            return None

    def __repr__(self) -> str:
        return f"Child(pid={self._pid})"


class Command:
    __slots__ = ("_program", "_args", "_env", "_cwd", "_stdin", "_stdout", "_stderr")

    def __init__(self, program: str | Path) -> None:
        program_str = program.as_str() if isinstance(program, Path) else str(program)
        self._program = program_str
        self._args: list[str] = []
        self._env: dict[str, str] | None = None
        self._cwd: str | None = None
        self._stdin: Stdio = Stdio.inherit()
        self._stdout: Stdio = Stdio.inherit()
        self._stderr: Stdio = Stdio.inherit()

    def arg(self, arg: str) -> Command:  # type: ignore
        self._args.append(str(arg))
        return self

    def args(self, args: Iterable[str]) -> Command:  # type: ignore
        for a in args:
            self._args.append(str(a))
        return self

    def env(self, key: str, val: str) -> Command:  # type: ignore
        if self._env is None:
            self._env = {}
        self._env[key] = val
        return self

    def envs(self, envs: dict[str, str]) -> Command:  # type: ignore
        if self._env is None:
            self._env = {}
        self._env.update(envs)
        return self

    def current_dir(self, dir: str | Path) -> Command:  # type: ignore
        self._cwd = dir.as_str() if isinstance(dir, Path) else str(dir)
        return self

    def stdin(self, cfg: Stdio) -> Command:  # type: ignore
        self._stdin = cfg
        return self

    def stdout(self, cfg: Stdio) -> Command:  # type: ignore
        self._stdout = cfg
        return self

    def stderr(self, cfg: Stdio) -> Command:  # type: ignore
        self._stderr = cfg
        return self

    def spawn(self) -> Child:  # type: ignore
        import subprocess
        stdin_cfg = None
        stdout_cfg = None
        stderr_cfg = None

        if self._stdin._kind == Stdio.PIPED:
            stdin_cfg = subprocess.PIPE
        elif self._stdin._kind == Stdio.NULL:
            stdin_cfg = subprocess.DEVNULL

        if self._stdout._kind == Stdio.PIPED:
            stdout_cfg = subprocess.PIPE
        elif self._stdout._kind == Stdio.NULL:
            stdout_cfg = subprocess.DEVNULL

        if self._stderr._kind == Stdio.PIPED:
            stderr_cfg = subprocess.PIPE
        elif self._stderr._kind == Stdio.NULL:
            stderr_cfg = subprocess.DEVNULL

        proc = subprocess.Popen(
            [self._program] + self._args,
            stdin=stdin_cfg,
            stdout=stdout_cfg,
            stderr=stderr_cfg,
            env=self._env,
            cwd=self._cwd,
        )
        return Child(proc)

    def output(self) -> Output:  # type: ignore
        import subprocess
        env = self._env
        proc = subprocess.run(
            [self._program] + self._args,
            capture_output=True,
            env=env,
            cwd=self._cwd,
        )
        return Output(
            ExitStatus(proc.returncode),
            proc.stdout,
            proc.stderr,
        )

    def status(self) -> ExitStatus:  # type: ignore
        import subprocess
        proc = subprocess.run(
            [self._program] + self._args,
            capture_output=False,
            env=self._env,
            cwd=self._cwd,
        )
        return ExitStatus(proc.returncode)

    def get_program(self) -> str:  # type: ignore
        return self._program

    def get_args(self) -> list[str]:  # type: ignore
        return self._args.copy()

    def __repr__(self) -> str:
        return f"Command({self._program!r})"


def args() -> list[str]:  # type: ignore
    return sys.argv[1:]


def env(key: str, default: str | None = None) -> str | None:  # type: ignore
    return os.environ.get(key, default)


def current_dir() -> Path:  # type: ignore
    return Path(os.getcwd())


def current_exe() -> Path:  # type: ignore
    return Path(os.path.realpath(sys.argv[0]))


def home_dir() -> Path | None:  # type: ignore
    home = os.path.expanduser("~")
    if home:
        return Path(home)
    return None


def temp_dir() -> Path:  # type: ignore
    return Path(tempfile.gettempdir())


class Formatter:
    __slots__ = ("_buf",)

    def __init__(self) -> None:
        self._buf: list[str] = []

    def write_str(self, s: str) -> None:  # type: ignore
        self._buf.append(s)

    def write_char(self, c: str) -> None:  # type: ignore
        self._buf.append(c)

    def write_fmt(self, args: str) -> None:  # type: ignore
        self._buf.append(args)

    def finish(self) -> str:  # type: ignore
        return "".join(self._buf)

    def as_str(self) -> str:  # type: ignore
        return "".join(self._buf)

    def __str__(self) -> str:
        return "".join(self._buf)


def format_(template: str, *args: Any, **kwargs: Any) -> str:
    return template.format(*args, **kwargs)


def write_(buf: Any, template: str, *args: Any, **kwargs: Any) -> None:
    formatted = template.format(*args, **kwargs)
    if hasattr(buf, 'write'):
        buf.write(formatted)
    elif hasattr(buf, 'append'):
        buf.append(formatted)


def writeln_(buf: Any, template: str = "", *args: Any, **kwargs: Any) -> None:
    formatted = template.format(*args, **kwargs) if template else ""
    if hasattr(buf, 'write'):
        buf.write(formatted + "\n")
    elif hasattr(buf, 'append'):
        buf.append(formatted + "\n")


def dbg_(*args: Any) -> Any:
    frames = traceback.extract_stack()
    if len(frames) >= 2:
        frame = frames[-2]
        loc = f"{frame.filename}:{frame.lineno}"
    else:
        loc = "<unknown>"
    parts = []
    for i, arg in enumerate(args):
        parts.append(f"{arg!r}")
    print(f"[{loc}] {', '.join(parts)}")
    return args[0] if len(args) == 1 else args


class _EnumerateIterator(Generic[T]):
    __slots__ = ("_iter", "_index")

    def __init__(self, iterable: Iterable[T], start: int = 0) -> None:
        self._iter = iter(iterable)
        self._index = start

    def __iter__(self) -> _EnumerateIterator[T]:
        return self

    def __next__(self) -> tuple[int, T]:
        idx = self._index
        val = next(self._iter)
        self._index += 1
        return (idx, val)


class Enumerate(Generic[T]):
    __slots__ = ("_iterable", "_start")

    def __init__(self, iterable: Iterable[T], start: int = 0) -> None:
        self._iterable = iterable
        self._start = start

    def __iter__(self) -> _EnumerateIterator[T]:
        return _EnumerateIterator(self._iterable, self._start)

    def __repr__(self) -> str:
        return "Enumerate(...)"


class _ZipIterator(Generic[T, U]):
    __slots__ = ("_iter_a", "_iter_b")

    def __init__(self, a: Iterator[T], b: Iterator[U]) -> None:
        self._iter_a = a
        self._iter_b = b

    def __iter__(self) -> _ZipIterator[T, U]:
        return self

    def __next__(self) -> tuple[T, U]:
        return (next(self._iter_a), next(self._iter_b))


class Zip(Generic[T, U]):
    __slots__ = ("_iter_a", "_iter_b")

    def __init__(self, a: Iterable[T], b: Iterable[U]) -> None:
        self._iter_a = a
        self._iter_b = b

    def __iter__(self) -> _ZipIterator[T, U]:
        return _ZipIterator(iter(self._iter_a), iter(self._iter_b))

    def __repr__(self) -> str:
        return "Zip(...)"


class _MapIterator(Generic[T, U]):
    __slots__ = ("_iter", "_fn")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], U]) -> None:
        self._iter = iterable
        self._fn = fn

    def __iter__(self) -> _MapIterator[T, U]:
        return self

    def __next__(self) -> U:
        return self._fn(next(self._iter))


class Map(Generic[T, U]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], U]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _MapIterator[T, U]:
        return _MapIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "Map(...)"


class _FilterIterator(Generic[T]):
    __slots__ = ("_iter", "_pred")

    def __init__(self, iterable: Iterator[T], pred: Callable[[T], bool]) -> None:
        self._iter = iterable
        self._pred = pred

    def __iter__(self) -> _FilterIterator[T]:
        return self

    def __next__(self) -> T:
        while True:
            val = next(self._iter)
            if self._pred(val):
                return val


class Filter(Generic[T]):
    __slots__ = ("_iterable", "_pred")

    def __init__(self, iterable: Iterable[T], pred: Callable[[T], bool]) -> None:
        self._iterable = iterable
        self._pred = pred

    def __iter__(self) -> _FilterIterator[T]:
        return _FilterIterator(iter(self._iterable), self._pred)

    def __repr__(self) -> str:
        return "Filter(...)"


class _FilterMapIterator(Generic[T, U]):
    __slots__ = ("_iter", "_fn")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], U | None]) -> None:
        self._iter = iterable
        self._fn = fn

    def __iter__(self) -> _FilterMapIterator[T, U]:
        return self

    def __next__(self) -> U:
        while True:
            val = self._fn(next(self._iter))
            if val is not None:
                return val


class FilterMap(Generic[T, U]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], U | None]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _FilterMapIterator[T, U]:
        return _FilterMapIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "FilterMap(...)"


class _FlatMapIterator(Generic[T, U]):
    __slots__ = ("_iter", "_fn", "_current")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], Iterable[U]]) -> None:
        self._iter = iterable
        self._fn = fn
        self._current: Iterator[U] | None = None

    def __iter__(self) -> _FlatMapIterator[T, U]:
        return self

    def __next__(self) -> U:
        while True:
            if self._current is not None:
                try:
                    return next(self._current)
                except StopIteration:
                    self._current = None
            val = next(self._iter)
            self._current = iter(self._fn(val))


class FlatMap(Generic[T, U]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], Iterable[U]]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _FlatMapIterator[T, U]:
        return _FlatMapIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "FlatMap(...)"


class _FlattenIterator(Generic[T]):
    __slots__ = ("_iter", "_current")

    def __init__(self, iterable: Iterable[Iterable[T]]) -> None:
        self._iter = iter(iterable)
        self._current: Iterator[T] | None = None

    def __iter__(self) -> _FlattenIterator[T]:
        return self

    def __next__(self) -> T:
        while True:
            if self._current is not None:
                try:
                    return next(self._current)
                except StopIteration:
                    self._current = None
            inner = next(self._iter)
            self._current = iter(inner)


class Flatten(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[Iterable[T]]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _FlattenIterator[T]:
        return _FlattenIterator(self._iterable)

    def __repr__(self) -> str:
        return "Flatten(...)"


class _PeekableIterator(Generic[T]):
    __slots__ = ("_iter", "_peeked", "_has_peeked")

    def __init__(self, iterable: Iterator[T]) -> None:
        self._iter = iterable
        self._peeked: T | None = None
        self._has_peeked = False

    def __iter__(self) -> _PeekableIterator[T]:
        return self

    def __next__(self) -> T:
        if self._has_peeked:
            self._has_peeked = False
            return self._peeked  # type: ignore
        return next(self._iter)

    def peek(self) -> T | None:  # type: ignore
        if not self._has_peeked:
            try:
                self._peeked = next(self._iter)
                self._has_peeked = True
            except StopIteration:
                return None
        return self._peeked

    def peek_mut(self) -> PeekMut[T]:  # type: ignore
        if not self._has_peeked:
            try:
                self._peeked = next(self._iter)
                self._has_peeked = True
            except StopIteration:
                return PeekMut(None, False)
        return PeekMut(self._peeked, True)


class PeekMut(Generic[T]):
    __slots__ = ("_value", "_valid")

    def __init__(self, value: T | None, valid: bool) -> None:
        self._value = value
        self._valid = valid

    def __bool__(self) -> bool:
        return self._valid

    def __enter__(self) -> PeekMut:
        return self

    def __exit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        if self._valid:
            return f"Some({self._value!r})"
        return "None"


class Peekable(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _PeekableIterator[T]:
        return _PeekableIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Peekable(...)"


class _FuseIterator(Generic[T]):
    __slots__ = ("_iter", "_exhausted")

    def __init__(self, iterable: Iterator[T]) -> None:
        self._iter = iterable
        self._exhausted = False

    def __iter__(self) -> _FuseIterator[T]:
        return self

    def __next__(self) -> T:
        if self._exhausted:
            raise StopIteration
        try:
            return next(self._iter)
        except StopIteration:
            self._exhausted = True
            raise

    def is_exhausted(self) -> bool:  # type: ignore
        return self._exhausted


class Fuse(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _FuseIterator[T]:
        return _FuseIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Fuse(...)"


class _ChainIterator(Generic[T]):
    __slots__ = ("_iter_a", "_iter_b", "_first_done")

    def __init__(self, a: Iterator[T], b: Iterator[T]) -> None:
        self._iter_a = a
        self._iter_b = b
        self._first_done = False

    def __iter__(self) -> _ChainIterator[T]:
        return self

    def __next__(self) -> T:
        if not self._first_done:
            try:
                return next(self._iter_a)
            except StopIteration:
                self._first_done = True
        return next(self._iter_b)


class Chain(Generic[T]):
    __slots__ = ("_iter_a", "_iter_b")

    def __init__(self, a: Iterable[T], b: Iterable[T]) -> None:
        self._iter_a = a
        self._iter_b = b

    def __iter__(self) -> _ChainIterator[T]:
        return _ChainIterator(iter(self._iter_a), iter(self._iter_b))

    def __repr__(self) -> str:
        return "Chain(...)"


class _CycleIterator(Generic[T]):
    __slots__ = ("_original", "_iter", "_exhausted")

    def __init__(self, iterable: Iterable[T]) -> None:
        self._original = list(iterable)
        self._iter = iter(self._original)
        self._exhausted = False

    def __iter__(self) -> _CycleIterator[T]:
        return self

    def __next__(self) -> T:
        if self._exhausted:
            self._iter = iter(self._original)
            self._exhausted = False
        try:
            return next(self._iter)
        except StopIteration:
            self._exhausted = True
            self._iter = iter(self._original)
            return next(self._iter)


class Cycle(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _CycleIterator[T]:
        return _CycleIterator(self._iterable)

    def __repr__(self) -> str:
        return "Cycle(...)"


class _TakeIterator(Generic[T]):
    __slots__ = ("_iter", "_remaining")

    def __init__(self, iterable: Iterator[T], n: int) -> None:
        self._iter = iterable
        self._remaining = n

    def __iter__(self) -> _TakeIterator[T]:
        return self

    def __next__(self) -> T:
        if self._remaining <= 0:
            raise StopIteration
        self._remaining -= 1
        return next(self._iter)


class Take(Generic[T]):
    __slots__ = ("_iterable", "_n")

    def __init__(self, iterable: Iterable[T], n: int) -> None:
        self._iterable = iterable
        self._n = n

    def __iter__(self) -> _TakeIterator[T]:
        return _TakeIterator(iter(self._iterable), self._n)

    def __repr__(self) -> str:
        return "Take(...)"


class _SkipIterator(Generic[T]):
    __slots__ = ("_iter", "_remaining")

    def __init__(self, iterable: Iterable[T], n: int) -> None:
        self._iter = iter(iterable)
        self._remaining = n

    def __iter__(self) -> _SkipIterator[T]:
        return self

    def __next__(self) -> T:
        while self._remaining > 0:
            next(self._iter)
            self._remaining -= 1
        return next(self._iter)


class Skip(Generic[T]):
    __slots__ = ("_iterable", "_n")

    def __init__(self, iterable: Iterable[T], n: int) -> None:
        self._iterable = iterable
        self._n = n

    def __iter__(self) -> _SkipIterator[T]:
        return _SkipIterator(self._iterable, self._n)

    def __repr__(self) -> str:
        return "Skip(...)"


class _RevIterator(Generic[T]):
    __slots__ = ("_buffer", "_index")

    def __init__(self, iterable: Iterable[T]) -> None:
        self._buffer = list(iterable)
        self._index = len(self._buffer) - 1

    def __iter__(self) -> _RevIterator[T]:
        return self

    def __next__(self) -> T:
        if self._index < 0:
            raise StopIteration
        val = self._buffer[self._index]
        self._index -= 1
        return val


class Rev(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _RevIterator[T]:
        return _RevIterator(self._iterable)

    def __repr__(self) -> str:
        return "Rev(...)"


class _InspectIterator(Generic[T]):
    __slots__ = ("_iter", "_fn")

    def __init__(self, iterable: Iterator[T], fn: Callable[[T], Any]) -> None:
        self._iter = iterable
        self._fn = fn

    def __iter__(self) -> _InspectIterator[T]:
        return self

    def __next__(self) -> T:
        val = next(self._iter)
        self._fn(val)
        return val


class Inspect(Generic[T]):
    __slots__ = ("_iterable", "_fn")

    def __init__(self, iterable: Iterable[T], fn: Callable[[T], Any]) -> None:
        self._iterable = iterable
        self._fn = fn

    def __iter__(self) -> _InspectIterator[T]:
        return _InspectIterator(iter(self._iterable), self._fn)

    def __repr__(self) -> str:
        return "Inspect(...)"


class _CopiedIterator(Generic[T]):
    __slots__ = ("_iter",)

    def __init__(self, iterable: Iterator[T]) -> None:
        self._iter = iterable

    def __iter__(self) -> _CopiedIterator[T]:
        return self

    def __next__(self) -> T:
        return next(self._iter)


class Copied(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _CopiedIterator[T]:
        return _CopiedIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Copied(...)"


class Cloned(Generic[T]):
    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable[T]) -> None:
        self._iterable = iterable

    def __iter__(self) -> _CopiedIterator[T]:
        return _CopiedIterator(iter(self._iterable))

    def __repr__(self) -> str:
        return "Cloned(...)"


class _PartitionIterator(Generic[T]):
    __slots__ = ("_iter", "_pred", "_true_buf", "_false_buf", "_true_idx", "_false_idx")

    def __init__(self, iterable: Iterator[T], pred: Callable[[T], bool]) -> None:
        items = list(iterable)
        self._true_buf = [item for item in items if pred(item)]
        self._false_buf = [item for item in items if not pred(item)]
        self._true_idx = 0
        self._false_idx = 0

    def __iter__(self) -> _PartitionIterator[T]:
        return self

    def __next__(self) -> tuple[list[T], list[T]]:
        if self._true_idx == 0 and self._false_idx == 0:
            self._true_idx = 1
            return (self._true_buf, self._false_buf)
        raise StopIteration


class Partition(Generic[T]):
    __slots__ = ("_iterable", "_pred")

    def __init__(self, iterable: Iterable[T], pred: Callable[[T], bool]) -> None:
        self._iterable = iterable
        self._pred = pred

    def collect(self) -> tuple[list[T], list[T]]:  # type: ignore
        true_list = []
        false_list = []
        for item in self._iterable:
            if self._pred(item):
                true_list.append(item)
            else:
                false_list.append(item)
        return (true_list, false_list)

    def __repr__(self) -> str:
        return "Partition(...)"


def matches(value: Any, pattern: Any) -> bool:
    if callable(pattern):
        return pattern(value)
    return value == pattern


def debug_assert(condition: bool, message: str = "") -> None:
    if __debug__:
        assert condition, message


def debug_assert_eq(a: Any, b: Any, message: str = "") -> None:
    if __debug__:
        assert_eq(a, b, message)


def debug_assert_ne(a: Any, b: Any, message: str = "") -> None:
    if __debug__:
        assert_ne(a, b, message)


def cfg(key: str, default: str = "") -> str:
    return os.environ.get(f"CFG_{key.upper()}", default)


def compile_error(message: str) -> None:
    raise SyntaxError(f"compile_error: {message}")


def option_env(key: str) -> str | None:
    return os.environ.get(key)


def include_str(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def include_bytes(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()


class SmallVec(Generic[T]):
    __slots__ = ("_data", "_inline", "_stack_limit")

    def __init__(self, items: Iterable[T] | None = None, stack_limit: int = 8) -> None:
        self._stack_limit = stack_limit
        self._inline: list[T] = []
        self._data: list[T] = []
        if items:
            for item in items:
                self.push(item)

    @classmethod
    def from_vec(cls, vec: list[T]) -> SmallVec[T]:
        v = cls(stack_limit=8)
        for item in vec:
            v.push(item)
        return v

    def push(self, item: T) -> None:
        if len(self._inline) < self._stack_limit:
            self._inline.append(item)
        else:
            self._data.append(item)

    def pop(self) -> T | None:  # type: ignore
        if self._data:
            return self._data.pop()
        if self._inline:
            return self._inline.pop()
        return None

    def len(self) -> int:  # type: ignore
        return len(self._inline) + len(self._data)

    def is_empty(self) -> bool:  # type: ignore
        return self.len() == 0

    def capacity(self) -> int:  # type: ignore
        return self._stack_limit + len(self._data)

    def clear(self) -> None:  # type: ignore
        self._inline.clear()
        self._data.clear()

    def swap_remove(self, index: int) -> T:  # type: ignore
        if index < len(self._inline):
            last_idx = len(self._inline) - 1
            self._inline[index], self._inline[last_idx] = self._inline[last_idx], self._inline[index]
            return self._inline.pop()
        offset = len(self._inline)
        local_idx = index - offset
        last_idx = len(self._data) - 1
        self._data[local_idx], self._data[last_idx] = self._data[last_idx], self._data[local_idx]
        return self._data.pop()

    def retain(self, f: Callable[[T], bool]) -> None:  # type: ignore
        self._inline = [x for x in self._inline if f(x)]
        self._data = [x for x in self._data if f(x)]

    def drain(self) -> Drain[T]:  # type: ignore
        items = self._inline + self._data
        self._inline.clear()
        self._data.clear()
        return Drain(items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._inline + self._data)

    def __getitem__(self, index: int) -> T:
        if index < len(self._inline):
            return self._inline[index]
        return self._data[index - len(self._inline)]

    def __setitem__(self, index: int, value: T) -> None:
        if index < len(self._inline):
            self._inline[index] = value
        else:
            self._data[index - len(self._inline)] = value

    def __len__(self) -> int:
        return self.len()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"SmallVec({list(self)})"


class ArrayVec(Generic[T]):
    __slots__ = ("_data", "_capacity", "_len")

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._data: list[T] = []
        self._len = 0

    @classmethod
    def with_capacity(cls, capacity: int) -> ArrayVec[T]:  # type: ignore
        return cls(capacity)

    def push(self, item: T) -> None:
        if self._len >= self._capacity:
            raise OverflowError("ArrayVec is full")
        self._data.append(item)
        self._len += 1

    def pop(self) -> T | None:  # type: ignore
        if self._len > 0:
            self._len -= 1
            return self._data.pop()
        return None

    def len(self) -> int:  # type: ignore
        return self._len

    def capacity(self) -> int:  # type: ignore
        return self._capacity

    def is_empty(self) -> bool:  # type: ignore
        return self._len == 0

    def is_full(self) -> bool:  # type: ignore
        return self._len >= self._capacity

    def clear(self) -> None:  # type: ignore
        self._data.clear()
        self._len = 0

    def truncate(self, len: int) -> None:  # type: ignore
        if len < self._len:
            self._data = self._data[:len]
            self._len = len

    def as_slice(self) -> list[T]:  # type: ignore
        return self._data[:self._len]

    def __iter__(self) -> Iterator[T]:
        return iter(self._data[:self._len])

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._data[index] = value

    def __len__(self) -> int:
        return self._len

    def __bool__(self) -> bool:
        return self._len > 0

    def __repr__(self) -> str:
        return f"ArrayVec({self._data[:self._len]})"


class TinyVec(Generic[T]):
    __slots__ = ("_inline", "_heap", "_is_inline")

    INLINE_LIMIT = 8

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._inline: list[T] = []
        self._heap: list[T] = []
        self._is_inline = True
        if items:
            for item in items:
                self.push(item)

    def push(self, item: T) -> None:
        if self._is_inline and len(self._inline) < self.INLINE_LIMIT:
            self._inline.append(item)
        else:
            if self._is_inline:
                self._heap = self._inline[:]
                self._inline = []
                self._is_inline = False
            self._heap.append(item)

    def pop(self) -> T | None:  # type: ignore
        if self._is_inline:
            if self._inline:
                return self._inline.pop()
            return None
        if self._heap:
            return self._heap.pop()
        return None

    def len(self) -> int:  # type: ignore
        return len(self._inline) + len(self._heap)

    def is_empty(self) -> bool:  # type: ignore
        return self.len() == 0

    def clear(self) -> None:  # type: ignore
        self._inline.clear()
        self._heap.clear()
        self._is_inline = True

    def as_slice(self) -> list[T]:  # type: ignore
        if self._is_inline:
            return self._inline[:]
        return self._heap[:]

    def into_vec(self) -> list[T]:  # type: ignore
        if self._is_inline:
            return self._inline
        return self._heap

    def retain(self, f: Callable[[T], bool]) -> None:  # type: ignore
        if self._is_inline:
            self._inline = [x for x in self._inline if f(x)]
        else:
            self._heap = [x for x in self._heap if f(x)]

    def __iter__(self) -> Iterator[T]:
        if self._is_inline:
            return iter(self._inline)
        return iter(self._heap)

    def __getitem__(self, index: int) -> T:
        if self._is_inline:
            return self._inline[index]
        return self._heap[index]

    def __setitem__(self, index: int, value: T) -> None:
        if self._is_inline:
            self._inline[index] = value
        else:
            self._heap[index] = value

    def __len__(self) -> int:
        return self.len()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __repr__(self) -> str:
        return f"TinyVec({self.as_slice()})"


class BitVec:
    __slots__ = ("_bits", "_len")

    def __init__(self, bits: Iterable[bool] | None = None) -> None:
        self._bits: list[bool] = list(bits) if bits else []
        self._len = len(self._bits)

    @classmethod
    def with_capacity(cls, capacity: int) -> BitVec:  # type: ignore
        v = cls()
        v._bits = [False] * capacity
        v._len = 0
        return v

    @classmethod
    def from_bytes(cls, data: bytes) -> BitVec:
        bits = []
        for byte in data:
            for i in range(8):
                bits.append(bool(byte & (1 << i)))
        return cls(bits)

    def push(self, bit: bool) -> None:
        self._bits.append(bit)
        self._len += 1

    def pop(self) -> bool | None:  # type: ignore
        if self._bits:
            self._len -= 1
            return self._bits.pop()
        return None

    def set(self, index: int, value: bool) -> None:  # type: ignore
        self._bits[index] = value

    def get(self, index: int) -> bool:  # type: ignore
        return self._bits[index]

    def flip(self, index: int) -> None:  # type: ignore
        self._bits[index] = not self._bits[index]

    def len(self) -> int:  # type: ignore
        return self._len

    def is_empty(self) -> bool:  # type: ignore
        return self._len == 0

    def capacity(self) -> int:  # type: ignore
        return len(self._bits)

    def clear(self) -> None:  # type: ignore
        self._bits.clear()
        self._len = 0

    def count_ones(self) -> int:  # type: ignore
        return sum(1 for b in self._bits if b)

    def count_zeros(self) -> int:  # type: ignore
        return sum(1 for b in self._bits if not b)

    def any(self) -> bool:  # type: ignore
        return any(self._bits)

    def all(self) -> bool:  # type: ignore
        return all(self._bits[:self._len])

    def to_bytes(self) -> bytes:  # type: ignore
        result = bytearray()
        for i in range(0, self._len, 8):
            byte = 0
            for j in range(8):
                if i + j < self._len and self._bits[i + j]:
                    byte |= 1 << j
            result.append(byte)
        return bytes(result)

    def as_slice(self) -> list[bool]:  # type: ignore
        return self._bits[:self._len]

    def __iter__(self) -> Iterator[bool]:
        return iter(self._bits[:self._len])

    def __getitem__(self, index: int) -> bool:
        return self._bits[index]

    def __setitem__(self, index: int, value: bool) -> None:
        self._bits[index] = value

    def __len__(self) -> int:
        return self._len

    def __bool__(self) -> bool:
        return self._len > 0

    def __repr__(self) -> str:
        return f"BitVec({self._len} bits)"


class OnceCell(Generic[T]):
    __slots__ = ("_value", "_initialized")

    def __init__(self) -> None:
        self._value: T = None  # type: ignore[assignment]
        self._initialized = False

    @classmethod
    def new(cls) -> OnceCell[T]:
        return cls()

    @classmethod
    def with_value(cls, value: T) -> OnceCell[T]:
        cell = cls()
        cell._value = value
        cell._initialized = True
        return cell

    def get(self) -> T | None:
        if not self._initialized:
            return None
        return self._value

    def set(self, value: T) -> bool:
        if self._initialized:
            return False
        self._value = value
        self._initialized = True
        return True

    def get_or_init(self, fn: Callable[[], T]) -> T:
        if self._initialized:
            return self._value
        self._value = fn()
        self._initialized = True
        return self._value

    def try_into_inner(self) -> T | None:
        if not self._initialized:
            return None
        return self._value

    def is_initialized(self) -> bool:
        return self._initialized

    def __repr__(self) -> str:
        if self._initialized:
            return f"OnceCell({self._value!r})"
        return "OnceCell(<uninitialized>)"

    def __bool__(self) -> bool:
        return self._initialized

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OnceCell):
            if not self._initialized or not other._initialized:
                return False
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        if self._initialized:
            return hash(self._value)
        return hash(None)


class Iter(Generic[T]):
    __slots__ = ("_iter",)

    def __init__(self, source: Iterable[T] | Iterator[T]) -> None:
        if isinstance(source, Iterator):
            self._iter = source
        else:
            self._iter = iter(source)

    @classmethod
    def from_fn(cls, fn: Callable[[int], T], start: int = 0) -> Iter[T]:
        def gen():
            i = start
            while True:
                yield fn(i)
                i += 1
        return cls(gen())

    @classmethod
    def repeat(cls, value: T) -> Iter[T]:
        def gen():
            while True:
                yield value
        return cls(gen())

    @classmethod
    def count(cls, start: int = 0, step: int = 1) -> Iter[int]:
        def gen():
            i = start
            while True:
                yield i
                i += step
        return cls(gen())

    @classmethod
    def zip(cls, a: Iterable[T], b: Iterable[U]) -> Iter[tuple[T, U]]:
        return cls(zip(a, b))

    @classmethod
    def chain(cls, *iters: Iterable[T]) -> Iter[T]:
        def gen():
            for it in iters:
                yield from it
        return cls(gen())

    def map(self, fn: Callable[[T], U]) -> Iter[U]:
        def gen():
            for v in self._iter:
                yield fn(v)
        return Iter(gen())

    def map_enumerate(self, fn: Callable[[int, T], U]) -> Iter[U]:
        def gen():
            for i, v in enumerate(self._iter):
                yield fn(i, v)
        return Iter(gen())

    def filter(self, predicate: Callable[[T], bool]) -> Iter[T]:
        def gen():
            for v in self._iter:
                if predicate(v):
                    yield v
        return Iter(gen())

    def filter_map(self, fn: Callable[[T], U | None]) -> Iter[U]:
        def gen():
            for v in self._iter:
                result = fn(v)
                if result is not None:
                    yield result
        return Iter(gen())

    def enumerate(self, start: int = 0) -> Iter[tuple[int, T]]:
        def gen():
            for i, v in enumerate(self._iter, start):
                yield (i, v)
        return Iter(gen())

    def peekable(self) -> PeekableIter[T]:
        return PeekableIter(self._iter)

    def take(self, n: int) -> Iter[T]:
        def gen():
            for i, v in enumerate(self._iter):
                if i >= n:
                    break
                yield v
        return Iter(gen())

    def take_while(self, predicate: Callable[[T], bool]) -> Iter[T]:
        def gen():
            for v in self._iter:
                if not predicate(v):
                    break
                yield v
        return Iter(gen())

    def skip(self, n: int) -> Iter[T]:
        def gen():
            for i, v in enumerate(self._iter):
                if i >= n:
                    yield v
        return Iter(gen())

    def skip_while(self, predicate: Callable[[T], bool]) -> Iter[T]:
        def gen():
            skipping = True
            for v in self._iter:
                if skipping and predicate(v):
                    continue
                skipping = False
                yield v
        return Iter(gen())

    def flat_map(self, fn: Callable[[T], Iterable[U]]) -> Iter[U]:
        def gen():
            for v in self._iter:
                yield from fn(v)
        return Iter(gen())

    def flatten(self) -> Iter[Any]:
        def gen():
            for v in self._iter:
                if hasattr(v, '__iter__'):
                    yield from v
                else:
                    yield v
        return Iter(gen())

    def inspect(self, fn: Callable[[T], Any]) -> Iter[T]:
        def gen():
            for v in self._iter:
                fn(v)
                yield v
        return Iter(gen())

    def step_by(self, step: int) -> Iter[T]:
        def gen():
            for i, v in enumerate(self._iter):
                if i % step == 0:
                    yield v
        return Iter(gen())

    def zip_with(self, other: Iterable[U], fn: Callable[[T, U], V]) -> Iter[V]:
        def gen():
            for a, b in zip(self._iter, other):
                yield fn(a, b)
        return Iter(gen())

    def fuse(self) -> Iter[T]:
        def gen():
            exhausted = False
            for v in self._iter:
                if exhausted:
                    break
                yield v
        return Iter(gen())

    def fold(self, init: U, fn: Callable[[U, T], U]) -> U:
        acc = init
        for v in self._iter:
            acc = fn(acc, v)
        return acc

    def reduce(self, fn: Callable[[T, T], T]) -> T | None:
        it = iter(self._iter)
        try:
            acc = next(it)
        except StopIteration:
            return None
        for v in it:
            acc = fn(acc, v)
        return acc

    def collect(self) -> list[T]:
        return list(self._iter)

    def collect_into(self, collection: Any) -> Any:
        for v in self._iter:
            collection.append(v)
        return collection

    def count(self) -> int:
        n = 0
        for _ in self._iter:
            n += 1
        return n

    def sum(self) -> T:
        return self.fold(0, lambda a, b: a + b)  # type: ignore

    def product(self) -> T:
        return self.fold(1, lambda a, b: a * b)  # type: ignore

    def min(self) -> T | None:
        return self.reduce(lambda a, b: a if a < b else b)

    def max(self) -> T | None:
        return self.reduce(lambda a, b: a if a > b else b)

    def all(self, predicate: Callable[[T], bool]) -> bool:
        for v in self._iter:
            if not predicate(v):
                return False
        return True

    def any(self, predicate: Callable[[T], bool]) -> bool:
        for v in self._iter:
            if predicate(v):
                return True
        return False

    def position(self, predicate: Callable[[T], bool]) -> int | None:
        for i, v in enumerate(self._iter):
            if predicate(v):
                return i
        return None

    def nth(self, n: int) -> T | None:
        for i, v in enumerate(self._iter):
            if i == n:
                return v
        return None

    def last(self) -> T | None:
        result = None
        for v in self._iter:
            result = v
        return result

    def next(self) -> T:
        return next(self._iter)

    def for_each(self, fn: Callable[[T], Any]) -> None:
        for v in self._iter:
            fn(v)

    def partition(self, predicate: Callable[[T], bool]) -> tuple[list[T], list[T]]:
        a, b = [], []
        for v in self._iter:
            (a if predicate(v) else b).append(v)
        return a, b

    def __iter__(self) -> Iterator[T]:
        return self._iter

    def __next__(self) -> T:
        return next(self._iter)

    def __repr__(self) -> str:
        return "Iter(...)"


class PeekableIter(Generic[T]):
    __slots__ = ("_iter", "_peeked", "_has_peeked")

    def __init__(self, source: Iterator[T]) -> None:
        self._iter = source
        self._peeked: T = None  # type: ignore[assignment]
        self._has_peeked = False

    def peek(self) -> T | None:
        if self._has_peeked:
            return self._peeked
        try:
            self._peeked = next(self._iter)
            self._has_peeked = True
            return self._peeked
        except StopIteration:
            return None

    def next(self) -> T:
        if self._has_peeked:
            self._has_peeked = False
            return self._peeked
        return next(self._iter)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        return self.next()


class Variant:
    __slots__ = ("_tag", "_value", "_enum_cls")

    def __init__(self, tag: str, value: Any, enum_cls: type | None = None) -> None:
        self._tag = tag
        self._value = value
        self._enum_cls = enum_cls

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def value(self) -> Any:
        return self._value

    def is_(self, *tags: str) -> bool:
        return self._tag in tags

    def unwrap(self) -> Any:
        return self._value

    def unwrap_or(self, default: Any) -> Any:
        return self._value

    def expect(self, message: str) -> Any:
        return self._value

    def map(self, fn: Callable[[Any], Any]) -> Variant:
        return Variant(self._tag, fn(self._value), self._enum_cls)

    def map_or(self, default: Any, fn: Callable[[Any], Any]) -> Any:
        return fn(self._value)

    def and_then(self, fn: Callable[[Any], Variant]) -> Variant:
        return fn(self._value)

    def or_else(self, fn: Callable[[str], Variant]) -> Variant:
        return self

    def match(self, *cases: tuple[str, Callable[[Any], Any]]) -> Any:
        for case in cases:
            pattern, handler = case[0], case[1]
            if isinstance(pattern, _MatchWildcard):
                return handler(self._value)
            if isinstance(pattern, tuple) and len(pattern) == 2:
                t, guard = pattern
                if t == self._tag and guard(self._value):
                    return handler(self._value)
            elif pattern == self._tag:
                return handler(self._value)
        raise MatchError(f"no match for {self!r}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Variant):
            return self._tag == other._tag and self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._tag, self._value))

    def __repr__(self) -> str:
        if self._value is None:
            return self._tag
        return f"{self._tag}({self._value!r})"


class _EnumMeta(type):
    def __new__(cls, name, bases, namespace) -> type:
        variants = {}
        for key, val in list(namespace.items()):
            if key.startswith("_") or callable(val):
                continue
            if isinstance(val, tuple) and len(val) >= 1 and isinstance(val[0], str):
                variants[val[0]] = val[1:]
            elif isinstance(val, str):
                variants[val] = ()
        namespace["_variants"] = variants
        for key in list(variants.keys()):
            if key in namespace:
                del namespace[key]
        obj = super().__new__(cls, name, bases, namespace)
        return obj

    def __getattr__(cls, name: str) -> Variant:
        if name.startswith("_"):
            raise AttributeError(name)
        variants = cls.__dict__.get("_variants", {})
        if name in variants:
            val = variants[name]
            return Variant(name, val[0] if len(val) == 1 else val, cls)
        raise AttributeError(f"enum {cls.__name__} has no variant '{name}'")


class Enum(metaclass=_EnumMeta):
    @classmethod
    def variants(cls) -> list[str]:
        return list(cls._variants.keys())  # type: ignore

    @classmethod
    def is_valid(cls, tag: str) -> bool:
        return tag in cls._variants  # type: ignore

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__dict__})"


def assert_(condition: bool, message: str = "assertion failed") -> None:
    if not condition:
        raise AssertionError(message)


def assert_eq(a: Any, b: Any, message: str | None = None) -> None:
    if a != b:
        msg = message or f"assertion failed: {a!r} != {b!r}"
        raise AssertionError(msg)


def assert_ne(a: Any, b: Any, message: str | None = None) -> None:
    if a == b:
        msg = message or f"assertion failed: {a!r} == {b!r}"
        raise AssertionError(msg)


def assert_matches(value: Any, pattern: str, message: str | None = None) -> None:
    if not re.match(pattern, str(value)):
        msg = message or f"assertion failed: {value!r} does not match {pattern!r}"
        raise AssertionError(msg)


def assert_type(value: Any, expected: type, message: str | None = None) -> None:
    if not isinstance(value, expected):
        msg = message or f"assertion failed: expected {expected.__name__}, got {type(value).__name__}"
        raise AssertionError(msg)


def dbg(value: Any, *args: Any, **kwargs: Any) -> Any:
    frame = inspect.currentframe()
    caller = frame.f_back if frame else None  # type: ignore
    var_name = ""
    if caller:
        code = caller.f_code
        for name in code.co_varnames:
            if caller.f_locals.get(name) is value:
                var_name = name
                break
    loc = ""
    if caller:
        loc = f"{caller.f_code.co_filename}:{caller.f_lineno}"
    prefix = f"[{var_name}]" if var_name else ""
    suffix = ""
    if args:
        suffix = " " + " ".join(str(a) for a in args)
    if kwargs:
        suffix += " " + " ".join(f"{k}={v!r}" for k, v in kwargs.items())
    print(f"{prefix} {value!r}{suffix} @ {loc}")
    return value


@dataclass(frozen=True, slots=True)
class CreateMeta:
    libname: str
    libversion: tuple[int, int]
    pyversion: tuple[int, int]
    author: str
    clone: str
    description: str
    license: str
    homepage: str
    keywords: tuple[str, ...]
    python_requires: str
    timestamp: str
    def unwrap(self) -> str:
        return self.libname

Meta = CreateMeta(
    libname="foundation",
    libversion=(1, 0),
    pyversion=(3, 13),
    author="@n11kol11c",
    clone="https://github.com/n11kol11c/foundation.git",
    description="An all-in-one comprehensive Python utility library for INI management, network scanning, data processing, and CLI tools.",
    license="MIT",
    homepage="https://github.com/n11kol11c/foundation",
    keywords=("ini", "network", "csv", "json", "xml", "cli", "html", "css"),
    python_requires=">=3.13",
    timestamp="2026-08-25",
)

class Option(Generic[T]):
    """
    Rust-like Option<T>.

        Some(value)
        None

    Examples:
        x: Option[int] = Some(10)
        x: Option[str] = None
    """

    def is_some(self) -> bool:
        return isinstance(self, Some)

    def is_none(self) -> bool:
        return isinstance(self, NoneOption)

    def unwrap(self) -> T:
        if isinstance(self, Some):
            return self.value
        raise RuntimeError(
            "called `Option.unwrap()` on a `None` value"
        )

    def expect(self, message: str) -> T:
        if isinstance(self, Some):
            return self.value
        raise RuntimeError(message)

    def unwrap_or(self, default: T) -> T:
        if isinstance(self, Some):
            return self.value
        return default

    def unwrap_or_else(
        self,
        fn: Callable[[], T],
    ) -> T:
        if isinstance(self, Some):
            return self.value
        return fn()

    def map(
        self,
        fn: Callable[[T], U],
    ) -> Option[U]:
        if isinstance(self, Some):
            return Some(fn(self.value))
        return None_

    def map_or(
        self,
        default: U,
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Some):
            return fn(self.value)
        return default

    def map_or_else(
        self,
        default: Callable[[], U],
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Some):
            return fn(self.value)
        return default()

    def and_(
        self,
        other: Option[U],
    ) -> Option[U]:
        if isinstance(self, Some):
            return other
        return None_

    def and_then(
        self,
        fn: Callable[[T], Option[U]],
    ) -> Option[U]:
        if isinstance(self, Some):
            return fn(self.value)
        return None_

    def or_(
        self,
        other: Option[T],
    ) -> Option[T]:
        if isinstance(self, Some):
            return self
        return other

    def or_else(
        self,
        fn: Callable[[], Option[T]],
    ) -> Option[T]:
        if isinstance(self, Some):
            return self
        return fn()

    def filter(
        self,
        predicate: Callable[[T], bool],
    ) -> Option[T]:
        if isinstance(self, Some):
            if predicate(self.value):
                return self
        return None_

    def inspect(
        self,
        fn: Callable[[T], Any],
    ) -> Option[T]:
        if isinstance(self, Some):
            fn(self.value)
        return self

    def __bool__(self) -> bool:
        return self.is_some()

    def __iter__(self):
        if isinstance(self, Some):
            yield self.value

    def __repr__(self) -> str:
        if isinstance(self, Some):
            return f"Some({self.value!r})"
        return "None"


@dataclass(frozen=True, slots=True)
class Some(Option[T]):
    value: T


class NoneOption(Option[NoReturn]):
    """
    Singleton implementation of Rust's None.
    """

    __slots__ = ()
    _instance: NoneOption | None = None

    def __new__(cls) -> NoneOption:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

None_ = NoneOption()
none = None_

class Result(Generic[T, E]):
    """
    Rust-like Result<T, E>.

        Ok(value)
        Err(exception)
    """

    def is_ok(self) -> bool:
        return isinstance(self, Ok)

    def is_err(self) -> bool:
        return isinstance(self, Err)

    def unwrap(self) -> T:
        if isinstance(self, Ok):
            return self.value

        raise RuntimeError(
            "called `Result.unwrap()` on an `Err` value: "
            f"{self.error!r}"
        )

    def expect(self, message: str) -> T:
        if isinstance(self, Ok):
            return self.value
        raise RuntimeError(
            f"{message}: {self.error!r}"
        )

    def unwrap_err(self) -> E:
        if isinstance(self, Err):
            return self.error
        raise RuntimeError(
            "called `Result.unwrap_err()` on an `Ok` value: "
            f"{self.value!r}"
        )

    def expect_err(self, message: str) -> E:
        if isinstance(self, Err):
            return self.error
        raise RuntimeError(
            f"{message}: {self.value!r}"
        )

    def unwrap_or(self, default: T) -> T:
        if isinstance(self, Ok):
            return self.value
        return default

    def unwrap_or_else(
        self,
        fn: Callable[[E], T],
    ) -> T:
        if isinstance(self, Ok):
            return self.value
        return fn(self.error)

    def map(
        self,
        fn: Callable[[T], U],
    ) -> Result[U, E]:
        if isinstance(self, Ok):
            return Ok(fn(self.value))
        return self

    def map_err(
        self,
        fn: Callable[[E], U],
    ) -> Result[T, U]:
        if isinstance(self, Err):
            return Err(fn(self.error))
        return self

    def map_or(
        self,
        default: U,
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Ok):
            return fn(self.value)
        return default

    def map_or_else(
        self,
        default: Callable[[E], U],
        fn: Callable[[T], U],
    ) -> U:
        if isinstance(self, Ok):
            return fn(self.value)
        return default(self.error)

    def and_(
        self,
        other: Result[U, E],
    ) -> Result[U, E]:
        if isinstance(self, Ok):
            return other
        return self

    def and_then(
        self,
        fn: Callable[[T], Result[U, E]],
    ) -> Result[U, E]:
        if isinstance(self, Ok):
            return fn(self.value)
        return self

    def or_(
        self,
        other: Result[T, U],
    ) -> Result[T, U]:
        if isinstance(self, Ok):
            return self
        return other

    def or_else(
        self,
        fn: Callable[[E], Result[T, U]],
    ) -> Result[T, U]:
        if isinstance(self, Err):
            return fn(self.error)
        return self

    def ok(self) -> Option[T]:
        if isinstance(self, Ok):
            return Some(self.value)
        return None_

    def err(self) -> Option[E]:
        if isinstance(self, Err):
            return Some(self.error)
        return None_

    def inspect(
        self,
        fn: Callable[[T], Any],
    ) -> Result[T, E]:
        if isinstance(self, Ok):
            fn(self.value)
        return self

    def inspect_err(
        self,
        fn: Callable[[E], Any],
    ) -> Result[T, E]:
        if isinstance(self, Err):
            fn(self.error)
        return self

    def __bool__(self) -> bool:
        return self.is_ok()

    def __repr__(self) -> str:
        if isinstance(self, Ok):
            return f"Ok({self.value!r})"
        return f"Err({self.error!r})"


@dataclass(frozen=True, slots=True)
class Ok(Result[T, NoReturn]):
    value: T

@dataclass(frozen=True, slots=True)
class Err(Result[NoReturn, E]):
    error: E

class Vec(Generic[T]):
    """
    Rust-inspired Vec<T> for Python.

    Backed by Python's list, while exposing a Rust-like API.
    """

    __slots__ = ("_data", "_capacity")

    def __init__(
        self,
        values: Iterable[T] = (),
        *,
        capacity: int | None = None,
    ) -> None:
        self._data = list(values)

        if capacity is None:
            self._capacity = len(self._data)
        else:
            if capacity < len(self._data):
                raise ValueError(
                    "capacity cannot be smaller than length"
                )

            self._capacity = capacity

    @classmethod
    def new(cls) -> Vec[T]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> Vec[T]:
        if capacity < 0:
            raise ValueError("capacity must be non-negative")

        return cls(capacity=capacity)

    @classmethod
    def from_iter(cls, values: Iterable[T]) -> Vec[T]:
        return cls(values)

    @classmethod
    def repeat(cls, value: T, n: int) -> Vec[T]:
        if n < 0:
            raise ValueError("n must be non-negative")

        return cls([value] * n)

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def capacity(self) -> int:
        return self._capacity


    def reserve(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required <= self._capacity:
            return

        new_capacity = max(
            required,
            max(1, self._capacity * 2),
        )

        self._capacity = new_capacity

    def reserve_exact(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required > self._capacity:
            self._capacity = required

    def shrink_to_fit(self) -> None:
        self._capacity = self.len()

    def shrink_to(self, min_capacity: int) -> None:
        if min_capacity < 0:
            raise ValueError(
                "min_capacity must be non-negative"
            )

        self._capacity = max(
            self.len(),
            min_capacity,
        )

    def push(self, value: T) -> None:
        self.reserve(1)
        self._data.append(value)

    def pop(self) -> Option[T]:
        if not self._data:
            return None_

        return Some(self._data.pop())

    def insert(self, index: int, value: T) -> None:
        if index < 0 or index > self.len():
            raise IndexError(
                f"index {index} out of bounds"
            )

        self.reserve(1)
        self._data.insert(index, value)

    def remove(self, index: int) -> T:
        self._check_index(index)
        return self._data.pop(index)

    def swap_remove(self, index: int) -> T:
        self._check_index(index)

        last = self._data.pop()

        if index == self.len():
            return last

        removed = self._data[index]
        self._data[index] = last

        return removed

    def clear(self) -> None:
        self._data.clear()

    def truncate(self, length: int) -> None:
        if length < 0:
            raise ValueError(
                "length must be non-negative"
            )

        del self._data[length:]


    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self.len():
            raise IndexError(
                f"index {index} out of bounds "
                f"for Vec of length {self.len()}"
            )

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Vec[T]:
        ...

    def __getitem__(
        self,
        index: int | slice,
    ) -> T | Vec[T]:

        if isinstance(index, slice):
            return Vec(self._data[index])

        self._check_index(index)
        return self._data[index]

    def get(self, index: int) -> Option[T]:
        if index < 0 or index >= self.len():
            return None_

        return Some(self._data[index])

    def first(self) -> Option[T]:
        if not self._data:
            return None_

        return Some(self._data[0])

    def last(self) -> Option[T]:
        if not self._data:
            return None_

        return Some(self._data[-1])

    def contains(self, value: T) -> bool:
        return value in self._data

    def position(
        self,
        predicate: Callable[[T], bool],
    ) -> Option[int]:

        for index, value in enumerate(self._data):
            if predicate(value):
                return Some(index)

        return None_

    def find(
        self,
        predicate: Callable[[T], bool],
    ) -> Option[T]:

        for value in self._data:
            if predicate(value):
                return Some(value)

        return None_

    def reverse(self) -> None:
        self._data.reverse()

    def sort(
        self,
        *,
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> None:

        self._data.sort(
            key=key,
            reverse=reverse,
        )

    def sort_unstable(
        self,
        *,
        key: Callable[[T], Any] | None = None,
        reverse: bool = False,
    ) -> None:

        self._data.sort(
            key=key,
            reverse=reverse,
        )

    def retain(
        self,
        predicate: Callable[[T], bool],
    ) -> None:

        self._data[:] = [
            value
            for value in self._data
            if predicate(value)
        ]

    def dedup(self) -> None:
        if len(self._data) < 2:
            return

        result = [self._data[0]]

        for value in self._data[1:]:
            if value != result[-1]:
                result.append(value)

        self._data[:] = result

    def append(self, other: Vec[T]) -> None:
        self.reserve(other.len())
        self._data.extend(other._data)

    def extend(
        self,
        values: Iterable[T],
    ) -> None:

        values = list(values)

        self.reserve(len(values))
        self._data.extend(values)

    def split_off(self, at: int) -> Vec[T]:
        if at < 0 or at > self.len():
            raise IndexError(
                f"split index {at} out of bounds"
            )

        result = Vec(self._data[at:])
        del self._data[at:]

        return result

    def iter(self) -> Iterator[T]:
        return iter(self._data)

    def enumerate(self) -> Iterator[tuple[int, T]]:
        return enumerate(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def to_list(self) -> list[T]:
        return self._data.copy()

    def into_iter(self) -> Iterator[T]:
        data = self._data

        self._data = []
        self._capacity = 0

        return iter(data)

    def __len__(self) -> int:
        return self.len()

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def __repr__(self) -> str:
        return f"Vec({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vec):
            return self._data == other._data

        return NotImplemented

class HashMap(Generic[K, V]):
    __slots__ = ("_data", "_capacity")

    def __init__(
        self,
        values: Iterable[tuple[K, V]] | dict[K, V] | None = None,
        *,
        capacity: int = 0,
    ) -> None:
        if capacity < 0:
            raise ValueError("capacity must be non-negative")

        self._data: dict[K, V] = {}
        self._capacity = max(capacity, 0)

        if values is not None:
            if isinstance(values, dict):
                self.extend(values.items())
            else:
                self.extend(values)

    @classmethod
    def new(cls) -> HashMap[K, V]:
        return cls()

    @classmethod
    def with_capacity(cls, capacity: int) -> HashMap[K, V]:
        return cls(capacity=capacity)

    @classmethod
    def from_iter(
        cls,
        values: Iterable[tuple[K, V]],
    ) -> HashMap[K, V]:
        return cls(values)

    @classmethod
    def from_dict(
        cls,
        values: dict[K, V],
    ) -> HashMap[K, V]:
        return cls(values.items())

    def len(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data

    def capacity(self) -> int:
        return max(self._capacity, len(self._data))

    def reserve(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required > self._capacity:
            self._capacity = max(
                required,
                max(1, self._capacity * 2),
            )

    def reserve_exact(self, additional: int) -> None:
        if additional < 0:
            raise ValueError("additional must be non-negative")

        required = self.len() + additional

        if required > self._capacity:
            self._capacity = required

    def try_reserve(self, additional: int) -> bool:
        try:
            self.reserve(additional)
            return True
        except (MemoryError, OverflowError):
            return False

    def shrink_to_fit(self) -> None:
        self._capacity = self.len()

    def shrink_to(self, min_capacity: int) -> None:
        if min_capacity < 0:
            raise ValueError("min_capacity must be non-negative")

        self._capacity = max(
            self.len(),
            min_capacity,
        )

    def insert(self, key: K, value: V) -> Option[V]:
        old = self._data.get(key, _MISSING)

        if old is _MISSING:
            self.reserve(1)
            self._data[key] = value
            return None_

        self._data[key] = value
        return Some(old)

    def insert_entry(self, key: K, value: V) -> OccupiedEntry[K, V]:
        self.insert(key, value)
        return OccupiedEntry(self, key)

    def get(self, key: K) -> Option[V]:
        value = self._data.get(key, _MISSING)

        if value is _MISSING:
            return None_

        return Some(value)

    def get_value(self, key: K) -> V | None:
        return self._data.get(key)

    def get_mut(self, key: K) -> Option[MutableValue[K, V]]:
        if key not in self._data:
            return None_

        return Some(MutableValue(self, key))

    def get_key_value(self, key: K) -> Option[tuple[K, V]]:
        if key not in self._data:
            return None_

        return Some((key, self._data[key]))

    def contains_key(self, key: K) -> bool:
        return key in self._data

    def remove(self, key: K) -> Option[V]:
        value = self._data.pop(key, _MISSING)

        if value is _MISSING:
            return None_

        return Some(value)

    def remove_entry(self, key: K) -> Option[tuple[K, V]]:
        if key not in self._data:
            return None_

        return Some((key, self._data.pop(key)))

    def clear(self) -> None:
        self._data.clear()

    def retain(self, predicate: Callable[[K, V], bool]) -> None:
        keys = [
            key
            for key, value in self._data.items()
            if not predicate(key, value)
        ]

        for key in keys:
            del self._data[key]

    def entry(self, key: K) -> Entry[K, V]:
        if key in self._data:
            return OccupiedEntry(self, key)

        return VacantEntry(self, key)

    def or_insert(self, key: K, value: V) -> V:
        entry = self.entry(key)
        return entry.or_insert(value)

    def or_insert_with(
        self,
        key: K,
        fn: Callable[[], V],
    ) -> V:
        entry = self.entry(key)
        return entry.or_insert_with(fn)

    def or_insert_with_key(
        self,
        key: K,
        fn: Callable[[K], V],
    ) -> V:
        entry = self.entry(key)
        return entry.or_insert_with_key(fn)

    def extend(
        self,
        values: Iterable[tuple[K, V]],
    ) -> None:
        values = list(values)
        self.reserve(len(values))

        for key, value in values:
            self._data[key] = value

    def extend_one(self, key: K, value: V) -> None:
        self.insert(key, value)

    def iter(self) -> Iterator[tuple[K, V]]:
        return iter(self._data.items())

    def iter_mut(self) -> Iterator[MutableValue[K, V]]:
        for key in self._data:
            yield MutableValue(self, key)

    def keys(self) -> Iterator[K]:
        return iter(self._data.keys())

    def values(self) -> Iterator[V]:
        return iter(self._data.values())

    def values_mut(self) -> Iterator[MutableValue[K, V]]:
        return self.iter_mut()

    def into_iter(self) -> Iterator[tuple[K, V]]:
        data = self._data

        self._data = {}
        self._capacity = 0

        return iter(data.items())

    def drain(self) -> Iterator[tuple[K, V]]:
        data = self._data

        self._data = {}
        self._capacity = 0

        return iter(data.items())

    def is_disjoint(self, other: HashMap[K, V]) -> bool:
        return not any(
            key in other._data
            for key in self._data
        )

    def len_common(self, other: HashMap[K, U]) -> int:
        return sum(
            key in other._data
            for key in self._data
        )

    def clone(self) -> HashMap[K, V]:
        result = HashMap[K, V]()
        result._data = self._data.copy()
        result._capacity = self._capacity
        return result

    def to_dict(self) -> dict[K, V]:
        return self._data.copy()

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __setitem__(self, key: K, value: V) -> None:
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        del self._data[key]

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:
        return f"HashMap({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashMap):
            return self._data == other._data

        if isinstance(other, dict):
            return self._data == other

        return NotImplemented


class Entry(Generic[K, V]):
    __slots__ = ()

    def is_occupied(self) -> bool:
        return isinstance(self, OccupiedEntry)

    def is_vacant(self) -> bool:
        return isinstance(self, VacantEntry)

    def key(self) -> K:
        raise NotImplementedError

    def or_insert(self, value: V) -> V:
        raise NotImplementedError

    def or_insert_with(self, fn: Callable[[], V]) -> V:
        raise NotImplementedError

    def or_insert_with_key(
        self,
        fn: Callable[[K], V],
    ) -> V:
        raise NotImplementedError

    def and_modify(
        self,
        fn: Callable[[MutableValue[K, V]], None],
    ) -> Entry[K, V]:
        if isinstance(self, OccupiedEntry):
            fn(MutableValue(self._map, self._key))

        return self


class OccupiedEntry(Entry[K, V]):
    __slots__ = ("_map", "_key")

    def __init__(
        self,
        map_: HashMap[K, V],
        key: K,
    ) -> None:
        self._map = map_
        self._key = key

    def key(self) -> K:
        return self._key

    def get(self) -> V:
        return self._map._data[self._key]

    def get_mut(self) -> MutableValue[K, V]:
        return MutableValue(self._map, self._key)

    def insert(self, value: V) -> V:
        old = self._map._data[self._key]
        self._map._data[self._key] = value
        return old

    def remove(self) -> V:
        return self._map._data.pop(self._key)

    def remove_entry(self) -> tuple[K, V]:
        return self._key, self._map._data.pop(self._key)

    def or_insert(self, value: V) -> V:
        return self.get()

    def or_insert_with(self, fn: Callable[[], V]) -> V:
        return self.get()

    def or_insert_with_key(
        self,
        fn: Callable[[K], V],
    ) -> V:
        return self.get()


class VacantEntry(Entry[K, V]):
    __slots__ = ("_map", "_key")

    def __init__(
        self,
        map_: HashMap[K, V],
        key: K,
    ) -> None:
        self._map = map_
        self._key = key

    def key(self) -> K:
        return self._key

    def insert(self, value: V) -> V:
        self._map.insert(self._key, value)
        return value

    def or_insert(self, value: V) -> V:
        return self.insert(value)

    def or_insert_with(self, fn: Callable[[], V]) -> V:
        return self.insert(fn())

    def or_insert_with_key(
        self,
        fn: Callable[[K], V],
    ) -> V:
        return self.insert(fn(self._key))


class MutableValue(Generic[K, V]):
    __slots__ = ("_map", "_key")

    def __init__(
        self,
        map_: HashMap[K, V],
        key: K,
    ) -> None:
        self._map = map_
        self._key = key

    @property
    def value(self) -> V:
        return self._map._data[self._key]

    @value.setter
    def value(self, value: V) -> None:
        self._map._data[self._key] = value

    def replace(self, value: V) -> V:
        old = self.value
        self.value = value
        return old

    def get(self) -> V:
        return self.value

    def set(self, value: V) -> None:
        self.value = value


class _Missing:
    __slots__ = ()


_MISSING = _Missing()