# ipacleaner 

**Clean and normalize IPA strings** mined from a MediaWiki dump file.


## Input

A UTF-8 encoded plain-text **lexicon file**,
where each line represents a word.
Each line should contain at least two fields,
the word and the IPA string of its pronunciation,
separated by a field separator character.

By default, the field separator is assumed to be the tab character (``U+0009 TAB``),
and the word and IPA fields the first and second one of each row.
Lines beginning with ``#`` (``U+0023 NUMBER SIGN``) are ignored.


## Output

A **new lexicon file** where the IPA string has been **cleaned** and **normalized**.

**Cleaned** means that Unicode characters commonly used in MediaWiki but not IPA valid
have been translated to the correct IPA character.
For example, to indicate the primary stress ``U+0027 APOSTROPHE`` is commonly used,
but the correct IPA character is ``U+02C8 MODIFIER LETTER VERTICAL LINE``.

**Normalized** means that the (cleaned) Unicode string has been parsed into a list
of IPA characters, possibly grouping multiple Unicode characters,
(e.g., ``t͡ʃ`` are 3 Unicode characters which correspond to a single IPA character),
and/or replacing non-preferred representations with the canonical ones
(e.g., the deprecated 1 Unicode character ligature ``ʧ`` is translated to the canonical ``t͡ʃ``).

Note that, by default, the output IPA string contains:

* consonants
* vowels
* stress marks
* length marks

That is, diacritics, tone marks, and word/syllable breaks are removed.
You can change this behavior using the ``--format`` parameter.

Also note that (word, cleaned+normalized IPA) pairs
are output only if cleaned Unicode string is IPA valid.
In other words, if after the cleaning step the Unicode string
still contains characters that are not IPA valid,
the pair (word, cleaned IPA) is discarded.
You can change this behavior using the ``--all`` parameter.
You can invert this behavior, that is, printing only the words with invalid IPA,
using the ``--invald`` parameter.


## Usage

```bash
$ python -m wiktts.ipacleaner LEXICON [OPTIONS]
```

Example:

```bash
$ python -m wiktts.ipacleaner enwiktionary-20160407.lex --output-file enwiktionary-20160407.lex.clean
```

Processing big lexicon files (>100k words) might take a couple of minutes.
The current code is not optimized for speed.

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.ipacleaner --help

usage: __main__.py [-h] [--output-file [OUTPUT_FILE]] [--format [FORMAT]]
                   [--comment [COMMENT]] [--delimiter [DELIMITER]]
                   [--word-index [WORD_INDEX]] [--ipa-index [IPA_INDEX]]
                   [--sort] [--quiet] [--stats] [--all] [--invalid]
                   lexicon

Clean and normalize IPA strings mined from a MediaWiki dump file.

positional arguments:
  lexicon               Lexicon file

optional arguments:
  -h, --help            show this help message and exit
  --output-file [OUTPUT_FILE]
                        Write output to file
  --format [FORMAT]     Format output according to this string (available
                        placeholders: {RVALID}, {CVALID}, {WORD}, {RIPA},
                        {RCV}, {RCVS}, {RCVSL}, {RCVSLW}, {RCVSLWS}{CIPA},
                        {CCV}, {CCVS}, {CCVSL}, {CCVSLW}, {CCVSLWS})
  --comment [COMMENT]   Ignore lines in the lexicon file starting with this
                        string (default: '#')
  --delimiter [DELIMITER]
                        Field delimiter of the lexicon file (default: '\t')
  --word-index [WORD_INDEX]
                        Field index of the word (default: 0)
  --ipa-index [IPA_INDEX]
                        Field index of the IPA string (default: 1)
  --sort                Sort the results
  --quiet               Do not print results to stdout
  --stats               Print the number of words with valid and invalid IPA
  --all                 Print results for all words (with or without valid IPA
                        after cleaning)
  --invalid             Print results for words with invalid IPA (after
                        cleaning)
```

## Example

Assuming a lexicon file ``enwiktionary-20160407.lex`` containing tab-separated pairs:

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
Aaronite	ˈeə(ɹ)n̩aɪt
Ab	ɑb
Ababda	ə.ˈbæb.də
...
```

invoking the following command:

```bash
$ python -m wiktts.ipacleaner enwiktionary-20160407.lex --output-file enwiktionary-20160407.lex.clean
```

will produce:

```
...
Aachen	ˈɑːkən
Aalesund	ˈɔləˌsʊn
Aalst	ɑlst
Aar	ɑɹ
Aarau	ˈaːra
Aare	ˈɑɹə
Aarhus	ˈɔːˌhuːs
Aaron	ˈɛəɹən
Aaronite	ˈeəɹnaɪt
Ab	ɑb
Ababda	əˈbæbdə
...
```



