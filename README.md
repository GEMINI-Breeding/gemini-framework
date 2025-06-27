# GEMINI Framework

This is the repository for GEMINI Framework back-end.

Many staple crops that are important for food, nutritional, and economic security in low- and middle-income countries have not experienced the same large gains in yield and quality over last decades as crops such as maize and soybean. Further, these crops are faced with increasing risk and uncertain growing conditions due to climate change. This project aims to develop a state-of-the-art breeding toolkit, building on the latest techniques in AI-enabled sensing, 3-D crop modeling, and molecular breeding, to create an inflection point in the productivity and quality curves of crops that are central in LMICs.

[More details about GEMINI Here](https://projectgemini.ucdavis.edu/)

## System Requirements

- Linux (Native, on Windows via WSL or on Mac via Parallels)
- [Docker Engine](https://docs.docker.com/engine/install/)
- Minimum 16 GB of RAM
- Minimum 256 GB Storage
- Python >= 3.11
- [Poetry] (https://python-poetry.org/docs/)

# Getting Started & Installation

## Installation Steps

Install all the prerequisites above before continuing

#### Step 1

Clone the repository and enter the root folder

```
$ git clone https://github.com/GEMINI-Breeding/gemini-framework.git
$ cd gemini-framework
```

#### Step 2

Run poetry installation command to install global `gemini` python module.

```
$ poetry install
```

#### Step 3

Setup the GEMINI Pipeline

```
$ gemini setup --default
```

#### Step 4

Build the Docker containers that make up the GEMINI Pipeline

```
$ gemini build
```

#### Step 5

Start the GEMINI Pipeline

```
$ gemini start
```

## Next Steps

The REST API will be available on http://localhost:7777


