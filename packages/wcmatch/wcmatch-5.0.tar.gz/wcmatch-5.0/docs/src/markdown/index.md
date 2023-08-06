# Wildcard Match

## Overview

Wildcard Match provides an enhanced `fnmatch`, `glob` and `pathlib` library. In some ways they are similar to Python's
builtin libraries as they provides functions to match, filter, and glob the file system. But it adds a number of
features found in Bash's globbing such as backslash escaping, brace expansion, extended glob pattern groups, etc. It
also adds a path centric matcher called `globmatch` which functions like `fnmatch`, but for paths. Paths that would
normally be returned when providing `glob` a pattern should also be properly match in `globmatch`.

Wildcard Match uses Bash as a guide when making decisions on behavior in `fnmatch` and `glob`. Behavior may differ from
Bash version to Bash version, but an attempt is made to keep Wildcard Match up with the latest relevant changes. With
all of this said, there may be a few corner cases in which we've intentionally chosen to not *exactly* mirror Bash. If
an issue is found where Wildcard Match seems to deviate in an illogical way, we'd love to hear about it in the
[issue tracker][issues].

If all you are looking for is an alternative `fnmatch` and/or `glob` that follows much more closely to Bash, Wildcard
Match has you covered, but Wildcard Match also adds a file search utility called `wcmatch` that is built on top of
`fnmatch` and `globmatch`. It was originally written for [Rummage](https://github.com/facelessuser/Rummage), but split
out into this project to be used by other projects that may find its approach useful.

- Provides features comparable to Python's builtin in `fnamtch` and `glob`.
- Adds support for `**` in glob.
- Adds support for escaping characters with `\`.
- Add support for POSIX style character classes inside sequences: `[[:alnum:]]`, etc. The `C` locale is used for byte
strings and Unicode properties for Unicode strings.
- Adds support for brace expansion: `a{b,{c,d}}` --> `ab ac ad`.
- Adds support for extended match patterns: `@(...)`, `+(...)`, `*(...)`, `?(...)`, and `!(...)`.
- Adds ability to match path names via the path centric `globmatch`.
- Provides an alternative file crawler called `wcmatch`.
- And more...

## Installation

Installation is easy with pip:

```bash
pip install wcmatch
```

## Libraries

- [`fnmatch`](./fnmatch.md): A file name matching library.
- [`glob`](./glob.md): A file system searching and file path matching library.
- [`pathlib`](./pathlib.md): A implementation of Python's `pathlib` that uses our own `glob` implementation.
- [`wcmatch`](./wcmatch.md): An alternative file search library built on `fnmatch` and `globmatch`.

--8<--
refs.txt
--8<--
