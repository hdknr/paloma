from django.conf import settings
from django.core.mail import get_connection
from django.utils.timezone import datetime ,now
from django.template import Template,Context
from django.db.models.loading import get_model as django_get_model

get_model = lambda p : django_get_model( *(p +'.').split('.')[:2] )
#: TODO: care of number of dots is larger then 1.

from celery import current_task,app
from celery.task import task
import exceptions
import logging
import traceback

from models import (
        Publish,Publication,Circle,Member,Message,
        Journal,
        default_return_path ,return_path_from_address
)
from mails import send_mail
from actions import process_action
from utils import class_path,make_eta

CONFIG = getattr(settings, 'PALOMA_EMAIL_TASK_CONFIG', {})

#: Actual Backend for sending email
BACKEND = getattr(settings, 'SMTP_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')

@task(serializer='pickle')          #: An EmailMessage object MUST be pickled.
def send_email(message, **kwargs):
    ''' message : django EmailMessage 
    '''
    logger = current_task.get_logger()
    try:
        conn = get_connection(backend=BACKEND)
        result = conn.send_messages([message])
        logger.debug("tasks.send_email:Successfully sent email message to %r.", message.to)
        return result
    except Exception, e:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        send_email.retry(exc=e)
        logger.debug( str(e) +  traceback.format_exc().replace('\n','/') )
        logger.warning("tasks.send_email:Failed to send email message to %r, retrying.",
                    message.to)
@task
def send_email_in_string(return_path,recipients, message_string,**extended):
    '''  message_stiring : string expression of Python email.message.Message object
    '''
    logger = current_task.get_logger()
    try:
        conn = get_connection(backend=BACKEND)
        result = conn.send_message_string(return_path,recipients,message_string,**extended)
        logger.debug("send_email_in_string:Successfully sent email message to %r.", recipients)
        return result
    except Exception, e:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.debug( traceback.format_exc() ) 
        logger.warning("send_email_in_string:Failed to send email message to %r, retrying.",
                    recipients)
        send_email_in_string.retry(exc=e)

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
    return getattr(m,task_name).delay( *args,**kwargs)

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
def process_journal(journal_id=None,*args,**kwargs):
    """ main bounce woker
    """
    log= current_task.get_logger()
    try:
        journal = Journal.objects.get(id = journal_id )
    except Exception,e:
        log.debug("task.process_journal:"+ str(e) )
        log.debug( traceback.format_exc().replace('\n','/') )
        return

    if journal.is_jailed == True:
        return

    #:Error Mail Handler 
    if process_error_mail(journal.recipient,journal.sender,journal.id):
        log.debug("task.process_journal:no error")
        return  

    #: actions
    if not process_action(journal.sender, journal.recipient,journal) :
        log.debug("deleting this journal")
        journal.delete()        #: delete ?????
        
@task
def enqueue_publish(sender,publish_id=None,publish=None,
        member_filter={},member_exclude={}):
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
    
    print "publishes=",q
    for publish in q:
        t=enqueue_mails_for_publish.delay(
            sender,publish.id ,member_filter,member_exclude) #: Asynchronized Call
        publish.status = "active"
        publish.activated_at = now()
        publish.task_id = t.task_id
        publish.save()

@task
def test(msg):
    print msg

@task
def enqueue_mails_for_publish(sender,publish_id,
            member_filter={}, member_exclude={},async=True):
    ''' Enqueu mails for speicifed Publish

        :param member_query: dict for query 

    .. todo::
        - Custum QuerSet fiilter to targetting user.
        - If called asynchronosly, enqueue_mail should be called synchronosly.
    '''
    log = current_task.get_logger()
    member_exclude.update( {'user':None } )
    try:   
        publish = Publish.objects.get(id = publish_id ) 
        for circle in publish.circles.all():
            for member in circle.member_set.filter(**member_filter).exclude( **member_exclude ):
                pub= Publication.objects.publish(publish,circle,member)
                assert pub.message != None
                if async:
                    t=enqueue_mail.delay(mail_id=pub.message.id)
                    pub.message.task_id = t.task_id
                    pub.message.save()
                else:
                    enqueue_mail(mail_obj=pub.message)
                    pub.message.task_id = "EAGER"
                    pub.message.save()

    except Exception,e:
        log.error( "enqueue_mails_for_publish():" +  str(e) )
        log.debug( traceback.format_exc().replace('\n','/') )

