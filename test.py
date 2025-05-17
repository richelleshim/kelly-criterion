import asyncio
import discord
import os

from dotenv import load_dotenv
load_dotenv()        

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



async def test_token():
    print(f"Testing token: {TOKEN[:5]}...{TOKEN[-5:]}")  # Print first and last 5 chars for safety
    
    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():
        print(f'Successfully logged in as {client.user}')
        await client.close()
    
    try:
        await client.start(TOKEN)
    except discord.errors.LoginFailure as e:
        print(f"Login failed: {e}")
    except Exception as e:
        print(f"Other error: {e}")

# Run the test
asyncio.run(test_token())