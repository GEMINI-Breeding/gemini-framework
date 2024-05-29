# GEMINI Framework

This is the repository for GEMINI Framework back-end.

Many staple crops that are important for food, nutritional, and economic security in low- and middle-income countries have not experienced the same large gains in yield and quality over last decades as crops such as maize and soybean. Further, these crops are faced with increasing risk and uncertain growing conditions due to climate change. This project aims to develop a state-of-the-art breeding toolkit, building on the latest techniques in AI-enabled sensing, 3-D crop modeling, and molecular breeding, to create an inflection point in the productivity and quality curves of crops that are central in LMICs.

[More details about GEMINI Here](https://projectgemini.ucdavis.edu/)

## Requirements

- Windows, Unix and MacOS (x86 and Apple Silicon)
- Local Installation of [PostgreSQL Database](https://www.postgresql.org/download/)
- [Docker Engine](https://docs.docker.com/engine/install/)
- Minimum 16GB RAM
- Minimum 256GB storage
- Python >=3.8
- [Task](https://taskfile.dev/installation/)

## Installation Steps

Install all the prerequisites above before continuing

#### Step 1

Clone the repository and enter the root foler

```
$ git clone https://github.com/GEMINI-Breeding/gemini-framework.git
$ cd gemini-framework
```

#### Step 2

Add a .env file in the root folder

Check ```.env.example``` in the root folder for all environment variables

**NOTE**: You can also rename ```.env.example``` to ```.env```

#### Step 3

If `task` is installed then just run task

```
$ task 
```

### Step 4

Install the package for use locally

```
$ pip install -e .
```

**WARNING**: Make sure you are installing the package while the environment you are working with is activated.







