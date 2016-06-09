# wiktts.lexcleaner 

**Clean and normalize a pronunciation lexicon**.


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
* the word and pronunciation fields are the first and second fields of each line.

You can change these defaults with the ``--comment``, ``--delimiter``, and
``--word-index``/``--pron-index`` parameters.


## Output

Four files will be created in the specified output directory:

* a ``.clean`` **new pronunciation lexicon file** where the word and pronunciation strings
  have been **cleaned** and **normalized**;
* a ``.letters`` file listing all the characters appearing in the words of the lexicon;
* a ``.phones`` file listing all the phones appearing in the pronunciation strings of the lexicon; and
* a ``.cleaner_stats`` file, containing the statistics of the cleaning process.

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


## Usage

```bash
$ python -m wiktts.lexcleaner LEXICON OUTPUTDIR [OPTIONS]
```

Example:

```bash
$ python -m wiktts.lexcleaner enwiktionary-20160407.lex /tmp/
```

Processing big lexicon files (>100k words) might take a couple of minutes.
The current code is not optimized for speed.

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.lexcleaner --help

usage: wiktts.lexcleaner [-h] [--chars [CHARS]]
                         [--word-cleaner [WORD_CLEANER]]
                         [--pron-cleaner [PRON_CLEANER]] [--format [FORMAT]]
                         [--comment [COMMENT]] [--delimiter [DELIMITER]]
                         [--word-index [WORD_INDEX]]
                         [--pron-index [PRON_INDEX]] [--lowercase]
                         [--comment-invalid] [--all] [--invalid] [--no-sort]
                         [--stats] [--stdout]
                         lexicon outputdir

Clean and normalize a pronunciation lexicon.

positional arguments:
  lexicon               Input lexicon file
  outputdir             Output files in this directory

optional arguments:
  -h, --help            show this help message and exit
  --chars [CHARS]       Map only the specified IPA characters
                        [all|letters|cvp|cvs|cvpl|cvsl|cvslw|cvslws] (default:
                        'all')
  --word-cleaner [WORD_CLEANER]
                        Apply replacements from the given file to words
  --pron-cleaner [PRON_CLEANER]
                        Apply replacements from the given file to
                        pronunciation strings
  --format [FORMAT]     Format output according to this template (available
                        placeholders: {WORDUNI}, {PRONUNI}, {PRONUNIVALID},
                        {IPA}, {CWORDUNI}, {CPRONUNI}, {CPRONUNIVALID},
                        {CIPA}, {FIPA})
  --comment [COMMENT]   Ignore lines in the lexicon file starting with this
                        string (default: '#')
  --delimiter [DELIMITER]
                        Field delimiter of the lexicon file (default: '\t')
  --word-index [WORD_INDEX]
                        Field index of the word (default: 0)
  --pron-index [PRON_INDEX]
                        Field index of the pronunciation (default: 1)
  --lowercase           Lowercase all the words
  --comment-invalid     Comment lines containing words with invalid IPA
                        pronunciation (after cleaning; you might want --no-
                        sort as well)
  --all                 Print results for all words (with or without valid IPA
                        pronunciation after cleaning)
  --invalid             Print results for words with invalid IPA pronunciation
                        (after cleaning)
  --no-sort             Do not sort the results
  --stats               Print statistics
  --stdout              Print results to standard output
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
aabomycin	æbomɪsɪn
aacu	ækʊ/
aalii	ɑːˈliːiː
aandblom	ˈɑːnt.blɒm
aardvark	ˈɑːd.vɑːk
aardwolf	ˈɑːdˌwʊlf
aardwolves	ˈɑrdˌwʊlvz
aasvoel	ˈɑs.ˌfoʊ.əl
aasvogel	ˈɑːsˌfəʊ.ɡəl
...
```

invoking the following command:

```bash
$ python -m wiktts.lexcleaner enwiktionary-20160407.lex /tmp/
```

will produce:

1. ``/tmp/enwiktionary-20160407.lex.clean``:
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
...
aabomycin	æbomɪsɪn
aacu	ækʊ
aalii	ɑːˈliːiː
aandblom	ˈɑːnt.blɒm
aardvark	ˈɑːd.vɑːk
aardwolf	ˈɑːdˌwʊlf
aardwolves	ˈɑrdˌwʊlvz
aasvoel	ˈɑs.ˌfoʊ.əl
aasvogel	ˈɑːsˌfəʊ.ɡəl
...
    ```

