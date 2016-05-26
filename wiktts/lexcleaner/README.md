# lexcleaner 

**Clean and normalize a pronunciation lexicon** mined from a MediaWiki dump file.


## Input

A UTF-8 encoded plain-text **pronunciation lexicon file**,
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


## Output

A **new pronunciation lexicon file** where the word and IPA strings
has been **cleaned** and **normalized**.

**Cleaned** means that Unicode characters commonly used in MediaWiki but not IPA valid
have been translated to the corresponding valid IPA character.
For example, in MediaWiki the primary stress is often indicated with ``U+0027 APOSTROPHE``,
while the correct IPA character is ``U+02C8 MODIFIER LETTER VERTICAL LINE``.

**Normalized** means that the (cleaned) Unicode string has been parsed into a list
of IPA characters, possibly grouping multiple Unicode characters,
(e.g., ``t͡ʃ`` are 3 Unicode characters which correspond to a single IPA character),
and/or replacing non-preferred representations with the canonical ones
(e.g., the deprecated 1 Unicode character ligature ``ʧ`` is translated to the canonical ``t͡ʃ``).

Also note that by default (word, cleaned+normalized IPA) pairs
are output only if the cleaned Unicode string is IPA valid.
In other words, if after the cleaning step the Unicode string
still contains characters that are not IPA valid,
the pair (word, cleaned IPA) is discarded.
You can change this behavior using the ``--all`` and ``--comment-invalid`` parameters.
You can invert this behavior, that is, printing only the words with invalid IPA,
using the ``--invalid`` parameter.
If you override the default, the resulting IPA string will contain
all recognized IPA characters,
while characters that are not IPA valid will be ignored.


## Usage

```bash
$ python -m wiktts.lexcleaner LEXICON [OPTIONS]
```

Example:

```bash
$ python -m wiktts.lexcleaner enwiktionary-20160407.lex --output-file enwiktionary-20160407.lex.clean
```

Processing big lexicon files (>100k words) might take a couple of minutes.
The current code is not optimized for speed.

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.lexcleaner

usage: __main__.py [-h] [--output-file [OUTPUT_FILE]]
                   [--letter-file [LETTER_FILE]] [--phone-file [PHONE_FILE]]
                   [--word-cleaner-file [WORD_CLEANER_FILE]]
                   [--ipa-cleaner-file [IPA_CLEANER_FILE]] [--format [FORMAT]]
                   [--comment [COMMENT]] [--delimiter [DELIMITER]]
                   [--word-index [WORD_INDEX]] [--ipa-index [IPA_INDEX]]
                   [--no-sort] [--quiet] [--stats] [--all] [--comment-invalid]
                   [--invalid] [--lowercase]
                   lexicon

Clean and normalize a pronunciation lexicon.

positional arguments:
  lexicon               Input lexicon file

optional arguments:
  -h, --help            show this help message and exit
  --output-file [OUTPUT_FILE]
                        Write output to file
  --letter-file [LETTER_FILE]
                        Write list of symbols (in words) to file
  --phone-file [PHONE_FILE]
                        Write list of symbols (in IPA strings) to file
  --word-cleaner-file [WORD_CLEANER_FILE]
                        Apply replacements from the given file to words
  --ipa-cleaner-file [IPA_CLEANER_FILE]
                        Apply replacements from the given file to IPA strings
  --format [FORMAT]     Format output according to this template (available
                        placeholders: {RWORDUNI}, {RIPAUNI}, {RIPAUNIVALID},
                        {RIPA}, {RCV}, {RCVP}, {RCVS}, {RCVPL}, {RCVSL},
                        {RCVSLW}, {RCVSLWS}, {CWORDUNI}, {CIPAUNI},
                        {CIPAUNIVALID}, {CIPA}, {CCV}, {CCVP}, {CCVS},
                        {CCVPL}, {CCVSL}, {CCVSLW}, {CCVSLWS})
  --comment [COMMENT]   Ignore lines in the lexicon file starting with this
                        string (default: '#')
  --delimiter [DELIMITER]
                        Field delimiter of the lexicon file (default: '\t')
  --word-index [WORD_INDEX]
                        Field index of the word (default: 0)
  --ipa-index [IPA_INDEX]
                        Field index of the IPA string (default: 1)
  --no-sort             Do not sort the results
  --quiet               Do not print results to stdout
  --stats               Print statistics
  --all                 Print results for all words (with or without valid IPA
                        after cleaning)
  --comment-invalid     Comment lines regarding words with invalid IPA (after
                        cleaning; you might want --no-sort as well)
  --invalid             Print results for words with invalid IPA (after
                        cleaning)
  --lowercase           Lowercase all the words
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
...
aacu	ækʊ/
aalii	ɑːˈliːiː
aandblom	ˈɑːnt.blɒm
aardvark	ˈɑːd.vɑːk
aardwolf	ˈɑːdˌwʊlf
aardwolves	ˈɑrdˌwʊlvz
aasvoel	ˈɑs.ˌfoʊ.əl
aasvogel	ˈɑːsˌfəʊ.ɡəl
ab	æb
ab extra	æb ˈɛk.strə
ab intra	ˌæb ˈɪn.trə
ab ovo	æ.ˈboʊ.ˌvoʊ
ab utili	æb ˈju.tl̩.i
...
```

invoking the following command:

```bash
$ python -m wiktts.lexcleaner enwiktionary-20160407.lex \
    --output-file enwiktionary-20160407.lex.clean \
    --letter-file enwiktionary-20160407.lex.letters \
    --phone-file enwiktionary-20160407.lex.phones
