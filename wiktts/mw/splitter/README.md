# mwsplitter 

**Split a MediaWiki dump into multiple files.**


## Input

A **MediaWiki dump file**, either uncompressed (``.xml``) or compressed (``.xml.bz2``).


## Output

**One or more XML files**, containing a fixed number of MediaWiki pages each.


## Usage

```bash
$ python -m wiktts.mw.splitter DUMP.XML[.BZ2] [OPTIONS]
```

Example:

```bash
$ python -m wiktts.mw.splitter enwiktionary-20160407-pages-meta-current.xml.bz2 --output-dir /tmp/out/ --ns 0 --pages-per-chunk 1000 --stats
```

### Options

Invoke with ``--help`` to get the list of available options:

```bash
$ python -m wiktts.mw.splitter --help

usage: __main__.py [-h] [--output-dir [OUTPUT_DIR]] [--ns NS [NS ...]]
                   [--pages-per-chunk [PAGES_PER_CHUNK]] [--prefix [PREFIX]]
                   [--max-number-pages [MAX_NUMBER_PAGES]] [--stats] [--head]
                   [--count] [--quiet]
                   dumpfile

Split a MediaWiki dump into multiple files or chunks in memory

positional arguments:
  dumpfile              Input MediaWiki dump.xml or dump.xml.bz2

optional arguments:
  -h, --help            show this help message and exit
  --output-dir [OUTPUT_DIR]
                        Output files in this directory
  --ns NS [NS ...]      Extract only pages with the specified ns values
                        (default: all)
  --pages-per-chunk [PAGES_PER_CHUNK]
                        Number of pages per output file (default: 1000)
  --prefix [PREFIX]     Use this prefix for the output file names (default:
                        '')
  --max-number-pages [MAX_NUMBER_PAGES]
                        Number of pages to extract (default: all)
  --stats               Print the statistics
  --head                Shortcut for --ns 0 --max-number-pages 1000
  --count               Only count the number of pages
  --quiet               Do not print created file paths to stdout
```



