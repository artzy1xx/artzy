from telethon import TelegramClient, events
from telethon.tl.types import InputMediaDice
import asyncio
import sys

# Your credentials
API_ID = 26774158
API_HASH = "1c8765a240ab2795b02942e96057c1e0"
PHONE_NUMBER = "+12892367853"

# Initialize client
client = TelegramClient('dices_session', API_ID, API_HASH)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.dice (\d+)'))
async def dice_handler(event):
    # Get target number from command
    target = int(event.pattern_match.group(1))

    # Validate target
    if not 1 <= target <= 6:
        return

    # Delete the command message
    await event.delete()

    # -*- coding: utf-8 -*-
    # Keep sending dice until we get the target
    while True:
        try:
            # Send a dice
            message = await client.send_file(
                event.chat_id,
                file=InputMediaDice('🎲')
            )

            # Get the dice value
            value = message.media.value

            # If it's not the target, delete it and try again
            if value != target:
                await message.delete()
            else:
                # We got our target number, keep it and exit
                break

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(0.5)

async def main():
    # Connect to the client
    await client.connect()

    # Check if we need to log in
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)
        code = input("Enter the code you received: ")
        try:
            await client.sign_in(PHONE_NUMBER, code)
        except Exception as e:
            if "Two-steps verification" in str(e) or "2FA" in str(e):
                password = input("Enter your 2FA password: ")
                await client.sign_in(password=password)

    print("Bot running. Type .dice [1-6] in any chat.")

    # Start the client
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
