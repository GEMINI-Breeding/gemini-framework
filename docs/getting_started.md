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


