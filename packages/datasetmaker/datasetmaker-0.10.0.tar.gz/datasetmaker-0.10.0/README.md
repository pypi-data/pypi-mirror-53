# Datasetmaker
[![image](https://img.shields.io/pypi/v/datasetmaker.svg)](https://pypi.org/project/datasetmaker/)
[![Build Status](https://travis-ci.com/datastory-org/datasetmaker.svg?token=V6phAxmvf7gFqpigH6TT&branch=master)](https://travis-ci.com/datastory-org/datasetmaker)

Datasetmaker is Datastory's toolkit for fetching, standardizing, and packaging data.

## Installation

```bash
$ pipenv install datasetmaker
```

## Usage

For any of the supported clients:
```python
import datasetmaker

client = datasetmaker.create_client('CLIENT ID')
client.get()
client.save('path/to/ddf-package')
```

## Develop

To get started contributing:

```bash
$ git clone git@github.com:datastory-org/datasetmaker.git
$ make init
```

### Code overview
At the core of the codebase are the `client`s, each mapping to a data source.

```python
from datasetmaker.models import Client

class MyClient(Client):
    def get(self):
        # Fetch, clean, and standardize data
    
    def save(self, path, **kwargs):
        # Save the data as a DDF package
```

Technically, all a client author needs to do is implement these two methods so that the resulting DDF package is valid. However, the data needs to be compliant with the Datastory's data ontology and standards.

The ontology is composed of a core DDF package (_datasetmaker/onto/data_) and schemas (_datasetmaker/onto/schemas.py_). Whenever new concepts are introduced, these files needs to be updated.

To facilitate the DDF package creation process, datasetmaker has a `Datapackage` class which parses the ontology and figures out how a specific dataset should be turned into a DDF package. Here's a quick glimpse of how it works:

```python
class MyClient(Client):
    def get(self):
        self.data = requests.get('data.com')
    
    def save(self, path, **kwargs):
        package = Datapackage(data=self.data)
        package.save(path, **kwargs)
```


## DDF

The output of datasetmaker clients are DDF packages. Read more about the [DDF data model](https://open-numbers.github.io/ddf.html).

## Testing

```bash
$ make test
```

## Updating the ontology

All new concepts must be added to _datasetmaker/onto/data/ddf--concepts.csv_.

A concept row has to include:
- concept
- concept_type
- name 

In addition, concept rows can define:
- collections ("World Development Indicators, Partisympatiundersölningen" etc.)
- tags ("agriculture, politics")
- description
- name_datastory (will override name)
- slug (will be used as slug, otherwise default to concept)
- source
- source_url
- updated
- unit
- scales [linear, log] (if there's a preferred default)

All canonical and stable entities must have a corresponding _datasetmaker/onto/data/ddf--entities--<name>.csv_ file.

An entitity row has to include:
- country (or whatever is the primary key, examples: school, region, organization)
- name 


In addition, an entity row can define:
- entity-domain columns (country belongs to region etc.) 
- string-type columns (for example capital name)

All entities must be added to the schema registry in _datasetmaker/onto/schemas.py_.


## Creating datastory-core

To merge existing packages, use the `merge_packages` function. Assuming two DDF packages called wikipedia and worldbank exist:

```python
import datasetmaker

datasetmaker.merge_packages(['wikipedia', 'worldbank'], dest='datastory-core')
```

## datapackage.json

This is the format of the datapackage.json.

```
"name": "world-bank" // used as ID and SLUG. Should follow format 'my-source'
"title": "World Bank" // title of data source
"status" : "published", // "draft"
"tags" : "education, sweden, swedish-education" //comma-separated tag IDs, based on canonical list (WikiData)
"language": {
   "id": "en" //use same locales as Datastory, 2 letter codes or specific code if we need to support a very custom language
},
"default-indicator" : "life_expectancy", //optional helper for users who browse
"default-primary-key" : "country-year", //optional helper to show nice data default
"translations": [
    {
        "id": "ar",
    },
    {
        "id": "es"
    },
    {
        "id": "fr"
    }
],  
"license": "", 
"author": "Datastory", (or original if simply copy / paste)
"source" : "Skolverket" // shorthand if all indicators in dataset come from same source
"created": "2018-11-04T08:25:30.708697+00:00", //gets added automatically
resources : [] //gets added automatically
ddfSchema : [] //gets added automatically
```


If a source has many subcollections, we can allow this but should ideally be avoided: (another option is as meta data in concepts.csv)

```
"name": "world-bank-wdi" // 
"title": "World Bank – World development indicators" // title of collection
```
