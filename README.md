# Budget CLI

[![Build](https://github.com/madalinpopa/budgetcli/actions/workflows/build.yaml/badge.svg)](https://github.com/madalinpopa/budgetcli/actions/workflows/build.yaml) [![Test](https://github.com/coderustle/budgetcli/actions/workflows/test.yaml/badge.svg)](https://github.com/coderustle/budgetcli/actions/workflows/test.yaml) [![License](https://img.shields.io/pypi/l/budgetcli)](https://img.shields.io/pypi/l/budgetcli)

A simple terminal app written in Python to manage budgets and expenses in Google Sheet.

## Features

- Add income transactions 
- Add outcome transactions 
- List transactions by month
- Add spending categories

## Installation

```
pip install budgetcli
```

In order to use the app you need first to enable Google Spreadsheet API and to generate app credentials with a
`client_id` and a `client_secret`.

Please follow the following link for more details: [Authorize credentials for a desktop application](https://developers.google.com/sheets/api/quickstart/python)

## Configuration

Before start adding transactions and data, you need to do the following steps:

**Provide Google spreadsheet id**
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
![](https://github.com/coderustle/budgetcli/blob/main/images/commands/init.gif)

## Usage

The commands follow the below structure.
```
budgetcli <VERB> <OBJECT> <OPTIONS>
```
### Incomes
To add an income you need to provide only an amount and a category. By default, all the income transactions are added
with default today date and without no description.

**Add an income**

![](https://github.com/coderustle/budgetcli/blob/main/images/commands/income.gif)

**Add an income with description**

![](https://github.com/coderustle/budgetcli/blob/main/images/commands/income-description.gif)

**Add an income with date and description**

![](https://github.com/coderustle/budgetcli/blob/main/images/commands/income-date.gif)

### Outcomes
Same for outcome transactions, you need to provide only an amount and a category. By default, all the outcome transactions are added
with default today date and without no description.

**Add an outcome**

![](https://github.com/coderustle/budgetcli/blob/main/images/commands/outcome.gif)

**Add an outcome with description**

![](https://github.com/coderustle/budgetcli/blob/main/images/commands/outcome-date.gif)

### List transactions

**List first 100 transactions**

![](https://github.com/coderustle/budgetcli/blob/main/images/commands/transactions.gif)

**List only first 10 transactions**

![](https://github.com/coderustle/budgetcli/blob/main/images/commands/transactions-rows.gif)

**List transactions for a specific month**
```bash
budgetcli list transactions --month April 
```
