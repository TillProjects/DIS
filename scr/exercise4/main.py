import os
import threading
import time
from collections import defaultdict

class PersistenceManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.buffer = {}
        self.transaction_pages = defaultdict(list)
        self.transactions = {}
        self.lsn_counter = 1
        self.log_file = "log.txt"
        self.buffer_lock = threading.Lock()
        open(self.log_file, 'w').close()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def begin_transaction(self):
        with self.buffer_lock:
            taid = len(self.transactions) + 1001
            self.transactions[taid] = 'active'
            return taid

    def commit(self, taid):
        with self.buffer_lock:
            self._write_log(f"{self._next_lsn()}, {taid}, EOT")
            self.transactions[taid] = 'committed'
            self._flush_buffer()

    def write(self, taid, pageid, data):
        with self.buffer_lock:
            lsn = self._next_lsn()
            self._write_log(f"{lsn}, {taid}, {pageid}, {data}")
            self.buffer[pageid] = (lsn, data, taid)
            self.transaction_pages[taid].append(pageid)
            self._check_buffer()

    def _next_lsn(self):
        lsn = self.lsn_counter
        self.lsn_counter += 1
        return lsn

    def _write_log(self, entry):
        with open(self.log_file, 'a') as f:
            f.write(entry + '\n')

    def _check_buffer(self):
        if len(self.buffer) > 5:
            for pageid, (lsn, data, taid) in list(self.buffer.items()):
                if self.transactions.get(taid) == 'committed':
                    self._write_page(pageid, lsn, data)
                    del self.buffer[pageid]

    def _flush_buffer(self):
        for pageid, (lsn, data, taid) in list(self.buffer.items()):
            if self.transactions.get(taid) == 'committed':
                self._write_page(pageid, lsn, data)
                del self.buffer[pageid]

    def _write_page(self, pageid, lsn, data):
        with open(f"page_{pageid}.txt", 'w') as f:
            f.write(f"{lsn}, {data}")

class Client(threading.Thread):
    def __init__(self, client_id, page_range):
        super().__init__()
        self.pm = PersistenceManager.get_instance()
        self.client_id = client_id
        self.page_range = page_range

    def run(self):
        for _ in range(3):
            taid = self.pm.begin_transaction()
            for _ in range(2):
                pageid = self._get_random_page()
                data = f"Data_{self.client_id}_{pageid}"
                self.pm.write(taid, pageid, data)
                time.sleep(0.1)
            self.pm.commit(taid)
            time.sleep(0.2)

    def _get_random_page(self):
        import random
        return random.randint(*self.page_range)

class RecoveryTool:
    def __init__(self, log_file='log.txt'):
        self.log_file = log_file

    def recover(self):
        committed = set()
        operations = []

        with open(self.log_file, 'r') as f:
            for line in f:
                parts = line.strip().split(', ')
                if len(parts) == 3 and parts[2] == 'EOT':
                    committed.add(int(parts[1]))
                elif len(parts) == 4:
                    lsn, taid, pageid, data = int(parts[0]), int(parts[1]), int(parts[2]), parts[3]
                    operations.append((lsn, taid, pageid, data))

        for lsn, taid, pageid, data in operations:
            if taid in committed:
                self._redo(pageid, lsn, data)

    def _redo(self, pageid, lsn, data):
        filename = f"page_{pageid}.txt"
        current_lsn = -1
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read().strip()
                if content:
                    parts = content.split(', ')
                    current_lsn = int(parts[0])
        if lsn > current_lsn:
            with open(filename, 'w') as f:
                f.write(f"{lsn}, {data}")

if __name__ == "__main__":
    clients = [Client(i, (10 * i, 10 * i + 9)) for i in range(3)]
    for client in clients:
        client.start()
    for client in clients:
        client.join()

    print("--- Simulating Recovery ---")
    recovery = RecoveryTool()
    recovery.recover()
    print("Recovery finished.")
