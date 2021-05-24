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
Sertiva.designs.list()

# to get detail design
Sertiva.designs.detail('<design_id>')
```

### Templates

```python
# to get list templates
Sertiva.templates.list()

# to get detail template
Sertiva.templates.detail('<template_id>')

# create new template
Sertiva.templates.create('<design_id>', '<title>', '<description>')

# update template
Sertiva.templates.update('<template_id>', '<title>', '<description>')
```

### Recipients

```python
# to get list draft recipients
Sertiva.recipients.list('<template_id>')

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

Sertiva.recipients.create('<template_id>', data_create)

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

Sertiva.recipients.update('<template_id>', data_update)

# delete recipient
data_delete = ['72150eae-b469-4fbf-9b02-226075a9cf10']

Sertiva.recipients.delete('<template_id>', data_delete)
```

### Credentials

```python
# get list all credentials
Sertiva.credentials.list()

# get detail some credential
Sertiva.credentials.detail('<credential_id>')
```

### Main

#### Issue using data recipients in draft

```python
# with all data in draft
Sertiva.mains.issue('<template_id>', '<issuance_date>', '<expiration_date>')

# with recipient ids
recipient_ids = ['6ad5c6e0-9ac7-488b-b05f-d8b32b73b4cf']

Sertiva.mains.issue('<template_id>', '<issuance_date>', '<expiration_date>', recipient_ids)
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
Sertiva.mains.issue('<template_id>', '<issuance_date>', '<expiration_date>', recipients)
```
- for data `id` you can make with `uuid`

#### Verify and Revoke

```python
# verify credential
data_to_verify = ['72150eae-b469-4fbf-9b02-226075a9cf10']

Sertiva.mains.verify(data_to_verify)

# revoke credential
data_to_revoke = ['72150eae-b469-4fbf-9b02-226075a9cf10']
reason = 'wrong certificate'

Sertiva.mains.revoke(data_to_revoke, reason)
```

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/btechpt/sertipy/issues). Or just send a pull request
