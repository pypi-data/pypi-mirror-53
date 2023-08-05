import re
from os import environ
from asyncio import ensure_future

from aiohubot import Adapter, TextMessage
from aioflowdock import Session

__version__ = '0.1.1'


class Flowdock(Adapter):
    def __init__(self, robot):
        super().__init__(robot)
        self.bot = self.stream = None
        self.flows = list()
        self.ignores = list()
        if environ.get('HUBOT_FLOWDOCK_ALLOW_ANONYMOUS_COMMANDS') != '1':
            self.ignores.append('0')
        ignored_users = environ.get('HUBOT_FLOWDOCK_IGNORE_USERS', "").split(",")
        self.ignores.extend(filter(None, ignored_users))
        if self.ignores:
            msg = f"Ignoring all messages from user ids {','.join(self.ignores)}"
            self.robot.logger.info(msg)

    async def send(self, envelope, *strings):
        self.robot.logger.debug(f"{envelope}, {strings}")
        for string in strings:
            if len(string) > 8096:
                string = "** End of Message Truncated **\n" + string
                string = string[:8096]
            metadata = (envelope.get("metadata")
                        or ("message" in envelope and envelope['message'].metadata)
                        or dict())
            flow = metadata.get("room", envelope['room'])
            thread_id = metadata.get("thread_id", "")
            msg_id = metadata.get("message_id", "")
            user = envelope['user']
            force_new_msg = bool(envelope.get("newMessage"))
            if user:
                if flow:
                    if thread_id and not force_new_msg:
                        await self.bot.thread_message(flow, thread_id, string, [])
                    elif msg_id and not force_new_msg:
                        await self.bot.comment(flow, msg_id, string, [])
                    else:
                        await self.bot.message(flow, string, [])
                elif user.id:
                    string = re.sub(fr"^@{user.name}: ", "", string)
                    await self.bot.private_message(user.id, string, [])
            elif flow:
                flow = self.find_flow(flow)
                await self.bot.message(flow, string, [])

    def reply(self, envelope, *strings):
        user = self.user_from_params(envelope)
        return self.send(envelope, *(f"@{user.name}: {s}" for s in strings))

    def user_from_params(self, params):
        return params.get("user", params)

    def find_flow(self, identifier):
        for flow in self.flows:
            if (identifier == flow.get("id") or
                identifier == self.flow_path(flow) or
                identifier.lower() == flow.get("name", "").lower()):
                return flow.get("id")

        return identifier

    def flow_path(self, flow):
        return flow["organization"]["parameterized_name"] + flow["parameterized_name"]

    def flow_from_params(self, params):
        for flow in self.flows():
            if params.get("room") == flow['id']:
                return flow

    def joined_flows(self):
        return [f for f in self.flows if f.get("joined") and f.get("open")]

    def user_from_id(self, id, **options):
        return self.robot.brain.user_for_id(id, **options)

    def change_user_nick(self, id, new_nick):
        if id in self.robot.brain.data.users():
            self.robot.brain.data['users'][id].name = new_nick

    def need_reconnect(self, data):
        try:
            content, evt, user = data['content'], data['event'], data['user']
        except Exception:
            return False

        events = ("backend.user.join", "flow-add", "flow-remove")
        return (self.my_id(content) and evt == "backend.user.block" or 
                self.my_id(user) and evt in events)

    def my_id(self, id):
        return str(id) == str(self.bot.userid)

    async def reconnect(self, reason):
        self.robot.logger.info(f"Reconnectiong: {reason}")
        await self.stream.end()
        self.stream.remove_all_listeners()
        await self._fetch_flows_and_connect()

    async def connect(self):
        ids = [f['id'] for f in self.joined_flows()]
        self.robot.logger.info("Flowdock: connecting")
        stream = self.bot.stream(ids, dict(active='idle', user=1))

        @stream.on("connected")
        def _connected():
            self.robot.logger.info("Flowdock: connected and streaming")
            names = [f['name'] for f in self.joined_flows()]
            self.robot.logger.info(f"Flowdock: listening to flows: {names}")

        @stream.on("clientError")
        async def client_error(error):
            self.robot.logger.error(f"Flowdock: client error: {error}", exc_info=True)
            await self.reconnect("Client Error")

        @stream.on("disconnected")
        def disconnected():
            self.robot.logger.info("Flowdock: disconnected")

        @stream.on("reconnecting")
        def reconnecting():
            self.robot.logger.info("Flowdock: reconnecting")

        @stream.on("message")
        async def message(data):
            try:
                ctx, evt, user = data['content'], data['event'], data.get("user")
            except KeyError:
                return None
            if self.need_reconnect(data):
                await self.reconnect("Reloading flow list")
            if self.my_id(user) and evt in ("backend.user.join", "flow-add"):
                info = dict(id=ctx.get("id"), name=ctx.get("name"))
                self.robot.emit("flow-add", info)
            if evt == 'user-edit' or evt == 'backend.user.join':
                ctx_user = ctx['user']
                self.change_user_nick(ctx_user['id'], ctx_user['nick'])

            if any([evt not in ("message", "comment"), not data.get("id"),
                   self.my_id(user), str(user) in self.ignores]):
                return None

            self.robot.logger.debug(f"Received message: {data}")
            author = self.user_from_id(user)
            thread_id = data.get("thread_id")
            if not thread_id:
                msg_id = None
            elif evt == 'message':
                msg_id = data['id']
            else:
                for tag in data.get("tags", list()):
                    if tag.startswith("influx:"):
                        msg_id = tag.split(":", 2)[1]
                        break
                else:
                    msg_id = None

            msg = ctx['text'] if evt == 'comment' else ctx
            # Reformat leading @mention name to be like "name: message" which is
            # what hubot expects. Add bot name into private message if not given.
            bot_prefix = f"{self.robot.name}:"
            hubot_msg = re.sub(fr"^@{self.bot.username}(,\\b)", bot_prefix, msg,
                               flags=re.I)
            if (not re.match(fr"^{self.robot.name}", hubot_msg, re.I)
                and data.get("flow") is None):
                hubot_msg = bot_prefix + hubot_msg

            author.room = author.flow = data.get("flow")
            metadata = dict(room=data.get("flow"))
            if thread_id:
                metadata['thread_id'] = thread_id
            if msg_id:
                metadata['message_id'] = msg_id

            msg_obj = TextMessage(author, hubot_msg, data.get("id"))
            # Support metadata even if hubot does not currently do that
            msg_obj.metadata = metadata

            await self.receive(msg_obj)

        await stream.connect()
        self.stream = stream

    def run(self):
        self.api_token = environ.get("HUBOT_FLOWDOCK_API_TOKEN", "")
        self.login_email = environ.get("HUBOT_FLOWDOCK_LOGIN_EMAIL", "")
        self.login_password = environ.get("HUBOT_FLOWDOCK_LOGIN_PASSWORD", "")
        if self.api_token:
            self.bot = Session(self.api_token)
        elif self.login_email and self.login_password:
            self.bot = Session(self.login_email, self.login_email)
        else:
            err = ("No credentials given: Supply either environment variable"
                   " HUBOT_FLOWDOCK_API_TOKEN or both HUBOT_FLOWDOCK_LOGIN_EMAIL"
                   " and HUBOT_FLOWDOCK_LOGIN_PASSWORD")
            raise AttributeError(err)

        @self.bot.on("error")
        def _handle_error(e):
            self.robot.logger.error(f"Unexpected error in Flowdock client: {e}")
            self.emit(e)

        fut = ensure_future(self._fetch_flows_and_connect(), loop=self._loop)
        fut.add_done_callback(lambda fut: self.emit("connected"))

        return fut

    async def _fetch_flows_and_connect(self):
        try:
            self.flows, resp = await self.bot.flows()
        except TypeError:
            return None
        self.bot.userid = resp.headers['flowdock-user']
        self.robot.logger.info(f"Found {len(self.flows)} flows, and I have joined"
                               f" {len(self.joined_flows())} of them.")
        for flow in self.flows:
            for user in flow.get("users", list()):
                if user.get("in_flow"):
                    saved_user = self.user_from_id(user['id'], name=user['nick'])
                    if saved_user.name != user['nick']:
                        self.change_user_nick(saved_user.id, user['nick'])
                    if str(user['id']) == str(self.bot.userid):
                        self.bot.username = user['nick']

        self.robot.logger.info("Connecting to Flowdock as user %s (id %s)" % (
                               self.bot.username, self.bot.userid))
        if not len(self.flows) or any(f for f in self.flows if not f["open"]):
            msg = ("Bot is not part of any flows and probably won't do much."
                   "  Join some flows manually or add the bot to some flows and"
                   "reconnect.")
            self.robot.logger.warning(msg)
        if self.bot.username.lower() != self.robot.name.lower():
            msg = ("You have configured this bot to user the wrong name %s."
                   "  Flowdock API says my name is %s.  You will run into"
                   " problem if you don't fix this!")
            self.robot.logger.warning(msg % (self.robot.name, self.bot.username))

        await self.connect()

# to fit the API
use = Flowdock
