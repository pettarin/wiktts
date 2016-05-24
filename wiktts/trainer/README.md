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

* [Phonetisaurus](https://github.com/AdolfVonKleist/Phonetisaurus) (Bash script TBD)
* [Sequitur](https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html)


## Output

A set of files will be created in the given directory,
with a syntax appropriate for the specified ML tool:

* a **train set file**, used to train a ML model;
* a **test set file**, used to test the trained ML model;
* a **symbol file**, containing the map from Unicode IPA character to its ML symbol; and
* (optional) a **Bash script** to train/test the resulting ML model.


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

usage: __main__.py [-h] [--include-chars [INCLUDE_CHARS]]
                   [--comment [COMMENT]] [--delimiter [DELIMITER]]
                   [--word-index [WORD_INDEX]] [--ipa-index [IPA_INDEX]]
                   [--train-size-int [TRAIN_SIZE_INT]]
                   [--train-size-frac [TRAIN_SIZE_FRAC]] [--quiet] [--stats]
                   [--output-script-only] [--output-script]
                   [--script-parameters [SCRIPT_PARAMETERS]]
                   tool lexicon outputdir

Prepare train/test/symbol files for ML tools.

positional arguments:
  tool                  ML tool [phonetisaurus|sequitur]
  lexicon               Input lexicon file
  outputdir             Write output files to this directory

optional arguments:
  -h, --help            show this help message and exit
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
  --train-size-frac [TRAIN_SIZE_FRAC]
                        Size of the train set relative to valid lexicon size
                        (default: 0.9)
  --quiet               Do not print results to stdout
  --stats               Print statistics
  --output-script-only  Only output the Bash script to run the ML tool
  --output-script       Output the Bash script to run the ML tool
  --script-parameters [SCRIPT_PARAMETERS]
                        Parameters to configure the Bash script to run the ML
                        tool
```

## Examples

Create train/test/symbol files for Sequitur G2P:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex /tmp/

Created file: /tmp/enwiktionary-20160407.lex.train
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.symbols
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
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.symbols
```

Split the given lexicon into 80% train + 20% test (instead of default 90% + 10%):

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
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.symbols
```

Output a Bash script to run Sequitur G2P:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex /tmp/ --output-script

Created file: /tmp/enwiktionary-20160407.lex.train
Created file: /tmp/enwiktionary-20160407.lex.test
Created file: /tmp/enwiktionary-20160407.lex.symbols
Created file: /tmp/run_sequitur.sh
```

Create only the Bash script:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean  /tmp/ --output-script-only

Created file: /tmp/run_sequitur.sh
```



