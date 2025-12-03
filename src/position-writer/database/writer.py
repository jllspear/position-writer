import time
from threading import Thread

from . import db_manager
from .enum import CommitBehavior
from ..mqtt.message_buffer import ParsedObjectBuffer


class BatchWriter:
    def __init__(self, buffer: ParsedObjectBuffer, commit_behavior: CommitBehavior):
        self.buffer = buffer
        self.commit_behavior = commit_behavior
        self._running = False
        self.thread = None

    def _write_loop(self):
        while self._running:
            time.sleep(self.commit_behavior.value)  # or .secs
            self.commit_buffered_elements()

    def commit_buffered_elements(self):
        elements = self.buffer.get_and_clear()
        if not elements:
            print("No elements to commit")
            return

        session = db_manager.get_sqlalchemy_session()

        try:
            with session.begin():
                session.add_all(elements)

            print(f"Successfully committed {len(elements)} elements")

        except Exception as e:
            print(f"Database error: {e}")
        finally:
            session.close()

    def start(self):
        self._running = True
        self.thread = Thread(target=self._write_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self._running = False
        if self.thread:
            self.thread.join()
        self.commit_buffered_elements()
