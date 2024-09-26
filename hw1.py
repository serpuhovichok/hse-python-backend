import math
import json


async def error(send, code):
    await send({
        "type": "http.response.start",
        "status": code,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    })
    await send({
        "type": "http.response.body",
        "body": f'{{"error": {code}}}'.encode(),
    })

async def result(send, value):
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    })
    await send({
        "type": "http.response.body",
        "body": f'{{"result": {value}}}'.encode(),
    })

async def app(scope, receive, send) -> None:
    if scope['method'] != 'GET':
        await error(send, 404)

    elif scope['path'] == '/factorial':
        if not scope['query_string'].startswith(b'n='):
            await error(send, 422)
        try:
            n = int(scope['query_string'][2:].decode())
            await result(send, math.factorial(n))
        except Exception as e:
            await error(send, 422)

    elif scope['path'].startswith('/fibonacci'):
        try:
            n = int(scope["path"][11:])
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            await result(send, b)
        except Exception as e:
            await error(send, 422)

    elif scope['path'] == '/mean':
        request_body = await receive()
        request_body = request_body["body"]
        if request_body is None:
            await error(send, 422)

        try:
            data = [int(n) for n in json.loads(request_body.decode('utf-8'))]
            await result(send, mean(data))
        except Exception as e:
            await error(send, 422)

    else:
        await error(send, 422)