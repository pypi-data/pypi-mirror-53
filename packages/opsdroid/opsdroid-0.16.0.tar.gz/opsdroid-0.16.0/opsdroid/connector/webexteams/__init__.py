"""A connector for Webex Teams."""
import json
import logging
import uuid

import aiohttp

from webexteamssdk import WebexTeamsAPI

from opsdroid.connector import Connector, register_event
from opsdroid.events import Message


_LOGGER = logging.getLogger(__name__)


class ConnectorWebexTeams(Connector):
    """A connector for Webex Teams."""

    def __init__(self, config, opsdroid=None):
        """Create a connector."""
        _LOGGER.debug("Loaded webex teams connector")
        super().__init__(config, opsdroid=opsdroid)
        self.name = "webexteams"
        self.config = config
        self.opsdroid = opsdroid
        self.default_room = None
        self.bot_name = config.get("bot-name", "opsdroid")
        self.bot_webex_id = None
        self.secret = uuid.uuid4().hex
        self.people = {}

    async def connect(self):
        """Connect to the chat service."""
        try:
            self.api = WebexTeamsAPI(access_token=self.config["access-token"])
        except KeyError:
            _LOGGER.error("Must set accesst-token for webex teams connector!")
            return

        await self.clean_up_webhooks()
        await self.subscribe_to_rooms()
        await self.set_own_id()

    async def webexteams_message_handler(self, request):
        """Handle webhooks from the Webex Teams api."""
        _LOGGER.debug("Handling message from Webex Teams")
        req_data = await request.json()

        _LOGGER.debug(req_data)

        msg = self.api.messages.get(req_data["data"]["id"])

        if req_data["data"]["personId"] != self.bot_webex_id:
            person = await self.get_person(req_data["data"]["personId"])

            try:
                message = Message(
                    msg.text,
                    person.displayName,
                    {"id": msg.roomId, "type": msg.roomType},
                    self,
                )
                await self.opsdroid.parse(message)
            except KeyError as error:
                _LOGGER.error(error)

        return aiohttp.web.Response(text=json.dumps("Received"), status=201)

    async def clean_up_webhooks(self):
        """Remove all existing webhooks."""
        for webhook in self.api.webhooks.list():
            self.api.webhooks.delete(webhook.id)

    async def subscribe_to_rooms(self):
        """Create webhooks for all rooms."""
        _LOGGER.debug("Creating Webex Teams webhook")
        webhook_endpoint = "/connector/webexteams"
        self.opsdroid.web_server.web_app.router.add_post(
            webhook_endpoint, self.webexteams_message_handler
        )

        self.api.webhooks.create(
            name="opsdroid",
            targetUrl="{}{}".format(self.config.get("webhook-url"), webhook_endpoint),
            resource="messages",
            event="created",
            secret=self.secret,
        )

    async def get_person(self, personId):
        """Get a person's info from the api or cache."""
        if personId not in self.people:
            self.people[personId] = self.api.people.get(personId)
        return self.people[personId]

    async def set_own_id(self):
        """Get the bot id and set it in the class."""
        self.bot_webex_id = self.api.people.me().id

    async def listen(self):
        """Listen for and parse new messages."""
        pass  # Listening is handled by the aiohttp web server

    @register_event(Message)
    async def send_message(self, message):
        """Respond with a message."""
        self.api.messages.create(message.target["id"], text=message.text)
