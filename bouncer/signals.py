from django.dispatch import Signal

send_invite = Signal(providing_args=['to_email', 'from_user_list'])
user_accepts_invite = Signal(providing_args=['new_user', 'invited_by_user_list'])