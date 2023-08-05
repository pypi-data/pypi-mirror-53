import logging
import six
import inspect
import os
import threading

from rook.logger import logger

from rook.processor.namespaces.container_namespace import ContainerNamespace
from rook.processor.namespaces.frame_namespace import FrameNamespace
from rook.augs.processor_extensions.namespaces.log_record_namespace import LogRecordNamespace


class LoggingLocationService(object):

    NAME = "logging"

    def __init__(self):
        self._lock = threading.RLock()

        self._hooked = False
        self._originalHandle = None

        self._augs = dict()

    def add_logging_aug(self, aug):
        with self._lock:
            self._installHooks()

            self._augs[aug.aug_id] = aug
            aug.set_active()

    def remove_aug(self, aug_id):
        with self._lock:
            try:
                del self._augs[aug_id]
            except KeyError:
                pass

            if not self._augs:
                self._removeHooks()

    def clear_augs(self):
        with self._lock:
            for aug_id in list(self._augs.keys()):
                self.remove_aug(aug_id)

            self._augs = dict()
            self._removeHooks()

    def close(self):
        self.clear_augs()
        self._removeHooks()

    def pre_fork(self):
        if self._lock:
            self._lock.acquire()

    def post_fork(self):
        if self._lock:
            self._lock.release()

        self._removeHooks()

    def _installHooks(self):
        with self._lock:
            if self._hooked:
                return

            def handle(other_self, record):
                try:
                    self.run_augs(record)
                except:
                    pass

                originalHandle = self._originalHandle
                if originalHandle is not None:
                    originalHandle(other_self, record)

            logging.Logger.handle, self._originalHandle = handle, logging.Logger.handle
            self._hooked = True

    def _removeHooks(self):
        with self._lock:
            if not self._hooked:
                return

            logging.Logger.handle, self._originalHandle = self._originalHandle, None
            self._hooked = False

    def run_augs(self, record):
        extracted = ContainerNamespace({'log_record': LogRecordNamespace(record)})

        with self._lock:
            for aug in six.itervalues(self._augs):
                aug.execute(None, extracted)
