# slackbot-sambot

Simple bot to test creating a slackbot.

This uses the RTM api which requires a Slack Classic app to be created: https://api.slack.com/apps?new_classic_app=1

To use, copy/paste and rename the .env.example file to .env and populate your oauth tokens from the newly created slack app

Install python 3.8.1 (should be compatible with any python 3 build)
run "pip install -r requirements.txt"
and finally "python main.py"

### Usage: 
write "sambot" in any chat that includes sambot to have him print his command set

Typical Commands:
```
*** SamBot Commands ***
sambot hello <name>
sambot ead <name>
sambot praise <name>
sambot scold <name>
sambot russian_roulette
sambot decide_for_us <option1> <option2> <option#>
sambot tell_me_a_joke <neutral|chuck|all>
sambot translate <fromlang> <tolang> <content>
```

All commands must start with sambot followed by the command and arguments if any

Sambot can also live translate, type in any language other than english for automatic translation. The translation capability is provided by google translate.

Enjoy