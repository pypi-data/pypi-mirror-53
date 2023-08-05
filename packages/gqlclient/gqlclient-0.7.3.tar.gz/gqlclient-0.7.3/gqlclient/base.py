"""
Base class to support the creation of graphql queries and mutations.
"""
from abc import ABC, abstractmethod
import json
from dataclasses import dataclass
import datetime
import logging
from typing import Dict, Optional


__all__ = ["GraphQLClientBase", "GraphQLException"]


logger = logging.getLogger(__name__)


@dataclass
class GraphQLException(Exception):
    errors: list


class DatetimeEncoder(json.JSONEncoder):
    """
    A JSON encoder which encodes datetimes as iso formatted strings.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat("T")
        return super().default(obj)


@dataclass
class DefaultParameters:
    """
    Default parameter object that will pass dataclass type checking
    """


class GraphQLClientBase(ABC):
    """
    Abstract class for formatting and executing GraphQL queries and mutations

    :param gql_uri: Fully qualified URI for the graphQL endpoint.
    """

    def __init__(self, gql_uri: str):
        self.gql_uri = gql_uri

    @staticmethod
    def _graphql_response_from_model(model_cls: type) -> str:
        """
        Generate a GraphQL Response query from the class for the response.

        :param model_cls: Dataclass type representing the desired response object from the graphql endpoint.

        :return: Portion of a graphql query which specifies the response object.
        """
        if not hasattr(model_cls, "__dataclass_fields__"):
            raise TypeError("Response model must be a dataclass")

        def parse_field(field):
            if hasattr(field.type, "__dataclass_fields__"):
                return (
                    field.name,
                    [parse_field(sfield) for sfield in field.type.__dataclass_fields__.values()],
                )
            else:
                return field.name

        def unpack(name: list):
            if not isinstance(name, tuple):
                return name
            return f"{name[0]} {{ {' '.join([unpack(n) for n in name[1]])} }}"

        names = [parse_field(f) for f in model_cls.__dataclass_fields__.values()]
        names = [unpack(name) for name in names]
        return ", ".join(names)

    @staticmethod
    def _graphql_query_parameters_from_model(model: object) -> str:
        """
        Generate a GraphQL query parameters from the class for the query.

        :param model: Dataclass instance representing the query parameters and actual search values (min 1)python

        :return: Portion of a graphql query which specifies the query parameters
        """

        if not hasattr(model, "__dataclass_fields__"):
            raise TypeError("Parameter model must be a dataclass")

        # Only create query parameters for those with values using graphql syntax mask for the query parameters
        parameters = ", ".join(
            [
                f"{field.name}: {json.dumps(getattr(model, field.name), cls=DatetimeEncoder)}"
                for field in model.__dataclass_fields__.values()
                if getattr(model, field.name)
            ]
        )
        return parameters

    def get_query(
        self,
        query_base: str,
        query_response_cls: type,
        query_parameters: Optional[object] = DefaultParameters,
    ) -> Dict[str, str]:
        """
        Create a GraphQL formatted query string.

        :param query_base: Name of the root type to be queried
        :param query_response_cls: A dataclass model class representing the structure of the response object
        with attributes  corresponding to the Graphql type and attribute names
        :param query_parameters: Optional. Instance of a dataclass model containing attributes corresponding
        to parameter names and values corresponding to the parameter value.

        :return: Dictionary that can be passed as json to the GraphQL API endpoint
        """

        # Construct graphql query
        gql_query = query_base
        parameters = self._graphql_query_parameters_from_model(query_parameters)
        if parameters:
            gql_query += f"({parameters})"

        gql_query += f"{{{self._graphql_response_from_model(query_response_cls)}}}"
        return {"query": f"{{{gql_query} }}"}

    def get_mutation(
        self,
        mutation_base: str,
        mutation_parameters: object,
        mutation_response_cls: Optional[type] = None,
    ) -> Dict[str, str]:
        """
        Create a GraphQL formatted mutation string.

        :param mutation_base: Name of the root type to be mutated
        :param mutation_parameters: Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.
        :param mutation_response_cls: Optional. A dataclass model class representing the structure of the
        response object with attributes corresponding to the Graphql type and attribute names.

        :return: Dictionary that can be passed as json to the GraphQL API endpoint
        """

        # Construct graphql mutation
        gql_mutation = (
            f"mutation {mutation_base} {{{mutation_base}"
            f"({self._graphql_query_parameters_from_model(mutation_parameters)}){{ok"
        )
        if mutation_response_cls:
            gql_mutation += f", {self._graphql_response_from_model(mutation_response_cls)}"
        gql_mutation += "}"

        return {"query": f"{gql_mutation} }}", "operationName": mutation_base}

    @abstractmethod
    def execute_gql_call(self, query: dict) -> dict:
        """
        Executes a GraphQL query or mutation.

        :param query: Dictionary formatted graphql query

        :return: Dictionary containing the response from the GraphQL endpoint
        """

    def execute_gql_query(
        self, query_base: str, query_response_cls: type, query_parameters: Optional[object] = DefaultParameters
    ) -> dict:
        """
        Executes a graphql query based upon input dataclass models.

        :param query_base: Name of the root type to be queried
        :param query_parameters: Optional. Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.
        :param query_response_cls: A dataclass model class representing the structure of the response
        object with attributes corresponding to the Graphql type and attribute names

        :return: Dictionary containing the response from the GraphQL endpoint
        """

        query = self.get_query(query_base, query_response_cls, query_parameters)
        result = self.execute_gql_call(query)
        if "errors" in result:
            raise GraphQLException(errors=result["errors"])
        return result["data"]

    def execute_gql_mutation(
        self,
        mutation_base: str,
        mutation_parameters: object,
        mutation_response_cls: Optional[type] = None,
    ) -> dict:
        """
        Executes a graphql mutation based upon input dataclass models.

        :param mutation_base: Name of the root type to be mutated
        :param mutation_parameters: Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.
        :param mutation_response_cls: Optional. A dataclass model class representing the structure of the
        response object with attributes corresponding to the Graphql type and attribute names.

        :return: Dictionary containing the response from the GraphQL endpoint
        """

        mutation = self.get_mutation(mutation_base, mutation_parameters, mutation_response_cls)
        result = self.execute_gql_call(mutation)
        if "errors" in result:
            raise GraphQLException(errors=result["errors"])
        return result["data"]
