from typing import AsyncIterator, Awaitable, Callable, Dict, Type

import inspect
import logging
import subprocess
import trio
import zmq
from contextlib import asynccontextmanager
from functools import partial
from hedgehog.utils.zmq import trio as zmq_trio
from hedgehog.protocol import ServerSide, Header, RawMessage, Message, RawPayload
from hedgehog.protocol.zmq.trio import DealerRouterSocket
from hedgehog.protocol.errors import HedgehogCommandError, UnsupportedCommandError, FailedCommandError
from .hardware import EmergencyStopUpdate, ShutdownUpdate


# TODO importing this from .handlers does not work...
HandlerCallback = Callable[['HedgehogServer', Header, Message], Awaitable[Message]]
Job = Callable[[], Awaitable[None]]

logger = logging.getLogger(__name__)


class HedgehogServer:
    def __init__(self, ctx: zmq_trio.Context, endpoint: str, handlers: Dict[Type[Message], HandlerCallback], updates: trio.abc.ReceiveChannel=None) -> None:
        self.ctx = ctx
        self._nursery = None
        self._lock = trio.StrictFIFOLock()
        self.endpoint = endpoint
        self.handlers = handlers
        self.updates = updates
        self.socket: DealerRouterSocket = None

    def stop(self):
        self._nursery.cancel_scope.cancel()

    async def _requests_task(self, *, task_status=trio.TASK_STATUS_IGNORED) -> None:
        async def handle_msg(ident: Header, msg_raw: RawMessage) -> RawMessage:
            try:
                msg = ServerSide.parse(msg_raw)
                logger.debug("Receive command: %s", msg)
                try:
                    handler = self.handlers[msg.__class__]
                except KeyError:
                    raise UnsupportedCommandError(msg.__class__.msg_name())
                try:
                    result = await handler(self, ident, msg)
                except HedgehogCommandError as err:
                    logger.info("For command:     %s", msg)
                    logger.info("-> Error:        %s", err)
                    raise
                except Exception as err:
                    logger.exception("Uncaught exception in command handler")
                    raise FailedCommandError("Uncaught exception: {}".format(repr(err))) from err
            except HedgehogCommandError as err:
                result = err.to_message()
            logger.debug("Send reply:      %s", result)
            return ServerSide.serialize(result)

        task_status.started()
        while True:
            ident, msgs_raw = await self.socket.recv_msgs_raw()
            async with self.job(f"handle {len(msgs_raw)} requests"):
                await self.socket.send_msgs_raw(ident, [await handle_msg(ident, msg) for msg in msgs_raw])

    async def _updates_task(self, *, task_status=trio.TASK_STATUS_IGNORED) -> None:
        task_status.started()
        if self.updates is None:
            return

        async for update in self.updates:
            logger.debug("Got HWC update:  %s", update)
            if isinstance(update, ShutdownUpdate):
                logger.info("Initiating shutdown")
                subprocess.run(['sudo', 'shutdown', '-h', '0'])
            else:
                logger.info("Ignored update:  %s", update)

    async def add_task(self, async_fn, *args, name=None):
        async def async_fn_wrapper(*, task_status=trio.TASK_STATUS_IGNORED) -> None:
            logger.debug("Added new task: %s", name if name else async_fn)
            try:
                await async_fn(*args, task_status=task_status)
            except Exception:
                logger.exception("Task raised an exception: %s", name if name else async_fn)
            else:
                logger.debug("Task finished: %s", name if name else async_fn)

        return await self._nursery.start(async_fn_wrapper)

    @asynccontextmanager
    async def job(self, job_name=None) -> None:
        LONG_RUNNING_THRESHOLD = 0.2
        CANCEL_THRESHOLD = 10

        if job_name is None:
            # one frame for context manager, two frames for caller
            _, _, _, job_name, _, _ = inspect.stack()[2]

        async with self._lock:
            nursery = None
            manually_cancelled = False
            begin = trio.current_time()
            try:
                async with trio.open_nursery() as nursery:
                    nursery.cancel_scope.deadline = begin + CANCEL_THRESHOLD

                    @nursery.start_soon
                    async def warn_long_running():
                        await trio.sleep(LONG_RUNNING_THRESHOLD)
                        logger.warning("Long running job on server loop: %s", job_name)

                    yield

                    # cancel the warning task
                    manually_cancelled = True
                    nursery.cancel_scope.cancel()
            finally:
                assert nursery is not None

                end = trio.current_time()
                if nursery.cancel_scope.cancelled_caught and not manually_cancelled:
                    logger.error("Long running job cancelled after %.1f ms: %s", (end - begin) * 1000, job_name)
                    raise trio.TooSlowError
                elif end - begin > LONG_RUNNING_THRESHOLD:
                    logger.warning("Long running job finished after %.1f ms: %s", (end - begin) * 1000, job_name)

    async def send_async(self, ident: Header, *msgs: Message) -> None:
        for msg in msgs:
            logger.debug("Send update:     %s", msg)
        await self.socket.send_msgs(ident, msgs)

    async def run(self, *, task_status=trio.TASK_STATUS_IGNORED):
        with DealerRouterSocket(self.ctx, zmq.ROUTER, side=ServerSide) as self.socket:
            async with trio.open_nursery() as self._nursery:
                self.socket.bind(self.endpoint)
                task_status.started()

                await self._nursery.start(self._requests_task)
                await self._nursery.start(self._updates_task)
        logger.info("Server stopped")
