from typing import Callable

from keios_zmq.log_provider import LogProvider


class MessageHandler:
    log = LogProvider.get_logger(__name__)

    def __init__(self,
                 message_handler: Callable[[bytearray], bytearray],
                 error_handler: Callable[[Exception], bytearray] = None):
        self._message_handler = message_handler
        self._error_handler = error_handler

    def handle(self, msg: bytearray):
        try:
            return self._message_handler(msg)
        except Exception as e:
            self.log.error("unhandled exception occurred")
            if self._error_handler is not None:
                return self._error_handler(e)
            else:
                self.log.error("no error handler has been set. ignoring...", e)
                raise e
