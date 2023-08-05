# Passit
[![CircleCI](https://circleci.com/gh/capriciousaton/passit.svg?style=svg)](https://circleci.com/gh/hash-vault/stronk)
[![stronk](https://img.shields.io/pypi/v/passit.svg)](https://pypi.org/project/stronk/)

Strong Python key and password generator tool.

## Requirements

Python 3.6+.

## Usage

### Key generation

To generate three keys with 256 characters:

```bash
passit 3 256
```

To generate the default single key with 16 characters:

```bash
passit
```

The maximum number of keys and characters that can be generated is 100 and 256:

```bash
passit 100 256
```

Add the flag -i to generate identifiers alongside the keys for easier readibility, which also gets printed to the
file.  This is disabled by default.

```bash
passit -i 3 256
```

### Errors

Passing string literals as arguments will throw an error.

### Output

The output of the keys is printed to stdout and stored in a file called "stronk.txt" in your 
current working directory.

## Contributing

See [the contributing guide](CONTRIBUTING.md).
