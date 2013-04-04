# -*- coding: utf-8 -*-

from django.test import TestCase
#
from django.conf import settings
from django.core import mail


class TaskTest(TestCase):
    fixtures=['auth.json','simple.json',]
    def test_smtp_status(self):
        ''' python manage.py test paloma.TaskTest.test_smtp_status '''
        from tasks import smtp_status 
        from django.contrib.auth.models import User      
        from paloma.models import Mail

        sender="test"
        message="OK"
        mail = Mail.objects.all()[0]
        mail.set_status()           #:reset
        self.assertIsNone(mail.status)
        self.assertIsNone(mail.smtped)
        
        mid =mail.mail_message_id

        smtp_status( sender,message,model_class='paloma.mail',message_id=mid,)

        mail = Mail.objects.all()[0]
        self.assertEqual(mail.status,message)
        self.assertIsNotNone(mail.smtped )
#
#class SerTest(TestCase):
#    ''' Serialization Test'''
#    def test_pickle(self):
#        ''' python ../manage.py test paloma.SerTest.test_pickle
#        '''
#        from email import message_from_string
#        msg='''From: gmail@hoge.com
#To: hdknr@foooooo.deb
#Subject:Hello
#
#My First mail'''
#        e = message_from_string(msg)
#        self.assertEqual(e['From'] , 'gmail@hoge.com')
#
#        # - serialize
#        import pickle
#        from cStringIO import StringIO
#
#        src = StringIO()
#        p = pickle.Pickler(src)
#
#
#        p.dump(e)
#        datastream = src.getvalue()
#        print repr(datastream),type(datastream)
#        
#        # - deserialize
#        dst = StringIO(datastream)        
#
#        up= pickle.Unpickler(dst)
#        e2 = up.load()
#        print type(e2)
#        #        
#        self.assertEqual(e['From'] , e2['From'] )
#
#class BounceTest(TestCase):
#
#    fixtures = ["enroll/auth.json","enroll/paloma.json",]
#
#    def test_returnpath(self):
#        ''' python ../manage.py test paloma.BounceTest.test_returnpath
#        '''
#        import exceptions
#        from paloma.models import default_return_path ,return_path_from_address
#        MSG_FMT="bcmsg-%(message_id)s@%(domain)s"
#
#        param = {'message_id': 3, "domain":"hogehoge.com" }
#
#        return_path = default_return_path(param)
#        result = return_path_from_address(return_path)
#
#        for (k,v) in result.items():
#            self.assertEqual(str(param[k]), v )
#
#        for mail in ['','admin@google.com', ]:
#            with self.assertRaises(exceptions.AttributeError) as cm:
#                print "return_path_from_address(%s)" % str(mail), "=> AttributeError"
#                result = return_path_from_address(mail)
#
#        for mail in [None] :
#            with self.assertRaises(exceptions.TypeError) as cm:
#                print "return_path_from_address(%s)" % str(mail), "=> TypeError"
#                result = return_path_from_address(mail)
#
#    def test_checkmail(self):
#        ''' python ../manage.py test paloma.BounceTest.test_checkmail
#        '''
#        import os
#        filename = "fixtures/return-path/wrong_address.eml"
#        filename = os.path.join( os.path.dirname(os.path.abspath(__file__)),filename )
#
#        from email import message_from_string
#        mobj= message_from_string( open(filename).read() )
#        print dir(mobj)
#        print "keys",mobj.keys()
#        for (k,v) in mobj.items():
#            print k,":",v
#
#    def test_disable_mailbox(self):
#        ''' python ../manage.py test paloma.BounceTest.test_disable_mailbox
#        '''
#        from paloma.models import Mailbox
#
#        self.failIfEqual(Mailbox.objects.all(),0,"Fixture is wrong. Provide some paloma.models.Message record")
#
#        bounce_th=2 #: bounce threshold
#        Mailbox.objects.all().update(is_active=True,bounces = bounce_th)  
#        
#        self.assertTrue( all( [ m.bounces >= bounce_th for m in Mailbox.objects.all() ] ) )
#        self.assertTrue( all( [ m.is_active for m in Mailbox.objects.all() ] ) )
#        
#        from paloma.tasks import disable_mailbox
#        t =disable_mailbox.apply(kwargs={"bounce_count":bounce_th},)
#        # t = disable_mailbox.subtask([bounce_th]).apply()
#        print t.state,t.result
#        print [ (m.is_active,m.bounces) 
#            for m in Mailbox.objects.filter(bounces__gte=bounce_th) ]
#        self.assertEqual(t.state,u"SUCCESS" )
#
#        self.assertTrue( all( [ m.is_active == False for m in Mailbox.objects.all() ] ) )
