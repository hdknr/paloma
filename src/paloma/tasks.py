from django.conf import settings
from django.db.models import Q
from django.core.mail import get_connection
from django.utils.timezone import now
from django.db.models.loading import get_model as django_get_model
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
import time


def get_model(p):
    # TODO: care of number of dots is larger then 1.
    return django_get_model(*(p + '.').split('.')[:2])


from celery import current_task, app
from celery.utils.log import get_task_logger
from celery.task import task
logger = get_task_logger('paloma')

import exceptions
import traceback


def _traceback(signature, msg):
    for err in msg.split('\n'):
        logger.debug(signature + ":" + err)

from models import (
    Publish,
    Publication,
    Message,
    Journal,
    return_path_from_address
)

from mails import send_mail
from actions import process_action
from utils import make_eta

CONFIG = getattr(settings, 'PALOMA_EMAIL_TASK_CONFIG', {})

#: Actual Backend for sending email
BACKEND = getattr(settings, 'SMTP_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')


@task(serializer='pickle')
def send_email(message, **kwargs):
    ''' message : django EmailMessage
    '''
    logger = current_task.get_logger()
    try:
        conn = get_connection(backend=BACKEND)
        result = conn.send_messages([message])
        logger.debug("tasks.send_email:Successfully sent email message to %r.",
                     message.to)
        return result
    except Exception, e:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        # send_email.retry(exc=e)
        logger.debug(str(e) + traceback.format_exc().replace('\n', '/'))
        logger.warning(
            "tasks.send_email:Failed to send email message to %r, retrying.",
            message.to)


@task
def send_email_in_string(return_path, recipients, message_string, **extended):
    '''  message_stiring :
            string expression of Python email.message.Message object
    '''
    logger = current_task.get_logger()
    try:
        conn = get_connection(backend=BACKEND)
        conn.open()
        result = conn.send_message_string(
            return_path, recipients, message_string, **extended)

        logger.debug(
            "send_email_in_string:Successfully sent email message to %r.",
            recipients)
        return result

    except:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.debug(traceback.format_exc())
        logger.warning(
            "{0}:Failed to send email message to {1}, retrying.".format(
                'send_email_instring', recipients))
        # send_email_in_string.retry(exc=e)


# @shared_task
@task
def send_raw_message(
        return_path, recipients,
        raw_message, *args, **kwargs):
    '''
    Send email using SMTP backend

    :param str return_path: the Envelope From address
    :param list(str) recipients: the Envelope To address
    :param str raw_message:
        string expression of Python :py:class:`email.message.Message` object
    '''

    try:
        conn = get_connection(backend=BACKEND)
        conn.open()     # django.core.mail.backends.smtp.EmailBackend
        conn.connection.sendmail(
            return_path, recipients, smart_str(raw_message))
    except:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.debug(traceback.format_exc())
        logger.warning(
            "{0}:Failed to send email message to {1}, retrying.".format(
                'send_email_instring', recipients))
        # send_raw_message.retry(exc=e)


def process_error_mail(recipient, sender, journal_id):
    """ Error Mail Checker and Handler

        - return True if mail was processed, owtherwise False

        :param recipient: destination mailbox address
        :type recipient: str
        :param sender: sender mailbox address
        :type recipient: str
        :param journal_id: Journal model id
        :type journal_id: int
        :rtype: bool (True : processed, False not processed)

    .. todo::
        - update journal error code or error reseon ?
    """

    if recipient in ['', None]:
        #: Simpley Error Mail!
        #: TODO: error marking...
        return True

    try:
        param = return_path_from_address(recipient)
        assert param['message_id'] != ""
        assert param['domain'] != ""

        try:
            #: Jourmal mail object
            journal_msg = Journal.objects.get(id=journal_id).mailobject()
            error_address = journal_msg.get('X-Failed-Recipients')
        except:
            pass

        try:
            #: Find message
            msg = Publish.objects.get(
                id=int(param['message_id']),
                publish__site__domain=param['domain'])

            # X-Failed-Recipients SHOULD be checked ?
            assert(
                error_address is None or
                error_address == msg.member.address)

            #: increment bounce number
            #: this mailbox will be disabled sometimes later.
            msg.member.bounces = msg.member.bounces + 1
            msg.member.save()

            #:
            return True

        except:
            pass

    except exceptions.AttributeError:
        # May be normal address..
        # Other handler will be called.
        return False

    return False


