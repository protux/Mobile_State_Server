from django.contrib.sessions.models import Session

SUCCESS_MESSAGES_SESSION_KEY = 'SUCCESS_MESSAGES'
ERROR_MESSAGES_SESSION_KEY = 'ERROR_MESSAGES'


def add_success_message(session: Session, message):
    messages = session.get(SUCCESS_MESSAGES_SESSION_KEY, [])
    messages += [message]
    session[SUCCESS_MESSAGES_SESSION_KEY] = messages
    session.save()


def get_success_messages(session: Session):
    return session.pop(SUCCESS_MESSAGES_SESSION_KEY, None)


def add_error_message(session: Session, message):
    messages = session.get(ERROR_MESSAGES_SESSION_KEY, [])
    messages += [message]
    session[ERROR_MESSAGES_SESSION_KEY] = messages
    session.save()


def get_error_messages(session: Session):
    return session.pop(ERROR_MESSAGES_SESSION_KEY, None)
