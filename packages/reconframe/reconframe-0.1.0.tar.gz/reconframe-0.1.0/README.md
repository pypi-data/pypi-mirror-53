# reconframe v0.1.0
A Reconnaissance Framework for Penetration Testing

# Installation
```bash
$ pip install reconframe
```

# Usage

## Creating a project
```bash
reconframe init [project name]
```
Creates an blank project within current directory or given optional project name. Equivalent to ```git clone --depth=1 https://github.com/0xcrypto/reconframe-project```

## Installing dependencies
```bash
reconframe install
```
Installs required dependencies using pip. Equivalent to ```pip install -r requirements.txt```

## Parsing external commands
```bash 
reconframe run <external command>
```
Runs an external command and parses output from STDOUT thereof. Must run from within project's directory as the information captured will be parsed and stored within the project.

## Running Strategies
```bash
reconframe start
```
Implements the strategies and gains the information.

## Prepare reports
```bash 
reconframe prepare [report name]
```
Prepares a detailed report of gained information. 

