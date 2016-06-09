# wiktts.lexdiffer 

Compare pronunciation lexica


## Input

Two UTF-8 encoded text files,
containing two pronunciation lexica.

Each line should contain two fields,
the word and a list of phones,
separated by a tab character (``U+0009 TAB``).

Phones are assumed to be mapped into arbitrary symbols,
separated by spaces.
Alternatively, if you specify the ``--ipa`` switch,
the phone sequence must be represented by a (clean) IPAString
in its canonical form output as UTF-8 encoded Unicode string.
(Such a representation is output e.g. by ``wiktts.lexcleaner``.)


## Output

Three files:

* a ``.diff`` file, containing the diff from lexicon1 to lexicon2 in plain text format;
* a ``.diff.html`` file, containing the diff in HTML format;
* a ``.diff_stats`` file, containing the diff statistics.


## Usage

```bash
$ python -m wiktts.lexdiffer LEXICON1 LEXICON2 [OPTIONS]
```

Example:

```bash
$ python -m wiktts.lexdiffer enwiktionary-20160407.lex.clean.tab enwiktionary-20160407.lex.clean.words.applied
$ python -m wiktts.lexdiffer enwiktionary-20160407.lex.clean another.lex.clean --ipa 
```

Processing big lexicon files (>100k words) might take a couple of minutes.
The current code is not optimized for speed.

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.lexdiffer --help

usage: wiktts.lexdiffer [-h] [--ipa] [--no-color] [--diff-only] [--no-sort]
                        [--stats] [--stdout]
                        lexicon1 lexicon2

Compare pronunciation lexica.

positional arguments:
  lexicon1     First lexicon file
  lexicon2     Second lexicon file (reference)

optional arguments:
  -h, --help   show this help message and exit
  --ipa        The input lexica contain IPA strings (not mapped)
  --no-color   Do not color output
  --diff-only  Do not output common lines
  --no-sort    Do not sort the results
  --stats      Print statistics
  --stdout     Print results to standard output
```

## Examples

TBW



