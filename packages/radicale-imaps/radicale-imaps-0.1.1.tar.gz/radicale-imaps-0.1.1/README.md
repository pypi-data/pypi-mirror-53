# Radicale IMAP authentication plugin

IMAP authentication plugin for [Radicale](http://radicale.org/).
This is a fork of [radicale-imap](https://github.com/comzeradd/radicale-imap) that uses IMAP4_SSL instead of IMAP4 to initiate connection.

## Installation

    python3 -m pip install radicale-imap

## Configuration

    [auth]
    type = radicale_imap
    imaps_host = address:port

## License

[GPL-3.0](LICENSE)
