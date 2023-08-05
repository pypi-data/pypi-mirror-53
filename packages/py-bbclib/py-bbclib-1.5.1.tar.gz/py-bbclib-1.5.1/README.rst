py-bbclib
====

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CircleCI](https://circleci.com/gh/beyond-blockchain/py-bbclib.svg?style=shield)](https://circleci.com/gh/beyond-blockchain/py-bbclib)


The library that defines BBc-1 transaction data structure is decoupled from [the bbc1 repository](https://github.com/beyond-blockchain/bbc1).

BBc-1 is a Python-based reference implementation of BBc-1, a trustable system of record keeping beyond blockchains. The transaction data structure definition is the most important part of BBc-1.
      
The design paper (white paper) and the analysis paper are available [here](https://beyond-blockchain.org/public/bbc1-design-paper.pdf) and [here](https://beyond-blockchain.org/public/bbc1-analysis.pdf). BBc-1 is inspired from blockchain technologies like Bitcoin, Ethereum, Hyperledger projects, and so on.
BBc-1 is a simple but reliable distributed ledger system in contrast with huge and complicated existing blockchain platforms.
The heart of BBc-1 is the transaction data structure and the relationship among transactions, which forms a graph topology.
A transaction should be signed by the players who are the stake holders of the deal. BBc-1 achieves data integrity and data transparency by the topology of transaction relationship and signatures on transactions. Simply put, BBc-1 does not have *blocks*, and therefore, requires neither mining nor native cryptocurrency.
BBc-1 can be applied to both private/enterprise use and public use. BBc-1 has a concept of *domain* for determining a region of data management. Any networking implementation (like Kademlia for P2P topology management) can be applied for each domain.
Although there are many TODOs in BBc-1, this reference implementation includes most of the concept of BBc-1 and would work in private/enterprise systems. When sophisticated P2P algorithms are ready, BBc-1 will be able to support public use cases.

For the details, please read documents in [docs/ directory](https://github.com/beyond-blockchain/py-bbclib/tree/develop/docs) or [the bbc1 repository](https://github.com/beyond-blockchain/bbc1). Not only documents but slide decks (PDF) explain the design of the BBc-1 and its implementation.

API doc is ready at [readthedocs.org](https://py-bbclib.readthedocs.io/en/latest/index.html).

# Trouble shooting

Installing py-bbclib through pip sometimes fails owing to pip cache trouble. It might occur in the case that you terminate the install process during libbbcsig building process.
This leads to a defect in the pip cache of libbbcsig module, and resulting in fail installing forever.

To solve the problem, you need to remove pip cache or pip install without using cache. How to solve it is explained below.

### Solution 1
Removing pip cache directory is a fundamental solution to this problem. The cache directories in various OS platform are as follows:

* Linux and Unix
  - ~/.cache/pip
* macOS
  - ~/Library/Caches/pip
* Windows
  - %LocalAppData%\pip\Cache

After removing the cache directory, install py-bbclib module again.

```bash
python3 -mvenv venv
. venv/bin/activate
pip install py-bbclib
```

### Solution 2
Disabling cache and re-installing the module is another solution, which is easier way.
```bash
python3 -mvenv venv
. venv/bin/activate
pip --no-cache-dir install -I py-bbclib 
```

# Namespace is changed at v1.4.1 

Before v1.4.1, the namesapce of py-bbclib module was "bbc1". However, This conflicts with that of bbc1 module.
Therefore, the namespace of py-bbclib has been changed to "bbclib" since v1.4.1.
Be careful when using py-bbclib module solely.


# Environment

* Python
    - Python 3.5.0 or later
    - virtualenv is recommended
        - ```python -mvenv venv```

* tools for macOS by Homebrew
    ```
    brew install libtool automake python3
    pip3 install virtualenv
    ```

* tools for Linux (Ubuntu 16.04 LTS, 18.04 LTS)
    ```
    sudo apt-get update
    sudo apt-get install -y git tzdata openssh-server python3 python3-dev python3-pip python3-venv libffi-dev net-tools autoconf automake libtool libssl-dev make
    ```

# Install

### install module using pip

    python -mvenv venv
    source venv/bin/activate
    pip install py-bbclib


### build from github repository (this repository)
This project needs an external library, [libbbcsig](https://github.com/beyond-blockchain/libbbcsig), for sign/verify of transaction data. This repository includes setup script to build the external library.

    git clone https://github.com/beyond-blockchain/py-bbclib
    cd py-bbclib
    bash prepare.sh

You will find a dynamic link library (libbbcsig.so or libbbcsig.dylib) in bbclib/libs/ directory.

 
