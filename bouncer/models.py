from datetime import date

from django.db import models
from django.conf import settings
from django.utils.http import int_to_base36
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.hashcompat import sha_constructor

from bouncer import signals as invites_signals

class WaitList(models.Model):
    # email of user who wants in the site
    email = models.EmailField()
    
    # date the user was added to the list
    date_added = models.DateTimeField(auto_now_add=True)
    
    # date the user was added to the site
    date_invited = models.DateField(null=True, blank=True)
    
    # what account the user joined with
    joined_as = models.ForeignKey(User, related_name="wait_list", blank=True, null=True)
    
    # who let the user into the site
    added_by = models.ForeignKey(User, related_name="users_added", blank=True, null=True)
    
    class Meta:
        verbose_name = "waitlister"
        verbose_name_plural = "wait list"
    
    def __unicode__(self):
        return u"%s" % self.email
    
    @property
    def is_user(self):
        return self.joined_as != None
    
    def save(self, *a, **kw):
        try:
            existing_user = User.objects.get(email=self.email)
            self.joined_as = existing_user
            self.date_invited = existing_user.date_joined
        except User.DoesNotExist:
            pass
        
        super(WaitList, self).save(*a, **kw)

class InvitesUser(models.Model):
    inviter = models.ForeignKey(User, unique=True)
    
    invite_count = models.IntegerField()
    
    def __unicode__(self):
        return u"%s has %s invites" % (self.inviter.username, self.invite_count)

class ActiveInvites(models.Manager):
    def get_query_set(self):
        return super(ActiveInvites, self).get_query_set().filter(date_accepted=None, ignored=False)

class Invite(models.Model):
    from_users = models.ManyToManyField(User, related_name="sent_invites_to", blank=True, null=True)
    
    to_email = models.EmailField()
    
    date_added = models.DateField(auto_now_add=True)
    last_date_sent = models.DateField(null=True, blank=True)
    
    date_accepted = models.DateField(null=True, blank=True)
    accepted_by = models.ForeignKey(User, related_name="invite", blank=True, null=True)
    
    is_ignored = models.BooleanField(default=False)
    
    objects = models.Manager()
    active_invites = ActiveInvites()
    
    @property
    def is_accepted(self):
        return self.date_accepted != None
    
    @property
    def token(self):
        return sha_constructor(settings.SECRET_KEY + unicode(int_to_base36(self.id)) + unicode(self.is_accepted) + unicode(self.is_ignored) + self.date_added.strftime('%Y-%m-%d %H:%M:%S')).hexdigest()[::2]
    
    @property
    def return_token(self):
        return "%s-%s" % (int_to_base36(self.id), self.token)
    
    def from_count(self):
        return self.from_users.count()
    
    def accept(self, user):
        if not self.is_accepted or self.is_ignored:
            self.date_accepted = date.today()
            self.accepted_by = user
            self.save()
            
            invites_signals.user_accepts_invite.send(sender=self, new_user=user, invited_by_user_list=self.from_users.all())
    
    def ignore(self):
        self.ignored = True
        self.save()
    
    def send(self):
        if not self.is_accepted or self.is_ignored:
            try:
                # check if this user is already a user of the site 
                user = User.objects.get(email=self.to_email)
                self.accept(user)
            
            except User.DoesNotExist:
                if self.last_date_sent and (date.today() - self.last_date_sent).days <= 7:
                    # only send at most one email a week
                    return
                
                # fire the send invite signal
                invites_signals.send_invite.send(sender=self, to_email=self.to_email, from_user_list=self.from_users.all())
                
                self.date_sent = date.today()
                self.save()

def user_post_save(sender, instance, created, **kwargs):
    if created:
        # check if the new user has been invited in the past
        try:
            invite = Invite.objects.get(to_email=instance.email)
            invite.accept(instance)
        except Invite.DoesNotExist:
            pass

post_save.connect(user_post_save, sender=User, dispatch_uid="invites.models")