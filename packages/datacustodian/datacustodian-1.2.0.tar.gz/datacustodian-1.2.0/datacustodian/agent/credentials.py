from datacustodian.base import AgentSectionBase, testmode

class Section(AgentSectionBase):
    async def exchange_purge(self):
        """Purges all credential exchange records from the agent.

        .. warning: This should only be run during unit testing;
            :attr:`datacustodian.base.testmode` is checked before any deletion
            takes place.
        """
        if testmode:
            recs = await self.exchange_ls()
            for rec in recs:
                credx_id = rec["credential_exchange_id"]
                await self.exchange_rm(credx_id)

    async def ls(self, start=0, count=10, wql=None, **kwargs):
        """Queries the `/credentials` endpoint to list credentials in the wallet
        of the agent.

        Args:
            start (int): start index for paging credentials.
            count (int): number of credentials to return.
            wql (dict): query filters following the structure of the wallet
                query language.

        Examples:
            List all the credentials in the wallet.

            >>> await agent.credentials.ls()
            {
              "results": [
                {
                  "referent": "36cae916-b310-4128-81a6-0eddc13290c1", #This is also the credential_id.
                  "attrs": {
                    "last_name": "B",
                    "salary": "100000",
                    "first_name": "Agent"
                  },
                  "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                  "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                  "rev_reg_id": null,
                  "cred_rev_id": null
                }
              ]
            }
        """
        params = {
            "start": start,
            "count": count,
        }
        if wql is not None:
            params["wql"] = wql
        r = await self.request("GET", "/credentials", params=params, **kwargs)
        return r

    async def get(self, cred_id, **kwargs):
        """Queries the `/credentials/{id}` endpoint to get a credential from
        the agent's wallet.

        Args:
            cred_id (str): credential identifier.

        Examples:
            Get the credential with `cred_id`.

            >>> cred_id = "36cae916-b310-4128-81a6-0eddc13290c1"
            >>> await agent.credentials.get(cred_id)
            {
              "referent": "36cae916-b310-4128-81a6-0eddc13290c1",
              "attrs": {
                "last_name": "B",
                "salary": "100000",
                "first_name": "Agent"
              },
              "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
              "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
              "rev_reg_id": null,
              "cred_rev_id": null
            }
        """
        r = await self.request("GET", f"/credentials/{cred_id}", **kwargs)
        return r

    async def rm(self, cred_id, **kwargs):
        """Queries the `/credentials/{id}/remove` endpoint to delete a credential
        from the wallet storage of the agent.

        Args:
            cred_id (str): credential identifier for the credential to delete.

        Examples:
            Delete the credential with `cred_id`.

            >>> cred_id = "36cae916-b310-4128-81a6-0eddc13290c1"
            >>> await agent.credentials.rm(cred_id)
            {}
        """
        r = await self.request("POST", f"/credentials/{cred_id}/remove", **kwargs)
        return r

    async def send(self, cred_def_id, connection_id, values, **kwargs):
        """Automates the process of sending a credential to a connection.

        Args:
            cred_def_id (str): credential definition identifier to send.
            connection_id (str): connection id for the unique pairwise connection
                with the entity receiving the credential.
            values (dict): key-value pairs to populate the attributes defined
                in the schema for the credential.

        ... note:: This method is almost identical to :meth:`offer` in its
            interface and output, however, the return value from this method
            includes an attribute `"auto_issue": true,`, so that as soon as
            the recipient of the offer sends a `request` back, the credential
            is immediately issued. Thus, see :meth:`offer` for an example.
        """
        body = {
            "credential_definition_id": cred_def_id,
            "connection_id": connection_id,
            "credential_values": values
        }
        r = await self.request("POST", "/credential_exchange/send", data=body, **kwargs)
        return r

    async def offer(self, cred_def_id, connection_id, **kwargs):
        """Sends a credential offer to a connection.

        Args:
            cred_def_id (str): credential definition identifier to send.
            connection_id (str): connection id for the unique pairwise connection
                with the entity receiving the credential.

        Examples:
            Send a credential offer to a connection.

            >>> await agent.credentials.offer(cred_def_id, connection_id)
            {
              "credential_offer": {
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "key_correctness_proof": {
                  "c": "35866109715936925676903054929804358665535653649424099774253790184615283595412",
                  "xz_cap": "...",
                  "xr_cap": [
                    ["salary", "..."],
                    ["first_name", "..."],
                    ["last_name", "..."],
                    ["master_secret", "..."]
                  ]
                },
                "nonce": "1160357048857630448462928"
              },
              "credential_definition_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "created_at": "2019-08-15 22:48:10.069399Z",
              "credential_exchange_id": "7f957ba1-d6d5-4b71-9405-d6a201d1243c",
              "updated_at": "2019-08-15 22:48:10.102907Z",
              "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
              "thread_id": "19f9aeca-024b-472e-9f49-d6d305910a2c",
              "state": "offer_sent",
              "initiator": "self"
            }

        Returns:
            dict: credential offer details.
        """
        body = {
            "credential_definition_id": cred_def_id,
            "connection_id": connection_id,
        }
        r = await self.request("POST", "/credential_exchange/send-offer", data=body, **kwargs)
        return r

    async def send_request(self, credx_id, **kwargs):
        """Requests an offered credential using the
        `/credential_exchange/{id}/send-request` endpoint.

        Args:
            credx_id (str): credential exchange identifier that was present
                in the offer for a credential.

        Examples:
            Requests a credential from the exchange.

            >>> credx_id = ""
            >>> await agent.credentials.send_request(credx_id)
            {
              "updated_at": "2019-08-15 22:54:59.458364Z",
              "created_at": "2019-08-15 22:54:35.762285Z",
              "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
              "credential_request": {
                "prover_did": "WHUpJ7SbrnbhMvwsJdmSNk",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "blinded_ms": {
                  "u": "...",
                  "ur": null,
                  "hidden_attributes": [
                    "master_secret"
                  ],
                  "committed_attributes": {}
                },
                "blinded_ms_correctness_proof": {
                  "c": "10765547151389406077873479387123367169215026470978008459443743423032776457833",
                  "v_dash_cap": "...",
                  "m_caps": {
                    "master_secret": "...""
                  },
                  "r_caps": {}
                },
                "nonce": "962284677669343385876123"
              },
              "state": "request_sent",
              "credential_definition_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
              "auto_issue": false,
              "credential_request_metadata": {
                "master_secret_blinding_data": {
                  "v_prime": "...",
                  "vr_prime": null
                },
                "nonce": "962284677669343385876123",
                "master_secret_name": "wallet"
              },
              "thread_id": "a97ab2d4-92a8-4041-83b5-0f3818467ea9",
              "credential_offer": {
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "key_correctness_proof": {
                  "c": "35866109715936925676903054929804358665535653649424099774253790184615283595412",
                  "xz_cap": "...",
                  "xr_cap": [
                    ["salary", "..."],
                    ["first_name", "..."],
                    ["last_name", "..."],
                    ["master_secret", "..."]
                  ]
                },
                "nonce": "990549642155389412323481"
              },
              "initiator": "external",
              "connection_id": "d1c86320-ff47-4d74-a073-dd0e5bf44176",
              "credential_exchange_id": "9e814d49-d43a-4d1b-80af-c850f65208ec"
            }
        """
        url = f"/credential_exchange/{credx_id}/send-request"
        r = await self.request("POST", url, **kwargs)
        return r

    async def issue(self, credx_id, values, **kwargs):
        """Issues a credential using the `/credential_exchange/{id}/issue`
        endpoint.

        Args:
            credx_id (str): credential exchange identifier that was present
                in the offer for a credential.
            values (dict): key-value pairs to populate the attributes in the
                schema for the credential.

        Examples:
            Issues a credential present in the exchange.

            >>> credx_id = "20d64056-404a-477b-bbca-854078b444b8"
            >>> values = {"first_name": "Agent", "last_name": "B", "salary": "100000"}
            >>> await agent.credentials.issue(credx_id)
            {
              "credential_offer": {
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "key_correctness_proof": {
                  "c": "35866109715936925676903054929804358665535653649424099774253790184615283595412",
                  "xz_cap": "...",
                  "xr_cap": [
                    ["salary", "..."],
                    ["first_name", "..."],
                    ["last_name", "..."],
                    ["master_secret", "..."]
                  ]
                },
                "nonce": "990549642155389412323481"
              },
              "credential_definition_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "created_at": "2019-08-15 22:54:35.413693Z",
              "credential_exchange_id": "20d64056-404a-477b-bbca-854078b444b8",
              "updated_at": "2019-08-15 22:58:53.614848Z",
              "credential_request": {
                "prover_did": "WHUpJ7SbrnbhMvwsJdmSNk",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "blinded_ms": {
                  "u": "...",
                  "ur": null,
                  "hidden_attributes": [
                    "master_secret"
                  ],
                  "committed_attributes": {}
                },
                "blinded_ms_correctness_proof": {
                  "c": "10765547151389406077873479387123367169215026470978008459443743423032776457833",
                  "v_dash_cap": "...",
                  "m_caps": {
                    "master_secret": "...""
                  },
                  "r_caps": {}
                },
                "nonce": "962284677669343385876123"
              },
              "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
              "thread_id": "a97ab2d4-92a8-4041-83b5-0f3818467ea9",
              "credential_values": {
                "first_name": "Agent",
                "last_name": "B",
                "salary": "100000"
              },
              "state": "issued",
              "credential": {
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "rev_reg_id": null,
                "values": {
                  "first_name": {
                    "raw": "Agent",
                    "encoded": "8006664698637344886691470880164057734793404650779432374858963233917812847007"
                  },
                  "salary": {
                    "raw": "100000",
                    "encoded": "100000"
                  },
                  "last_name": {
                    "raw": "B",
                    "encoded": "101089167133868482642301738280228084727114034694682239136375376240207457290844"
                  }
                },
                "signature": {
                  "p_credential": {
                    "m_2": "94785095336025468746497660823015684431407080898007803979568358415687969945701",
                    "a": "...",
                    "e": "...",
                    "v": "..."
                  },
                  "r_credential": null
                },
                "signature_correctness_proof": {
                  "se": "...",
                  "c": "64126379367933652852224916865576559682747302721261059605930753484992066732863"
                },
                "rev_reg": null,
                "witness": null
              },
              "initiator": "self"
            }
        """
        url = f"/credential_exchange/{credx_id}/send-request"
        r = await self.request("POST", url, **kwargs)
        return r

    async def store(self, credx_id, **kwargs):
        """Stores a credential received through the exchange. Uses the
        `/credential_exchange/{id}/store` endpoint.

        Args:
            credx_id (str): credential exchange identifier that was present
                in the offer for a credential.

        Examples:
            Stores a credential received through the exchange in the agent's
            wallet.

            >>> credx_id = "9e814d49-d43a-4d1b-80af-c850f65208ec"
            >>> await agent.credentials.store(credx_id)
            {
              "updated_at": "2019-08-15 23:04:01.076174Z",
              "created_at": "2019-08-15 22:54:35.762285Z",
              "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
              "credential_request": {
                "prover_did": "WHUpJ7SbrnbhMvwsJdmSNk",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "blinded_ms": {
                  "u": "...",
                  "ur": null,
                  "hidden_attributes": [
                    "master_secret"
                  ],
                  "committed_attributes": {}
                },
                "blinded_ms_correctness_proof": {
                  "c": "10765547151389406077873479387123367169215026470978008459443743423032776457833",
                  "v_dash_cap": "...",
                  "m_caps": {
                    "master_secret": "...""
                  },
                  "r_caps": {}
                },
                "nonce": "962284677669343385876123"
              },
              "raw_credential": {
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "rev_reg_id": null,
                "values": {
                  "first_name": {
                    "raw": "Agent",
                    "encoded": "8006664698637344886691470880164057734793404650779432374858963233917812847007"
                  },
                  "salary": {
                    "raw": "100000",
                    "encoded": "100000"
                  },
                  "last_name": {
                    "raw": "B",
                    "encoded": "101089167133868482642301738280228084727114034694682239136375376240207457290844"
                  }
                },
                "signature": {
                  "p_credential": {
                    "m_2": "...",
                    "a": "...",
                    "e": "...",
                    "v": "..."
                  },
                  "r_credential": null
                },
                "signature_correctness_proof": {
                  "se": "...",
                  "c": "...""
                },
                "rev_reg": null,
                "witness": null
              },
              "state": "stored",
              "credential_definition_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
              "auto_issue": false,
              "credential_id": "36cae916-b310-4128-81a6-0eddc13290c1",
              "credential": {
                "referent": "36cae916-b310-4128-81a6-0eddc13290c1",
                "attrs": {
                  "last_name": "B",
                  "salary": "100000",
                  "first_name": "Agent"
                },
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "rev_reg_id": null,
                "cred_rev_id": null
              },
              "credential_request_metadata": {
                "master_secret_blinding_data": {
                  "v_prime": "...",
                  "vr_prime": null
                },
                "nonce": "962284677669343385876123",
                "master_secret_name": "wallet"
              },
              "thread_id": "a97ab2d4-92a8-4041-83b5-0f3818467ea9",
              "credential_offer": {
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "key_correctness_proof": {
                  "c": "35866109715936925676903054929804358665535653649424099774253790184615283595412",
                  "xz_cap": "...",
                  "xr_cap": [
                    ["salary", "..."],
                    ["first_name", "..."],
                    ["last_name", "..."],
                    ["master_secret", "..."]
                  ]
                },
                "nonce": "990549642155389412323481"
              },
              "initiator": "external",
              "connection_id": "d1c86320-ff47-4d74-a073-dd0e5bf44176",
              "credential_exchange_id": "9e814d49-d43a-4d1b-80af-c850f65208ec"
            }
        """
        url = f"/credential_exchange/{credx_id}/store"
        r = await self.request("POST", url, **kwargs)
        return r

    async def report_problem(self, credx_id, error, **kwargs):
        """Stores a credential received through the exchange. Uses the
        `/credential_exchange/{id}/store` endpoint.

        Args:
            credx_id (str): credential exchange identifier used in the messaging.
            error (str): localized error message about the credential exchange
                referenced by `credx_id`.

        Examples:
            Report a problem with the credential exchange referenced by
            `credx_id`.

            >>> credx_id = "9e814d49-d43a-4d1b-80af-c850f65208ec"
            >>> localized_error = "I don't like the salary."
            >>> await agent.credentials.report_problem(credx_id, localized_error)
            {}
        """
        body = {
          "explain_ltxt": error
        }
        url = f"/credential_exchange/{credx_id}/problem_report"
        r = await self.request("POST", url, **kwargs)
        return r

    async def exchange_ls(self, **kwargs):
        """Queries the `/credential_exchange` endpoint to list all the
        credential exchange records in the datastore of the agent.

        Examples:
            List all the credential exchange records in the datastore.

            >>> await agent.credentials.exchange_ls()
            {
              "results": [
                {
                  "updated_at": "2019-08-15 22:48:10.696277Z",
                  "created_at": "2019-08-15 22:48:10.696277Z",
                  "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                  "state": "offer_received",
                  "credential_definition_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                  "auto_issue": false,
                  "thread_id": "19f9aeca-024b-472e-9f49-d6d305910a2c",
                  "credential_offer": {
                    "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                    "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                    "key_correctness_proof": {
                      "c": "35866109715936925676903054929804358665535653649424099774253790184615283595412",
                      "xz_cap": "...",
                      "xr_cap": [
                        ["salary", "..."],
                        ["first_name", "..."],
                        ["last_name", "..."],
                        ["master_secret", "..."]
                      ]
                    },
                    "nonce": "1160357048857630448462928"
                  },
                  "initiator": "external",
                  "connection_id": "d1c86320-ff47-4d74-a073-dd0e5bf44176",
                  "credential_exchange_id": "34075072-00d7-4352-aa2d-e533448c8962"
                }
              ]
            }
        """
        r = await self.request("GET", "/credential_exchange", **kwargs)
        return r["results"]

    async def exchange_get(self, credx_id, **kwargs):
        """Queries the `/credential_exchange/{id}` endpoint to get a credential
        exchange record from the datastore of the agent.

        Args:
            credx_id (str): credential exchange identifier.

        Examples:
            Get the credential exchange record with `credx_id`.

            >>> credx_id = "34075072-00d7-4352-aa2d-e533448c8962"
            >>> await agent.credentials.exchange_get(credx_id)
            {
              "updated_at": "2019-08-15 22:48:10.696277Z",
              "created_at": "2019-08-15 22:48:10.696277Z",
              "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
              "state": "offer_received",
              "credential_definition_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
              "auto_issue": false,
              "thread_id": "19f9aeca-024b-472e-9f49-d6d305910a2c",
              "credential_offer": {
                "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                "key_correctness_proof": {
                  "c": "35866109715936925676903054929804358665535653649424099774253790184615283595412",
                  "xz_cap": "...",
                  "xr_cap": [
                    ["salary", "..."],
                    ["first_name", "..."],
                    ["last_name", "..."],
                    ["master_secret", "..."]
                  ]
                },
                "nonce": "1160357048857630448462928"
              },
              "initiator": "external",
              "connection_id": "d1c86320-ff47-4d74-a073-dd0e5bf44176",
              "credential_exchange_id": "34075072-00d7-4352-aa2d-e533448c8962"
            }
        """
        r = await self.request("GET", f"/credential_exchange/{credx_id}", **kwargs)
        return r

    async def exchange_rm(self, credx_id, **kwargs):
        """Queries the `/credential_exchange/{id}/remove` endpoint to delete a
        credential exchange record from the datastore of the agent.

        Args:
            credx_id (str): credential exchange identifier for the record to
                delete.

        Examples:
            Delete the credential exchange record with `credx_id`.

            >>> credx_id = "34075072-00d7-4352-aa2d-e533448c8962"
            >>> await agent.credentials.exchange_rm(credx_id)
            {}
        """
        url = f"/credential_exchange/{credx_id}/remove"
        r = await self.request("POST", url, **kwargs)
        return r
