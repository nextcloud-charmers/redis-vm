# redis-vm
Deploy redis to a vm charm

# Use with Nextcloud
The nextcloud config file for PHP: "/var/www/nextcloud/config/redis.config.php" - should be looking like this to use with redis.

```
<?php
$CONFIG = array (
  'memcache.distributed' => '\OC\Memcache\Redis',
  'memcache.locking' => '\OC\Memcache\Redis',
  'filelocking.enabled' => true,
  'memcache.local' => '\OC\Memcache\Redis',

  'redis' => [
     'host' => '192.168.2.49',
     'port' => 6379,
  ],
);
```

# TODO
There is a lot of work left on this charm

- [] Add in relation
- [] Add in proper binding for the service to the ingress address.
- [] Allow for security in the config
- [] etc.

