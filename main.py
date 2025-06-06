import os
from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import chainlit as cl
from typing import Optional, Dict, Any

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
user_pass = os.getenv("USER_PASS")

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
    name="Student Assistant Agent",
    instructions="An agent that Helps Students with their studies in a short and concise manner",
)

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", user_pass):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User
) -> Optional[cl.User]:
    '''Handle the OAuth callback from github'''
    
    print(f'Provider: {provider_id}')
    print(f'User data: {raw_user_data}')
    
    return default_user

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set('history', [])

    await cl.Message(content = 'Ask your question from Uzair\'s Agent: ').send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get('history')
    
    history.append({'role': 'user', 'content': message.content})

    formatted_history = []
    for msg in history:
        role = 'user' if msg['role'] == 'user' else 'model'
        formatted_history.append({'role': role, 'parts': [{'text': msg['content']}]})
    
    prompt = message.content
    result = Runner.run_sync(
        agent,
        prompt,
        run_config=config
    )
    
    history.append({'role': 'assistant', 'content': result.final_output})
    cl.user_session.set('history', history)
    
    await cl.Message(content = result.final_output).send()