2. ``/tmp/enwiktionary-20160407.lex.letters``:
    ```
 	U+0020	SPACE
!	U+0021	EXCLAMATION MARK
&	U+0026	AMPERSAND
'	U+0027	APOSTROPHE
*	U+002A	ASTERISK
+	U+002B	PLUS SIGN
,	U+002C	COMMA
-	U+002D	HYPHEN-MINUS
.	U+002E	FULL STOP
/	U+002F	SOLIDUS
0	U+0030	DIGIT ZERO
1	U+0031	DIGIT ONE
2	U+0032	DIGIT TWO
3	U+0033	DIGIT THREE
4	U+0034	DIGIT FOUR
5	U+0035	DIGIT FIVE
6	U+0036	DIGIT SIX
7	U+0037	DIGIT SEVEN
8	U+0038	DIGIT EIGHT
9	U+0039	DIGIT NINE
@	U+0040	COMMERCIAL AT
A	U+0041	LATIN CAPITAL LETTER A
B	U+0042	LATIN CAPITAL LETTER B
C	U+0043	LATIN CAPITAL LETTER C
D	U+0044	LATIN CAPITAL LETTER D
E	U+0045	LATIN CAPITAL LETTER E
F	U+0046	LATIN CAPITAL LETTER F
G	U+0047	LATIN CAPITAL LETTER G
H	U+0048	LATIN CAPITAL LETTER H
I	U+0049	LATIN CAPITAL LETTER I
J	U+004A	LATIN CAPITAL LETTER J
K	U+004B	LATIN CAPITAL LETTER K
L	U+004C	LATIN CAPITAL LETTER L
M	U+004D	LATIN CAPITAL LETTER M
N	U+004E	LATIN CAPITAL LETTER N
O	U+004F	LATIN CAPITAL LETTER O
P	U+0050	LATIN CAPITAL LETTER P
Q	U+0051	LATIN CAPITAL LETTER Q
R	U+0052	LATIN CAPITAL LETTER R
S	U+0053	LATIN CAPITAL LETTER S
T	U+0054	LATIN CAPITAL LETTER T
U	U+0055	LATIN CAPITAL LETTER U
V	U+0056	LATIN CAPITAL LETTER V
W	U+0057	LATIN CAPITAL LETTER W
X	U+0058	LATIN CAPITAL LETTER X
Y	U+0059	LATIN CAPITAL LETTER Y
Z	U+005A	LATIN CAPITAL LETTER Z
a	U+0061	LATIN SMALL LETTER A
b	U+0062	LATIN SMALL LETTER B
c	U+0063	LATIN SMALL LETTER C
d	U+0064	LATIN SMALL LETTER D
e	U+0065	LATIN SMALL LETTER E
f	U+0066	LATIN SMALL LETTER F
g	U+0067	LATIN SMALL LETTER G
h	U+0068	LATIN SMALL LETTER H
i	U+0069	LATIN SMALL LETTER I
j	U+006A	LATIN SMALL LETTER J
k	U+006B	LATIN SMALL LETTER K
l	U+006C	LATIN SMALL LETTER L
m	U+006D	LATIN SMALL LETTER M
n	U+006E	LATIN SMALL LETTER N
o	U+006F	LATIN SMALL LETTER O
p	U+0070	LATIN SMALL LETTER P
q	U+0071	LATIN SMALL LETTER Q
r	U+0072	LATIN SMALL LETTER R
s	U+0073	LATIN SMALL LETTER S
t	U+0074	LATIN SMALL LETTER T
u	U+0075	LATIN SMALL LETTER U
v	U+0076	LATIN SMALL LETTER V
w	U+0077	LATIN SMALL LETTER W
x	U+0078	LATIN SMALL LETTER X
y	U+0079	LATIN SMALL LETTER Y
z	U+007A	LATIN SMALL LETTER Z
Á	U+00C1	LATIN CAPITAL LETTER A WITH ACUTE
Æ	U+00C6	LATIN CAPITAL LETTER AE
É	U+00C9	LATIN CAPITAL LETTER E WITH ACUTE
Ü	U+00DC	LATIN CAPITAL LETTER U WITH DIAERESIS
à	U+00E0	LATIN SMALL LETTER A WITH GRAVE
á	U+00E1	LATIN SMALL LETTER A WITH ACUTE
â	U+00E2	LATIN SMALL LETTER A WITH CIRCUMFLEX
ä	U+00E4	LATIN SMALL LETTER A WITH DIAERESIS
æ	U+00E6	LATIN SMALL LETTER AE
ç	U+00E7	LATIN SMALL LETTER C WITH CEDILLA
è	U+00E8	LATIN SMALL LETTER E WITH GRAVE
é	U+00E9	LATIN SMALL LETTER E WITH ACUTE
ê	U+00EA	LATIN SMALL LETTER E WITH CIRCUMFLEX
ë	U+00EB	LATIN SMALL LETTER E WITH DIAERESIS
í	U+00ED	LATIN SMALL LETTER I WITH ACUTE
î	U+00EE	LATIN SMALL LETTER I WITH CIRCUMFLEX
ñ	U+00F1	LATIN SMALL LETTER N WITH TILDE
ó	U+00F3	LATIN SMALL LETTER O WITH ACUTE
ô	U+00F4	LATIN SMALL LETTER O WITH CIRCUMFLEX
õ	U+00F5	LATIN SMALL LETTER O WITH TILDE
ö	U+00F6	LATIN SMALL LETTER O WITH DIAERESIS
ø	U+00F8	LATIN SMALL LETTER O WITH STROKE
ú	U+00FA	LATIN SMALL LETTER U WITH ACUTE
û	U+00FB	LATIN SMALL LETTER U WITH CIRCUMFLEX
ü	U+00FC	LATIN SMALL LETTER U WITH DIAERESIS
ą	U+0105	LATIN SMALL LETTER A WITH OGONEK
ć	U+0107	LATIN SMALL LETTER C WITH ACUTE
č	U+010D	LATIN SMALL LETTER C WITH CARON
ē	U+0113	LATIN SMALL LETTER E WITH MACRON
ı	U+0131	LATIN SMALL LETTER DOTLESS I
ń	U+0144	LATIN SMALL LETTER N WITH ACUTE
Œ	U+0152	LATIN CAPITAL LIGATURE OE
œ	U+0153	LATIN SMALL LIGATURE OE
ř	U+0159	LATIN SMALL LETTER R WITH CARON
ū	U+016B	LATIN SMALL LETTER U WITH MACRON
ž	U+017E	LATIN SMALL LETTER Z WITH CARON
ǁ	U+01C1	LATIN LETTER LATERAL CLICK
ǃ	U+01C3	LATIN LETTER RETROFLEX CLICK
ș	U+0219	LATIN SMALL LETTER S WITH COMMA BELOW
σ	U+03C3	GREEK SMALL LETTER SIGMA
₂	U+2082	SUBSCRIPT TWO
    ```