```

will produce:

1. ``enwiktionary-20160407.lex.clean``:
    ```
    ...
aachen	ˈɑːkən
aacu	ækʊ
aalesund	ˈɔ.ləˌsʊn
aalii	ɑːˈliːiː
aalst	ɑlst
aandblom	ˈɑːnt.blɒm
aar	ɑɹ
aarau	ˈaːra
aardvark	ˈɑːd.vɑːk
aardwolf	ˈɑːdˌwʊlf
aardwolves	ˈɑrdˌwʊlvz
aare	ˈɑ.ɹə
aarhus	ˈɔːˌhuːs
aaron	ˈɛəɹən
aaronite	ˈeəɹn̩aɪt
aarp	eɪ eɪ ɑɹ ˈpi
aasvoel	ˈɑs.ˌfoʊ.əl
aasvogel	ˈɑːsˌfəʊ.ɡəl
ab	æb
ab	ɑb
    ...
    ```

2. ``enwiktionary-20160407.lex.letters``:
    ```
' '	SPACE (U+0020)
'!'	EXCLAMATION MARK (U+0021)
'&'	AMPERSAND (U+0026)
'''	APOSTROPHE (U+0027)
'*'	ASTERISK (U+002A)
'+'	PLUS SIGN (U+002B)
','	COMMA (U+002C)
'-'	HYPHEN-MINUS (U+002D)
'.'	FULL STOP (U+002E)
'/'	SOLIDUS (U+002F)
'0'	DIGIT ZERO (U+0030)
'1'	DIGIT ONE (U+0031)
'2'	DIGIT TWO (U+0032)
'3'	DIGIT THREE (U+0033)
'4'	DIGIT FOUR (U+0034)
'5'	DIGIT FIVE (U+0035)
'6'	DIGIT SIX (U+0036)
'7'	DIGIT SEVEN (U+0037)
'8'	DIGIT EIGHT (U+0038)
'9'	DIGIT NINE (U+0039)
'@'	COMMERCIAL AT (U+0040)
'a'	LATIN SMALL LETTER A (U+0061)
'b'	LATIN SMALL LETTER B (U+0062)
'c'	LATIN SMALL LETTER C (U+0063)
...
'ř'	LATIN SMALL LETTER R WITH CARON (U+0159)
'ū'	LATIN SMALL LETTER U WITH MACRON (U+016B)
'ž'	LATIN SMALL LETTER Z WITH CARON (U+017E)
'ǁ'	LATIN LETTER LATERAL CLICK (U+01C1)
'ǃ'	LATIN LETTER RETROFLEX CLICK (U+01C3)
'ș'	LATIN SMALL LETTER S WITH COMMA BELOW (U+0219)
'σ'	GREEK SMALL LETTER SIGMA (U+03C3)
'₂'	SUBSCRIPT TWO (U+2082)
    ```

3. ``enwiktionary-20160407.lex.phones``:
    ```
' '	word-break suprasegmental (U+0020)
'.'	syllable-break suprasegmental (U+002E)
'a'	open front unrounded vowel (U+0061)
'ä'	open central unrounded vowel (U+0061 U+0308)
'b'	voiced bilabial plosive consonant (U+0062)
'c'	voiceless palatal plosive consonant (U+0063)
'd'	voiced alveolar plosive consonant (U+0064)
'd̪'	voiced dental plosive consonant (U+0064 U+032A)
'd͡b'	voiced labio-alveolar plosive consonant (U+0064 U+0361 U+0062)
'd͡z'	voiced alveolar sibilant-affricate consonant (U+0064 U+0361 U+007A)
...
'̬'	voiced diacritic (U+032C)
'̯'	non-syllabic diacritic (U+032F)
'̰'	creaky-voiced diacritic (U+0330)
'͡'	tie-bar-above diacritic (U+0361)
'θ'	voiceless dental non-sibilant-fricative consonant (U+03B8)
'χ'	voiceless uvular non-sibilant-fricative consonant (U+03C7)
'‿'	linking suprasegmental (U+203F)
    ```



