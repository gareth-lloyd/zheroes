#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/zheroes.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=zheroes
GROUP=zheroes
cd /srv/zheroes/zheroes/
source /srv/zheroes-venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS --timeout 600 --user=$USER --group=$GROUP --log-level=info --log-file=$LOGFILE 2>>$LOGFILE zheroes.wsgi:application
