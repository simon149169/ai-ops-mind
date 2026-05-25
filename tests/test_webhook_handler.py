import pytest
from app.utils.dedup import generate_fingerprint, is_duplicate
import hashlib

def test_generate_fingerprint():
    data = {'alertname': 'HighErrorRate', 'service': 'payment-service', 'severity': 'critical'}
    fingerprint = generate_fingerprint(data)
    assert len(fingerprint) == 64
    assert isinstance(fingerprint, str)

def test_fingerprint_consistency():
    data1 = {'alertname': 'Test', 'service': 'svc1', 'severity': 'P0'}
    data2 = {'service': 'svc1', 'alertname': 'Test', 'severity': 'P0'}
    fp1 = generate_fingerprint(data1)
    fp2 = generate_fingerprint(data2)
    assert fp1 == fp2
