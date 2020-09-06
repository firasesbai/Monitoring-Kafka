docker run --env-file kafka-connectors-manager.env -v /data/kafka_connectors_manager/:/usr/src/kafka-connectors-manager/logs \
--name kafka-connectors-manager --restart=always -d kafka-connectors-manager:1.0
