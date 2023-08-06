from datacustodian.base import AgentSectionBase


def compile_menu(name):
    """Compiles the menu from application specifications.

    Args:
        name (str): name of the menu to compile.
    """
    return {}


class Section(AgentSectionBase):
    async def close(self, connection_id, **kwargs):
        """Queries the `/action-menu/{id}/close` endpoint to close the active
        menu.

        Args:
            connection_id (str): identifier of the connection to close our menu
                for.

        Examples:
            Close our active menu for a connection.

            >>> await agent.menu.close("d1c86320-ff47-4d74-a073-dd0e5bf44176")
            {}
        """
        r = await self.request("POST", f"/action-menu/{connection_id}/close", **kwargs)
        return r


    async def fetch(self, connection_id, **kwargs):
        """Queries the `/action-menu/{id}/fetch` endpoint to fetch the active
        menu of the connection.

        Args:
            connection_id (str): identifier of the connection to fetch a menu
                for.

        Examples:
            Fetch the active menu of a connection.

            >>> await agent.menu.fetch("d1c86320-ff47-4d74-a073-dd0e5bf44176")
            {}
        """
        r = await self.request("POST", f"/action-menu/{connection_id}/fetch", **kwargs)
        return r["result"]


    async def request(self, connection_id, **kwargs):
        """Queries the `/action-menu/{id}/request` endpoint to request the active
        menu of the connection.

        Args:
            connection_id (str): identifier of the connection to request a menu
                for.

        Examples:
            Request the active menu of a connection.

            >>> await agent.menu.request("d1c86320-ff47-4d74-a073-dd0e5bf44176")
            {}
        """
        r = await self.request("POST", f"/action-menu/{connection_id}/request", **kwargs)
        return r


    async def perform(self, connection_id, name, params, **kwargs):
        """Queries the `/action-menu/{id}/fetch` endpoint to fetch the active
        menu of the connection.

        Args:
            connection_id (str): identifier of the connection to perform a menu
                action at.
            name (str): name of the menu item to perform.
            params (dict): key-values pairs to use as parameters for the action.

        Examples:
            Fetch the active menu of a connection.

            >>> connection_id = "d1c86320-ff47-4d74-a073-dd0e5bf44176"
            >>> await agent.menu.perform(connection_id, "greet", {"msg": "hello"})
            {}
        """
        body = {
            "name": name,
            "params": params
        }
        r = await self.request("POST", f"/action-menu/{connection_id}/perform", data=body, **kwargs)
        return r


    async def send(self, connection_id, name, **kwargs):
        """Queries the `/action-menu/{id}/send-menu` endpoint to send the active
        menu (configured by application specs) to the connection.

        Args:
            connection_id (str): identifier of the connection to perform a menu
                action at.
            name (str): name of the menu to send to the connection.

        Examples:
            Sends the active menu for consent to a connection.

            >>> connection_id = "d1c86320-ff47-4d74-a073-dd0e5bf44176"
            >>> await agent.menu.send(connection_id, "consent")
            {}
        """
        body = compile_menu(name)
        r = await self.request("POST", f"/action-menu/{connection_id}/send-menu", data=body, **kwargs)
        return r
