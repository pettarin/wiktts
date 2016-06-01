# wiktts.mw.splitter 

**Split a MediaWiki dump into multiple files.**


## Input

A **MediaWiki dump file**, either uncompressed (``.xml``) or compressed (``.xml.bz2``).


## Output

**One or more XML files**, containing a fixed number of MediaWiki pages each.


## Usage

```bash
$ python -m wiktts.mw.splitter DUMP.XML[.BZ2] [OPTIONS]
```

Examples:

```bash
$ python -m wiktts.mw.splitter enwiktionary-20160407-pages-meta-current.xml.bz2 --output-dir /tmp/out/
$ python -m wiktts.mw.splitter enwiktionary-20160407-pages-meta-current.xml.bz2 --output-dir /tmp/out/ --stats
$ python -m wiktts.mw.splitter enwiktionary-20160407-pages-meta-current.xml.bz2 --output-dir /tmp/out/ --namespaces 0 1 2 --pages-per-chunk 10000
$ python -m wiktts.mw.splitter enwiktionary-20160407-pages-meta-current.xml.bz2 --output-dir /tmp/out/ --head
$ python -m wiktts.mw.splitter enwiktionary-20160407-pages-meta-current.xml.bz2 --count 
```

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.mw.splitter --help

usage: wiktts.mw.splitter [-h] [--output-dir [OUTPUT_DIR]]
                          [--namespaces NAMESPACES [NAMESPACES ...]]
                          [--pages-per-chunk [PAGES_PER_CHUNK]]
                          [--prefix [PREFIX]]
                          [--max-number-pages [MAX_NUMBER_PAGES]] [--head]
                          [--count] [--hide-progress] [--stats]
                          dumpfile

Split a MediaWiki dump into multiple files

positional arguments:
  dumpfile              Input MediaWiki dump.xml or dump.xml.bz2

optional arguments:
  -h, --help            show this help message and exit
  --output-dir [OUTPUT_DIR]
                        Output files in this directory
  --namespaces NAMESPACES [NAMESPACES ...]
                        Extract only pages with namespace in the specified
                        list (default: all)
  --pages-per-chunk [PAGES_PER_CHUNK]
                        Number of pages per output file (default: 1000)
  --prefix [PREFIX]     Use this prefix for the output file names (default:
                        '')
  --max-number-pages [MAX_NUMBER_PAGES]
                        Number of pages to extract (default: all)
  --head                Shortcut for --namespaces 0 --max-number-pages 1000
  --count               Only count the number of pages
  --hide-progress       Do not print extraction progress messages
  --stats               Print statistics
```

