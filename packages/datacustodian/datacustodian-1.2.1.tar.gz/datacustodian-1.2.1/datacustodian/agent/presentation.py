from datacustodian.base import AgentSectionBase
from datacustodian.utility import params_from_locals

def create_referent(name=None, start=None, end=None, operator=None, value=None,
                    schema_id=None, schema_issuer_did=None, schema_name=None,
                    schema_version=None, issuer_did=None, cred_def_id=None):
    """Creates a referent entry for either an attribute or a predicate; the
    referent entry is included in a proof request.

    Args:
        name (str): name of the attribute to include in the proof request.
        start (datetime.datetime): start date of the interval during which the
            attribute should be proofed.
        end (datetime.datetime): end date of the interval during which the
            attribute should be proofed.
        operator (str): for *predicate*, which predicate type should be used.
            Currently, only `>=` is supported.
        value: reference value to compare the attribute value to in the
            predicate using `operator`.
        schema_id (str): identifier of the schema that the proofed attribute
            should come from; acts as a restriction for the referent.
        schema_issuer_did (str): DID of the issuer who published the schema to
            the ledger; acts as a restriction for the referent.
        schema_name (str): name of the schema that the proofed attribute
            should come from; acts as a restriction for the referent.
        schema_version (str): version number that a proofed attribute value
            should correspond to; used with `schema_id` or `schema_name` to
            further restrict the referent value.
        issuer_did (str): DID of the entity that issued the credential; the
            proof will only be valid if the attribute's value comes from a
            credential issued by this DID.
        cred_def_id (str): identifier for the credential definition; the proof
            will only be valid if the credential was issued against this
            definition.

    Examples:
        Construct a zero knowledge proof predicate that age is greater than 18.

        >>> create_referent(name="age", operator=">=", value=18)
    """
    result = {
        "name": name
    }
    if start is not None or end is not None:
        non_revoked = {}
        if start is not None:
            non_revoked["from"] = int(start.timestamp())
        if end is not None:
            non_revoked["to"] = int(end.timestamp())
        result["non_revoked"] = non_revoked

    vlist = ["schema_id", "schema_issuer_did", "schema_name", "schema_version",
             "issuer_did", "cred_def_id"]
    restrictions = params_from_locals(vlist, locals())
    if len(restrictions) > 0:
        result["restrictions"] = restrictions

    if operator is not None:
        result["p_type"] = operator
        result["p_value"] = value

    return result

