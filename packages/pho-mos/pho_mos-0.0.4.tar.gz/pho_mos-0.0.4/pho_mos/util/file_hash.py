import hashlib
import os.path

BLOCK_SIZE = 512

# Мб пригодится в будущем хешерование больших файлов из ОС:
def from_file_sha(file_path, blocksize=BLOCK_SIZE) -> str:
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        buf = f.read(blocksize)
        while buf:
            buf = f.read(blocksize)
            if not buf:
                break
            sha1.update(buf)
    return sha1.hexdigest()
