from django.conf import settings
from django.core.mail import get_connection
from django.utils.timezone import now
from django.template import Template,Context

from celery import current_task,app
from celery.task import task

import logging
import traceback

from models import (
        Publish,Circle,Member,Mail,
        default_return_path ,return_path_from_address
)
from mails import send_mail
from actions import process_action
from utils import class_path

CONFIG = getattr(settings, 'PALOMA_EMAIL_TASK_CONFIG', {})

#: Actual Backend for sending email
BACKEND = getattr(settings, 'SMTP_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')

#@task(**TASK_CONFIG)
# `send_emials( list_of_messages ,**kwargs )` can be defned too,
# but that makes serialized message bigger.
@task(serializer='pickle')
def send_email(message, **kwargs):
    ''' 
    .. todo::
        - change "sennder address" for VERP 
        - kwargs should have "return_path" .
    '''
    logger = current_task.get_logger()
    try:
        conn = get_connection(backend=BACKEND)
        result = conn.send_messages([message])
        logger.debug("send_email:Successfully sent email message to %r.", message.to)
        return result
    except Exception, e:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.debug( traceback.format_exc() ) 
        logger.warning("send_email:Failed to send email message to %r, retrying.",
                    message.to)
        send_email.retry(exc=e)

def process_error_mail(recipient,sender,journal_id):
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

    if recipient in ['',None]:
        #: Simpley Error Mail!
        #: TODO: error marking... 
        return True
    
    try:
        param =  return_path_from_address(recipient)
        assert param['message_id'] != ""
        assert param['domain'] != ""
        
        try:
            #: Jourmal mail object
            journal_msg=Journal.objects.get(id=journal_id).mailobject()
            error_address= journal_msg.get('X-Failed-Recipients')
        except:
            pass

        try:
            #: Find message
            msg = Mail.objects.get(id=int(param['message_id']),
                    publish__site__domain = param['domain'])

            #:X-Failed-Recipients SHOULD be checked ?
            assert ( error_address == None or error_address == msg.member.address )

            #: increment bounce number
            #: this mailbox will be disabled sometimes later.
            msg.member.bounces = msg.member.bounces+ 1
            msg.member.save()

            #:
            return True

        except:
            pass
            
    except exceptions.AttributeError,e:
        #:May be normal address..
        #:Other handler will be called.
        return False
         
    return False

def call_task_by_name(mod_name,task_name,*args,**kwargs):
    """ call task by name """
    
    m = __import__(mod_name,globals(),locals(),["*"])
    getattr(m,task_name).delay( *args,**kwargs)

    
@task
def journalize(sender,recipient,text,is_jailed=False,*args,**kwawrs):
    """ recourde bounce mail
    """
    from models import Journal
    log= current_task.get_logger()

    log.debug('From=%s To %s (jailed=%s)'  % (sender,recipient,is_jailed) )

    #: First of all, save messa to the Journal
    journal=None
    try:
        journal=Journal( 
            sender=sender,
            recipient=recipient,
            is_jailed=is_jailed,
            text=text)
        journal.save()
    except Exception,e:
        log.error( str(e) )
    
    return journal and journal.id

@task
def process_journal(sender,journal_id=None,*args,**kwargs):
    """ main bounce woker
    """
    from models import Journal
    log= current_task.get_logger()
    try:
        journal = journal or Journal.objecs.get(id = journal_id )
    except Exception,e:
        log.debug( str(e) )
        return

    if journal.is_jailed == True:
        return

    #:Error Mail Handler 
    if process_error_mail(journal.recipient,journal.sender,journal.id):
        log.debug("no error")
        return  

    #: actions
    process_action(journal.sender, journal.recipent,journal)
        
@task
def enqueue_publish(sender,publish_id=None,publish=None):
    ''' enqueue specifid mail publish, or all publish

        - id : Publish identfier
    '''
    log = current_task.get_logger()

    q = [publish]
    if publish == None:
        args = {'status': "scheduled",}
        if publish_id:
            args['id'] = publish_id
        log.debug("specified Publish is = %s" % str(args))
        q =  Publish.objects.filter(**args)
    
    for publish in q: 
        enqueue_mails_for_publish.delay(sender,publish.id ) #: Asynchronized Call
        publish.status = "active"
        publish.save()

