# wiktts.trainer 

Prepare train/test/symbol files for ML tools.


## Input

A UTF-8 encoded plain-text **clean+normalized lexicon file**,
where each line represents a word.
Each line should contain at least two fields,
the word and its pronunciation,
separated by a field separator character.
Each line might contain additional fields.

By default:
* lines beginning with ``#`` (``U+0023 NUMBER SIGN``) are ignored;
* the field separator is the tab character (``U+0009 TAB``); and
* the word and pronunciation fields are the first and second fields of each line.

You can change these defaults with the ``--comment``, ``--delimiter``, and
``--word-index``/``--pron-index`` parameters.

Currently, the following tools are supported:

* [Sequitur](https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html)
* [Phonetisaurus (latest commit on GitHub master)](https://github.com/AdolfVonKleist/Phonetisaurus)
  (NOTE: the "test" code has been adapted from the self-evaluation code in v0.8.
  You might want to use ``wiktts.lexdiffer`` to compare e.g. the test (known) lexicon and
  the results of the trained model applied to the same word list.)
* [Phonetisaurus v0.8a](https://code.google.com/archive/p/phonetisaurus/)
  (IMPORTANT NOTE: v0.8a does not seems to support UTF-8 encoded train/test files,
  and only works for ASCII encoded files.
  Hence, you might need to remove non-ASCII characters from the words in your lexicon
  if you intend to use this version of Phonetisaurus.)


## Output

A set of files will be created in the given directory,
with a syntax appropriate for the specified ML tool:

* a set of **train files**
  (``.train``, ``.train.tab``, ``.train.words``, ``.train.symbols``),
  used to train a ML model;
* a set of **test files**
  (``.test``, ``.test.tab``, ``.test.words``, ``.test.symbols``),
  used to test the trained ML model;
* a set of **lexicon files**,
  (``.tab``, ``.words``, ``.symbols``),
  not directly used in training/testing a ML model,
  but that might be useful for later evaluation;
* a **trainer statistics files** (``.trainer_stats``); and
* a **Bash script** to train/test/apply the ML model.

For the first three sets of files:

* ``.tab`` contains the corrisponding lexicon, tab-separated
  (format accepted by other tools like ``wiktts.lexdiffer``),
  even if e.g. ``.train`` is space-separated;
* ``.words`` contains only the words in the lexicon, one per line;
* ``.symbols`` contains the mapping from symbol to IPA descriptors
  used to create the train/test files.


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
                      [--word-index [WORD_INDEX]] [--pron-index [PRON_INDEX]]
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
  --chars [CHARS]       Map only the specified IPA characters
                        [all|letters|cvp|cvs|cvpl|cvsl|cvslw|cvslws] (default:
                        'letters')
  --mapper [MAPPER]     Map IPA characters using the specified mapper
                        [arpabet|auto|kirshenbaum] (default: 'auto')
  --comment [COMMENT]   Ignore lines in the lexicon file starting with this
                        string (default: '#')
  --delimiter [DELIMITER]
                        Field delimiter of the lexicon file (default: '\t')
  --word-index [WORD_INDEX]
                        Field index of the word (default: 0)
  --pron-index [PRON_INDEX]
                        Field index of the pronunciation (default: 1)
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

Assuming a clean lexicon file ``enwiktionary-20160407.lex.clean`` exists
in the current working directory:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/

Created file: /tmp/enwiktionary-20160407.lex.clean.train
Created file: /tmp/enwiktionary-20160407.lex.clean.train.tab
Created file: /tmp/enwiktionary-20160407.lex.clean.train.words
Created file: /tmp/enwiktionary-20160407.lex.clean.train.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.test
Created file: /tmp/enwiktionary-20160407.lex.clean.test.tab
Created file: /tmp/enwiktionary-20160407.lex.clean.test.words
Created file: /tmp/enwiktionary-20160407.lex.clean.test.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.tab
Created file: /tmp/enwiktionary-20160407.lex.clean.words
Created file: /tmp/enwiktionary-20160407.lex.clean.symbols
Created file: /tmp/enwiktionary-20160407.lex.clean.trainer_stats
Created file: /tmp/run_sequitur.sh
```

where the first lines of ``/tmp/enwiktionary-20160407.lex.clean.train`` look like:

```
avgas 085 062 081 085 013
cliquishly 082 005 046 082 092 079 005 046
foresyllable 063 023 014 013 092 005 038 030 004
matting 028 085 009 092 069
declarator 008 089 082 005 038 001 048 092 009 038 001
ever 089 062 038
opisthokont 024 031 092 013 050 038 090 082 024 007 009
silflay 013 092 005 063 005 048 092
somehow 013 027 028 056 087 090
...
```

and ``/tmp/enwiktionary-20160407.lex.clean.symbols`` has the symbol-to-IPA map:

```
001	voiced alveolar approximant consonant	(ɹ)
002	voiceless alveolar approximant consonant	(ɹ̥)
003	voiced alveolar flap consonant	(ɾ)
004	voiced alveolar lateral-approximant velarized consonant	(lˠ)
005	voiced alveolar lateral-approximant consonant	(l)
006	voiceless alveolar lateral-fricative consonant	(ɬ)
007	voiced alveolar nasal consonant	(n)
008	voiced alveolar plosive consonant	(d)
009	voiceless alveolar plosive consonant	(t)
...
```

If you just need to output the Bash script,
the following command is faster:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --script-only

Created file: /tmp/run_sequitur.sh
```

The ``--stats`` switch prints onstdout
the statistics also saved into the ``.trainer_stats`` file:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --stats
...
Lexicon path:          enwiktionary-20160407.lex.clean
Output directory:      /tmp/
Lowercase words:       False
Map IPA characters:    letters
Mapper:                auto
Tool:                  sequitur
Train size:            0.9
Words:
  Total: 36952
  Train: 33256
  Test:  3696
Symbols:
  Total: 92
  Train: 90
  Test:  70
```

To use the Kirshenbaum ASCII IPA mapper:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --mapper kirshenbaum

$ head -n 9 /tmp/enwiktionary-20160407.lex.clean.train

Davidson d e I v I d s @ n
abyssalrock @ b I s l r A. k
affairs @ f E r z
mimeo m I m I @ U
oncology A. N k A. l @ dZ i
definitely d E f I n I t l i
schrecklichkeit S r<trl> E k l I C k a I t
gas g & s
grandducal g r & n d d j u k @ l
```

By default, only consonants and vowels are mapped, and all the other IPA characters are ignored.
You can change this behavior with the ``--chars`` switch.
For example, ``cvpl`` will output letters, plus primary stress and long suprasegmentals:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/ --stats --chars cvpl 
...
Lexicon path:          enwiktionary-20160407.lex.clean
Output directory:      /tmp/
Lowercase words:       False
Map IPA characters:    cvpl
Mapper:                auto
Tool:                  sequitur
Train size:            0.9
Words:
  Total: 36952
  Train: 33256
  Test:  3696
Symbols:
  Total: 94
  Train: 94
  Test:  67
```

(Note how the total number of symbols went from 92 to 94.)



