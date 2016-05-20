# mwsplitter 

**Split a MediaWiki dump into multiple files.**


## Input

A **MediaWiki dump file**, either uncompressed (``.xml``) or compressed (``.xml.bz2``).


## Output

**One or more XML files**, containing a fixed number of MediaWiki pages each.


## Usage

```bash
$ python -m wiktts.mwminer.mwsplitter DUMP.XML[.BZ2] [OPTIONS]
```

Example:

```bash
$ python -m wiktts.mwminer.mwsplitter enwiktionary-20160407-pages-meta-current.xml.bz2 --output-dir /tmp/out/ --ns 0 --pages-per-chunk 1000 --stats
```

### Options

Invoke with ``--help`` to get the list of available options,
including how to modify the output file:

```bash
$ python -m wiktts.mwminer.mwsplitter --help
```



