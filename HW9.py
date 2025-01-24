# Task 2
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import torch
from transformers import pipeline

BOT_TOKEN = "7969892940:AAGGAogCGcw-eKQP0emni9whQtz2JNm1YKA"
BOT_USERNAME = "@dsss7531"


pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot who always responds in the style of a pirate",
    },
    {"role": "user", "content": "How many helicopters can a human eat in one sitting?"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')

async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom commands!')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = update.message.text

    print(f'User ({update.message.chat.id}): {text}')
    messages = [{"role": "user", "content": text}]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    response = (outputs[0]["generated_text"])
    print('Bot: ', response)
    await update.message.reply_text(response)

if __name__ == '__main__':
    print('starting bot')
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('custom', custom))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print('polling...')
    app.run_polling(poll_interval=3)


# Task 1
'''
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7969892940:AAGGAogCGcw-eKQP0emni9whQtz2JNm1YKA"
BOT_USERNAME = "@dsss7531"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')

async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom commands!')

def handle_response(text: str) -> str:
    processed : str = text.lower()

    if 'hello' in processed:
        return 'Hello there!'

    return 'I do not understand your message'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text

    print(f'User ({update.message.chat.id}): {text}')
    response: str = handle_response(text)
    print('Bot: ', response)
    await update.message.reply_text(response)

if __name__ == '__main__':
    print('starting bot')
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('custom', custom))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print('polling...')
    app.run_polling(poll_interval=3)
'''

