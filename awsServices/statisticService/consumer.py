import json
import logging
import pika
from controllers import create_table, put_item, update_item
from enums import PageMessageAction
from pika.exchange_type import ExchangeType


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def on_message(chan, method_frame, header_frame, body, userdata=None):
    """Called when a message is received. Log message and ack it."""
    page = json.loads(body.decode()) 
    page_id = page.get(PageMessageAction.KEY_PAGE_ID.value)
    LOGGER.info('Delivery properties: %s, message metadata: %s', method_frame, header_frame)
    LOGGER.info('Userdata: %s, message body: %s', userdata, page)
    action = page.get(PageMessageAction.NAME.value, '')
    if action != '':
        page.pop(PageMessageAction.NAME.value)
    if action == PageMessageAction.CREATE.value:
        put_item(page_id)
    elif action == PageMessageAction.UPDATE.value:
        field = page.get(PageMessageAction.FIELD.value)
        increase = page.get(PageMessageAction.INCREASE.value)
        update_item(page_id, field, increase)
    

def main():
    """Main method."""
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('my-rabbit',
                                    5672,
                                    '/',
                                    credentials,
                                    heartbeat=0)#TODO use keep alive
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(
        exchange='test_exchange',
        exchange_type=ExchangeType.direct,
        passive=False,
        durable=True,
        auto_delete=False)
    channel.queue_declare(queue='standard', auto_delete=True)
    channel.queue_bind(
        queue='standard', exchange='test_exchange', routing_key='standard_key')
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume('standard', on_message, auto_ack=True)

    try:
        create_table() #create statistics table: exec 1 time on container startup
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


if __name__ == '__main__':
    main()