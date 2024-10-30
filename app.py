from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
from characterai import aiocai
import time
from flask_socketio import SocketIO, emit, send


userTurn = False
user_input = None
aiTurn = True
yourChat = None
chatCreated = False

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
    
    print("inget")

    char = '0yCipW7-xP5kWWT9ptFbvE324QFNbCIZe2gb8AWvlXM'

    client = aiocai.Client('ecf4941c89f3fb09372078ed8cb36b679e6074c9')
    yourChat = user_chats.get(user_sid)

    if yourChat is not None:

        async with await client.connect() as chat:
            print('connecting')
            text = user_input
            message = await chat.send_message(
                char, yourChat, text
            )
            print('end stage msg')
            print(message.text)
            return message.text
    else:
        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(
            char, me.id
            )
            user_chats[user_sid] = new.chat_id
            return answer.text


        
        


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)





@app.route('/long-poll', methods=['GET'])
async def long_poll():
    global user_input
    output_message = await getmessage((user_input))
        

    return output_message




@app.route("/", methods=['GET', 'POST'])
def home():
    global chatCreated
    output = 'deez'
    if chatCreated == False:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        output = loop.run_until_complete(checkChat())
        chatCreated = True

    return render_template('index.html', text=output)


async def baiter():
    print('test that')

@socketio.on('test')
def test(test):
    print('why does this work')

@socketio.on('submit')
def submit(submit):
    user_sid = request.sid
    print('input received')
    user_input = submit
    print(user_input)
    print('getting message')
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)
    output_message = loop1.run_until_complete(getmessage(user_input, user_sid))
    print('outputted, returning')
    socketio.emit('output', output_message, to=request.sid)


if __name__ == "__main__":
    socketio.run(app)




