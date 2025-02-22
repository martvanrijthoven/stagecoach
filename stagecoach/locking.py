import os
from pathlib import Path
import time


class LockInUseError(Exception):
    """Custom exception for lock-in-use errors."""
    pass


class LockManager:
    """A class to handle file-based locking for the entire stage output directory."""
    
    def __init__(self, name: str, folder: Path, unlock: bool = False, wait: bool = False):
        self._lock_file = folder / f"{name}.lock"
        self._wait = wait
        if unlock:
            self.remove_lock()

    def create_lock(self) -> bool:
        try:
            fd = os.open(self._lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)  # Ensure the file descriptor is closed
        except FileExistsError:
            raise LockInUseError(f"Lock file already exists: {self._lock_file}")
        return True

    def remove_lock(self):
        self._lock_file.unlink(missing_ok=True)

    def __enter__(self):
        if self._wait:
            while True:
                try:
                    self.create_lock()
                    break
                except LockInUseError:
                    print(f"Waiting for lock to be released: {self._lock_file}")
                    time.sleep(2)
        else:
            self.create_lock()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.remove_lock()
