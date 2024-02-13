import discord
import requests
import emoji
import colorama
from colorama import Fore

# Inizializza colorama per abilitare l'uso dei colori ANSI nel terminale
colorama.init()

# Token del tuo bot Discord
BOT_TOKEN = 'MTIwNTgzNTM0NjEwNTg2ODMwOA.GbITzt.hiwM0OzFXuF-qfBkK0BiDuWlB9r-7uMlXhS3Go'
# Token API di DeepL
DEEPL_API_TOKEN = 'df6aa9e5-4aaf-4948-2d1e-3b4475df97de:fx'

# ID del canale da cui prelevare i messaggi
CANALE_INPUT_ID = 1018597700712812667  # QUA DOVREI METTERE L'ID DEL CANALE DI DARKANDARKER OSSIA : 988662112454836234

# ID del canale in cui inviare i messaggi tradotti
CANALE_OUTPUT_ID = 1144646757159010384  # MIO SERVER

# Inizializza il client Discord
intents = discord.Intents.default()
intents.message_content = True  # Abilita l'accesso ai contenuti dei messaggi
client = discord.Client(intents=intents)


def translate_text(text, target_lang='IT'):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_TOKEN,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    try:
        translated_text = response.json()['translations'][0]['text']
    except KeyError as e:
        print(Fore.RED + "Errore durante la traduzione con Deepl:")
        print(response.text)
        raise e
    return translated_text


def add_emoji(text):
    # Lista di parole chiave e le corrispondenti emoji
    emoji_mapping = {
        "modifiche": ":tools:",
        "risolto": ":wrench:",
        "effetto": ":loud_sound:",
        "La caratteristica": ":shield:",
        "La Forza": ":mechanical_arm:",
        "La penetrazione": ":dagger:",
        "Developer Comments": ":pencil:",
        "Il tempo": ":hourglass_flowing_sand:",
        "Il marketplace": ":shopping_cart:",
        "I giocatori in partita avranno": ":hourglass_flowing_sand:",
        "Prefisso di accesso": ":wrench:",
        "Mago": ":magic_wand:",
        "Il server": ":rocket:",
    }

    # Divide il testo in righe
    lines = text.split("\n")
    new_lines = []

    # Parole chiave nel testo e aggiunta delle emoji corrispondenti
    for line in lines:
        # Aggiungi l'emoji solo se la parola chiave è presente nella riga
        for word, emoji_code in emoji_mapping.items():
            if word.lower() in line.lower():
                # Aggiungi l'emoji all'inizio della riga
                line = f"{emoji.emojize(emoji_code)} {line}"
                # Interrompi il ciclo per evitare duplicazioni di emoji
                break

        new_lines.append(line)

    return "\n".join(new_lines)


@client.event
async def on_ready():
    print(Fore.GREEN + "Connessione API RIUSCITA con Deepl")
    print(Fore.MAGENTA + f"Connessione API RIUSCITA DISCORD come {client.user}")


@client.event
async def on_message(message):
    # Verifica se il messaggio proviene dal canale di input e non è inviato da un bot
    if message.channel.id == CANALE_INPUT_ID and not message.author.bot:
        print(Fore.MAGENTA + f"Messaggio ricevuto nel canale di input {message.channel.name}: {message.content}")

        # Verifica se il bot ha il permesso di inviare messaggi nel canale di output
        canale_output = client.get_channel(CANALE_OUTPUT_ID)
        if canale_output:
            print(Fore.MAGENTA + "Il bot ha il permesso di inviare messaggi nel canale di output.")
            # Traduci il messaggio utilizzando l'API di Deepl
            testo_tradotto = translate_text(message.content)
            print(Fore.MAGENTA + f"Messaggio tradotto con Deepl: {testo_tradotto}")

            # Ornamenta il testo tradotto con emoji
            testo_ornamentato = add_emoji(testo_tradotto)
            print(Fore.MAGENTA + f"Messaggio ornamentato: {testo_ornamentato}")

            # Invia il messaggio ornamentato nel canale di output
            await send_long_message(canale_output, testo_ornamentato)
        else:
            print(Fore.RED + "Il bot non ha accesso al canale di output.")


async def send_long_message(channel, message_content):
    # Dividi il messaggio in chunk di massimo 2000 caratteri e li invia uno alla volta
    chunks = [message_content[i:i + 2000] for i in range(0, len(message_content), 2000)]
    for chunk in chunks:
        await channel.send(chunk)


# Avvia il bot Discord
client.run(BOT_TOKEN)
