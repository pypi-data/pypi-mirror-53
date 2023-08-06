# libhockey

[![PyPi Version](https://img.shields.io/pypi/v/libhockey.svg)](https://pypi.org/project/libhockey/)
[![License](https://img.shields.io/pypi/l/libhockey.svg)](https://github.com/Microsoft/libhockey/blob/master/LICENSE)

`libhockey` is a wrapper around the Hockey App REST API. It's aim is to be a simple and easy to use as possible.

It doesn't cover every single API, but does the basics. Feel free to open an issue or a pull request for API support.

## Getting started

Just add the following and you are ready to go:

```python

import libhockey

client = libhockey.HockeyClient(access_token="...")
```

## Examples

#### Listing all versions of an app

```python
for version in client.versions.generate_all("[app id]"):
    print(version.download_url)
```

#### Uploading a build

```python
download_link = client.versions.upload("/path/to/app.ipa", "Release notes go here")
```

#### Find new crashes in a build

```python

current_crashes = client.crashes.groups_for_version("[app id]", "[current version id]")
previous_crashes = client.crashes.groups_for_version("[app id]", "[previous version id]")
new_crashes = list(set(current_crashes) - set(previous_crashes))

for crash in new_crashes:
    print(f"({crash.number_of_crashes}) {crash.crash_file} - {crash.crash_class}:{crash.crash_method}")
```


# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
