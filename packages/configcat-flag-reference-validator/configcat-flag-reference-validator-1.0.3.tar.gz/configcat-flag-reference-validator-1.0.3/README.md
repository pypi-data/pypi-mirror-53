# flag-reference-validator 
[![PyPI](https://img.shields.io/pypi/v/configcat-flag-reference-validator.svg)](https://pypi.python.org/pypi/configcat-flag-reference-validator) [![Docker version](https://img.shields.io/badge/docker-latest-blue)](https://hub.docker.com/r/configcat/flag-reference-validator)

CLI tool for validating ConfigCat feature flag references in your source code.

This tool can be used for discovering ConfigCat feature flag usages in your source code and validating them against your own ConfigCat configuration dashboard. It searches for ConfigCat SDK usage and greps the feature flag keys from the source code, then it compares them with the keys got from your ConfigCat dashboard.

## Installation

This CLI tool is written in python so you have to have python installed on your system.

1. Install the [The silver searcher](https://github.com/ggreer/the_silver_searcher) used for source code scanning.
    - Linux
        ```bash
        apt-get install silversearcher-ag
        ```
    - Windows
        ```powershell
        choco install ag
        ```
2. Install the reference validator using pip.
    ```bash
    pip install configcat-flag-reference-validator
    ```
3. Execute the validator.
    ```bash
    configcat-validator [YOUR-CONFIGCAT-APIKEY] [DIRECTORY-TO-SCAN] 
    ```

### Docker

Pull the configcat/flag-reference-validator docker image to your environment. The image provides an entrypoint `configcat-validator` to execute the validator.
```powershell
docker pull configcat/flag-reference-validator

docker run configcat-validator [YOUR-CONFIGCAT-APIKEY] [DIRECTORY-TO-SCAN]
```

## Arguments

| Name                       | Required | Default value     | Description                                |
|----------------------------|----------|-------------------|--------------------------------------------|
| configcat_api_key          | yes      | N/A               | The api key of your ConfigCat project.     |
| search_dir                 | yes      | N/A               | The directory to scan for flag references. |
| -s, --configcat_cdn_server | no       | cdn.configcat.com | The domain name of the ConfigCat CDN where you ConfigCat configuration file is stored. |
| -f, --fail_on_warnings     | no       | false             | Signals an error when the validation fails. By default only warnings are showed. |
| -v, --verbose              | no       | false             | Turns on detailed logging. |

## Example
The following command will execute a flag reference validation on the ./repo folder and signals a failure when it finds flag key mismatches.
```bash
configcat-validator \
    [YOUR-CONFIGCAT-APIKEY] \
    ./repo \
    --fail_on_warnings \
    --verbose
```
Output:
```bash
INFO:configcat.reference_validator.config_fetcher:Fetching the current ConfigCat configuration from cdn.configcat.com.
INFO:configcat.reference_validator.config_fetcher:Successful fetch, 2 settings found: ['key1', 'key2'].
INFO:configcat.reference_validator.reference_finder:Scanning the ./repo directory for ConfigCat setting references.
INFO:configcat.reference_validator.reference_finder:6 references found: {'key1', 'key2', 'key3'}.
WARNING:configcat.reference_validator.reference_validator:Feature flag/Setting keys not found in ConfigCat (but present in source code): {'key3'}.
Exited with code 1
```

## CI Integrations
- [CircleCI Orb](https://circleci.com/orbs/registry/orb/configcat/flag_reference_validator)

## About ConfigCat
- [Documentation](https://docs.configcat.com)
- [Blog](https://blog.configcat.com)
