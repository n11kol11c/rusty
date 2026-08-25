from __future__ import annotations

from rusty.core.option import Option, Some, NoneOption, None_, none
from rusty.core.result import Result, Ok, Err, PropagateError, propagate, ask, try_ask
from rusty.core.enum import Enum, Variant, match, _, Match, MatchError
from rusty.core.traits import (
    CloneTrait, CopyTrait, DebugTrait, DisplayTrait, DefaultTrait,
    EqTrait, OrdTrait, HashTrait, DropTrait,
    FromTrait, IntoTrait, TryFromTrait, TryIntoTrait,
    AsRefTrait, AsMutTrait, DerefTrait, DerefMutTrait,
    clone, debug, display, default_of, from_, into,
    try_from, try_into, as_ref, as_mut, deref, deref_mut, drop,
)
from rusty.core.convert import (
    Range, RangeInclusive, RangeFrom, RangeTo, RangeToInclusive, RangeFull,
    range_, range_inclusive, range_from, range_to, range_to_inclusive,
)
from rusty.core.error import Error, Backtrace, Location, context

from rusty.collections.vec import Vec
from rusty.collections.hashmap import HashMap, Entry, OccupiedEntry, VacantEntry
from rusty.collections.hashset import HashSet
from rusty.collections.btreemap import BTreeMap
from rusty.collections.btreeset import BTreeSet
from rusty.collections.vecdeque import VecDeque
from rusty.collections.binary_heap import BinaryHeap
from rusty.collections.linked_list import LinkedList
from rusty.collections.extra import Drain, IntoIter, Slice

from rusty.iter.iterator import Iter
from rusty.iter.adapters import (
    Enumerate, Zip, Map, Filter, FilterMap, FlatMap, Flatten,
    Peekable, PeekMut, Fuse, Chain, Cycle, Take, Skip, Rev,
    Inspect, Copied, Cloned, Partition,
)

from rusty.memory.box import Box
from rusty.memory.rc import Rc, Weak
from rusty.memory.arc import Arc
from rusty.memory.cell import Cell
from rusty.memory.refcell import RefCell, Ref, RefMut, BorrowError, BorrowMutError
from rusty.memory.oncecell import OnceCell
from rusty.memory.lazy import Lazy
from rusty.memory.cow import Cow
from rusty.memory.pin import (
    Pin, ManuallyDrop, MaybeUninit, NonNull, PhantomData,
    Borrow, BorrowMut,
)

from rusty.sync.atomic import Atomic, AtomicBool, AtomicInt
from rusty.sync.mutex import Mutex, MutexGuard
from rusty.sync.rwlock import RwLock, RwLockReadGuard, RwLockWriteGuard
from rusty.sync.barrier import Barrier
from rusty.sync.condvar import Condvar
from rusty.sync.channel import Channel, Sender, Receiver
from rusty.sync.once import Once
from rusty.sync.semaphore import Semaphore

from rusty.time.duration import Duration, UNIX_EPOCH, Elapsed
from rusty.time.instant import Instant
from rusty.time.system_time import SystemTime

from rusty.io.read import Read, BufRead
from rusty.io.write import Write
from rusty.io.buffered import BufReader, BufWriter
from rusty.io.cursor import Cursor, SeekFrom

from rusty.fs.path import Path, PathBuf
from rusty.fs.file import OpenOptions, File
from rusty.fs.metadata import (
    FileType, Permissions, Metadata, DirEntry, ReadDir,
)

from rusty.net.address import Ipv4Addr, Ipv6Addr, IpAddr, SocketAddr, Shutdown
from rusty.net.tcp import TcpStream, TcpListener, Incoming
from rusty.net.udp import UdpSocket

from rusty.process.command import Command
from rusty.process.child import Child, Stdio
from rusty.process.output import (
    ExitStatus, Output, ExitCode,
    args, env, current_dir, current_exe, home_dir, temp_dir,
)

from rusty.async_.future import Future, Poll, Waker, JoinHandle, Stream, spawn, join_all