@task
def enqueue_mail(mail_id=None,mail_class="paloma.Message",mail_obj=None,async=True,):
    ''' Enqueue a Meail
    '''
    mail_obj= mail_obj or get_model(mail_class).objects.get(id=mail_id) 

    log = current_task.get_logger()
    log.debug('tasks.enqueue_mail %s %s' % (mail_id,mail_obj))

    current_time = now()

    try:
        if async==False or mail_obj.is_timeup:
            #: sendmail right now
            deliver_mail(mail_obj=mail_obj) 
            mail_obj.task_id='EAGER' 
            mail_obj.save()
            
        else :
            #: sendmail later
            print "sending later......"
            t= deliver_mail.apply_async([mail_obj.id,str(mail_obj._meta)], 
                                        eta=make_eta(mail_obj.publish.dt_start) )
            mail_obj.task_id = t.task_id
            mail_obj.save()
    except Exception,e:
        log.error("enqueue_mail(): %s" % str(e))
        log.debug( str(e) +"\n"+  traceback.format_exc().replace('\n','/') )
         

@task
def deliver_mail(mail_id=None,mail_class=None,mail_obj=None):
    ''' send actual mail
        
    .. todo::
        - Message status is required
    '''
    log = current_task.get_logger()
    try:
        msg = mail_obj if mail_obj != None else get_model(mail_class).objects.get(id=mail_id) 
        #:TODO: check mail status. If already "SENDING" or "CANCELD", don't send
        #       check schedue status. If already "CANCELD", don't send
        send_mail(msg.subject,     #:TODO: Message should have rendered subject
                  msg.text,
                  msg.from_address , #:TODO: Owner "symbol" to be defined and compose from address
                  msg.recipients,
                  return_path = msg.return_path,  #: RETRUN-PATH
                  message_id = msg.mail_message_id,     #: MESSSAGE-ID
                  model_class= str(msg._meta),          #: for replay model class in logging
            )
        #:TODO: change the status
                  
    except Exception,e:
        #: STMP error... ?
        log.error("send_mail(): %s" % str(e))
        log.debug( str(e) +  traceback.format_exc().replace('\n','/') )
        #:TODO: 
        #   - error mail to Message
        #   - change status of Message

###############

def do_enqueue_publish(publish, right_now=False,*args,**kwargs):
    ''' helper te enqueue_publish 
    '''
    task_args= ("admin",publish.id) + args
    if right_now or publish.dt_start == None:
        t = enqueue_publish.apply_async( task_args,kwargs ,)
    else:
        print  ">>>",publish.dt_start,make_eta(publish.dt_start) 
        t = enqueue_publish.apply_async( task_args,kwargs ,
                eta= make_eta(publish.dt_start) ) 

    publish.task_id =t.id
    publish.save()

def do_cancel_publish(publish):
    ''' helper  cancel task'''
    if publish.task_id != None:
        app.current_app().control.revoke(publish.task_id)

def apply_publish(publish):
    ''' do something depend on status '''
    if  publish.status == 'scheduled':
        do_enqueue_publish(publish)
    elif publish.status == "canceled":
        do_cancel_publish(publish)

@task
def smtp_status(sender,msg,**extended):
    log = current_task.get_logger()
    log.debug('tasks.smtp_status:%s:%s:%s' % ( sender, msg,str(extended) ) ) 
#     model_class = get_model( *(extended.get('model_class','')+'.').split('.')[:2])
    model_class = get_model( extended.get('model_class',''))
    model_class and getattr(model_class,'update_status',lambda *x,**y:None)(msg,**extended)
