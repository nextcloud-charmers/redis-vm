#!/usr/bin/env python3
# Copyright 2022 Erik Lonroth
# See LICENSE file for licensing details.
#

"""
The redis documentation:

https://redis.io/docs/getting-started/installation/install-redis-on-linux/

"""
import os
import shutil
import socket
import subprocess
import logging
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus, WaitingStatus
from redis_ops_manager import RedisOpsManager
from charms.redis_k8s.v0.redis import RedisProvides
from typing import Optional



from literals import ( CONFIG_DIR, REDIS_PORT, LEADER_HOST_KEY )

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

class RedisVmCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.redis_ops_manager = RedisOpsManager()
        self.redis_provides = RedisProvides(self, port=REDIS_PORT)
        
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.update_status, self._update_status)

    def _on_config_changed(self, event):
        """Handle changed configuration.
        """
        shutil.copy("templates/redis.conf.tmpl", f"{CONFIG_DIR}/redis.conf")

    def _on_install(self, event):
        """Install redis"""
        os.system("curl -fsSL https://packages.redis.io/gpg | sudo gpg --yes --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg")
        with open("/etc/apt/sources.list.d/redis.list", "w+") as fh:
            fh.write("deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb focal main")
        os.system("sudo apt-get update")
        os.system("sudo apt-get install redis")
        os.system("sudo systemctl enable redis")
        
        logger.info("Installed Redis")
    
    def _update_status(self, event):
        """Handle update-status event."""
        self._set_status()

    def _on_start(self, event):
        """Handle start event."""
        self.redis_ops_manager.start()

    def _set_status(self):
        """
        Manage the status of the service.
        """
        stat = subprocess.call(["redis-cli", "ping"])
        if(stat == 0):  # if 0 (active), print "Active"
            v = self.redis_ops_manager.version()
            self.unit.set_workload_version(v)
            self.unit.status = ActiveStatus("Active")
        else:
            self.unit.status = WaitingStatus("Redis service inactive.")

    @property
    def current_master(self) -> Optional[str]:
        """Get the current master."""
        #TODO: Make this work with peer relation as we implement it.
        return socket.gethostname()

if __name__ == "__main__":  # pragma: nocover
    main(RedisVmCharm)
