import asyncio
import os
import django

from channels.layers import get_channel_layer

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()


async def main():
    channel_layer = get_channel_layer()

    # send
    message = {"content": "hello"}
    await channel_layer.send("hello", message)

    # receive
    response = await channel_layer.receive("hello")

    print("message == response : ", message == response)


if __name__ == "__main__":
    asyncio.run(main())
