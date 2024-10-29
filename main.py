from flask import Flask, render_template, request, jsonify
import asyncio
from characterai import aiocai
import time

userTurn = False
user_input = None
aiTurn = True
yourChat = None
chatCreated = False

async def checkChat():
    global yourChat
    global chatCreated
    if yourChat is None:
        char = '0yCipW7-xP5kWWT9ptFbvE324QFNbCIZe2gb8AWvlXM'

        client = aiocai.Client('ecf4941c89f3fb09372078ed8cb36b679e6074c9')

        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(
            char, me.id
            )
            yourChat = new.chat_id
            return answer.text
        chatCreated = True
                                
async def getmessage(user_input):
    
    print("inget")
    global yourChat

    char = '0yCipW7-xP5kWWT9ptFbvE324QFNbCIZe2gb8AWvlXM'

    client = aiocai.Client('ecf4941c89f3fb09372078ed8cb36b679e6074c9')

    if yourChat is not None:

        async with await client.connect() as chat:
            text = user_input
            message = await chat.send_message(
                char, yourChat, text
            )
            return message.text


    
        
        

    

        
        


app = Flask(__name__)



@app.route('/submit-input/<input_text>', methods=['GET'])
def submit_input(input_text):
    global  user_input
    user_input = input_text
    print(user_input)
    return jsonify({"message": "Input received", "input": user_input}), 200

@app.route('/long-poll', methods=['GET'])
async def long_poll():
    global user_input
    print('here')

    # Wait for user input to be available
   
        
    # Process the input and prepare a response
    print(user_input)
    output_message = await getmessage((user_input))
        

    return jsonify(output_message)




@app.route("/", methods=['GET', 'POST'])
def home():
    global chatCreated
    output = 'deez'
    if chatCreated == False:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        output = loop.run_until_complete(checkChat())
        chatCreated = True
    if request.method == 'POST':
        user_input = request.form['user_input']
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        output = loop.run_until_complete(getmessage(user_input))

    return render_template('index.html', text=output)

if __name__ == "__main__":
    app.run()




