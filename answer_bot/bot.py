import logging
import wikipedia

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = ''
wikipedia.set_lang('en')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await bot.send_message(message.chat.id, "Welcome to the ANSWERING bot! Send me any topic and I'll give you a summary from Wikipedia.")

@dp.message_handler()
async def send_wiki(message: types.Message):
    try:
        response = wikipedia.summary(message.text, sentences=2)  # Limiting to 2 sentences
        await bot.send_message(message.chat.id, response)
    except wikipedia.exceptions.DisambiguationError as e:
        await bot.send_message(message.chat.id, f"This topic is ambiguous, please be more specific: {e.options}")
    except wikipedia.exceptions.PageError:
        await bot.send_message(message.chat.id, "There is no summary available for this topic.")
    except Exception as e:
        await bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
