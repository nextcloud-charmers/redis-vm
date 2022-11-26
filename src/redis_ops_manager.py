import re
import subprocess
import sys

class RedisOpsManager:

    def __init__(self):
        self.redis_cfg = "/etc/redis/redis.conf"
    
    def version(self):
        try:
            r = subprocess.run(["redis-cli", "-v"],capture_output=True).stdout.decode()
            ver = re.search(r'redis-cli\s*([\d.]+)', r).group(1)
            return ver
        except Exception as e:
            print("Error parsing out version from redis-cli -v", e)
            sys.exit(1)