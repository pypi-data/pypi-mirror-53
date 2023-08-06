# `salesforce-expense` README


[![PyPI version](https://badge.fury.io/py/salesforce-expense.svg)](https://badge.fury.io/py/salesforce-expense)
[![Build Status](https://api.travis-ci.org/giuliocalzolari/salesforce-expense.svg?branch=master)](https://travis-ci.org/giuliocalzolari/salesforce-expense/)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=giuliocalzolari_salesforce-expense&metric=bugs)](https://sonarcloud.io/dashboard?id=giuliocalzolari_salesforce-expense)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=giuliocalzolari_salesforce-expense&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=giuliocalzolari_salesforce-expense)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=giuliocalzolari_salesforce-expense&metric=security_rating)](https://sonarcloud.io/dashboard?id=giuliocalzolari_salesforce-expense)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=giuliocalzolari_salesforce-expense&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=giuliocalzolari_salesforce-expense)

This Python package provides a CLI tool which can submit expense claims to
SalesForce programmatically.

## Installation

To install the tool from PyPI, just use `pip`:

```bash
pip install salesforce-expense
```

To install from local source for development (if not using `pipenv` then ensure
that `setupext-janitor` is installed locally first, so that `setup.py`
correctly cleans up the `dist` directory):

```bash
./setup.py clean --all
./setup.py bdist_wheel
pip install dist/salesforce_expense-*.whl
```

## Configuration

The script requires a local configuration file with your SalesForce credentials
included in it, located at `~/.pse.json`. It should look like:

```json
{
  "username": "your-salesforce-email@example.com",
  "password": "fdgdhrx6MA==",
  "token": "afghfyfgbgnegrfbgdhtd"
}
```

`password` must be `base64` encoded as follows:

```bash
echo -n "my-password" | base64
```

To obtain the security token for your Salesforce account, follow
[this guide](https://onlinehelp.coveo.com/en/ces/7.0/administrator/getting_the_security_token_for_your_salesforce_account.htm).

### Password Alternatives

It is also possible to store password & security token in your OS' keyring. This supports any backends listed by the [Python keyring library](https://pypi.org/project/keyring).

To do so, your config file (`~/.pse.json`) should contain just `username` and `credential_store` values:
```json
{
  "username": "your-salesforce-email@example.com",
  "credential_store": "keyring"
}
```

Default values for the keyring assume everything is stored under the `salesforce_cli` application in your keyring. Your password would be stored as a `salesforce_cli` item with username `your-salesforce-email@example.com_password`, while the security token would be stored as `salesforce_cli`, `your-salesforce-email@example.com_token`.

Under MacOS this can be added with the "Keychain Access" application, under the default "login" keychain. `salesforce_cli` is the Keychain Item Name for both instances, and the `your-salesforce-email@example.com_password` or `your-salesforce-email@example.com_token` string is the Account Name.

## Usage

At present the only command is `add`.

```bash
expense add -p 'PX9999 - [REMOTE] - Onsite' -d 'Accomdoation on-site' -a 149.61 --date 2019-10-21 --currency NOK --non-billable --category Accommodation -f receipt.pdf
```

`billable` defaults to true, and the type defaults to `Sustenance`. Other
values will be prompted for. If you don't specify a file to upload, the script
will request access to your webcam and try to grab a photo that way.

## TODO

-   Clean up remaining documentation
-   Run linter over the code
-   Add additional currencies
-   Add submission
-   Add listing
-   Support the dry-run flag
-   Add OCR for receipt files to determine the date and amount
-   Integrate with billing systems
-   Port to Android?

## License

`salesforce-expense` is licensed under the [WTFPL](LICENSE).
