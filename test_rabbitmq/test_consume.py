import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1", port=5672))

channel = conn.channel()
channel.queue_declare(queue="test")


def callback(channel, method, properties, body):
    print(channel)
    print(method)
    print(properties)
    print(body)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print("-----------------------")


channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=False)
print("正在接收消息")
channel.start_consuming()
