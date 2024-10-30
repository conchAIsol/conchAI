import asyncio
import websockets
import uuid
from http.server import SimpleHTTPRequestHandler, HTTPServer
from characterai import aiocai
import threading

user_chats = {}

async def checkChat(user_sid):
    if user_sid not in user_chats:
        char = '0yCipW7-xP5kWWT9ptFbvE324QFNbCIZe2gb8AWvlXM'
        client = aiocai.Client('ecf4941c89f3fb09372078ed8cb36b679e6074c9')

        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(
            char, me.id
            )
            user_chats[user_sid] = new.chat_id
            return answer.text
    else:
        return None 
    
async def getmessage(user_input, user_sid):
    print("getmsg called")
    if user_sid not in user_chats:
        print("ifmsg")
        char = '0yCipW7-xP5kWWT9ptFbvE324QFNbCIZe2gb8AWvlXM'
        client = aiocai.Client('ecf4941c89f3fb09372078ed8cb36b679e6074c9')

        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(
            char, me.id
            )
            user_chats[user_sid] = new.chat_id
            print(answer.text)
            return answer.text
    else:
        print("elsemsg")
        char = '0yCipW7-xP5kWWT9ptFbvE324QFNbCIZe2gb8AWvlXM'
        client = aiocai.Client('ecf4941c89f3fb09372078ed8cb36b679e6074c9')
        yourChat = user_chats.get(user_sid)
        async with await client.connect() as chat:
            print('connecting')
            text = user_input
            message = await chat.send_message(
                char, yourChat, text
            )
            print('end stage msg')
            print(message.text)
            return message.text

async def createChat(user_sid):
    if user_sid not in user_chats:
        print("ifmsg")
        char = '0yCipW7-xP5kWWT9ptFbvE324QFNbCIZe2gb8AWvlXM'
        client = aiocai.Client('ecf4941c89f3fb09372078ed8cb36b679e6074c9')

        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(
            char, me.id
            )
            user_chats[user_sid] = new.chat_id
            print('created new chat', user_chats[user_sid])
            return answer.text


async def handler(websocket, path):

    print('handling')

    user_sid = str(uuid.uuid4())
    await createChat(user_sid)

    async for message in websocket:
        response = await getmessage(message, user_sid)
        await websocket.send(response)



def run_http_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print('websocket server started lh')

        threading.Thread(target=run_http_server, daemon=True).start()
        await asyncio.Future()



if __name__ == "__main__":
    asyncio.run(main())
