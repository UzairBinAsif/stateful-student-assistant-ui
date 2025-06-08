import os, asyncio
from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import chainlit as cl
from typing import Optional, Dict, Any
from chainlit import Message

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
user_pass = os.getenv("USER_PASS")
user_name = os.getenv("USER_NAME")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(
    name="Civil Engineering Specialized Student Assistant Agent",
    instructions="An agent that Helps Students with their studies in a short and concise manner, made by Uzair Bin Asif",
)

# @cl.password_auth_callback
# def auth_callback(username: str, password: str):
#     # Fetch the user matching username from your database
#     # and compare the hashed password with the value stored in the database
#     if (username, password) == (user_name, user_pass):
#         return cl.User(
#             identifier="admin", metadata={"role": "admin", "provider": "credentials"}
#         )
#     else:
#         return None

# @cl.oauth_callback
# def oauth_callback(
#     provider_id: str,
#     token: str,
#     raw_user_data: Dict[str, str],
#     default_user: cl.User
# ) -> Optional[cl.User]:
#     '''Handle the OAuth callback from github'''
    
#     print(f'Provider: {provider_id}')
#     print(f'User data: {raw_user_data}')
    
#     return default_user

# async def slow_typing(text, delay=0.01):
#     msg = await cl.Message(content='').send()
#     for char in text:
#         msg.content += char
#         await msg.update()
#         await asyncio.sleep(delay)

# async def stream_text(text, chunk_size=5, delay=0.05):
#     msg = await Message(content="").send()
#     for i in range(0, len(text), chunk_size):
#         msg.content += text[i:i+chunk_size]
#         await msg.update()
#         await asyncio.sleep(delay)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set('history', [])

    # await slow_typing('Hey there, How can Uzair\'s Assistant help you today?')
    await cl.Message(content = 'Hey there, How can Uzair\'s Assistant help you today?').send()

# @cl.on_message
# async def handle_message(message: cl.Message):
#     prompt = message.content
#     history = cl.user_session.get('history')    
#     history.append({'role': 'user', 'content': prompt})

#     formatted_history = []
#     for msg in history:
#         role = 'user' if msg['role'] == 'user' else 'model'
#         formatted_history.append({'role': role, 'parts': [{'text': msg['content']}]})

#     result = Runner.run_sync(
#                 agent,
#                 prompt,
#                 run_config=config
#             )
#     # text_response = response.text if hasattr(response, 'text') else ''
#     history.append({'role': 'assistant', 'content': result.final_output})
#     cl.user_session.set('history', history)
    
#     # await stream_text(result.final_output)
#     await cl.Message(content = result.final_output).send()

@cl.on_message
async def handle_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        result = await asyncio.to_thread(
            Runner.run_sync,
            agent,
            message.content,
            run_config=config
        )
        await msg.stream_token(result.final_output)
    except Exception as e:
        await msg.stream_token(f"Error: {str(e)}")