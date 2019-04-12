import pika

conn = pika.BlockingConnection()

channel = conn.channel()
channel.queue_declare(queue="test")
channel.basic_publish(exchange="", routing_key="test", body="interesting!")
print("成功发送一条消息到rabbitmq")
conn.close()
