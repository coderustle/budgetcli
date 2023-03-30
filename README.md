# My Budget CLI


## Installation

1. Clone the repository.
2. Change directory to local repository
3. Run the pip install command `pip install .`

In order to use the app you need first to enable Google Spreadsheet API and to generate app credentials with a
`client_id` and a `client_secret`.

Please follow the following link for more details: [Authorize credentials for a desktop application](https://developers.google.com/sheets/api/quickstart/python)

Before start adding transactions and data, you need to do the following steps:

**Provide the google sheet id**
```
budgetcli config spreadsheet ID
```

**Copy the credentials_json.secret to app config**
```
budgetcli config /path/to/client_secret.json
```

**Authorize the app access to sheet data**
```
budgetcli auth
```

**Init sheet tables headers**
```
budgetcli auth
```


