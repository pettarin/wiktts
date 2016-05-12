# mwsplitter 

Split a MediaWiki dump into multiple files.

## Input

A MediaWiki dump file, either uncompressed (``.xml``) or compressed (``.xml.bz2``).

## Output

One or more XML files, containing a fixed number of MediaWiki pages each.

## Usage

```bash
$ python mwsplitter.py DUMP.XML[.BZ2] [OPTIONS]
```

Example:

```bash
$ python mwsplitter.py itwiktionary-20160407-pages-meta-current.xml.bz2 --output-dir /tmp/out/ --ns 0 --pages-per-chunk 1000 --stats
```

### Options

Invoke with ``--help`` to get the list of available options,
including how to modify the output file:

```bash
$ python mwsplitter.py --help
```




# mwminer 

Mine IPA strings from a MediaWiki dump.

## Input

A MediaWiki dump file, either uncompressed (``.xml``) or compressed (``.xml.bz2``), or a directory containing chunks (``.xml``).

## Output

An UTF-8 encoded file,
containing one tab-separated pair
``ID\tword\tIPA``
per line,
where:

* ``ID`` is the ``/mediawiki/page/id`` string,
* ``word`` is the ``/mediawiki/page/title`` string, and
* ``IPA`` is the IPA string mined for ``word``.

The mined word string is not modified in any way.

The mined IPA string is modified only
by removing the leading and trailing ``/.../`` or ``[...]``.
Hence, you might need to clean it further,
depending on the intended application.
For example, you might need to "normalize" it
by replacing digrams with two letters (``/ʧ/`` => ``/tS/``),
converting to ASCII-IPA (Kirshenbaum), etc.

## Usage

```bash
$ python mwminer.py PARSER DUMP [OPTIONS]
```

Example:

```bash
$ python mwminer.py itwiktionary itwiktionary-20160407-pages-meta-current.xml.bz2 --output-file itwiktionary-20160407.txt
```

Please note that processing big MediaWiki dump files will take several minutes.
(The ``mwsplitter`` and ``mwminer`` scripts have been optimized
for readability, improvability, and extensibility, not for fast processing.
MediaWiki dumps are published monthly, after all!)

It is advisible to store your intermediate results,
for example the list of IPA strings extracted from a dump,
into intermediate files.

### Options

Invoke with ``--help`` to get the list of available options,
including how to modify the output file:

```bash
$ python mwminer.py --help
```

## IPA Parsers

* ``dawiktionary``: Danish Wiktionary (poor recall)
* ``dewiktionary``: German Wiktionary
* ``enwiktionary``: English Wiktionary
* ``eswiktionary``: Spanish Wiktionary
* ``fiwiktionary``: Finnish Wiktionary (poor recall)
* ``frwiktionary``: French Wiktionary
* ``iswiktionary``: Icelandic Wiktionary (poor recall)
* ``itwiktionary``: Italian Wiktionary
* ``ltwiktionary``: Lithuanian Wiktionary (broken)
* ``lvwiktionary``: Latvian Wiktionary (broken)
* ``nlwiktionary``: Dutch Wiktionary
* ``nowiktionary``: Norwegian Wiktionary (broken)
* ``plwiktionary``: Polish Wiktionary
* ``ptwiktionary``: Portuguese Wiktionary (poor recall, needs work to distinguish pt-pt and pt-br)
* ``ruwiktionary``: Russian Wiktionary
* ``svwiktionary``: Swedish Wiktionary (poor recall)

To support a new language (say, ``zz``):

1. copy an existing parser from the ``parsers/`` directory, naming it ``zzwiktionary.py`` or ``zzwiki.py``,
2. modify it according to the markup convention of the zz-Wiktionary or zz-Wikipedia,
3. use ``zzwiktionary`` or ``zzwiki`` as the first argument.

An IPA parser processes the MediaWiki text of a ``<page>`` by:

1. locating the language block corresponding to the target language;
2. locating the pronunciation block inside the language block;
3. locating the IPA tag/template matching the provided regular expressions;
4. extracting the IPA string, associating it to the ``<title>`` value of the current ``<page>``.

Please note that a ``<page>`` might:

1. not contain a language block corresponding to the target language (e.g., only ``en`` inside the Italian Wiktionary);
2. contain more than one language block, only one (the first) matching the target language (e.g., ``it`` and ``en`` blocks inside the Italian Wiktionary);
3. not contain pronunciation blocks;
4. not contain a pronunciation block for the target language, but it might contain a pronunciation block for another language;
5. not contain IPA strings;
6. not contain an IPA string for the target language, but it might contain IPA strings for another language;
7. contain multiple IPA strings (e.g., UK/RP and US pronunciations for English, or Brazil/Portugal pronunciations for Portuguese);
8. combine audio and IPA string tags/templates;
9. contain IPA strings with Unicode characters that are invalid IPA characters.

## Example

```xml
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="it">
  <siteinfo>
    <sitename>Wikizionario</sitename>
    <dbname>itwiktionary</dbname>
    <base>https://it.wiktionary.org/wiki/Pagina_principale</base>
    <generator>MediaWiki 1.27.0-wmf.19</generator>
    <case>case-sensitive</case>
    <namespaces>
      <namespace key="-2" case="case-sensitive">Media</namespace>
      <namespace key="-1" case="first-letter">Speciale</namespace>
      <namespace key="0" case="case-sensitive" />
      <namespace key="1" case="case-sensitive">Discussione</namespace>
      <namespace key="2" case="first-letter">Utente</namespace>
      ...
    </namespaces>
  </siteinfo>
  ...
  <page>
    <title>libero</title>
    <ns>0</ns>
    <id>778</id>
    <revision>
      <id>2373198</id>
      <parentid>2322095</parentid>
      <timestamp>2016-01-11T07:48:16Z</timestamp>
      <contributor>
        <username>HydrizBot</username>
        <id>42131</id>
      </contributor>
      <minor />
      <comment>Bot: Aggiungo [[pt:libero]]</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{Vedi|Libero}}
{{W|dividere le traduzioni per significato}}
== {{-it-}} ==
{{-agg-|it}}
{{It-decl-agg4|liber}}
{{Pn|w}} ''m sing''
# non [[imprigionato]] o in [[schiavitù]]
#*''dopo due anni di galera sono tornato {{Pn}}''
# con [[possibilità]] di [[scelta]] [[arbitraria]] o [[personale]]
#*''oggi scriveremo un testo {{Pn}}''
# non [[bloccato]]
# relativo al [[telefono]], quando è possibile effettuare una chiamata o quando segnala che il [[ricevente]] non è impegnato in una [[conversazione]]
#*''riesci a telefonare? sì, dà {{Pn}}''
#*''gli sto telefonando adesso, dà {{Pn}}''
# [[privo]], [[senza]] qualche cosa
#*''hai un impegno? no, sono {{Pn}}
#*''finalmente sono {{Pn}} dagli esami!''
# {{Term|sport|it}} nel gioco della [[pallavolo]], il [[giocatore]] che può [[sostituire]] un [[difensore]] per un [[numero]] [[arbitrario]] di volte durante la [[partita]]

{{-sill-}}
; lì | be | ro

{{-pron-}}
{{IPA|/'libero/}}

{{-etim-}}
derivato dal latino ''[[liber]]''

...
[[sv:libero]]
[[th:libero]]
[[tr:libero]]
[[zh:libero]]</text>
      <sha1>0298h68958ma2ygqwpuzfd59pc3mw4k</sha1>
    </revision>
  </page>
  ...
</mediawiki>
```

produces (spaces added for clarity):

```
...
778 \t libero \t 'libero
...
```

