from datacustodian.base import AgentSectionBase

class Section(AgentSectionBase):
    async def register_nym(self, did, verkey, alias=None, role=None, **kwargs):
        """Queries the `/ledger/register-nym` endpoint to register a new public
        identity on the ledger.

        Examples:
            Register a new identity on the ledger.

            >>> await agent.ledger.register_nym("2C3zPtmvHgk91KLxqg63iz", "edrchXRJiMioFY47ic1ezS8WzvhwKk48392gR4KAmgv")
        """
        params = {
            "did": did,
            "verkey": verkey,
            "alias": alias,
            "role": role
        }
        await self.request("POST", "/ledger/register-nym", params=params, **kwargs)

    async def get_verkey(self, did, **kwargs):
        """Queries the `/ledger/did-verkey` endpoint to fetch the verkey for a
        public DID.

        Examples:
            Get the verkey for a public DID from the ledger.

            >>> await agent.ledger.get_verkey("9TBnu8U8EUfsnnsjwFLhik")
            {
                "verkey": "5cAkN3qKsREofYcPZPKrcNJ7g1YM1a5LyJN9B9kcGz5J",
            }
        """
        params = {
            "did": did
        }
        r = await self.request("GET", "/ledger/did-verkey", params=params, **kwargs)
        return r["verkey"]

    async def get_endpoint(self, did, **kwargs):
        """Queries the `/ledger/did-endpoint` endpoint to fetch the endpoint for a
        public DID.

        Examples:
            Get the endpoint for a public DID from the ledger.

            >>> await agent.ledger.get_verkey("9TBnu8U8EUfsnnsjwFLhik")
            {
                "endpoint": "http://some.domain.com:8020",
            }
        """
        params = {
            "did": did
        }
        r = await self.request("GET", "/ledger/did-endpoint", params=params, **kwargs)
        return r["endpoint"]
