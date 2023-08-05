gqlclient
=========

|codecov|


.. image:: https://readthedocs.org/projects/graphql-client/badge/?version=latest
   :target: https://dkistdc.readthedocs.io/projects/graphql-client/en/latest/?badge=latest
   :alt: Documentation Status

A pythonic interface for making requests to a GraphQL server using
standard library or pydantic dataclasses to spare you from string manipulation.

Features
--------

-  Use standard library dataclasses to specify graphql parameters and responses

-  Use `pydantic <https://pypi.org/project/pydantic/>`__ dataclasses to
   specify graphql parameters and responses that have type validation

-  Create and execute GraphQL Queries based upon typed models

-  Create and execute GraphQL Mutations based upon typed models

-  Async support

Installation
------------

.. code:: bash

   pip install gqlclient

with ``asyncio`` support

.. code:: bash

   pip install gqlclient[async]

Examples
--------

**Query**

.. code:: python

   from pydantic.dataclasses import dataclass

   from gqlclient import GraphQLClient

   @dataclass
   class Parameters:
       attr_one: str
       attr_two: int

   @dataclass
   class Response:
       attr_three: int
       attr_four: str
       
   client = GraphQLClient(gql_uri="http://localhost:5000/graphql")
   parameters = Parameters(attr_one="foo", attr_two=3)
   query = client.get_query(query_base="baseType", query_response_cls=Response, query_parameters=parameters)
   print(query)
   #{'query': '{baseType(attr_one: "foo", attr_two: 3){attr_three, attr_four} }'}
   response = client.execute_gql_query(query_base="baseType", query_response_cls=Response, query_parameters=parameters)
   print(response)
   #{"baseType"{"attr_three":5, "attr_four":"bar"}}

**Mutation**

.. code:: python

   from pydantic.dataclasses import dataclass

   from gqlclient import GraphQLClient


   @dataclass
   class Parameters:
       attr_one: str
       attr_two: int


   @dataclass
   class Response:
       attr_three: int
       attr_four: str
       
   client = GraphQLClient(gql_uri="http://localhost:5000/graphql")
   parameters = Parameters(attr_one="foo", attr_two=3)
   query = client.get_mutation(mutation_base="baseMutation", mutation_response_cls=Response, mutation_parameters=parameters)
   print(query)
   #{'query': 'mutation baseType {baseType(attr_one: "foo", attr_two: 3){ok, attr_three, attr_four} }', 'operationName': 'baseType'}

   response = client.execute_gql_mutation(mutation_base="baseMutation", mutation_response_cls=Response, mutation_parameters=parameters)
   print(response)
   #{"baseMutation": {"ok": true, "Response": {"attr_three":5, "attr_four":"bar"} }}

.. |codecov| image:: https://codecov.io/bb/dkistdc/graphql_client/branch/master/graph/badge.svg
   :target: https://codecov.io/bb/dkistdc/graphql_client
