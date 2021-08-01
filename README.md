# 🤖 Conversational Game Bot (for Telegram: Chat App)

A simple, conversational games bot for Telegram to help keep chats active and fun. Responses are stored locally in `.txt` files. The default database is SFW, though it's easy to add or remove responses by editing the text files found in the data folder.

Conversational games the bot has at the moment. You can get a list of commands by typing `/help`.
- **Truth Or Dare**
- **Never Have I Ever**
- **[Would You Rather](http://either.io/)**
- **This Or That**
- **[Will You Press The Button](https://willyoupressthebutton.com/)**

## 🚀 Getting Started

### Inviting

I'm not hosting any public instances of the bot right now, but I may in the future. Until then, you'll have to self-host it. Follow the steps down below to get started hosting the bot yourself.

### Prerequisites

- [Python](https://www.python.org/) 3.8 or above.
- [python-telegram-bot](https://pypi.org/project/python-telegram-bot) (API Wrapper)

### Installing

1. Clone the repository. (I recommend creating a virtual environment)
```
git clone https://github.com/waterrmalann/telegram-conversational-games-bot.git
```
2. Install the requirements.txt
```
python -m pip install -r requirements.txt
```
3. Create a bot and grab the bot token by messaging `@BotFather` on Telegram.
4. Open `config.json` and put the bot token in `BOT_TOKEN`.
5. Run the project
```
python cgb.py
```

### Adding new responses or editing them

Responses are located at the data folder in text files where they're separated using newlines. Currently, local response databases exist only for Truth or Dare, Never Have I Ever, and This or That. Would You Rather and Press The Button works by requesting their websites to fetch questions. I do plan on also making a local database for both of these games just in case the request approach fails or stops working in the future.

## 🤝 Contributing

Contributions are accepted and there really isn't any strict rules. Feel free to open a pull request to fix any issues or to make improvements you think that should be made. You can also add new games or new responses to the current local database. Any contribution will be accepted as long as it doesn't stray too much from the objective of the bot. If you're in doubt about whether the PR would be accepted or not, you can always open an issue to get my opinion on it.

### To-Do

You can also help me with the current to-do list I have in mind (in no particular order).
- Add command cooldowns.
- Inline mode support.
- Avoid repetition of the same response for the same person.
- Larger database of questions.
- Backup local database of questions for press the button and would you rather.
- Ability to add custom responses per-group. (maybe)
- Ability to request responses to be added to the main database (through a command).
- NSFW Database of questions that show up only when explicitly enabled.

License
----

AGPLv3, see [LICENSE](LICENSE)