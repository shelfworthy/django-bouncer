from django.utils.http import base36_to_int
from django.shortcuts import get_object_or_404

from .models import Invite, WaitList

def add_to_waitlist(email):
    return WaitList.objects.get_or_create(
        email = email
    )

def add_invite(to_email, from_user=None):
    invite, created = Invite.objects.get_or_create(
        to_email = to_email
    )
    
    if from_user:
        invite.from_users.add(from_user)
    
    invite.send()

def get_invite_for_token(return_token):
    uidb36, token = return_token.split('-', 1)
    
    try:
        invite = Invite.objects.get(id=base36_to_int(uidb36))
        
        if token == invite.token():
            return invite
        else:
            return None
    
    except Invite.DoesNotExist:
        return None

def ignore_invite(return_token):
    invite = get_invite_for_token(return_token)
    
    if invite:
        invite.ignore()