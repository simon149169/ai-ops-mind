import pytest
from app.services.log_analyzer import analyze_logs
from app.utils.log_parser import parse_logs, extract_error_messages, extract_services

def test_parse_log_line():
    log_line = "2026-05-25 03:14:22 ERROR [payment-service] Connection refused to mysql-primary:3306"
    result = parse_logs(log_line)
    assert len(result) == 1
    assert result[0].get('level') == 'ERROR'
    assert result[0].get('service') == 'payment-service'

def test_extract_error_messages():
    logs = [
        {'level': 'ERROR', 'message': 'Connection refused'},
        {'level': 'INFO', 'message': 'Service started'},
        {'level': 'ERROR', 'message': 'Timeout'}
    ]
    errors = extract_error_messages(logs)
    assert len(errors) == 2
    assert 'Connection refused' in errors

def test_extract_services():
    logs = [
        {'service': 'payment-service', 'message': 'Error'},
        {'service': 'gateway', 'message': 'Timeout'},
        {'service': 'payment-service', 'message': 'Retry'}
    ]
    services = extract_services(logs)
    assert len(services) == 2
    assert 'payment-service' in services
    assert 'gateway' in services
