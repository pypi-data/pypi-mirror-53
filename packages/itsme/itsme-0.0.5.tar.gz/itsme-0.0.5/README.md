# Python Package

## Prerequisites

-   [python3][python-link]
-   [setuptools][setuptools-link]

## Building

-   Generate the [shared libraries][shared-lib]
-   Run `./build.ps1` or `build.sh`, the output can be used on any platform

## Consuming

### Install the generated wheel package

    pip install pip install .\dist\itsme-0.0.1-py3-none-any.whl

### Import ITSME and use it.

```python
import itsme

enc_cert = '''-----BEGIN RSA PRIVATE KEY-----
my_key
-----END RSA PRIVATE KEY-----'''

signing_cert = '''-----BEGIN RSA PRIVATE KEY-----
my_key
-----END RSA PRIVATE KEY-----'''

client_id = 'my_client_id'
service_code = 'my_service_code'
redirect_url = 'https://i/redirect'
signing_cert_id = 'certificate_id'


client = itsme.Client(client_id, service_code, redirect_url,
                      signing_cert_id, signing_cert, enc_cert)
itsme_auth_url = client.get_authentication_url('profile email', '')
print(itsme_auth_url)
user = client.get_user_details('authorization_code_I_received_upon_redirect')
print(user.name)
```

A [demo project][demo-project] is included here as well which contains all this information in a working setup.

[python-link]: https://www.python.org/
[setuptools-link]: https://pypi.org/project/setuptools/
[shared-lib]: ../clang/README.md
[demo-project]: ../demos/python
