import re
from datetime import datetime
from typing import List, Dict, Any

def parse_log_line(line: str) -> Dict[str, Any]:
    patterns = [
        r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>[A-Z]+) \[(?P<service>[^\]]+)\] (?P<message>.+)',
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?) (?P<level>[A-Z]+) (?P<service>[^ ]+): (?P<message>.+)',
        r'(?P<level>[A-Z]+)\[(?P<service>[^\]]+)\]: (?P<message>.+)',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            result = match.groupdict()
            if 'timestamp' in result:
                try:
                    result['timestamp'] = datetime.fromisoformat(result['timestamp'].replace('Z', '+00:00'))
                except:
                    pass
            return result
    return {"message": line}

def parse_logs(log_text: str) -> List[Dict[str, Any]]:
    lines = log_text.strip().split('\n')
    parsed = []
    for line in lines:
        if line.strip():
            parsed.append(parse_log_line(line))
    return parsed

def extract_error_messages(logs: List[Dict[str, Any]]) -> List[str]:
    errors = []
    for log in logs:
        level = log.get('level', '').upper()
        if level in ['ERROR', 'CRITICAL', 'FATAL']:
            errors.append(log.get('message', ''))
    return errors

def extract_services(logs: List[Dict[str, Any]]) -> List[str]:
    services = set()
    for log in logs:
        if 'service' in log:
            services.add(log['service'])
    return sorted(list(services))
