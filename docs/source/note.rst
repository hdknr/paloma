======
Note
======

runnsing celery worker
====================================

`celery_workman.py <https://github.com/harajuku-tech/celery_workman>`_  help you.


configure worker
-------------------

workers.py has configuration parameters for django-celery.
Define wrapper command argment to run django-celery propery

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/example/app$ vi workers.py


app.workers
----------------

app.workers.configure is called by paloma_worker.py command.

.. automodule:: app.workers
    :members:


To start worker
-------------------------

.. code-block:: bash

    (slu)hdknr@wzy:~/ve/slu/src/paloma/example$ celery_workman.py app start
     
     -------------- celery@wzy v3.0.16 (Chiastic Slide)
    ---- **** ----- 
    --- * ***  * -- [Configuration]
    -- * - **** --- . broker:      amqp://paloma@localhost:5672/paloma
    - ** ---------- . app:         default:0x1fe35d0 (djcelery.loaders.DjangoLoader)
    - ** ---------- . concurrency: 1 (processes)
    - ** ---------- . events:      ON
    - ** ---------- 
    - *** --- * --- [Queues]
    -- ******* ---- . mypaloma:    exchange:mypaloma(direct) binding:mypaloma
    --- ***** ----- 
    
    [Tasks]
      . celery.backend_cleanup
      . celery.chain
      . celery.chord
      . celery.chord_unlock
      . celery.chunks
      . celery.group
      . celery.map
      . celery.starmap
      . paloma.tasks.ask_by_mail
      . paloma.tasks.bounce
      . paloma.tasks.disable_mailbox
      . paloma.tasks.enqueue_schedule
      . paloma.tasks.enroll_by_mail
      . paloma.tasks.generate_message
      . paloma.tasks.generate_messages_for_schedule
      . paloma.tasks.journalize
      . paloma.tasks.process_journal
      . paloma.tasks.reset_by_mail
      . paloma.tasks.send_email
      . paloma.tasks.send_message
      . paloma.tasks.trigger_schedule


Stopping Worker
------------------------

.. code-block:: bash

    (slu)hdknr@wzy:~/ve/slu/src/paloma/example$ celery_workman.py app stop
    celeryd-multi v3.0.16 (Chiastic Slide)
    > Stopping nodes...
            > celery.wzy: TERM -> 27690
    

Run at when Debian Linux is booted.
=======================================

sysvinit
---------

copy paloma.sh ::

    sudo cp paloma.sh /etc/init.d/paloma

Configure autostart::

    sudo /etc/inid.d/paloma install

Stop autostart ::

    sudo /etc/inid.d/paloma uninstall

supervisord
----------------

Put the following file (sluworker.ini) under /etc/supervisord.conf.d (depends on your inistallation).

::

    [program:sluworker]
    command=/home/hdknr/ve/slu/bin/celery_workman.py /home/hdknr/ve/slu/src/paloma/example/app start
    autostart=true
    autorestart=true
    startsecs=10
    stopwaitsecs=600
    user=hdknr
    directory=/home/hdknr/ve/slu/src/paloma/example/app


testing
==============================

a bogus message

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ cat /tmp/msg.txt 

    From: gmail@hoge.com
    To: hdknr@foooooo.deb
    Subject:Hello
    
    My First mail

send a bogus message

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ cat /tmp/msg.txt  | python manage.py mail --command=send


list postfix queue

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ python manage.py postfix --command=qlist

    5595554E34*    2310 Mon Mar  5 04:14:19  MAILER-DAEMON

delete message form postfix queue 

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ python manage.py postfix --command=delete --id=5595554E34

    postsuper: 5595554E34: removed
    postsuper: Deleted: 1 message


