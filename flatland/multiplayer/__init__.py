"""
This section handles the game server and the game client.

The client connects via Sockets to the Server and exchange continuously with it.

The clients only send the commands of the player, the server handles all the logic.

THe client is taking care of animations and rendering.
"""

from . import client, server
