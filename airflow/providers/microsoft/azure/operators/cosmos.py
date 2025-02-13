#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from typing import TYPE_CHECKING

from airflow.models import BaseOperator
from airflow.providers.microsoft.azure.hooks.cosmos import AzureCosmosDBHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class AzureCosmosInsertDocumentOperator(BaseOperator):
    """
    Inserts a new document into the specified Cosmos database and collection
    It will create both the database and collection if they do not already exist

    :param database_name: The name of the database. (templated)
    :type database_name: str
    :param collection_name: The name of the collection. (templated)
    :type collection_name: str
    :param document: The document to insert
    :type document: dict
    :param azure_cosmos_conn_id: Reference to the
        :ref:`Azure CosmosDB connection<howto/connection:azure_cosmos>`.
    :type azure_cosmos_conn_id: str
    """

    template_fields = ('database_name', 'collection_name')
    ui_color = '#e4f0e8'

    def __init__(
        self,
        *,
        database_name: str,
        collection_name: str,
        document: dict,
        azure_cosmos_conn_id: str = 'azure_cosmos_default',
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.database_name = database_name
        self.collection_name = collection_name
        self.document = document
        self.azure_cosmos_conn_id = azure_cosmos_conn_id

    def execute(self, context: "Context") -> None:
        # Create the hook
        hook = AzureCosmosDBHook(azure_cosmos_conn_id=self.azure_cosmos_conn_id)

        # Create the DB if it doesn't already exist
        if not hook.does_database_exist(self.database_name):
            hook.create_database(self.database_name)

        # Create the collection as well
        if not hook.does_collection_exist(self.collection_name, self.database_name):
            hook.create_collection(self.collection_name, self.database_name)

        # finally insert the document
        hook.upsert_document(self.document, self.database_name, self.collection_name)
