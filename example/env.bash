#!/bin/bash
PORT=9000
DJANGO="python manage.py"
SRC=../src

DJRUN()
{
    $DJANGO runserver 0.0.0.0:$PORT
}

DJSYNC()
{
    $DJANGO syncdb
}
DJSHELL()
{
    $DJANGO shell
}

DJDB()
{
    $DJANGO dbshell
}

DJDUMP_PALOMA()
{
    $DJANGO dumpdata --indent=2 $1  > $SRC/paloma/fixtures/$2/$1.json
}


TESTMAIL()
{
    $DJANGO  mail send --file $SRC/paloma/fixtures/test.eml
}
CI_LOG()
{
    tail -f /var/celery.log | grep -v djcelery_periodictasks
}
CI_SCHEDULED()
{
    $DJANGO  celery inspect scheduled
}
CI_REVOKED()
{
    $DJANGO  celery inspect revoked
}
CI_RESTART()
{
    sudo /etc/init.d/paloma stop
    sleep 1
    mv /tmp/celery.log /tmp/celery.1.log
    sudo /etc/init.d/paloma start
}
CI_LOG()
{
    tail -f /tmp/celery.log | grep -v djcelery_periodictasks | grep -v Celerybeat
}
PL_WITHDRAW()
{
    $DJANGO membership withdraw --username=$1
}
