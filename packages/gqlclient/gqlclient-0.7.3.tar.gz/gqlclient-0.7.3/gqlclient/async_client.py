"""
Implementation of the Base graphql client to support the asynchronous creation and
execution of graphql queries and mutations
"""
import logging

import aiohttp

from gqlclient.base import GraphQLClientBase


__all__ = ["AsyncGraphQLClient"]


logger = logging.getLogger(__name__)


class AsyncGraphQLClient(GraphQLClientBase):
    """
    Helper class for formatting and executing asynchronous GraphQL queries and mutations

    """

    async def execute_gql_call(self, query: dict) -> dict:
        """
        Executes a GraphQL query or mutation using aiohttp.

        :param query: Dictionary formatted graphql query.

        :return: Dictionary containing the response from the GraphQL endpoint.
        """

        logger.debug(f"Executing graphql call: host={self.gql_uri}")

        async with aiohttp.ClientSession() as session:
            async with session.post(self.gql_uri, data=query) as response:
                result = await response.json()
                if response.status > 299:
                    raise ValueError(
                        f"Server returned invalid response: "
                        f"code=HTTP{response.status}, "
                        f"detail={response.json()} "
                    )
                return result
