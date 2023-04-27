# Budget CLI

[![Build](https://github.com/madalinpopa/budgetcli/actions/workflows/build.yaml/badge.svg)](https://github.com/madalinpopa/budgetcli/actions/workflows/build.yaml)

A simple terminal app written in Python to manage budgets and expenses in Google Sheet.

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

**Add an income**
```
budgetcli add income 2023-03-20 salary "short description" 4000
```
**Add an outcome**
```
budgetcli add outcome 2023-03-20 rent "short description" 400
```
**List transactions. Default first 100 rows**
```
budgetcli list transactions 
```
**List only first 10 transactions**

```
budgetcli list transactions --rows=10 
```

**List transactions for a specific month**
```
budgetcli list transactions --month=April 
```
