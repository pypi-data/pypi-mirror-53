from datacustodian.base import AgentSectionBase

class Section(AgentSectionBase):
    async def ls(self, **kwargs):
        """Queries the `/wallet/did` endpoint to list DIDs in the wallet of the
        agent.

        Examples:
            List all the DIDs in the wallet.

            >>> await agent.wallet.ls()
            {
              "results": [
                {
                  "did": "2C3zPtmvHgk91KLxqg63iz",
                  "verkey": "edrchXRJiMioFY47ic1ezS8WzvhwKk48392gR4KAmgv",
                  "public": "true"
                }
              ]
            }
        """
        r = await self.request("GET", "/wallet/did", **kwargs)
        return r["results"]

    async def create(self, **kwargs):
        """Queries the `/wallet/did/create` endpoint to create a new DID.

        Examples:
            Create a new DID in the local wallet. This does *not* post the did
            to the ledger.

            >>> await agent.wallet.create()
            {
              "result": {
                "did": "9TBnu8U8EUfsnnsjwFLhik",
                "verkey": "5cAkN3qKsREofYcPZPKrcNJ7g1YM1a5LyJN9B9kcGz5J",
                "public": "false"
              }
            }
        """
        r = await self.request("POST", "/wallet/did/create", **kwargs)
        return r["result"]

    async def set_public(self, did, **kwargs):
        """Queries the `/wallet/did/public` endpoint to set the public DID of
        the wallet. That is the DID the wallet will use to interact with the
        ledger by signing requests.

        Args:
            did (str): the DID that should be set as public on the wallet.

        Examples:
            Set the public DID on the wallet.

            >>> await agent.wallet.set_public("9TBnu8U8EUfsnnsjwFLhik")
            {
              "result": {
                "did": "9TBnu8U8EUfsnnsjwFLhik",
                "verkey": "5cAkN3qKsREofYcPZPKrcNJ7g1YM1a5LyJN9B9kcGz5J",
                "public": "true"
              }
            }
        """
        params = {"did": did}
        r = await self.request("POST", "/wallet/did/public", params=params, **kwargs)
        return r["result"]

    async def get_public(self, **kwargs):
        """Queries the `/wallet/did/public` endpoint to get the public DID of
        the wallet. That is the DID the wallet will use to interact with the
        ledger by signing requests.

        Examples:
            Get the public DID on the wallet.

            >>> await agent.wallet.get_public()
            {
              "result": {
                "did": "2C3zPtmvHgk91KLxqg63iz",
                "verkey": "edrchXRJiMioFY47ic1ezS8WzvhwKk48392gR4KAmgv",
                "public": "true"
              }
            }
        """
        r = await self.request("GET", "/wallet/did/public", **kwargs)
        return r["result"]
