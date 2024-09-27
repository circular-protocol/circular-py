# Circular Protocol Python API

The Circular Protocol API suite provides a robust and efficient interface for interacting with the Circular Protocol, a decentralized and highly scalable blockchain network. These APIs enable developers to integrate, query, and execute operations on the Circular Protocol blockchain, supporting a wide range of decentralized applications (dApps), financial transactions, and smart contracts.

## Docs
Official documentation for the Python API and many more languages on [GitBook](https://circular-protocol.gitbook.io/circular-sdk/api-docs/python)

## Installation

You can install the package via pip. Here's how to do it:

```bash
pip install circular_protocol_api
```

Or cloning this repository with

```bash
pip install .
```

## Usage

Import the package and instantiate the Circular Protocol API class.

```python
from circular_protocol_api import CircularProtocolAPI

# Example usage
circular = CircularAPI()
blockchain = 0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2
test_addr = 0xbd1d7ff426d094605a0902c78812dded6bbebdb42b20d9c722dc87bde0f30f44

print(circular.getWallet(blockchain, test_addr))

```


### Access data

The result is a Python dictionary so you could access values via the `.get()` method.

## License

MIT License (MIT)

## Contact

- Author: Danny De Novi
- Email: dannydenovi29@gmail.com / info@circularlabs.io

---