def call_task_by_name(mod_name, task_name, *args, **kwargs):
    """ call task by name """

    m = __import__(mod_name, globals(), locals(), ["*"])
    return getattr(m, task_name).delay(*args, **kwargs)


@task
def journalize(sender, recipient, text, is_jailed=False, *args, **kwawrs):
    """ recourde bounce mail
    """
    from models import Journal

    logger.debug(
        'paloma.tasks.journalize:From=%s To %s (jailed=%s)' % (
            sender, recipient, is_jailed))

    #: First of all, save message to the Journal
    journal = None
    try:
        journal = Journal(
            sender=sender,
            recipient=recipient,
            is_jailed=is_jailed,
            text=text)
        journal.save()

    except Exception:
        _traceback("paloma.tasks.journalize:",
                   traceback.format_exc())

    return journal and journal.id


@task
def process_journal(journal_id=None, *args, **kwargs):
    """ main bounce woker
    """
    logger.debug(_(u"Processing Journal %(id)s Backend %(backend)s") % {
        "id": str(journal_id), "backend": settings.SMTP_EMAIL_BACKEND,
    })

    try:
        journal = Journal.objects.get(id=journal_id)
        journal_forward(journal)     # forward mail if Alias exists
    except Exception:
        _traceback("task.process_journal", traceback.format_exc())
        return

    if journal.is_jailed is True:
        logger.debug("task.process_journal: this message is a jailed message.")
        return

    # Error Mail Handler
    if process_error_mail(journal.recipient, journal.sender, journal.id):
        logger.debug("task.process_journal:no error")
        return

    # actions
    if not process_action(journal.sender, journal.recipient, journal):
        logger.warn(_(u'No Action for Journal from=%(form)s to=%(to)s') % {
            "from": journal.sender, "to": journal.recipient,
        })
        # "task.process_journal:deleting this journal
        #  because no action is defined in the application.")
        journal.delete()
        # delete  TODO: provide delete flag and set True, and delete later.

    logger.debug("paloma.tasks.process_journal:processed")


@task
def enqueue_publish(sender, publish_id=None, publish=None,
                    member_filter={}, member_exclude={}):
    ''' enqueue specifid mail publish, or all publish

        - id : Publish identfier
    '''
    log = current_task.get_logger()

    q = [publish]
    if publish is None:
        args = {'status': "scheduled", }
        if publish_id:
            args['id'] = publish_id
        log.debug("specified Publish is = %s" % str(args))
        q = Publish.objects.filter(**args)

    for publish in q:
        t = enqueue_mails_for_publish.delay(
            sender, publish.id,
            member_filter, member_exclude)  # Asynchronized Call
        publish.status = "active"
        publish.activated_at = now()
        publish.task_id = t.task_id
        publish.save()


@task
def enqueue_mails_for_publish(
    sender, publish_id,
    member_filter={}, member_exclude={},
    signature="pub", async=True
):
    ''' Enqueu mails for speicifed Publish

        :param member_query: dict for query

    .. todo::
        - Custum QuerSet fiilter to targetting user.
        - If called asynchronosly, enqueue_mail should be called synchronosly.
    '''
    log = current_task.get_logger()
    # Never use: member_exclude.update({'user': None, })
    member_filter.update({'is_active': True})   # only for Active Address
    default_ban = Q(address__endswith='@localhost') | Q(user__isnull=True)

    try:
        publish = Publish.objects.get(id=publish_id)
        for circle in publish.circles.all():
            for member in circle.member_set.filter(
                    **member_filter).exclude(default_ban):
                time.sleep(20.0 / 1000.0)
                pub = Publication.objects.publish(
                    publish, circle, member, signature)

                assert pub.message is not None
                t = enqueue_mail.apply_async(
                    (), {'mail_id': pub.message.id, })

                pub.message.task_id = t.id
                pub.message.save()

    except Exception, e:
        print traceback.format_exc()
        log.error("enqueue_mails_for_publish():" + str(e))
        log.debug(traceback.format_exc().replace('\n', '/'))


