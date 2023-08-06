# MySQL DB Anonymizer

This is a tool to generate a MySQL dump but anonymizing some field on the tables

## Install

```
pip install db_anonnymizer
```

## Usage
```
db_anonnymizer mysql://user:pass@host/db config.yml
```

The config file is a YAML document with the following structure:

```yaml
tablename:
    fieldname: faker
```
    
For this tool we used [Faker](https://faker.readthedocs.io/en/latest/index.html) with the following providers enabled:
- person
- internet 
- bank
- company

You can use them to fake any data

Ex:

```yaml
access_request:
  email: company_email
```