# trainer 

Prepare train/test/symbol files for LTS/G2P tools.


## Input

A UTF-8 encoded plain-text **clean+normalized lexicon file**,
where each line represents a word.
Each line should contain at least two fields,
the word and the IPA string of its pronunciation,
separated by a field separator character.
Each line might contain additional fields.

By default:
* lines beginning with ``#`` (``U+0023 NUMBER SIGN``) are ignored;
* the field separator is the tab character (``U+0009 TAB``); and
* the word and IPA fields are the first and second fields of each line.

You can change these defaults with the ``--comment``, ``--delimiter``, and
``--word-index``/``--ipa-index`` parameters.

Currently, the following LTS/G2P tools are supported:

* [Phonetisaurus](https://github.com/AdolfVonKleist/Phonetisaurus)
* [Sequitur](https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html)


## Output

A set of files will be created in the given directory,
with a syntax appropriate for the specified LTS/G2P tool:

* a **train set file**, used to train a G2P model;
* a **test set file**, used to test the trained G2P model; and
* a **symbol file**, containing the mapping between item and Unicode IPA character.


## Usage

```bash
$ python -m wiktts.trainer G2PTOOL LEXICON OUTPUTDIR [OPTIONS]
```

Example:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/
```

Processing big lexicon files (>100k words) might take a couple of minutes.
The current code is not optimized for speed.

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.trainer --help

usage: __main__.py [-h] [--script [SCRIPT]] [--include-chars [INCLUDE_CHARS]]
                   [--comment [COMMENT]] [--delimiter [DELIMITER]]
                   [--word-index [WORD_INDEX]] [--ipa-index [IPA_INDEX]]
                   [--train-size-int [TRAIN_SIZE_INT]]
                   [--train-size-perc [TRAIN_SIZE_PERC]] [--quiet] [--stats]
                   [--script-only]
                   g2ptool lexicon outputdir

Prepare train/test/symbol files for LTS/G2P tools.

positional arguments:
  g2ptool               G2P tool [phonetisaurus|sequitur]
  lexicon               Input lexicon file
  outputdir             Write output files to this directory

optional arguments:
  -h, --help            show this help message and exit
  --script [SCRIPT]     Output Bash script to run G2P tool with given
                        parameters
  --include-chars [INCLUDE_CHARS]
                        Include only the given IPA characters
                        [all|cv|cvp|cvs|cvpl|cvsl|cvslw|cvslws] (default:
                        'cv')
  --comment [COMMENT]   Ignore lines in the lexicon file starting with this
                        string (default: '#')
  --delimiter [DELIMITER]
                        Field delimiter of the lexicon file (default: '\t')
  --word-index [WORD_INDEX]
                        Field index of the word (default: 0)
  --ipa-index [IPA_INDEX]
                        Field index of the IPA string (default: 1)
  --train-size-int [TRAIN_SIZE_INT]
                        Size of the train set, in words
  --train-size-perc [TRAIN_SIZE_PERC]
                        Size of the train set relative to valid lexicon size
                        (default: 0.9)
  --quiet               Do not print results to stdout
  --stats               Print statistics
  --script-only         Only output the Bash script
```

## Example

Invoking the following command:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/

Created file: /tmp/enwiktionary-20160407.lex.train
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.symbols
```



