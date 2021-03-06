========================
Postfix Configuration
========================

MySQL bound postfix
=========================

Install MySQL bound postfix. For Debian Linux ::

    $ sudo aptitude install postfix-mysql

Paloma application initialization
================================================

Postfix MySQL virtual configutaiton of this sample uses the application database and tables.

- create MySQL database for the app.
- run syncdb

::

    $ python ../manage.py syncdb

- run migrate if required becase the sample app depends on :term:`south` migration tool.

::

    $ python ../manage.py migrate djcelery
    $ python ../manage.py migrate paloma


/etc/postfix configuration files
========================================================

For quick, run create configuration files

.. code-block:: bash

    $ python manage.py postfix makeconfig --user=hdknr

where, "user" means that "bounce handler" runs specified user's previlege. 

that'll create following files

.. code-block:: bash

    $ tree etc/

    etc/
    └── postfix
        ├── main.cf
        ├── master.cf
        └── virtual
            ├── alias.cf
            ├── domain.cf
            ├── mailbox.cf
            ├── mysql
            │   ├── alias.cf
            │   ├── domain.cf
            │   ├── mailbox.cf
            │   └── transport.cf
            └── transport.cf    

Next, execute the followings to create symbolic links

.. code-block:: bash

    $ python manage.py postfix setconfig

goes ::

    $ ls -l /etc/postfix/ 

    lrwxrwxrwx 1 root root    57  3月 25 18:02 main.cf -> /home/hdknr/ve/slu/src/paloma/example/etc/postfix/main.cf
    lrwxrwxrwx 1 root root    59  3月 25 18:02 master.cf -> /home/hdknr/ve/slu/src/paloma/example/etc/postfix/master.cf

and ::

    $ ls -l /etc/postfix/virtual/

    合計 4
    lrwxrwxrwx 1 root root 63  3月 25 11:30 mysql -> /home/hdknr/ve/slu/src/paloma/example/etc/postfix/virtual/mysql    


/etc/hosts
============

- Edit hosts files for main.cf to work.

::

    127.0.0.1       paloma localhost paloma.localhost paloma.deb


Add a Domain
=============

.. code-block:: bash

    $ python manage.py postfix add_domain paloma.com


Send a test mail
==================

Restart postfix
------------------

::

    $ sudo /etc/init.d/postfix restart

    Stopping Postfix Mail Transport Agent: postfix.
    Starting Postfix Mail Transport Agent: postfix.
    (tact)hdknr@sparrow:/etc/postfix$ sudo tail -f /var/log/mail.log 
    May  7 03:59:18 sparrow postfix/master[9689]: daemon started -- version 2.7.1, configuration /etc/postfix
    May  7 04:08:14 sparrow postfix/master[9689]: terminating on signal 15
    May  7 04:08:14 sparrow postfix/master[10661]: daemon started -- version 2.7.1, configuration /etc/postfix


sample mail
------------------------------

All mails to **paloma.deb** domain and other domain are captured by paloma_bouncer.py and saved in Journal model table.

send ::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ echo `date` | mail -s "test1" user1@paloma.deb
    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ echo `date` | mail -s "test2" user1@hdknr.deb         


mail log ::

    Apr  4 03:18:45 cats postfix/master[1804]: daemon started -- version 2.7.1, configuration /etc/postfix
    
    Apr  4 03:53:42 cats postfix/pickup[1810]: A31E2550A7: uid=2000 from=<hdknr>Apr  4 03:53:42 cats postfix/cleanup[3286]: A31E2550A7: message-id=<20120403185342.A31E2550A7@paloma.localhost>
    Apr  4 03:53:42 cats postfix/qmgr[1811]: A31E2550A7: from=<hdknr@paloma.localhost>, size=329, nrcpt=1 (queue active)
    Apr  4 03:53:43 cats postfix/pipe[3291]: A31E2550A7: to=<user1@paloma.deb>, relay=paloma, delay=1.4, delays=0.41/0.06/0/0.96, dsn=2.0.0, status=sent (delivered via paloma service)
    Apr  4 03:53:43 cats postfix/qmgr[1811]: A31E2550A7: removed
    Apr  4 03:53:52 cats postfix/pickup[1810]: DC11A550A7: uid=2000 from=<hdknr>
    Apr  4 03:53:52 cats postfix/cleanup[3286]: DC11A550A7: message-id=<20120403185352.DC11A550A7@paloma.localhost>
    Apr  4 03:53:52 cats postfix/qmgr[1811]: DC11A550A7: from=<hdknr@paloma.localhost>, size=328, nrcpt=1 (queue active)
    Apr  4 03:53:53 cats postfix/pipe[3307]: DC11A550A7: to=<user1@hdknr.deb>, relay=jail, delay=0.85, delays=0.02/0.03/0/0.8, dsn=2.0.0, status=sent (delivered via jail service)
    Apr  4 03:53:53 cats postfix/qmgr[1811]: DC11A550A7: removed

Journal ::

    >>> from paloma.models import Journal
    >>> print map(lambda j : (j.sender,j.receipient,j.is_jailed), Journal.objects.all() )
    [(u'hdknr@paloma.localhost', u'user1@hdknr.deb', True), (u'hdknr@paloma.localhost', u'user1@paloma.deb', False)]

