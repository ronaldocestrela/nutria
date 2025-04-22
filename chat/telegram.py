# imports buildin
import logging
import asyncio
import os

# imports third party
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.enums import ChatAction

from dotenv import load_dotenv

# imports local
from agents.nutritionist import NutritionistAgent

load_dotenv()

class TelegramBot:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        
        self.app = Client(
            api_id=os.getenv("TELEGRAM_API_ID"),
            api_hash=os.getenv("TELEGRAM_API_HASH"),
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            name="NutriaAgentBot"
        )
        
        self._setup_handlers()
        self.logger.info("Bot configurado com sucesso.")
    
    def _setup_handlers(self):
        start_handler = MessageHandler(self.start_bot,
            filters.command("start") & filters.private)
        text_filter = filters.text & filters.private
        message_handler = MessageHandler(self.handle_message, text_filter)
        photo_filter = filters.photo & filters.private
        photo_handler = MessageHandler(self.handle_photo, photo_filter)
        
        self.app.add_handler(start_handler)
        self.app.add_handler(message_handler)
        self.app.add_handler(photo_handler)
    
    async def start_bot(self, client: Client, message: Message):
        await message.reply_text(
            "Olá! Eu sou o NutrIA. Envie uma mensagem ou uma foto de um prato de comida para começar."
        )
        self.logger.info(f"Usuário {message.from_user.id} iniciou o bot.")
    
    async def handle_message(self, client: Client, message: Message):
        user_id = message.from_user.id
        user_input = message.text
        user_name = message.from_user.username
        
        await client.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        
        agent = NutritionistAgent(session_id=str(user_id))
        
        try:
            response = await agent.run(f"telegram_id: {user_name} " + f"mensagem: {user_input}")
        
        except Exception as e:
            self.logger.error(f"Erro ao processar a mensagem do usuário {user_id}: {e}", exc_info=True)
            response = "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde."
        
        await message.reply_text(response)
        self.logger.info(f"Resposta enviada para o usuário {user_name}: {response}")
    
    async def handle_photo(self, client: Client, message: Message):
        user_id = message.from_user.id
        await client.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        
        storage_dir = os.path.join(os.getcwd(), "storage")
        os.makedirs(storage_dir, exist_ok=True)
        
        photo_file_name = f"{user_id}_{message.photo.file_id}.jpg"
        photo_path = os.path.join(storage_dir, photo_file_name)
        await message.download(file_name=photo_path)
        
        agent = NutritionistAgent(session_id=str(user_id))
        
        try:
            response = await agent.run(photo_path)
        
        except Exception as e:
            self.logger.error(f"Erro ao processar a mensagem do usuário {user_id}: {e}", exc_info=True)
            response = "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde."
        
        await message.reply_text(response)
        self.logger.info(f"Resposta enviada para o usuário {user_id}: {response}")

    def run(self):
        self.logger.info("Iniciando o bot...")
        self.app.run()