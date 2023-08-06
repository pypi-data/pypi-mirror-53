from datacustodian.base import AgentSectionBase

class Section(AgentSectionBase):
    async def new_schema(self, name, version, attributes, **kwargs):
        """Calls the `/schemas` endpoint to send a new schema definition to the
        ledger.

        Args:
            name (str): name for the schema.
            version (str): unique (to this name) version number.
            attributes (list): of `str` attribute names defined by the schema.

        Examples:
            Create a new schema on the ledger.

            >>> attrs = ["first_name", "last_name", "salary"]
            >>> await agent.definitions.new_schema("Job", "0.0", attrs)
            {
              "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0"
            }
        """
        body = {
          "attributes": attributes,
          "schema_name": name,
          "schema_version": version
        }
        r = await self.request("POST", "/schemas", data=body, **kwargs)
        return r

    async def get_schema(self, schema_id, **kwargs):
        """Queries the `/schemas/{id}` endpoint to get the definition of a schema.

        Args:
            schema_id (str): identifier for the schema.

        Examples:
            Get a schema definition from the ledger (or locally if possible).

            >>> schema_id = "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0"
            >>> await agent.definitions.get_schema(schema_id)
            {
              "schema_json": {
                "ver": "1.0",
                "id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "name": "Job",
                "version": "0.0",
                "attrNames": [
                  "salary",
                  "last_name",
                  "first_name"
                ],
                "seqNo": 13
              }
            }
        """
        r = await self.request("GET", f"/schemas/{schema_id}", **kwargs)
        return r

    async def new_credential(self, schema_id, **kwargs):
        """Calls the `/credential-definitions` endpoint to send a new credential
        definition to the ledger.

        Args:
            schema_id (str): identifier for the schema that the credential
                definition will be based on.

        Examples:
            Create a new credential definition on the ledger.

            >>> await agent.definitions.new_credential("GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0")
            {
              "credential_definition_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default"
            }
        """
        body = {
          "schema_id": schema_id
        }
        r = await self.request("POST", "/credential-definitions", data=body, **kwargs)
        return r

    async def get_credential(self, credential_id, **kwargs):
        """Queries the `/credential/{id}` endpoint to get the definition of a
        credential.

        Args:
            credential_id (str): identifier for the credential.

        Examples:
            Get a credential definition from the ledger (or locally if possible).

            >>> cred_id = "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default"
            >>> await agent.definitions.get_credential(cred_id)
            {
              "credential_definition": {
                "ver": "1.0",
                "id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "schemaId": "13",
                "type": "CL",
                "tag": "default",
                "value": {
                  "primary": {
                    "n": "...",
                    "s": "...",
                    "r": {
                      "last_name": "...",
                      "master_secret": "...",
                      "first_name": "...",
                      "salary": "...",
                    },
                    "rctxt": "...",
                    "z": "..."
                  }
                }
              }
            }
        """
        r = await self.request("GET", f"/credential-definitions/{credential_id}", **kwargs)
        return r["credential_definition"]
