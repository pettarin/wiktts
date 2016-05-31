# trainer 

Prepare train/test/symbol files for ML tools.


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

Currently, the following tools are supported:

* [Sequitur](https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html)
* [Phonetisaurus (latest commit on GitHub master)](https://github.com/AdolfVonKleist/Phonetisaurus)
  (NOTE: the evaluation is based on code adapted from v0.8 and needs more work)
* [Phonetisaurus v0.8a](https://code.google.com/archive/p/phonetisaurus/)
  (IMPORTANT NOTE: v0.8a does not seems to support UTF-8 encoded train/test files, they must be ASCII encoded files!)


## Output

A set of files will be created in the given directory,
with a syntax appropriate for the specified ML tool:

* a **train set file**, used to train a ML model;
* a **test set file**, used to test the trained ML model;
* a **symbol file**, containing the map from Unicode IPA character to its ML symbol; and
* a **Bash script** to train/test/apply the ML model.


## Usage

```bash
$ python -m wiktts.trainer TOOL LEXICON OUTPUTDIR [OPTIONS]
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

usage: __main__.py [-h] [--chars [CHARS]] [--mapper [MAPPER]]
                   [--comment [COMMENT]] [--delimiter [DELIMITER]]
                   [--word-index [WORD_INDEX]] [--ipa-index [IPA_INDEX]]
                   [--train-size-int [TRAIN_SIZE_INT]]
                   [--train-size-frac [TRAIN_SIZE_FRAC]] [--quiet] [--stats]
                   [--output-script-only]
                   [--script-parameters [SCRIPT_PARAMETERS]]
                   [--create-output-dir] [--lowercase]
                   tool lexicon outputdir

Prepare train/test/symbol files for ML tools.

positional arguments:
  tool                  ML tool
                        [phonetisaurus_08a|phonetisaurus_master|sequitur]
  lexicon               Clean lexicon input file
  outputdir             Write output files to this directory

optional arguments:
  -h, --help            show this help message and exit
  --chars [CHARS]       Output the IPA characters of specified type
                        [all|cv|cvp|cvs|cvpl|cvsl|cvslw|cvslws] (default:
                        'cv')
  --mapper [MAPPER]     Map IPA chars using the specified mapper
                        [arpabet|auto|kirshenbaum] (default: 'auto')
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
  --train-size-frac [TRAIN_SIZE_FRAC]
                        Size of the train set relative to valid lexicon size
                        (default: 0.9)
  --quiet               Do not print results to stdout
  --stats               Print statistics
  --output-script-only  Only output the Bash script to run the ML tool
  --script-parameters [SCRIPT_PARAMETERS]
                        Parameters to configure the Bash script to run the ML
                        tool
  --create-output-dir   Create the output directory if it does not exist
  --lowercase           Lowercase all the words
```

## Examples

Create train/test/symbol files for Sequitur G2P:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex /tmp/

Created file: /tmp/enwiktionary-20160407.lex.train
Created file: /tmp/enwiktionary-20160407.lex.train.words
Created file: /tmp/enwiktionary-20160407.lex.train.symbols
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.test.words
Created file: /tmp/enwiktionary-20160407.lex.test.symbols
Created file: /tmp/enwiktionary-20160407.lex.words
Created file: /tmp/enwiktionary-20160407.lex.symbols
Created file: /tmp/run_sequitur.sh
```

Print statistics:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex /tmp/ --stats

Words:
  Total: 33871
  Train: 30483
  Test:  3388
Symbols:
  Total: 88
  Train: 87
  Test:  63
Created file: /tmp/enwiktionary-20160407.lex.train
Created file: /tmp/enwiktionary-20160407.lex.train.words
Created file: /tmp/enwiktionary-20160407.lex.train.symbols
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.test.words
Created file: /tmp/enwiktionary-20160407.lex.test.symbols
Created file: /tmp/enwiktionary-20160407.lex.words
Created file: /tmp/enwiktionary-20160407.lex.symbols
Created file: /tmp/run_sequitur.sh
```

Split the given lexicon into 80% train + 20% test (instead of default 90% train + 10% test):

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex /tmp/ --stats --train-size-frac 0.8

Words:
  Total: 33871
  Train: 27096
  Test:  6775
Symbols:
  Total: 88
  Train: 84
  Test:  72
Created file: /tmp/enwiktionary-20160407.lex.train
Created file: /tmp/enwiktionary-20160407.lex.train.words
Created file: /tmp/enwiktionary-20160407.lex.train.symbols
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.test.words
Created file: /tmp/enwiktionary-20160407.lex.test.symbols
Created file: /tmp/enwiktionary-20160407.lex.words
Created file: /tmp/enwiktionary-20160407.lex.symbols
Created file: /tmp/run_sequitur.sh
```

Create only the Bash script:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean  /tmp/ --output-script-only

Created file: /tmp/run_sequitur.sh
```



