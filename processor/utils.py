import boto.sqs
from django.conf import settings
from boto.sqs.message import Message
import json
import logging


def push_message_to_sqs_queue(message):
    """
    A utility function that pushes the message to the common SQS queue.
    :param message: A JSON document with the request details.
    """

    connection = boto.sqs.connect_to_region('ap-southeast-1',
                                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                            aws_secret_access_key=settings.AWS_SECRET_KEY)

    queue = connection.get_queue(settings.COMMON_SQS_QUEUE)
    message_wrapper = Message()
    message_wrapper.set_body(message)
    queue.write(message_wrapper)
    logging.info('Sent a message to SQS queue with message = %s' % message)



def push_record_to_sqs_queue(victim_id):
    """
    Prepares the message to be written to the SQS queue, that will later be used for the status confirmation campaign.
    :param victim_id: The unique ID of the victim.
    """
    from victim.models import Victim
    victim = Victim.objects.get(id=victim_id)
    message = {
        'phone_number': victim.phone_number,
        'notification_phone_number': victim.notification_contact_number,
        'victim_id': victim.id,
        'operation_id': victim.operation.id
    }
    json_message = json.dumps(message)
    logging.info('Trying to send a message to SQS queue with message = %s' % json_message)
    push_message_to_sqs_queue(json_message)



def get_message_from_sqs_queue():
    """
    Retrieves 10 messages from the SQS queue.
    """
    connection = boto.sqs.connect_to_region('ap-southeast-1',
                                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                            aws_secret_access_key=settings.AWS_SECRET_KEY)

    queue = connection.get_queue(settings.COMMON_SQS_QUEUE)
    messages = queue.get_messages(10, visibility_timeout=settings.RETRY_AFTER)
    return messages
