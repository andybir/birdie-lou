To test payments in development:
$ export PATH=$PATH:/usr/local/opt/rabbitmq/sbin
$ rabbitmq-server
$ celery -A myshop worker -l info