from datacustodian.base import AgentSectionBase
from datacustodian.utility import params_from_locals

class Section(AgentSectionBase):
    async def ls(self, initiator=None, invitation_key=None, my_did=None,
                 state=None, their_did=None, their_role=None, **kwargs):
        """Queries the `/connections` endpoint to list all pairwise connections
        for the agent.

        Args:
            initiator (str): one of ['self', 'external'] specifying who initiated
                the connection.
            invitation_key (str): invitation key from the invitation.
            my_did (str): DID of this agent used to form the connection.
            state (str): one of ["init", "invitation", "request", "response",
                "active", "error", "inactive"], indicating the state of the
                connection.
            their_did (str): DID of the external entity that this agent
                connected with.
            their_role (str): role assigned to the external entity when the
                connection was created.

        Examples:
            List all pairwise connections for an agent.

            >>> await agent.connections.ls()
            [
                {
                  "their_label": "ugs_agent_B",
                  "routing_state": "none",
                  "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
                  "created_at": "2019-08-14 22:14:44.806956Z",
                  "invitation_key": "1mfQscKnr4MANyQzdu7p4XHX4A3Mdkd8yMNBi1t6gk2",
                  "accept": "manual",
                  "their_did": "WHUpJ7SbrnbhMvwsJdmSNk",
                  "updated_at": "2019-08-14 22:16:08.489664Z",
                  "state": "request",
                  "initiator": "self",
                  "activity": [
                    {
                      "id": "fe6ee5043e2c4c8da3c9e55ebe7b37ef",
                      "meta": null,
                      "time": "2019-08-14 22:16:08.531713Z",
                      "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
                      "direction": "received",
                      "type": "request"
                    },
                    {
                      "id": "bfcf1a8c389944f5a78e338139ea1ad0",
                      "meta": null,
                      "time": "2019-08-14 22:14:44.971868Z",
                      "direction": "sent",
                      "type": "invitation",
                      "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9"
                    }
                  ]
                },
                ...
            ]
        """
        vlist = ["initiator", "invitation", "my_did", "state", "their_did", "their_role"]
        params = params_from_locals(vlist, locals())
        r = await self.request("GET", "/connections", params=params, **kwargs)
        return r["results"]

    async def get(self, connection_id, **kwargs):
        """Queries the `/connections/{id}` endpoint to get details for a single
        connection.

        Args:
            connection_id (str): unique identifier for the connection with the
                other agent.

        Examples:
            Retrieve details for a single connection at the agent.

            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> await agent.connections.get(connection_id)
            {
              "their_label": "ugs_agent_B",
              "routing_state": "none",
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "created_at": "2019-08-14 22:14:44.806956Z",
              "invitation_key": "1mfQscKnr4MANyQzdu7p4XHX4A3Mdkd8yMNBi1t6gk2",
              "accept": "manual",
              "their_did": "WHUpJ7SbrnbhMvwsJdmSNk",
              "updated_at": "2019-08-14 22:16:08.489664Z",
              "state": "request",
              "initiator": "self"
            }
        """
        r = await self.request("GET", f"/connections/{connection_id}", **kwargs)
        return r

    async def rm(self, connection_id, **kwargs):
        """Queries the `/connections/{id}/remove` endpoint to delete an existing
        pairwise connection.

        Args:
            connection_id (str): unique identifier for the connection with the
                other agent that should be removed.

        Examples:
            Remove a connection to another agent.

            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> await agent.connections.rm(connection_id)
            {}
        """
        r = await self.request("POST", f"/connections/{connection_id}/remove", **kwargs)
        return r

    async def invite(self, auto_accept=False, public=False, my_label=None,
                     my_endpoint=None, their_role=None, multi_use=False, **kwargs):
        """Calls the `/connections/create-invitation` endpoint to create an
        invitation that can be sent to a prospective connection through some
        external means (out of band), or by calling the
        `/connections/receive-invitation` endpoint of the other agent.

        Args:
            auto_accept (bool): when True, auto-accept the invitation response
                if the other party accepts it.
            public (bool): when True, use the public DID to create the invitation.
            my_label (str): this agent's label for this connection.
            my_endpoint (str): endpoint where other party can reach this agent.
                If not specified, defaults to the one in the application
                specs for this agent.
            their_role (str): a role to assign the connection.
            multi_use (bool): set to True to create an invitation for multiple use.

        Examples:
            Create an invitation to connect.

            >>> await agent.connections.invite()
            {
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "invitation": {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
                "@id": "41b8d06c-3a28-46a0-b2e8-3e8a79882ac9",
                "serviceEndpoint": "http://datacustodian:8020",
                "recipientKeys": [
                  "1mfQscKnr4MANyQzdu7p4XHX4A3Mdkd8yMNBi1t6gk2"
                ],
                "label": "ugs_agent"
              },
              "invitation_url": "http://datacustodian:8020?c_i=eyJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9jb25uZWN0aW9ucy8xLjAvaW52aXRhdGlvbiIsICJAaWQiOiAiNDFiOGQwNmMtM2EyOC00NmEwLWIyZTgtM2U4YTc5ODgyYWM5IiwgInNlcnZpY2VFbmRwb2ludCI6ICJodHRwOi8vZGF0YWN1c3RvZGlhbjo4MDIwIiwgInJlY2lwaWVudEtleXMiOiBbIjFtZlFzY0tucjRNQU55UXpkdTdwNFhIWDRBM01ka2Q4eU1OQmkxdDZnazIiXSwgImxhYmVsIjogInVnc19hZ2VudCJ9"
            }
        """
        params = {}
        if auto_accept:
            params["accept"] = "auto"
        if public:
            params["public"] = 1
        if multi_use:
            params["multi_use"] = 1

        vlist = ["my_label", "my_endpoint", "their_role"]
        params.update(params_from_locals(vlist, locals()))
        r = await self.request("POST", "/connections/create-invitation",
                               params=params, **kwargs)
        return r

    async def receive(self, invitation, auto_accept=False, **kwargs):
        """Uses the `/connections/receive-invitation` endpoint to receive an
        out-of-band invitation created by :meth:`invite`.

        Args:
            invitation (dict): invitation data generated by :meth:`invite`.
            auto_accept (bool): when True, auto-accept the invitation once it
                has been stored.

        Examples:
            Receive an invitation from another agent.
            >>> invite = {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
                "@id": "41b8d06c-3a28-46a0-b2e8-3e8a79882ac9",
                "serviceEndpoint": "http://datacustodian:8020",
                "recipientKeys": [
                  "1mfQscKnr4MANyQzdu7p4XHX4A3Mdkd8yMNBi1t6gk2"
                ],
                "label": "ugs_agent"
            }
            >>> await agent.connections.receive(invite, True)
            {
              "routing_state": "none",
              "accept": "manual",
              "their_label": "ugs_agent",
              "created_at": "2019-08-14 22:15:37.633626Z",
              "connection_id": "d1c86320-ff47-4d74-a073-dd0e5bf44176",
              "initiator": "external",
              "invitation_key": "1mfQscKnr4MANyQzdu7p4XHX4A3Mdkd8yMNBi1t6gk2",
              "updated_at": "2019-08-14 22:15:37.633626Z",
              "state": "invitation"
            }
        """
        params = {}
        if auto_accept:
            params["accept"] = "auto"
        r = await self.request("POST", "/connections/receive-invitation",
                               params=params, **kwargs)
        return r

    async def accept(self, connection_id, my_endpoint=None, my_label=None,
                     **kwargs):
        """Uses the `/connections/accept-invitation` endpoint to accept an
        invitation that was previous received used :meth:`receive`.

        Args:
            connection_id (str): identifier for the connection after receiving
                the invitation.
            my_endpoint (str): endpoint where the other party can reach this agent.
                Defaults to the application specifications when not given.
            my_label (str): label to assign to this connection from this agent's
                perspective.

        Examples:
            Receive an invitation from another agent.
            >>> connection_id = "d1c86320-ff47-4d74-a073-dd0e5bf44176"
            >>> await agent.connections.accept(connection_id)
            {
              "routing_state": "none",
              "request_id": "4a008c6b-0bbe-4b83-80d5-f4a15ad7d065",
              "accept": "manual",
              "their_label": "ugs_agent",
              "created_at": "2019-08-14 22:15:37.633626Z",
              "connection_id": "d1c86320-ff47-4d74-a073-dd0e5bf44176",
              "initiator": "external",
              "invitation_key": "1mfQscKnr4MANyQzdu7p4XHX4A3Mdkd8yMNBi1t6gk2",
              "my_did": "WHUpJ7SbrnbhMvwsJdmSNk",
              "updated_at": "2019-08-14 22:16:07.334387Z",
              "state": "request"
            }
        """
        params = params_from_locals(["my_endpoint", "my_label"], locals())
        url = f"/connections/{connection_id}/accept-invitation"
        r = await self.request("POST", url, params=params, **kwargs)
        return r

    async def respond(self, connection_id, my_endpoint=None, **kwargs):
        """Responds to an accepted invitation using the `/connections/accept-request`
        endpoint. This changes the state of an invitation from `request` to
        `response`.

        Args:
            connection_id (str): this agent's identifier for the connection.
            my_endpoint (str): endpoint where the other party can reach this agent.
                Defaults to the application specifications when not given.

        Examples:
            Respond to invitation acceptance by another agent.
            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> await agent.connections.respond(connection_id)
            {
              "their_label": "ugs_agent_B",
              "routing_state": "none",
              "connection_id": "fea81719-b76c-4b5f-a3bd-a428dae408c9",
              "created_at": "2019-08-14 22:14:44.806956Z",
              "invitation_key": "1mfQscKnr4MANyQzdu7p4XHX4A3Mdkd8yMNBi1t6gk2",
              "accept": "manual",
              "their_did": "WHUpJ7SbrnbhMvwsJdmSNk",
              "updated_at": "2019-08-15 21:46:27.739164Z",
              "my_did": "4c3zJvY1cfzo5a8nkr9if7",
              "state": "response",
              "initiator": "self"
            }
        """
        params = params_from_locals(["my_endpoint"], locals())
        url = f"/connections/{connection_id}/accept-request"
        r = await self.request("POST", url, params=params, **kwargs)
        return r

    async def replace(self, connection_id, new_id, **kwargs):
        """Replaces an existing connection with another one. This uses the
        `/connections/{id}/establish-inbound/{ref_id}` endpoint.

        Args:
            connection_id (str): this agent's identifier for the connection.
            new_id (str): new connection_id to replace the old one with.

        Examples:
            Replace an inbound connection_id with a different one.
            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> new_id = "fea81719-b76c-4b5f-a3bd-a428dae408d0"
            >>> await agent.connections.replace(connection_id, new_id)
            {}
        """
        url = f"/connections/{connection_id}/establish-inbound/{new_id}"
        r = await self.request("POST", url, **kwargs)
        return r

    async def introduce(self, connection_id, other_connection, message, **kwargs):
        """Introduces an existing connection to another one. This uses the
        `/connections/{id}/start-introduction` endpoint.

        Args:
            connection_id (str): this agent's identifier for the connection.
            other_connection (str): the entity to introduce `connection_id` to.
            message (str): a message to send with the introduction.

        Examples:
            Introduce one connection to another.
            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> other_id = "fea81719-b76c-4b5f-a3bd-a428dae408d0"
            >>> await agent.connections.introduce(connection_id, new_id, "Hi")
            {}
        """
        params = {
            "target_connection_id": other_connection,
            "message": message
        }
        url = f"/connections/{connection_id}/start-introduction"
        r = await self.request("POST", url, params=params, **kwargs)
        return r

    async def message(self, connection_id, content, **kwargs):
        """Sends a secure, end-to-end encrypted message to a connection.

        Args:
            connection_id (str): this agent's identifier for the connection.
            content (str): a message to send with the introduction.

        Examples:
            Send an encrypted message to a connection.
            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> await agent.connections.message(connection_id, "Hi")
            {}
        """
        body = {
            "content": content
        }
        url = f"/connections/{connection_id}/send-message"
        r = await self.request("POST", url, data=body, **kwargs)
        return r

    async def ping(self, connection_id, **kwargs):
        """Sends a secure, end-to-end encrypted ping to a connection.

        Args:
            connection_id (str): this agent's identifier for the connection.

        Examples:
            Send an encrypted ping to a connection.
            >>> connection_id = "fea81719-b76c-4b5f-a3bd-a428dae408c9"
            >>> await agent.connections.ping(connection_id)
            {}
        """
        url = f"/connections/{connection_id}/send-ping"
        r = await self.request("POST", url, **kwargs)
        return r
