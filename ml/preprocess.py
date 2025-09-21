import re
import pandas as pd

LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<process>[^\[]+)(?:\[(?P<pid>\d+)\])?:\s+(?P<message>.*)$'
)

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def parse_log_file(logfile, output_csv="parsed_logs.csv"):
    parsed_data = []
    with open(logfile, "r") as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                parsed_data.append(parsed)
    
    df = pd.DataFrame(parsed_data)
    df.to_csv(output_csv, index=False)
    print(f"✅ Parsed logs saved to {output_csv}")

if __name__ == "__main__":
    parse_log_file("../server/indexdir/logs.txt")  # or wherever your raw logs are stored
