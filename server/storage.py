from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
import os

INDEX_DIR = "indexdir"

# Define schema
schema = Schema(
    timestamp=TEXT(stored=True),
    host=TEXT(stored=True),
    process=TEXT(stored=True),
    message=TEXT(stored=True)
)

# Create index if it doesn’t exist
if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)
    ix = create_in(INDEX_DIR, schema)
else:
    ix = open_dir(INDEX_DIR)

def index_log(log_line):
    """
    Example log line:
    Sep 21 13:09:25 P2926 systemd-resolved[6476]: Clock change detected
    """
    parts = log_line.strip().split()
    if len(parts) < 5:
        return  # skip malformed lines

    timestamp = " ".join(parts[0:3])
    host = parts[3]
    process = parts[4].strip(":")
    message = " ".join(parts[5:])

    writer = ix.writer()
    writer.add_document(timestamp=timestamp, host=host, process=process, message=message)
    writer.commit()