@task
def enqueue_mail(mail_id=None, mail_class="paloma.Message",
                 mail_obj=None, async=True,):
    ''' Enqueue a Meail
    '''
    mail_obj = mail_obj or get_model(mail_class).objects.get(id=mail_id)

    try:
        if async:
            t = deliver_mail.apply_async((), {'mail_id': mail_obj.id, })

            mail_obj.task_id = t.task_id
        else:
            deliver_mail(mail_obj=mail_obj)
        mail_obj.save()

        logger.debug(
            _('task.enqueue_mail: id=%(id)d is delivered (%(async)s)') % {
                "id": mail_obj.id, "async": async})

    except Exception, e:
        print e
        logger.error("enqueue_mail(): %s" % str(e))
        map(lambda msg: logger.debug(str(msg)),
            traceback.format_exc().split('\n'))


@task
def deliver_mail(mail_id=None, mail_class='paloma.Message',
                 mail_obj=None,
                 *args, **kwargs):
    ''' send actual mail

    .. todo::
        - Message status is required
    '''
    try:
        msg = mail_obj or get_model(mail_class).objects.get(id=mail_id)

        # TODO: check mail status.
        #       If already "SENDING" or "CANCELD", don't send
        #       check schedue status. If already "CANCELD", don't send

        #  from mails import send_mail
        send_mail(
            msg.subject,
            msg.text,
            msg.from_address,
            msg.recipients,
            return_path=msg.return_path,
            message_id=msg.mail_message_id,
            model_class=str(msg._meta),
        )

        # TODO: change the status
        logger.debug(_('tasks.deliver_mail'
                       ':successfully delivered'
                       'Message.id = %d') % (msg.id))

    except Exception, e:
        logger.error("deliver_mail: %s" % str(e))
        logger.error(
            "mail_obj = %s mail_id = %s" % (str(mail_obj), mail_id))
        map(lambda msg: logger.debug(str(msg)),
            traceback.format_exc().split('\n'))
        # TODO:
        #   - error mail to Message
        #   - change status of Message


@task
def send_templated_message(member_or_address, template_name, params,
                           message_id=None, circle=None):
    msg = Message.objects.create_from_template(
        member_or_address, template_name, params,
        message_id, circle)
    enqueue_mail(mail_obj=msg)
    logger.debug(
        _('send_templated_message:Messsage.id=%d id enqueued') % msg.id
    )

###############


def do_enqueue_publish(publish, right_now=False, *args, **kwargs):
    ''' helper te enqueue_publish
    '''
    task_args = ("admin", publish.id) + args
    if right_now or publish.is_timeup:
        t = enqueue_publish.apply_async(task_args, kwargs, )
    else:
        t = enqueue_publish.apply_async(
            task_args, kwargs,
            eta=make_eta(publish.dt_start))

    publish.task_id = t.id
    publish.save()


def do_cancel_publish(publish):
    ''' helper  cancel task'''
    if publish.task_id is not None:
        app.current_app().control.revoke(publish.task_id)


def apply_publish(publish):
    ''' do something depend on status '''
    if publish.status == 'scheduled':
        do_enqueue_publish(publish)
    elif publish.status == "canceled":
        do_cancel_publish(publish)


@task
def smtp_status(sender, msg, **extended):
    log = current_task.get_logger()
    log.debug(
        'tasks.smtp_status:{0}:{1}:{2}'.format(
            sender, msg, str(extended)))

    # model_class = get_model(
    #       *(extended.get('model_class','')+'.').split('.')[:2])
    model_class = get_model(extended.get('model_class', ''))
    model_class and getattr(
        model_class, 'update_status', lambda *x, **y: None)(msg, **extended)


@task
def test(msg="test", *args, **kwargs):
    t = current_task
    print "request=", t.request
    print dir(t.request)
    print "is_eager=", t.request.is_eager
    print "id=", t.request.id
    print msg, args, kwargs


def journal_forward(journal):
    for forward_to in journal.forwards():
        send_email_in_string(
            journal.forward_from(),
            forward_to.alias,
            journal.text
        )
