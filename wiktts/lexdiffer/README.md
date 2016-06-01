# lexdiffer 

Compare pronunciation lexica


## Input

Two UTF-8 encoded text files,
containing two pronunciation lexica.

Each line should contain at least two fields,
the word and a list of phones,
separated by a field separator character.
Each line might contain additional fields.

Phones can be represented by (Unicode) IPA characters
or they can be arbitrarily mapped.

By default:
* lines beginning with ``#`` (``U+0023 NUMBER SIGN``) are ignored;
* the field separator is the tab character (``U+0009 TAB``); and
* the word and the list of phonemes fields are the first and second fields of each line.

You can change these defaults with the ``--comment``, ``--delimiter``, and
``--word-index``/``--phonemes-index`` parameters.


## Output

TBW


## Usage

```bash
$ python -m wiktts.lexdiffer LEXICON1 LEXICON2 [OPTIONS]
```

Example:

```bash
$ python -m wiktts.lexdiffer enwiktionary-20160407.lex.clean enwiktionary-20160407.lex.clean.words.applied
```

Processing big lexicon files (>100k words) might take a couple of minutes.
The current code is not optimized for speed.

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.lexdiffer --help

TBW
```

## Examples

TBW



