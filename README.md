# Budget CLI

[![Build](https://github.com/madalinpopa/budgetcli/actions/workflows/build.yaml/badge.svg)](https://github.com/madalinpopa/budgetcli/actions/workflows/build.yaml) [![Test](https://github.com/coderustle/budgetcli/actions/workflows/test.yaml/badge.svg)](https://github.com/coderustle/budgetcli/actions/workflows/test.yaml) [![License](https://img.shields.io/pypi/l/budgetcli)](https://img.shields.io/pypi/l/budgetcli)

A simple terminal app written in Python to manage budgets and expenses in Google Sheet.

## Features

- Ability to track incomes and expenses as transactions
- Ability to list transactions by month

## Installation

```
pip install budgetcli
```

In order to use the app you need first to enable Google Spreadsheet API and to generate app credentials with a
`client_id` and a `client_secret`.

Please follow the following link for more details: [Authorize credentials for a desktop application](https://developers.google.com/sheets/api/quickstart/python)

## Configuration

Before start adding transactions and data, you need to do the following steps:

**Provide the google spreadsheet id**
```
budgetcli config spreadsheet-id ID
```

**Copy the client_secret_XXX.json to app config**
```
budgetcli config credentials-file-path /path/to/client_secret.json
```

**Authorize the app access to spreadsheet data**
```
budgetcli auth
```

**Init sheet tables headers**
```
budgetcli init
```

## Usage

The commands follow the below structure.
```
budgetcli <VERB> <OBJECT> <OPTIONS>
```
### Incomes
To add an income you need to provide only an amount and a category. By default, all the income transactions are added
with default today date and without no description.

**Add an income**
```bash
budgetcli add income 5000 Salary
```
**Add an income with description**
```bash
budgetcli add income 500 projects --description "Project A"
```
**Add an income with date and description**
```bash
budgetcli add income 500 projects --description "Project A" --date 2023-04-01
```

### Outcomes
Same for outcome transactions, you need to provide only an amount and a category. By default, all the outcome transactions are added
with default today date and without no description.

**Add an outcome**
```bash
budgetcli add outcome 400 Rent
```
```bash
budgetcli add outcome 400 Rent --date 2023-05-01 --description "Rent for April"
```
### List transactions
**List transactions. Default first 100 rows**
```
budgetcli list transactions 
```
**List only first 10 transactions**

```bash
budgetcli list transactions --rows 10 
```

**List transactions for a specific month**
```bash
budgetcli list transactions --month April 
```
