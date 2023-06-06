import re
import subprocess
import sys
import os

from literals import (
    CONFIG_DIR
)

class RedisOpsManager:

    def __init__(self):
        self.redis_cfg = CONFIG_DIR
    
    def version(self):
        try:
            r = subprocess.run(["redis-cli", "-v"],capture_output=True).stdout.decode()
            ver = re.search(r'redis-cli\s*([\d.]+)', r).group(1)
            return ver
        except Exception as e:
            print("Error parsing out version from redis-cli -v", e)
            sys.exit(1)
    
    def start(self):
        os.system("sudo systemctl start redis-server")

    def reload_or_restart(self):
        os.system("sudo systemctl reload-or-restart redis-server")