@task
def enqueue_mails_for_publish(sender,publish_id,async=True):
    ''' Enqueu mails for speicifed Publish

    .. todo::
        - Custum QuerSet fiilter to targetting user.
        - If called asynchronosly, enqueue_mail should be called synchronosly.
    '''
    log = current_task.get_logger()
    try:   
        publish = Publish.objects.get(id = publish_id ) 
        for circle in publish.circles.all():
            for member in circle.member_set.exclude(user=None):
                #: TODO: Exclude  user == None or is_active ==False or forward == None
                if async:
                    enqueue_mail.delay(sender,publish.id,circle.id,member.id )
                else:
                    enqueue_mail(sender,publish.id,circle.id,member.id,async )
    except Exception,e:
        log.error( "enqueue_mails_for_publish():" +  str(e) )

@task
def enqueue_mail(sender,publish_id,circle_id, member_id,async=True ): 
    ''' Generate (or update) message for specifed circle and member

    '''
    log = current_task.get_logger()
    current_time = now()
    try:
        publish = Publish.objects.get(id=publish_id )
        circle = Circle.objects.get(id=circle_id)
        member= Member.objects.get(id=member_id)

        context = publish.get_context(circle,member.user)        
        msg,craeted= Mail.objects.get_or_create(publish=publish,member=member ) #:re-use the same mail
        msg.text = Template(publish.text).render(Context(context))
        msg.save()

        if async==False or current_time >= publish.dt_start: #:TODO : 1 minutes 
            #: sendmail right now
            deliver_mail(mail_obj=msg) 
        else :
            #: sendmail later
            deliver_mail.apply_async([msg.id],eta=msg.dt_start )

    except Exception,e:
        print traceback.format_exc()
        log.error("generate_message()" + str(e))

@task
def deliver_mail(mail_id=None,mail_obj=None):
    ''' send actual mail
        
    .. todo::
        - Message status is required
    '''
    log = current_task.get_logger()
    try:
        msg = mail_obj if mail_obj != None else Mail.objects.get(id=mail_id) 
        #:TODO: check mail status. If already "SENDING" or "CANCELD", don't send
        #       check schedue status. If already "CANCELD", don't send
        send_mail(msg.publish.subject,     #:TODO: Message should have rendered subject
                  msg.text,
                  msg.publish.site.authority_address, #:TODO: Owner "symbol" to be defined and compose from address
                  [msg.member.address],
                  return_path = msg.get_return_path(),  #: RETRUN-PATH
                  message_id = msg.mail_message_id,     #: MESSSAGE-ID
                  model_class= str(msg._meta),          #: for replay model class in logging
            )
        #:TODO: change the status
                  
    except Mail.DoesNotExist ,e:
        log.error("send_mail():No Message record for id=%s" % mail_id)
    except Exception,e:
        #: STMP error... ?
        log.error("send_mail(): %s" % str(e))
        #:TODO: 
        #   - error mail to Message
        #   - change status of Message

def do_enqueue_publish(publish):
    ''' helper te enqueue_publish '''
    t = enqueue_schedule.apply_async(("admin",publish.id),{},eta=publish.dt_start)
    publish.task =t.id
    publish.save()

def do_cancel_publish(publish):
    ''' helper  cancel task'''
    if publish.task != None:
        app.current_app().control.revoke(publish.task)

def apply_publish(publish):
    ''' do something depend on status '''
    if  publish.status == 'scheduled':
        do_enqueue_publish(publish)
    elif publish.status == "canceled":
        do_cancel_publish(publish)

@task
def smtp_status(sender,exception,**extended):
    from django.db.models.loading import get_model
    log = current_task.get_logger()
    log.debug('smtp_status:%s:%s:%s' % ( sender, exception,str(extended) ) ) 
    model_class = get_model( *(extended.get('model_class','')+'.').split('.')[:2])
    model_class and getattr(model_class,'update_status',lambda *x,**y:None)(model_class,exception,**extended)
