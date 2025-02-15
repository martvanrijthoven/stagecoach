import os
from pathlib import Path


class LockInUseError(Exception):
    """Custom exception for lock-in-use errors."""
    pass


class LockManager:
    """A class to handle file-based locking for the entire stage output directory."""
    
    def __init__(self, name: str, folder: Path, unlock: bool = False):
        self._lock_file = folder / f"{name}.lock"
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
        self.create_lock()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.remove_lock()
