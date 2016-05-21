# wiktts 

Mining MediaWiki dumps to create better TTS engines (using Machine Learning)

* Version: 0.0.1
* Date: 2016-05-21
* Developer: [Alberto Pettarin](http://www.albertopettarin.it/)
* License: the MIT License (MIT)
* Contact: [click here](http://www.albertopettarin.it/contact.html)


## Summary

TBW

This repository contains the following Python tools:

* ``wiktts.mw.splitter`` split a [MediaWiki dump](https://dumps.wikimedia.org/backup-index.html) into chunks
* ``wiktts.mw.miner``: mine [IPA](http://www.internationalphoneticassociation.org/) strings from a MediaWiki dump file
* ``wiktts.ipacleaner``: clean+normalize Unicode IPA strings
* TBD A tool to create train and test sets for [Sequitur G2P](https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html)
* TBD A tool to create train and test sets for [Phonetisaurus G2P](https://github.com/AdolfVonKleist/Phonetisaurus)


## Dependencies

1. Python 2.7.x or 3.5.x 
2. Python module ``lxml`` (``pip install lxml``)
3. Python module ``ipapy`` (``pip install ipapy``)


## Installation

1. Install the dependencies listed above. 

2. Clone this repo:
    ```bash
    $ git clone https://github.com/pettarin/wiktts.git
    ```

3. Download the dump(s) you want to work on from [Wikimedia Downloads](https://dumps.wikimedia.org/backup-index.html):
    ```bash
    $ cd dumps
    $ wget "https://dumps.wikimedia.org/enwiktionary/20160407/enwiktionary-20160407-pages-meta-current.xml.bz2"
    ```


## Usage

### wiktts.mw.splitter

```bash
$ python -m wiktts.mw.splitter DUMP.XML[.BZ2] [OPTIONS]
```

[Details](wiktts/mw/splitter/README.md)

### wiktts.mw.miner

```bash
$ python -m wiktts.mw.miner PARSER DUMP [OPTIONS]
```

[Details](wiktts/mw/miner/README.md)

### wiktts.ipacleaner

```bash
$ python -m wiktts.ipacleaner LEXICON [OPTIONS]
```

[Details](wiktts/ipacleaner/README.md)


## License

**wiktts** is released under the MIT License.


## References

See the [REFERENCES file](REFERENCES.md).


## Acknowledgments

* Many thanks to [Dr. Tony Robinson](https://www.speechmatics.com/) for many useful discussions on this project.



