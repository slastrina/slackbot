from slack import RTMClient
import json

def get_config():
    with open(".env") as fl:
        return json.load(fl)

import random
import pyjokes
from pyjokes.jokes_en import jokes_en
from googletrans import Translator

def russian_roulette(event):
    fatal_bullet = random.randint(0, 5)

    message = ''

    if fatal_bullet == 0:
        message += '(X)'
    else:
        message += '(O)'

    for x in range(5):
        if fatal_bullet == x + 1:
            message += ' X'
        else:
            message += ' O'

    if fatal_bullet == 0:
        message += ' Bang your dead!!!'

    return message

def pick_option(opt):
    res = opt.split(' ')
    if len(res) > 1:
        return res[random.randint(0, len(res) - 1)]
    else:
        return None


def bot_help(event):
    help_message = """*** SamBot Commands ***
sambot hello <name>
sambot ead <name>
sambot praise <name>
sambot scold <name>
sambot russian_roulette
sambot decide_for_us <option1> <option2> <option#>
sambot tell_me_a_joke <neutral|chuck|all>
sambot translate <fromlang> <tolang> <content> (https://ctrlq.org/code/19899-google-translate-languages)
"""

    return help_message


def command_splitter(message):
    result = message.split(' ')

    if len(result):
        if len(result) >= 3:
            return [result[0].lower(), result[1].lower(), ' '.join(result[2:])]
        elif len(result) == 2:
            return [result[0].lower(), result[1].lower(), None]
        else:
            return [result[0].lower(), None, None]
    else:
        return [None, None, None]


def message_text(event):
    service, command, rest = command_splitter(event)

    if not service == 'sambot':
        try:
            trans = translator.detect(event)
            language = trans.lang
            percent = trans.confidence * 100
            if language != 'en' and not percent < 70:
                translation = translator.translate(event, src=language).text

                return f'Translation (lang: {language}, {percent:.1f}%): {translation}'
        except Exception as ex:
            print(ex, event)

        return None

    if command:

        if command == 'hello':
            return f'Gday {rest}'

        if command == 'praise':
            if not rest:
                rest = 'Sam'
            return f'{rest} is awesome at everything'

        if command == 'ead':
            if rest and 'sambot' in rest.lower():
                return f'Yea Nah, You Eat a Dick'
            elif rest:
                return f'Eat a Dick {rest}'
            else:
                return f'Who should eat a dick?'

        if command == 'russian_roulette':
            return russian_roulette(event)

        if command == 'tell_me_a_joke':
            if rest in jokes_en:
                return pyjokes.get_joke(category=rest)
            else:
                return pyjokes.get_joke()

        if command == 'decide_for_us':
            option = pick_option(rest)

            if option:
                return f'Lets go with {option}'

        if command == 'scold':
            if 'sambot' in rest.lower():
                return f'Yea Nah, Your worthless'
            else:
                return f'{rest} you could do better'

        if command == 'translate':
            from_lang, to_lang, content = rest.split(" ", 2)
            translation = translator.translate(content, src=from_lang, dest=to_lang).text

            try:
                return f'Translation (From:{from_lang} To: {to_lang}): {translation}'
            except ValueError:
                return f'Invalid Usage, Expected sambot translate fromlang tolang content'

        return 'Unknown Command'

    else:
        return bot_help(event)

@RTMClient.run_on(event="message")
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    print(data)
    if 'text' in data:
        response = message_text(data['text'])

        if response:
            channel_id = data['channel']
            thread_ts = data['ts']
            user = data['user']

            # web_client.chat_postMessage(
            #     channel=channel_id,
            #     text=f"Hi <@{user}>!",
            #     thread_ts=thread_ts
            # )

            web_client.chat_postMessage(
                channel=channel_id,
                text=f"{response}"
            )

config = get_config()

translator = Translator()

slack_token = config['bot_user_oath_token']

rtm_client = RTMClient(
    token=slack_token,
    connect_method='rtm.start'
)

rtm_client.start()