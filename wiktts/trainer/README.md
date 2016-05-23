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

TBW

```

## Example

Assuming a clean lexicon file ``enwiktionary-20160407.lex.clean`` containing:

```
...
Aachen	ˈɑːkən
Aalesund	ˈɔ.ləˌsʊn
Aalst	ɑlst
Aar	ɑɹ
Aarau	ˈaːra
Aare	ˈɑ.ɹə
Aarhus	ˈɔːˌhuːs
Aaron	ˈɛəɹən
Aaronite	ˈeəɹn̩aɪt
Ab	ɑb
Ababda	ə.ˈbæb.də
...
```

invoking the following command:

```bash
$ python -m wiktts.trainer sequitur enwiktionary-20160407.lex.clean /tmp/
```

will produce:

```
TBW
```



