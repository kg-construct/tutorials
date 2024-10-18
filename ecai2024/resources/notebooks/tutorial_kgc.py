# -*- coding: utf-8 -*-
"""Tutorial_KGC.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1if-wmQbzZHQlXLazc3VnLIvRkxEyaI9N

# **[Yatter](https://github.com/oeg-upm/yatter) Tutorial**

This tool translates mapping rules from YARRRML in a turtle-based serialization of RML or R2RML.

First of all, we need to install the library via pip.
"""

!pip install yatter==1.1.5

"""And make the necessary imports (yatter, ruamel for YAML and urllib for the requests)"""

import yatter, time
from ruamel.yaml import YAML
from urllib import request

"""We just need to call the function `translate` from the `yatter` package, with a yaml object as a parameter, it returns the mapping translated into RML as an string"""

yaml = YAML(typ='safe', pure=True)
yarrrml_mapping = request.urlopen("https://raw.githubusercontent.com/kg-construct/tutorials/refs/heads/main/ecai2024/resources/yarrrml_mapping.yml").read().decode('utf-8')

print(f'\n\n------Input Mapping in YARRRML----------\n\n{yarrrml_mapping}')
time.sleep(1)
rml_content = yatter.translate(yaml.load(yarrrml_mapping))
print(f'\n\n------Translated Mapping in RML----------\n\n{rml_content}')

"""# **[Morph-KGC](https://github.com/oeg-upm/morph-kgc) Tutorial**

**[Morph-KGC](https://github.com/oeg-upm/morph-kgc)** is an engine that constructs **[RDF](https://www.w3.org/TR/rdf11-concepts/)** and **[RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html)** knowledge graphs from heterogeneous data sources with the **[R2RML](https://www.w3.org/TR/r2rml/)** and **[RML](https://w3id.org/rml/core/spec)** mapping languages. The full documentation of Morph-KGC is available in **[Read the Docs](https://morph-kgc.readthedocs.io/en/latest/)**.

There are two different options to run Morph-KGC:

- As a **library**, integrating with **[RDFLib](https://rdflib.readthedocs.io)** and **[Oxigraph](https://oxigraph.org/pyoxigraph)**.
- Via the **command line**.


This tutorial shows the different alternatives to run Morph-KGC. Here, we use [RML](https://w3id.org/rml/core/spec) mappings, but the more user-friendly [YARRRML](https://rml.io/yarrrml/spec/) mapping format is also supported. Data transformation, computation, or filtering before generating triples is also supported with [RML-FNML](https://w3id.org/rml/fnml/spec).

## **Load Knowledge Graph to [RDFLib](https://rdflib.readthedocs.io)**

**[RDFLib](https://rdflib.readthedocs.io)** is the reference library to work with RDF in Python. Morph-KGC can be used as a **library** to create a knowledge graph and load it to RDFLib. In this example we will use the Aircrafts Example with **CSV** data. Morph-KGC allows to access mappings and data **remotely**, so we will use this functionality to avoid downloading the data and the mappings ourselves. The RML mappings are available [here](https://github.com/kg-construct/tutorials/blob/main/ecai2024/resources/rml_mapping.rml.ttl) and the data is available [here](https://github.com/kg-construct/tutorials/tree/main/ecai2024/resources/data).

First of all, we need to **install** [Morph-KGC](https://pypi.org/project/morph-kgc) (this will also install [RDFLib](https://pypi.org/project/rdflib/) and [Oxigraph](https://pypi.org/project/pyoxigraph/)).
"""

!pip install morph-kgc==2.8.0

"""Now we just need to **import** Morph-KGC and we are ready to go!"""

import morph_kgc

"""To run Morph-KGC it is necessary to provide some information. This is done via a config **INI** file. When running Morph-KGC as a **library**, this configuration can be provided as a **string** or as a **file path**. Below there is a basic config file for our example provided as a string. The _config_ indicates the path to a mapping file."""

