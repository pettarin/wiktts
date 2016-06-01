# wiktts.trainer 

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

Examples:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --script-only
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --lowercase
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --train-size-frac 0.8
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --mapper kirshenbaum
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --mapper arpabet 
```

Processing big lexicon files (>100k words) might take a couple of minutes.
The current code is not optimized for speed.

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.trainer --help

usage: wiktts.trainer [-h] [--chars [CHARS]] [--mapper [MAPPER]]
                      [--comment [COMMENT]] [--delimiter [DELIMITER]]
                      [--word-index [WORD_INDEX]] [--ipa-index [IPA_INDEX]]
                      [--train-size-int [TRAIN_SIZE_INT]]
                      [--train-size-frac [TRAIN_SIZE_FRAC]] [--stats]
                      [--script-only]
                      [--script-parameters [SCRIPT_PARAMETERS]] [--lowercase]
                      tool lexicon outputdir

Prepare train/test/symbol files for ML tools.

positional arguments:
  tool                  ML tool
                        [sequitur|phonetisaurus_08a|phonetisaurus_master]
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
  --stats               Print statistics
  --script-only         Only output the Bash script to run the ML tool
  --script-parameters [SCRIPT_PARAMETERS]
                        Parameters to configure the Bash script to run the ML
                        tool
  --lowercase           Lowercase all the words
```


## Example

Assuming a clean lexicon file ``enwiktionary-20160407.lex.clean`` exists:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/

Created file: /tmp/enwiktionary-20160407.lex.clean.train
Created file: /tmp/enwiktionary-20160407.lex.clean.train.words
Created file: /tmp/enwiktionary-20160407.lex.clean.train.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.test
Created file: /tmp/enwiktionary-20160407.lex.clean.test.words
Created file: /tmp/enwiktionary-20160407.lex.clean.test.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.words
Created file: /tmp/enwiktionary-20160407.lex.clean.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.trainer_stats
Created file: /tmp/run_sequitur.sh
```

where the first lines of ``/tmp/enwiktionary-20160407.lex.clean.train`` look like:

```
coelacanth 013 046 005 038 082 085 007 050
sixths 013 092 082 013
rorqual 014 024 014 082 017 038 005
complexity 082 038 028 031 005 089 082 013 092 009 046
Hannah 056 085 007 038
colthood 082 038 090 005 009 056 090 008
dinghy 008 092 069 081 046
lidar 005 087 092 008 025 001
broiler 030 001 026 092 005 038
...
```

and ``/tmp/enwiktionary-20160407.lex.clean.symbols`` has the symbol-to-IPA map:

```
001	voiced alveolar approximant consonant	ɹ
002	voiceless alveolar approximant consonant	ɹ̥
003	voiced alveolar flap consonant	ɾ
004	voiced alveolar lateral-approximant velarized consonant	lˠ
005	voiced alveolar lateral-approximant consonant	l
006	voiceless alveolar lateral-fricative consonant	ɬ
007	voiced alveolar nasal consonant	n
008	voiced alveolar plosive consonant	d
009	voiceless alveolar plosive consonant	t
...
```

To create the Bash script only:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --script-only

Created file: /tmp/run_sequitur.sh
```

To print statistics:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --stats

Created file: /tmp/enwiktionary-20160407.lex.clean.train
Created file: /tmp/enwiktionary-20160407.lex.clean.train.words
Created file: /tmp/enwiktionary-20160407.lex.clean.train.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.test
Created file: /tmp/enwiktionary-20160407.lex.clean.test.words
Created file: /tmp/enwiktionary-20160407.lex.clean.test.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.words
Created file: /tmp/enwiktionary-20160407.lex.clean.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.trainer_stats
Created file: /tmp/run_sequitur.sh
Words:
  Total: 36954
  Train: 33258
  Test:  3696
Symbols:
  Total: 92
  Train: 92
  Test:  63
```

To use the Kirshenbaum ASCII IPA mapper:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --mapper kirshenbaum

Created file: /tmp/enwiktionary-20160407.lex.clean.train
Created file: /tmp/enwiktionary-20160407.lex.clean.train.words
Created file: /tmp/enwiktionary-20160407.lex.clean.train.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.test
Created file: /tmp/enwiktionary-20160407.lex.clean.test.words
Created file: /tmp/enwiktionary-20160407.lex.clean.test.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.words
Created file: /tmp/enwiktionary-20160407.lex.clean.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.trainer_stats
Created file: /tmp/run_sequitur.sh
```

where the first lines of ``/tmp/enwiktionary-20160407.lex.clean.train`` look like:

```
zooplasty z o U @ p l & s t i
duppy d V p i
sedge s E dZ
cinema s I n @ m A
Ogham o U @ m
pegs p E g z
cen- s i n
down d a U n
pedication p E d I k e I S @ n
...
```



