# GSenha Client Python
[![Build Status](https://travis-ci.com/globocom/gsenha-python.svg?branch=master)](https://travis-ci.com/globocom/gsenha-python)

Client for [gsenha-api](https://github.com/globocom/gsenha-api)

## Install

    pip install gsenha

## Usage

    from gsenha import PasswordManager
    pm = PasswordManager(GSENHA_ENDPOINT, GSENHA_USER, GSENHA_PASS, GSENHA_KEY|GSENHA_KEY_PATH, verify='path_to_your_private_cert')
    pm.get_passwords(folder, name1, name2, name*)

* GSENHA_ENDPOINT: Endpoint for [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA_USER: User for [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA_PASS: Password for [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA_KEY: User's private key for [gsenha-api](https://github.com/globocom/gsenha-api)
* GSENHA\_KEY\_PATH: User's private key path for [gsenha-api](https://github.com/globocom/gsenha-api)

GSenha should use raw private key as string or load file from filesystem.

You can use these *enviroment variables* and don't pass all of them when initialize **PasswordManager**:

    from gsenha import PasswordManager
    pm = PasswordManager()
    pm.get_passwords(folder, name1, name2, name*)

## Contribute

For development and contributing, please follow [Contributing Guide](https://github.com/globocom/gsenha-python/blob/master/CONTRIBUTING.md) and ALWAYS respect the [Code of Conduct](https://github.com/globocom/gsenha-python/blob/master/CODE_OF_CONDUCT.md)
    