from rusty.macros.assertions import assert_eq, assert_ne, assert_, debug_assert, debug_assert_eq, debug_assert_ne
from rusty.macros.debugging import Formatter, format_, write_, writeln_, dbg_, dbg, cfg, option_env, include_str, include_bytes, matches
from rusty.macros.panic import panic, todo, unimplemented, ScopeGuard, defer

from rusty.other import (
    Ordering, ControlFlow, Reverse, Wrapping, Saturating, NonZero,
    SmallVec, ArrayVec, TinyVec, BitVec, CreateMeta,
)

__all__ = [
    # core.option
    "Option", "Some", "NoneOption", "None_", "none",
    # core.result
    "Result", "Ok", "Err", "PropagateError", "propagate", "ask", "try_ask",
    # core.enum
    "Enum", "Variant", "match", "_", "Match", "MatchError",
    # core.traits
    "CloneTrait", "CopyTrait", "DebugTrait", "DisplayTrait", "DefaultTrait",
    "EqTrait", "OrdTrait", "HashTrait", "DropTrait",
    "FromTrait", "IntoTrait", "TryFromTrait", "TryIntoTrait",
    "AsRefTrait", "AsMutTrait", "DerefTrait", "DerefMutTrait",
    "clone", "debug", "display", "default_of", "from_", "into",
    "try_from", "try_into", "as_ref", "as_mut", "deref", "deref_mut", "drop",
    # core.convert
    "Range", "RangeInclusive", "RangeFrom", "RangeTo", "RangeToInclusive", "RangeFull",
    "range_", "range_inclusive", "range_from", "range_to", "range_to_inclusive",
    # core.error
    "Error", "Backtrace", "Location", "context",
    # collections
    "Vec", "HashMap", "Entry", "OccupiedEntry", "VacantEntry",
    "HashSet", "BTreeMap", "BTreeSet", "VecDeque", "BinaryHeap",
    "LinkedList", "Drain", "IntoIter", "Slice",
    # iter
    "Iter", "Enumerate", "Zip", "Map", "Filter", "FilterMap", "FlatMap", "Flatten",
    "Peekable", "PeekMut", "Fuse", "Chain", "Cycle", "Take", "Skip", "Rev",
    "Inspect", "Copied", "Cloned", "Partition",
    # memory
    "Box", "Rc", "Weak", "Arc", "Cell", "RefCell", "Ref", "RefMut",
    "BorrowError", "BorrowMutError", "OnceCell", "Lazy", "Cow",
    "Pin", "ManuallyDrop", "MaybeUninit", "NonNull", "PhantomData",
    "Borrow", "BorrowMut",
    # sync
    "Atomic", "AtomicBool", "AtomicInt",
    "Mutex", "MutexGuard", "RwLock", "RwLockReadGuard", "RwLockWriteGuard",
    "Barrier", "Condvar", "Channel", "Sender", "Receiver",
    "Once", "Semaphore",
    # time
    "Duration", "UNIX_EPOCH", "Elapsed", "Instant", "SystemTime",
    # io
    "Read", "Write", "BufRead", "BufReader", "BufWriter", "Cursor", "SeekFrom",
    # fs
    "Path", "PathBuf", "OpenOptions", "File",
    "FileType", "Permissions", "Metadata", "DirEntry", "ReadDir",
    # net
    "Ipv4Addr", "Ipv6Addr", "IpAddr", "SocketAddr", "Shutdown",
    "TcpStream", "TcpListener", "Incoming", "UdpSocket",
    # process
    "Command", "Child", "Stdio", "ExitStatus", "Output", "ExitCode",
    "args", "env", "current_dir", "current_exe", "home_dir", "temp_dir",
    # async_
    "Future", "Poll", "Waker", "JoinHandle", "Stream", "spawn", "join_all",
    # macros
    "assert_eq", "assert_ne", "assert_", "debug_assert", "debug_assert_eq", "debug_assert_ne",
    "Formatter", "format_", "write_", "writeln_", "dbg_", "dbg", "cfg",
    "option_env", "include_str", "include_bytes", "matches",
    "panic", "todo", "unimplemented", "ScopeGuard", "defer",
    # other
    "Ordering", "ControlFlow", "Reverse", "Wrapping", "Saturating", "NonZero",
    "SmallVec", "ArrayVec", "TinyVec", "BitVec", "CreateMeta",
]