config = """
             [KGC-Tutorial]
             mappings: https://raw.githubusercontent.com/kg-construct/tutorials/refs/heads/main/ecai2024/resources/rml_mapping.rml.ttl
         """

"""We just need to call `materialize` passing our _config_ and Morph-KGC will create the knowledge graph and load it to RDFLib."""

g = morph_kgc.materialize(config)

"""**That is it!** Now we can work with our RDFLib graph: query, navigate or save the graph and more. For instance, below we query the KG"""

sparql_query = """
         PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
         PREFIX dct: <http://purl.org/dc/terms/>
         PREFIX ex: <http://www.ex.org/>

         SELECT * WHERE {
             ?aircraft a ex:Aircraft .
             ?aircraft ex:hasID ?id .
             ?aircraft ex:hasAircraftModel ?model
         }
      """

answers = g.query(sparql_query)

for row in answers:
    print(f' Aircraft {row["aircraft"]} has id {row["id"]} and model {row["model"]}')

"""## **Create Knowledge Graph via Command Line**

Morph-KGC can also be executed from the **command line**. This is the most recommended option if you work with **large volumes of data**. As before, we need to create a config file. In this example we use again the data from the GTFS-Madrid-Bench.
"""

# create the config file
!echo "[CONFIGURATION]" > config.ini
!echo "logging_level: DEBUG" >> config.ini
!echo "[AIRCRAFTSKG]" >> config.ini
!echo "mappings: https://raw.githubusercontent.com/kg-construct/tutorials/refs/heads/main/ecai2024/resources/rml_mapping.rml.ttl" >> config.ini

# show the config file
!cat config.ini

"""The following command will create the knowledge graph and write it to a _knowledge-graph.nt_ file. You just need to provide the path to the _config_ file."""

!python3 -m morph_kgc config.ini

"""Let's take a look to a subset of the generated RDF!"""

!head knowledge-graph.nt

"""With the generated RDF we could for instance load it to RDFLib (or any triplestore) and pose queries.

## **Load Knowledge Graph to [Oxigraph](https://oxigraph.org/pyoxigraph/)**

While RDFLib provides much functionality, it does not support **[RDF-star](https://w3c.github.io/rdf-star/cg-spec/2021-12-17.html)** yet. Morph-KGC can create RDF-star knowledge graphs using **[RML-star](https://w3id.org/rml/star/spec)** mappings and load them to **[Oxigraph](https://oxigraph.org/pyoxigraph/)**.

The following example creates an RDF-star knowledge graph of scientific software metadata (the Morph-KGC software in this example), extracted with [SoMEF](https://github.com/KnowledgeCaptureAndDiscovery/somef). SoMEF extract some characteristics of the software which are annotated with the technique that was used to extract them and also with a confidence value. The **JSON** data is available [here](https://github.com/oeg-upm/morph-kgc/blob/main/examples/tutorial/oeg-upm_morph-kgc.json) and the RML-star mappings are available [here](https://github.com/oeg-upm/morph-kgc/blob/main/examples/tutorial/mapping.somef.ttl).

As with RDFLib, we just need to create the _config_ and call `materialize_oxigraph`.
"""

import morph_kgc

config = """
             [SoMEF]
             mappings: https://raw.githubusercontent.com/oeg-upm/morph-kgc/main/examples/tutorial/mapping.somef.ttl
         """

g = morph_kgc.materialize_oxigraph(config)

"""We loaded our knowledge graph to an Oxigraph store, we can now query it with **[SPARQL-star](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html#sparql-star)**. The query below retrieves the license, the technique used to obtain the information and the confidence value."""

q = """
         PREFIX sd: <https://w3id.org/okn/o/sd#>
         PREFIX em: <https://www.w3id.org/okn/o/em#>

         SELECT * WHERE {
             ?sowtware a sd:Software .
             << ?software sd:license ?license >> em:confidence ?confidence .
             << ?software sd:license ?license >> em:technique ?technique .
         }
    """

q_res = g.query(q)

for solution in q_res:
    print(solution['software'], solution ['license'], solution ['technique'], solution['confidence'])