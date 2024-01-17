/etc/init.d/redis-server stop

service olad stop

sudo docker compose -f docker-compose.yml -f docker-compose.override.yml  -f docker-compose.dev.yml up -d --build cvat_opa cvat_db cvat_redis_inmem cvat_redis_ondisk cvat_server
