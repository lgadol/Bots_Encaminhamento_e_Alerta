import os
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURAÇÕES ---
API_ID = 0 # API_ID
API_HASH = ''

# Nome do arquivo de sessão que será criado para não precisar logar toda vez
SESSION_NAME = 'forwarder_session'

# --- IDs DOS CANAIS ---
# ID do canal de ORIGEM (o canal de promoções)
SOURCE_CHANNEL_ID = -1

# ID do grupo de DESTINO (o seu grupo privado com o outro bot)
DESTINATION_CHAT_ID = -1

# ---------------------

# Configura o logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

# Cria o cliente Telethon
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH) # usando uma plataforma como Koyeb/Render usar essa linha
client = TelegramClient(StringSession(), API_ID, API_HASH) # Para Deploy em Nuvem (assunto mais avançado)

# Este código será executado toda vez que uma nova mensagem chegar no canal de origem.
@client.on(events.NewMessage(chats=SOURCE_CHANNEL_ID))
async def forwarder_handler(event):
    """Encaminha a nova mensagem para o chat de destino."""
    try:
        await event.message.forward_to(DESTINATION_CHAT_ID)
        logging.info(f"Mensagem encaminhada do canal {SOURCE_CHANNEL_ID} para o grupo {DESTINATION_CHAT_ID}")
    except Exception as e:
        logging.error(f"Erro ao encaminhar mensagem: {e}")


async def main():
    """Função principal para iniciar o cliente."""
    logging.info("Iniciando o bot encaminhador...")
    # Conecta o cliente.
    await client.start()
    logging.info("Bot encaminhador conectado e aguardando novas mensagens.")
    # Mantém o script rodando para sempre
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Roda a função principal
    client.loop.run_until_complete(main())