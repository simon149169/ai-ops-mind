import hashlib
import redis
from app.config import settings
from typing import Optional

redis_client = redis.from_url(settings.REDIS_URL)

def generate_fingerprint(data: dict) -> str:
    keys = sorted(data.keys())
    fingerprint_str = "|".join(f"{k}={data[k]}" for k in keys if k != "fired_at")
    return hashlib.sha256(fingerprint_str.encode()).hexdigest()

def is_duplicate(fingerprint: str, ttl: int = 300) -> bool:
    key = f"dedup:{fingerprint}"
    if redis_client.get(key):
        return True
    redis_client.setex(key, ttl, "1")
    return False

def get_alert_count(service: Optional[str] = None, minutes: int = 5) -> int:
    if service:
        pattern = f"alert:*:{service}:*"
    else:
        pattern = "alert:*"
    keys = redis_client.keys(pattern)
    return len(keys)

def store_alert(alert_id: str, service: str, severity: str, ttl: int = 300):
    key = f"alert:{severity}:{service}:{alert_id}"
    redis_client.setex(key, ttl, severity)
