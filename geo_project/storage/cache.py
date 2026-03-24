import redis, os, functools, json
from typing import Dict, Callable, Any
from redis import cache
from geo_project.geo_config.logger import get_logger

logger = get_logger(__name__)

_cache_r = None

cache_params: Dict[str, str | int] = {
    "host": os.getenv("REDIS_HOST", "geo-redis-cache"),
    "port": 6379,
    "db": 0,
    "socket_timeout": 5,
    "socket_connect_timeout": 5,
    "decode_responses": True
}

def get_cache():
    global _cache_r
    if _cache_r is None:
        _cache_r = redis.Redis(**cache_params)
        try:
            _cache_r.ping()
        except redis.ConnectionError as e:
            logger.error("Redis connection error:", e)
            _cache_r = redis.Redis(**cache_params)

    return _cache_r

def cache(key_prefix: str, ttl: int = 60):
    def decorator(func: Callable):
        if os.getenv("DISABLE_CACHE") == "1":
            return func
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            r = get_cache()
            safe_args = args[1:]
            key_data: Dict[str, Any] = {
                "args": safe_args,
                "kwargs": kwargs
            }

            key: str = f"{key_prefix}:{json.dumps(key_data, sort_keys=True)}"
            cached = r.get(key)
            if cached:
                return json.loads(cached)
            
            result = func(*args, **kwargs)

            try:
                r.setex(key, ttl, json.dumps(result))
            except TypeError as e:
                logger.error("Type error in cache data:", e)
                pass

            return result
        return wrapper
    return decorator