class Section(AgentSectionBase):
    async def ls(self, connection_id=None, initiator=None, state=None,
                 credential_definition_id=None, schema_id=None, **kwargs):
        """Queries the `/presentation-exchange` endpoint to list all the
        presentation exchange records in the agent's datastore.

        Args:
            connection_id (str): only return presentations with the specified
                connection.
            initiator (str): filter by who initiated the presentation exchangec.
            state (str): filter on the state of the presentation.
            credential_definition_id (str): filter by the credential included
                in the presentation.
            schema_id (str): filter by the schema identifier.

        Examples:
            List all the presentation records in the datastore.

            >>> await agent.presentation.ls()
            {
              "results": [
                {
                  "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
                  "presentation_request": {
                    "name": "Salary Proof",
                    "version": "0.0",
                    "nonce": "191449145666872341135494923504241174741",
                    "requested_attributes": {
                      "cac58096-4ac1-4614-a1be-20a60d3fd687": {
                        "restrictions": [
                          {
                            "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                          }
                        ],
                        "name": "first_name"
                      }
                    },
                    "requested_predicates": {
                      "6aee4954-d5e3-4f4a-abb4-337962679fbc": {
                        "p_type": ">=",
                        "restrictions": [
                          {
                            "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                          }
                        ],
                        "p_value": "60000",
                        "name": "salary"
                      }
                    }
                  },
                  "thread_id": "415ef51f-91b3-4e37-a53f-f0ddf41f7bfb",
                  "updated_at": "2019-08-16 17:30:46.383567Z",
                  "created_at": "2019-08-16 17:30:46.383567Z",
                  "state": "request_sent",
                  "initiator": "self",
                  "presentation_exchange_id": "fd55fc4b-771d-48f8-94fc-54aec235c891"
                }
              ]
            }
        """
        vlist = ["connection_id", "initiator", "state", "credential_definition_id", "schema_id"]
        params = params_from_locals(vlist, locals())
        r = await self.request("GET", "/presentation_exchange", params=params, **kwargs)
        return r["results"]

    async def create_request(self, connection_id, name, version, referents, **kwargs):
        """Queries the `/presentation_exchange/create_request` endpoint to
        create a new proof request for presentation of credentials.

        Args:
            connection_id (str): identifier for the connection that the request
                will be sent to.
            name (str): name to give to the proof request.
            version (str): corresponding version number for `name`.
            referents (list): of `dict` returned by :func:`create_referent`.

        Examples:
            Create a new proof request for name and salary.

            >>> company_did = "GCDUzc9PwYpwW8ouRxuioN"
            >>> first_name = create_referent("first_name", issuer_did=company_did)
            >>> salary = create_referent("salary", operator=">=", value="80000")
            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> referents = [first_name, last_name, salary]
            >>> await agent.presentation.create_request(connection_id, "salary_proof", "0.0", referents)
            {
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "presentation_request": {
                "name": "Salary Proof",
                "version": "0.0",
                "nonce": "191449145666872341135494923504241174741",
                "requested_attributes": {
                  "cac58096-4ac1-4614-a1be-20a60d3fd687": {
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "name": "first_name"
                  }
                },
                "requested_predicates": {
                  "6aee4954-d5e3-4f4a-abb4-337962679fbc": {
                    "p_type": ">=",
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "p_value": "60000",
                    "name": "salary"
                  }
                }
              },
              "thread_id": "415ef51f-91b3-4e37-a53f-f0ddf41f7bfb",
              "updated_at": "2019-08-16 17:30:46.383567Z",
              "created_at": "2019-08-16 17:30:46.383567Z",
              "state": "request_sent",
              "initiator": "self",
              "presentation_exchange_id": "fd55fc4b-771d-48f8-94fc-54aec235c891"
            }
        """
        attrs = [r for r in referents if "p_type" not in r]
        preds = [r for r in referents if "p_type" in r]
        body = {
            "connection_id": connection_id,
            "name": name,
            "version": version,
            "requested_predicates": preds,
            "requested_attributes": attrs
        }
        url = "/presentation_exchange/create_request"
        r = await self.request("POST", url, data=body, **kwargs)
        return r

    async def send_request(self, connection_id, name, version, referents, **kwargs):
        """Calls the `/presentation_exchange/send_request` endpoint to
        create a new proof request for presentation of credentials *and* send
        it to the agent for `connection_id`.

        Args:
            connection_id (str): identifier for the connection that the request
                will be sent to.
            name (str): name to give to the proof request.
            version (str): corresponding version number for `name`.
            referents (list): of `dict` returned by :func:`create_referent`.

        Examples:
            Send a new proof request for name and salary.

            >>> company_did = "GCDUzc9PwYpwW8ouRxuioN"
            >>> first_name = create_referent("first_name", issuer_did=company_did)
            >>> salary = create_referent("salary", operator=">=", value="80000")
            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> referents = [first_name, last_name, salary]
            >>> await agent.presentation.send_request(connection_id, "salary_proof", "0.0", referents)
            {
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "presentation_request": {
                "name": "Salary Proof",
                "version": "0.0",
                "nonce": "168259910145131537618888911963208560244",
                "requested_attributes": {
                  "c4cb4166-e803-4c18-acd9-10dbae55582e": {
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "name": "first_name"
                  }
                },
                "requested_predicates": {
                  "8ca161c7-f652-41f7-8a50-8a9662e60475": {
                    "p_type": ">=",
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "p_value": "60000",
                    "name": "salary"
                  }
                }
              },
              "thread_id": "99014d31-56b0-4045-bd6f-9b6bcdffb459",
              "updated_at": "2019-08-16 17:38:34.310596Z",
              "created_at": "2019-08-16 17:38:34.310596Z",
              "state": "request_sent",
              "initiator": "self",
              "presentation_exchange_id": "63a646a0-2f40-4ab4-9a6a-f84a067b7f5a"
            }
        """
        attrs = [r for r in referents if "p_type" not in r]
        preds = [r for r in referents if "p_type" in r]
        body = {
            "connection_id": connection_id,
            "name": name,
            "version": version,
            "requested_predicates": preds,
            "requested_attributes": attrs
        }
        url = "/presentation_exchange/create_request"
        r = await self.request("POST", url, data=body, **kwargs)
        return r

    async def get(self, presx_id, **kwargs):
        """Queries the `/presentation_exchange/{id}` endpoint to get the details
        of a presentation exchange/proof request from this agent's perspective.

        Args:
            presx_id (str): presentation exchange identifier.

        Examples:
            Gets the details of a presentation exchange from this agent's
            point of view.

            >>> presx_id = "fd55fc4b-771d-48f8-94fc-54aec235c891"
            >>> await agent.presentation.get(presx_id)
            {
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "presentation_request": {
                "name": "Salary Proof",
                "version": "0.0",
                "nonce": "191449145666872341135494923504241174741",
                "requested_attributes": {
                  "cac58096-4ac1-4614-a1be-20a60d3fd687": {
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "name": "first_name"
                  }
                },
                "requested_predicates": {
                  "6aee4954-d5e3-4f4a-abb4-337962679fbc": {
                    "p_type": ">=",
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "p_value": "60000",
                    "name": "salary"
                  }
                }
              },
              "thread_id": "415ef51f-91b3-4e37-a53f-f0ddf41f7bfb",
              "updated_at": "2019-08-16 17:30:46.383567Z",
              "created_at": "2019-08-16 17:30:46.383567Z",
              "state": "request_sent",
              "initiator": "self",
              "presentation_exchange_id": "fd55fc4b-771d-48f8-94fc-54aec235c891"
            }
        """
        url = f"/presentation_exchange/{presentation_id}"
        r = await self.request("GET", url, **kwargs)
        return r

    async def rm(self, presx_id, **kwargs):
        """Calls the `/presentation_exchange/{id}/remove` endpoint to delete
        a presentation exchange record.

        Args:
            presx_id (str): presentation exchange identifier.

        Examples:
            Delete a presentation exchange record.

            >>> presx_id = "fd55fc4b-771d-48f8-94fc-54aec235c891"
            >>> await agent.presentation.rm(presx_id)
            {}
        """
        url = f"/presentation_exchange/{presentation_id}/remove"
        r = await self.request("POST", url, **kwargs)
        return r

    async def find(self, presx_id, start=None, count=None, query=None, **kwargs):
        """Calls the `/presentation_exchange/{id}/credentials` endpoint to
        find a list of credentials that satisfy a proof request.

        Args:
            presx_id (str): presentation exchange identifier.
            start (int): start index for paging results.
            count (int): number of credential matches to return.
            query (dict): additional query parameters that follow the wallet
                query language specification.

        Returns:
            list: of credential `dict` with credentials that could fulfill the
            proof request.

        Examples:
            Compile credentials for a proof request.

            >>> presx_id = "5863046c-f731-4705-a3b0-b8507ce78f1b"
            >>> await agent.presentation.find(presx_id)
            [
              {
                "cred_info": {
                  "referent": "36cae916-b310-4128-81a6-0eddc13290c1",
                  "attrs": {
                    "first_name": "Agent",
                    "last_name": "B",
                    "salary": "100000"
                  },
                  "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                  "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                  "rev_reg_id": null,
                  "cred_rev_id": null
                },
                "interval": null,
                "presentation_referents": [
                  "78e43f6d-a8f9-4a49-9964-bb670d02b9ee",
                  "4b9c17d9-05fa-4cda-aaa1-d36672816f1b"
                ]
              }
            ]
        """
        params = params_from_locals(["start", "count", "query"], locals())
        url = f"/presentation_exchange/{presentation_id}/credentials"
        r = await self.request("GET", url, params=params, **kwargs)
        return r

    async def query(self, presx_id, referent, start=None, count=None, query=None,
                    **kwargs):
        """Calls the `/presentation_exchange/{id}/credentials/{referent}` endpoint to
        compile a list of credentials that satisfy a proof request. This allows
        additional filtering to select only the credential that matches a given
        referent. The referent is present in the `presentation_referents` key
        of the output of :meth:`build`.

        Args:
            presx_id (str): presentation exchange identifier.
            referent (str): presentation referent to filter by.
            start (int): start index for paging results.
            count (int): number of credential matches to return.
            query (dict): additional query parameters that follow the wallet
                query language specification.

        Returns:
            list: of credential `dict` with credentials that could fulfill the
            proof request.

        Examples:
            Compile credentials for a proof request.

            >>> presx_id = "5863046c-f731-4705-a3b0-b8507ce78f1b"
            >>> referent = "78e43f6d-a8f9-4a49-9964-bb670d02b9ee"
            >>> await agent.presentation.query(presx_id, referent)
            [
              {
                "cred_info": {
                  "referent": "36cae916-b310-4128-81a6-0eddc13290c1",
                  "attrs": {
                    "first_name": "Agent",
                    "salary": "100000",
                    "last_name": "B"
                  },
                  "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                  "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                  "rev_reg_id": null,
                  "cred_rev_id": null
                },
                "interval": null,
                "presentation_referents": [
                  "78e43f6d-a8f9-4a49-9964-bb670d02b9ee"
                ]
              }
            ]
        """
        params = params_from_locals(["start", "count", "query"], locals())
        url = f"/presentation_exchange/{presentation_id}/credentials/{referent}"
        r = await self.request("GET", url, params=params, **kwargs)
        return r

    async def send(self, presx_id, selection=None, self_attested=None, **kwargs):
        """Builds and sends a proof by selecting which credential to use as
        proof for each item in the proof request.

        .. warning: If `selection=None` is kept as the default, then the first
            credential that can provide each attribute is automatically selected.
            If no credential can provide the attribute, then it is added to the
            self-attested attributes section.

        Args:
            presx_id (str): presentation exchange identifier; this provides the
                proof request to get a list of the needed attributes/predicates.
            selection (dict): keys are attributes from the proof request, values
                are the credential_ids to use (taken from the `referent` key)
                in the `cred_info` section of the response from :meth:`find` or
                :meth:`query`.
            self_attested (dict): keys are attribute names; values are the
                self-attested values to place in the proof response.

        Examples:

            >>>
            {
              "state": "presentation_sent",
              "initiator": "external",
              "presentation": {
                "proof": {
                  "proofs": [
                    {
                      "primary_proof": {
                        "eq_proof": {
                          "revealed_attrs": {
                            "first_name": "8006664698637344886691470880164057734793404650779432374858963233917812847007"
                          },
                          "a_prime": "...",
                          "e": "...",
                          "v": "...",
                          "m": {
                            "last_name": "...",
                            "master_secret": "...",
                            "salary": ""
                          },
                          "m2": "..."
                        },
                        "ge_proofs": [
                          {
                            "u": {
                              "0": "...",
                              "1": "...",
                              "2": "...",
                              "3": "..."
                            },
                            "r": {
                              "0": "...",
                              "1": "...",
                              "2": "...",
                              "3": "...",
                              "DELTA": "..."
                            },
                            "mj": "...",
                            "alpha": "...",
                            "t": {
                              "0": "...",
                              "1": "...",
                              "2": "...",
                              "3": "...",
                              "DELTA": "..."
                            },
                            "predicate": {
                              "attr_name": "salary",
                              "p_type": "GE",
                              "value": 60000
                            }
                          }
                        ]
                      },
                      "non_revoc_proof": null
                    }
                  ],
                  "aggregated_proof": {
                    "c_hash": "...",
                    "c_list": [
                      [], #List of integer numbers
                      [], #List of integer numbers
                      [], #List of integer numbers
                      [], #List of integer numbers
                      [], #List of integer numbers
                      []  #List of integer numbers
                    ]
                  }
                },
                "requested_proof": {
                  "revealed_attrs": {
                    "4b9c17d9-05fa-4cda-aaa1-d36672816f1b": {
                      "sub_proof_index": 0,
                      "raw": "Agent",
                      "encoded": "..."
                    }
                  },
                  "self_attested_attrs": {},
                  "unrevealed_attrs": {},
                  "predicates": {
                    "78e43f6d-a8f9-4a49-9964-bb670d02b9ee": {
                      "sub_proof_index": 0
                    }
                  }
                },
                "identifiers": [
                  {
                    "schema_id": "GCDUzc9PwYpwW8ouRxuioN:2:Job:0.0",
                    "cred_def_id": "GCDUzc9PwYpwW8ouRxuioN:3:CL:13:default",
                    "rev_reg_id": null,
                    "timestamp": null
                  }
                ]
              },
              "connection_id": "d1c86320-ff47-4d74-a073-dd0e5bf44176",
              "presentation_request": {
                "name": "Salary Proof",
                "version": "0.0",
                "nonce": "68507530790756417550294277798316714343",
                "requested_attributes": {
                  "4b9c17d9-05fa-4cda-aaa1-d36672816f1b": {
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "name": "first_name"
                  }
                },
                "requested_predicates": {
                  "78e43f6d-a8f9-4a49-9964-bb670d02b9ee": {
                    "p_type": ">=",
                    "restrictions": [
                      {
                        "issuer_did": "GCDUzc9PwYpwW8ouRxuioN"
                      }
                    ],
                    "p_value": 60000,
                    "name": "salary"
                  }
                }
              },
              "created_at": "2019-08-16 17:41:15.691958Z",
              "updated_at": "2019-08-16 18:32:53.059550Z",
              "thread_id": "7cb3670f-54f5-4fc1-b37f-904585dd7388",
              "presentation_exchange_id": "5863046c-f731-4705-a3b0-b8507ce78f1b"
            }
        """
        #Include self-attested attributes (not included in credentials)
        r = {
            "requested_attributes": {},
            "requested_predicates": {},
            "self_attested_attributes": {}
        }

        request = self.get(presx_id)
        for coll in ["requested_attributes", "requested_predicates"]:
            for referent in request[coll]:
                attrname = request[coll][referent]["name"]
                cred_id = selection.get(attrname, None)

                if cred_id is None:
                    creds = await self.query(presx_id, referent)
                    if len(creds) > 0:
                        cred_id = creds[0]["cred_info"]["referent"]

                if cred_id is not None:
                    r[coll][referent] = {
                        "cred_id": cred_id,
                        "revealed": True,
                    }
                elif "p_value" not in request[coll][referent]:
                    r["self_attested_attributes"][referent] = self_attested.get(attrname)

        url = f"/presentation_exchange/{presentation_id}/send_presentation"
        r = await self.request("POST", url, data=r, **kwargs)
        return r

    async def verify(self, presx_id, **kwargs):
        """Calls the `/presentation_exchange/{id}/verify` endpoint to
        verify that the proof sent back is valid.

        Args:
            presx_id (str): presentation exchange identifier.

        Returns:
            bool: `True` if the verification succeeded. To view the full details
            of the proof submitted, use :meth:`get` with the same `presx_id`,
            which will include the full details and present a state of `verified`.

        Examples:
            Verify a proof request associated with this presentation exchange.

            >>> presx_id = "5863046c-f731-4705-a3b0-b8507ce78f1b"
            >>> await agent.presentation.verify(presx_id)
            True
        """
        url = f"/presentation_exchange/{presentation_id}/verify_presentation"
        r = await self.request("POST", url, **kwargs)
        return r["state"] == "verified"