3. ``/tmp/enwiktionary-20160407.lex.phones``:
    ```
 	word-break suprasegmental (U+0020)
.	syllable-break suprasegmental (U+002E)
a	open front unrounded vowel (U+0061)
b	voiced bilabial plosive consonant (U+0062)
c	voiceless palatal plosive consonant (U+0063)
d	voiced alveolar plosive consonant (U+0064)
d̪	voiced dental plosive consonant (U+0064 U+032A)
d͡b	voiced labio-alveolar plosive consonant (U+0064 U+0361 U+0062)
d͡z	voiced alveolar sibilant-affricate consonant (U+0064 U+0361 U+007A)
d͡ʒ	voiced palato-alveolar sibilant-affricate consonant (U+0064 U+0361 U+0292)
e	close-mid front unrounded vowel (U+0065)
f	voiceless labio-dental non-sibilant-fricative consonant (U+0066)
h	voiceless glottal non-sibilant-fricative consonant (U+0068)
i	close front unrounded vowel (U+0069)
j	voiced palatal approximant consonant (U+006A)
k	voiceless velar plosive consonant (U+006B)
kʼ	voiceless velar ejective consonant (U+006B U+02BC)
k͡p	voiceless labio-velar plosive consonant (U+006B U+0361 U+0070)
l	voiced alveolar lateral-approximant consonant (U+006C)
lˠ	voiced alveolar lateral-approximant velarized consonant (U+006C U+02E0)
m	voiced bilabial nasal consonant (U+006D)
n	voiced alveolar nasal consonant (U+006E)
n͡m	voiced labio-alveolar nasal consonant (U+006E U+0361 U+006D)
o	close-mid back rounded vowel (U+006F)
p	voiceless bilabial plosive consonant (U+0070)
q͡χ	voiceless uvular non-sibilant-affricate consonant (U+0071 U+0361 U+03C7)
r	voiced alveolar trill consonant (U+0072)
s	voiceless alveolar sibilant-fricative consonant (U+0073)
t	voiceless alveolar plosive consonant (U+0074)
t̪	voiceless dental plosive consonant (U+0074 U+032A)
t͡p	voiceless labio-alveolar plosive consonant (U+0074 U+0361 U+0070)
t͡s	voiceless alveolar sibilant-affricate consonant (U+0074 U+0361 U+0073)
t͡ʃ	voiceless palato-alveolar sibilant-affricate consonant (U+0074 U+0361 U+0283)
u	close back rounded vowel (U+0075)
v	voiced labio-dental non-sibilant-fricative consonant (U+0076)
w	voiced labio-velar approximant consonant (U+0077)
x	voiceless velar non-sibilant-fricative consonant (U+0078)
y	close front rounded vowel (U+0079)
z	voiced alveolar sibilant-fricative consonant (U+007A)
æ	near-open front unrounded vowel (U+00E6)
ç	voiceless palatal non-sibilant-fricative consonant (U+00E7)
ð	voiced dental non-sibilant-fricative consonant (U+00F0)
ø	close-mid front rounded vowel (U+00F8)
ŋ	voiced velar nasal consonant (U+014B)
ŋ͡m	voiced labio-velar nasal consonant (U+014B U+0361 U+006D)
œ	open-mid front rounded vowel (U+0153)
ǀ	voiceless dental click consonant (U+01C0)
ɐ	near-open central unrounded vowel (U+0250)
ɑ	open back unrounded vowel (U+0251)
ɒ	open back rounded vowel (U+0252)
ɔ	open-mid back rounded vowel (U+0254)
ɕ	voiceless alveolo-palatal sibilant-fricative consonant (U+0255)
ɘ	close-mid central unrounded vowel (U+0258)
ə	mid central unrounded vowel (U+0259)
ɚ	mid central unrounded rhotacized vowel (U+025A)
ɛ	open-mid front unrounded vowel (U+025B)
ɜ	open-mid central unrounded vowel (U+025C)
ɝ	open-mid central unrounded rhotacized vowel (U+025D)
ɡ	voiced velar plosive consonant (U+0261)
ɡ͡b	voiced labio-velar plosive consonant (U+0261 U+0361 U+0062)
ɥ	voiced labio-palatal approximant consonant (U+0265)
ɦ	voiced glottal non-sibilant-fricative consonant (U+0266)
ɨ	close central unrounded vowel (U+0268)
ɪ	near-close near-front unrounded vowel (U+026A)
ɪ̈	near-close central unrounded vowel (U+026A U+0308)
ɬ	voiceless alveolar lateral-fricative consonant (U+026C)
ɭ	voiced retroflex lateral-approximant consonant (U+026D)
ɯ	close back unrounded vowel (U+026F)
ɱ	voiced labio-dental nasal consonant (U+0271)
ɲ	voiced palatal nasal consonant (U+0272)
ɵ	close-mid central rounded vowel (U+0275)
ɶ	open front rounded vowel (U+0276)
ɸ	voiceless bilabial non-sibilant-fricative consonant (U+0278)
ɹ	voiced alveolar approximant consonant (U+0279)
ɹ̥	voiceless alveolar approximant consonant (U+0279 U+0325)
ɻ	voiced retroflex approximant consonant (U+027B)
ɽ	voiced retroflex flap consonant (U+027D)
ɾ	voiced alveolar flap consonant (U+027E)
ʀ	voiced uvular trill consonant (U+0280)
ʁ	voiced uvular non-sibilant-fricative consonant (U+0281)
ʂ	voiceless retroflex sibilant-fricative consonant (U+0282)
ʃ	voiceless palato-alveolar sibilant-fricative consonant (U+0283)
ʈ	voiceless retroflex plosive consonant (U+0288)
ʉ	close central rounded vowel (U+0289)
ʊ	near-close near-back rounded vowel (U+028A)
ʊ̈	near-close central rounded vowel (U+028A U+0308)
ʌ	open-mid back unrounded vowel (U+028C)
ʍ	voiceless labio-velar approximant consonant (U+028D)
ʏ	near-close near-front rounded vowel (U+028F)
ʒ	voiced palato-alveolar sibilant-fricative consonant (U+0292)
ʔ	voiceless glottal plosive consonant (U+0294)
ʙ	voiced bilabial trill consonant (U+0299)
ʰ	aspirated diacritic (U+02B0)
ʲ	palatalized diacritic (U+02B2)
ʳ	alveolar trill diacritic (U+02B3)
ʷ	labialized diacritic (U+02B7)
ˈ	primary-stress suprasegmental (U+02C8)
ˌ	secondary-stress suprasegmental (U+02CC)
ː	long suprasegmental (U+02D0)
ˑ	half-long suprasegmental (U+02D1)
˞	rhotacized diacritic (U+02DE)
ˠ	velarized diacritic (U+02E0)
ˡ	lateral-release diacritic (U+02E1)
̀	low-level tone (U+0300)
́	high-level tone (U+0301)
̃	nasalized diacritic (U+0303)
̆	extra-short suprasegmental (U+0306)
̙	retracted-tongue-root diacritic (U+0319)
̚	no-audible-release diacritic (U+031A)
̝	raised diacritic (U+031D)
̥	voiceless diacritic (U+0325)
̩	syllabic diacritic (U+0329)
̪	dental diacritic (U+032A)
̬	voiced diacritic (U+032C)
̯	non-syllabic diacritic (U+032F)
̰	creaky-voiced diacritic (U+0330)
͡	tie-bar-above diacritic (U+0361)
θ	voiceless dental non-sibilant-fricative consonant (U+03B8)
χ	voiceless uvular non-sibilant-fricative consonant (U+03C7)
‿	linking suprasegmental (U+203F)
    ```

4. ``/tmp/enwiktionary-20160407.lex.cleaner_stats``:
    ```
Lexicon path:          enwiktionary-20160407.lex
Output directory:      /tmp/
Word cleaner:          None
Pronunciation cleaner: None
Lowercase word:        False
Sort words:            True
Include valid:         True
Include invalid:       False
Words
  Total:           36967
  Raw Valid:       33871 (91.625%)
  Raw Invalid:     3096 (8.375%)
  Cleaned Valid:   36952 (99.959%)
  Cleaned Invalid: 15 (0.041%)
    ```



