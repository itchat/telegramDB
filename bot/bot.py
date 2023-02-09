from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, Application, ContextTypes
from db.database import Database
from config import authorized, token


class Bot:
    def __init__(self):
        self.batch_save_mode = None
        self.db = Database()
        self.bot = Application.builder().token(token).build()
        self.bot.add_handler(CommandHandler("start", self.start))
        self.bot.add_handler(CommandHandler("batch", self.set_mode))
        self.bot.add_handler(CommandHandler("cancel", self.cancel))
        self.bot.add_handler(CommandHandler("search", self.search))
        self.bot.add_handler(CommandHandler("delete", self.delete))
        self.bot.add_handler(CommandHandler("random", self.random))
        self.bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.save))
        self.bot.run_polling()

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in authorized:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Pong!")

    async def set_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in authorized:
            self.batch_save_mode = True
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Enter the messages to add, type /cancel to exit batch save mode.")

    async def save(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in authorized:
            if self.batch_save_mode:
                text = update.message.text_markdown_v2_urled
                self.db.save_to_database(text)
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Message saved.")

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in authorized:
            self.batch_save_mode = False
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Batch save mode canceled.")

    async def delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in authorized:
            record_id = context.args[0]
            self.db.delete_record(record_id)
            await update.message.reply_text('Record {} deleted successfully.'.format(record_id))

    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in authorized:
            try:
                result = self.db.search_in_database(context.args[0])
                if result:
                    for message in result:
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=f"__{message['id']}\. {message['text']}__",
                                                       parse_mode="MarkdownV2")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="No messages found.")
            except IndexError as e:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="`Ex: /search Messages.`",
                                               parse_mode="MarkdownV2")

    async def random(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in authorized:
            try:
                result = self.db.read_database()
                # print(result)
                if result:
                    for message in result:
                        print(message)
                        await context.bot.send_message(chat_id=update.effective_chat.id,
                                                       text=f"{message['id']}\. {message['text']}",
                                                       parse_mode="MarkdownV2")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="No messages found.")
            except IndexError as e:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{e}", parse_mode="MarkdownV2")
