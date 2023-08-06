from datacustodian.base import AgentSectionBase

class Section(AgentSectionBase):
    async def modules(self, **kwargs):
        """Queries the `/modules` endpoint to list modules enabled for the agent.

        Examples:
            List all *additional* enabled modules for the agent.

            >>> await agent.server.modules()
            {
              "result": []
            }
        """
        r = await self.request("GET", "/modules", **kwargs)
        return r["result"]

    async def status(self, **kwargs):
        """Queries the `/status` endpoint to return server status information.

        Examples:
            Get server states for an agent.

            >>> await agent.server.status()
            {}
        """
        r = await self.request("GET", "/status", **kwargs)
        return r

    async def reset(self, **kwargs):
        """Calls the `/status/reset` endpoint to reset the server statistics
        returned by :meth:`status`.

        Examples:
            Reset server status statistics.

            >>> await agent.server.reset()
            {}
        """
        r = await self.request("GET", "/status/reset", **kwargs)
        return r

    async def protocols(self, query='*', **kwargs):
        """Calls the `/protocols` endpoint to list all the supported messaging
        protocols supported by the agent.

        Args:
            query (str): part of a protocol to filter on. Note that this must
                include the whole initial `did` string, but may end in `*` to
                provide some measure of querying.

        Examples:
            List agent's supported protocols to do with credentials.

            >>> await agent.server.protocols('did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/cred*')
            {
              "results": {
                "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-presentation/0.1": {},
                "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/0.1": {}
              }
            }
        """
        params = {"query": query}
        r = await self.request("GET", "/protocols", params=params, **kwargs)
        return r["results"]
