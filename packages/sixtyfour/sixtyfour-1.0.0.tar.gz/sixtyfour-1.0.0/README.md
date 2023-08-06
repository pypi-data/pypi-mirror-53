# sixtyfour

A simplified interface for encoding and decoding base64. Can be used a Python library or a commandline tool.

## Python

Encoding and decoding strings

```python
from sixtyfour import str_to_b64, b64_to_str
b64 = str_to_b64('Hello World')
print(b64)  # SGVsbG8gV29ybGQ=
txt = b64_to_str(b64)
print(txt)  # Hello World
```

## CLI

You cat feed `sixtyfour` from stdin or use the `--file` flag to specify a file. In either case you can use the `--decode` flag for decoding.

```
Usage: sixtyfour [OPTIONS]

Options:
  -f, --file FILENAME
  -d, -D, --decode
  --help               Show this message and exit.

```
