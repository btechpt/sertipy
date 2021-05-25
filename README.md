# Sertipy

##### Python library for the Sertiva Web API

## Instalation

```bash
pip install sertipy
```

or upgrade

```bash
pip install sertipy --upgrade
```

## Quick Start

To get started, install sertipy and create an account on [Sertiva](https://sertiva.id/). Add your client ID and client
SECRET to your environment:

### User authentication

```python
# import library or package sertipy
from sertipy.client import Sertiva

# make obj client sertiva
sertiva = Sertiva(client_id='<your_client_id>', client_secret='<your_client_secret>')
```

## Feature

Sertipy supports all of the features of the Sertiva Web API including access to all end points, and support for user
authorization. For details on the capabilities check [Sertiva Web API](https://api-reference.sertiva.id/)

### Designs

```python
# to get list designs
sertiva.designs.list()

# to get detail design
sertiva.designs.detail('<design_id>')
```

### Templates

```python
# to get list templates
sertiva.templates.list()

# to get detail template
sertiva.templates.detail('<template_id>')

# create new template
sertiva.templates.create('<design_id>', '<title>', '<description>')

# update template
sertiva.templates.update('<template_id>', '<title>', '<description>')
```

### Recipients

```python
# to get list draft recipients
sertiva.recipients.list('<template_id>')

# create new draft recipient
data_create = [
    {
        "name": "John Doe",
        "email": "john@doe.com",
        "fields": {
            "credentialSubject": {
                "activityDate": "2021-05-01T19:23:24.000000"
            }
        }
    },
]

sertiva.recipients.create('<template_id>', data_create)

# update draft recipient
data_update = [
    {
        "id": "72150eae-b469-4fbf-9b02-226075a9cf10",
        "phone": "0898989898989",
        "fields": {
            "credentialSubject": {
                "credentialNumber": "ID/1/1000"
            }
        }
    },
]

sertiva.recipients.update('<template_id>', data_update)

# delete recipient
data_delete = ['72150eae-b469-4fbf-9b02-226075a9cf10']

sertiva.recipients.delete('<template_id>', data_delete)
```

### Credentials

```python
# get list all credentials
sertiva.credentials.list()

# get detail some credential
sertiva.credentials.detail('<credential_id>')
```

### Main

#### Issue using data recipients in draft

```python
# with all data in draft
sertiva.mains.issue('<template_id>', '<issuance_date>', '<expiration_date>')

# with recipient ids
recipient_ids = ['6ad5c6e0-9ac7-488b-b05f-d8b32b73b4cf']

sertiva.mains.issue('<template_id>', '<issuance_date>', '<expiration_date>', recipient_ids)
```

#### Issue Using data recipients directly (without make draft recipient)

```python
recipients = [{
    "id": "72150eae-b469-4fbf-9b02-226075a9cf10",
    "name": "John Doe",
    "email": "john@doe.com",
    "fields": {
        "credentialSubject": {
            "credentialNumber": "ID/1/1000",
            "activityDate": "2021-05-01T19:23:24.000000"
        }
    }
},]
sertiva.mains.issue('<template_id>', '<issuance_date>', '<expiration_date>', recipients)
```
- for data `id` you can make with `uuid`

#### Verify and Revoke

```python
# verify credential
data_to_verify = ['72150eae-b469-4fbf-9b02-226075a9cf10']

sertiva.mains.verify(data_to_verify)

# revoke credential
data_to_revoke = ['72150eae-b469-4fbf-9b02-226075a9cf10']
reason = 'wrong certificate'

sertiva.mains.revoke(data_to_revoke, reason)
```

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/btechpt/sertipy/issues). Or just send a pull request
