import tempfile
from pathlib import Path
from utils import file_hash, backup_file

def test_file_hash():
 with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
 f.write(b"test data")
 f.flush()
 h = file_hash(f.name)
 assert len(h) == 64
 assert h == file_hash(f.name) # deterministic

def test_backup(tmp_path):
 target = tmp_path / "test.dll"
 target.write_bytes(b"original content")
 backup_file(target)
 backup = tmp_path / ".backup" / "test.dll"
 assert backup.exists()
 assert backup.read_bytes() == b"original content"
