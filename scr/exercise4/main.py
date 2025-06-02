import os
import threading
import time
from collections import defaultdict
import random
import sys

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
        """
        Ensures a single shared instance of the PersistenceManager (Singleton pattern).
        Returns:
            PersistenceManager: the shared instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
        
    def begin_transaction(self):
        """
        Starts a new transaction by assigning a unique transaction ID and logging BOT.
        Returns:
            int: newly assigned transaction ID
        """
        with self.buffer_lock:
            taid = len(self.transactions) + 1001
            self.transactions[taid] = 'active'
            self._write_log(f"{self._next_lsn()}, {taid}, BOT")  # Begin of Transaction
            return taid

    def commit(self, taid):
        """
        Commits the given transaction.
        Args:
            taid (int): Transaction ID to commit
        """
        with self.buffer_lock:
            self._write_log(f"{self._next_lsn()}, {taid}, EOT")
            self.transactions[taid] = 'committed'
            self._flush_buffer()

    def write(self, taid, pageid, data):
        """
        Buffers a write operation and logs it.
        Args:
            taid (int): Transaction ID performing the write
            pageid (int): Identifier of the page being written to
            data (str): The data to write
        """
        with self.buffer_lock:
            lsn = self._next_lsn()
            self._write_log(f"{lsn}, {taid}, {pageid}, {data}")
            self.buffer[pageid] = (lsn, data, taid)
            self.transaction_pages[taid].append(pageid)
            self._check_buffer()

    def _next_lsn(self):
        """
        Generates the next unique LSN (log sequence number).
        Returns:
            int: new LSN
        """
        lsn = self.lsn_counter
        self.lsn_counter += 1
        return lsn

    def _write_log(self, entry):
        """
        Appends a log entry to the log file.
        Args:
            entry (str): The log entry to write
        """
        with open(self.log_file, 'a') as f:
            f.write(entry + '\n')

    def _check_buffer(self):
        """
        Flushes committed pages to disk if buffer exceeds threshold (noforce, nosteal policy).
        """
        if len(self.buffer) > 5:
            for pageid, (lsn, data, taid) in list(self.buffer.items()):
                if self.transactions.get(taid) == 'committed':
                    self._write_page(pageid, lsn, data)
                    del self.buffer[pageid]

    def _flush_buffer(self):
        """
        Flushes all pages of committed transactions from the buffer to disk.
        """
        for pageid, (lsn, data, taid) in list(self.buffer.items()):
            if self.transactions.get(taid) == 'committed':
                self._write_page(pageid, lsn, data)
                del self.buffer[pageid]

    def _write_page(self, pageid, lsn, data):
        """
        Writes a single page's data and LSN to persistent storage.
        Args:
            pageid (int): Page ID
            lsn (int): Log sequence number
            data (str): Data to write
        """
        with open(f"page_{pageid}.txt", 'w') as f:
            f.write(f"{lsn}, {data}")

# Thread class that simulates a client performing transactions
class Client(threading.Thread):
    def __init__(self, client_id, page_range):
        """
        Initializes a client.
        Args:
            client_id (int): Unique client identifier
            page_range (tuple): Range of page IDs the client may write to
        """
        super().__init__()
        self.pm = PersistenceManager.get_instance()
        self.client_id = client_id
        self.page_range = page_range

    def run(self):
        """
        Executes a series of transactions with random writes.
        """
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
        """
        Selects a random page ID within the client's range.
        Returns:
            int: Random page ID
        """
        return random.randint(*self.page_range)

# Tool that implements crash recovery by performing analysis and redo
class RecoveryTool:
    def __init__(self, log_file='log.txt'):
        self.log_file = log_file

    def recover(self, verbose=False):
        committed = set()
        operations = []

        print("🔍 Analyzing log for committed transactions and pending operations...")
        with open(self.log_file, 'r') as f:
            for line in f:
                parts = line.strip().split(', ')
                if len(parts) == 3 and parts[2] == 'EOT':
                    committed.add(int(parts[1]))
                elif len(parts) == 4:
                    lsn, taid, pageid, data = int(parts[0]), int(parts[1]), int(parts[2]), parts[3]
                    operations.append((lsn, taid, pageid, data))

        print(f"✅ Winner Transactions (committed): {sorted(committed)}")
        print("📝 Pending Operations:")
        for lsn, taid, pageid, data in operations:
            if taid in committed:
                print(f"  - LSN {lsn}, TID {taid}, Page {pageid}, Data '{data}'")

        for lsn, taid, pageid, data in operations:
            if taid in committed:
                self._redo(pageid, lsn, data)
                if verbose:
                    print(f"  🔁 Redo applied: Page {pageid} ← {data} (LSN {lsn})")

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
    random.seed(42)

    if len(sys.argv) < 2:
        print("Please run with argument 1 (normal), 2 (crash), or 3 (recovery)")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "1":
        print("Running: Normal execution")
        clients = [Client(i, (10 * i, 10 * i + 9)) for i in range(5)]
        for client in clients:
            client.start()
        for client in clients:
            client.join()
        print("Normal execution completed: All transactions committed.")

    elif mode == "2":
        print("💥 Running: Simulated crash (interrupt early)")
        clients = [Client(i, (10 * i, 10 * i + 9)) for i in range(5)]
        for client in clients:
            client.start()
        time.sleep(0.8)
        print("💣 Simulated crash: Terminating before all commits")
        os._exit(1)

    elif mode == "3":
        print("🔁 Running: Recovery mode")
        recovery = RecoveryTool()
        recovery.recover(verbose=True)
        print("✅ Recovery completed.")

    else:
        print("❗ Invalid argument. Use 1 (normal), 2 (crash), or 3 (recovery).")
