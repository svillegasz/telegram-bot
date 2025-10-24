# Telegram Bot

A Python-based Telegram bot built with `python-telegram-bot` that provides echo functionality and personalized greetings.

## Features

- **Personalized Greetings**: Greets users by their first and last name from their Telegram profile
- **Echo Messages**: Echoes back any text message sent to the bot
- **Unknown Command Handler**: Responds to unrecognized commands with a helpful message
- **Environment-based Configuration**: Secure token management using `.env` files
- **Comprehensive Logging**: Track bot activity and errors

## Prerequisites

- Python 3.13 or higher
- Poetry (Python dependency manager) [(installation guide)](https://python-poetry.org/docs/#installation)
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd telegram-bot
```

### 2. Install Dependencies

```bash
poetry install
```

## Configuration

### 1. Set Up Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**⚠️ Important**: Never commit your `.env` file to version control. It's already listed in `.gitignore`.

## Usage

### Start the Bot

Run the bot using Poetry:

```bash
poetry run python telegram_bot/app.py
```

The bot will start polling for messages and respond to commands.

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Initiates conversation with personalized greeting using your Telegram name |
| Any text | Bot echoes your message back to you |
| Unknown commands | Bot responds with "Sorry, I didn't understand that command." |

### Testing Your Bot

1. Open Telegram and search for your bot by username
2. Send `/start` - you should receive: "Hello [Your Name]! 👋 I'm a bot, please talk to me!"
3. Send any text message - the bot will echo it back
4. Send any unknown command like `/help` - the bot will respond with an error message

## Development

### Project Structure

```
telegram-bot/
├── telegram_bot/
│   ├── __init__.py
│   └── app.py           # Main bot application
├── tests/
│   └── __init__.py
├── .env                 # Environment variables (not in git)
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── pyproject.toml      # Project dependencies
├── poetry.lock         # Locked dependencies
└── README.md           # This file
```

### Key Dependencies

- `python-telegram-bot` (>=22.5,<23.0): Telegram Bot API wrapper
- `python-dotenv` (>=1.0.0): Environment variable management

### Extending the Bot

To add new commands:

1. Define an async handler function:
```python
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Your response"
        )
```

2. Register the handler in `__main__`:
```python
my_handler = CommandHandler('mycommand', my_command)
application.add_handler(my_handler)
```

### Logging

The bot uses Python's built-in logging module. Logs include:
- Timestamp
- Logger name
- Log level (INFO, ERROR, etc.)
- Message content

Check console output for real-time logs.

## Troubleshooting

### "TELEGRAM_BOT_TOKEN not found" Error

**Problem**: The bot can't find your token.

**Solution**: 
- Ensure `.env` file exists in the project root
- Verify `TELEGRAM_BOT_TOKEN` is set correctly in `.env`
- No spaces around the `=` sign in `.env`

### Bot Doesn't Respond

**Problem**: Bot is running but doesn't reply to messages.

**Solution**:
- Verify your token is correct
- Check if you're messaging the correct bot
- Ensure the bot is running (check console for logs)
- Check your internet connection

### Import Errors

**Problem**: Module import errors when running the bot.

**Solution**:
```bash
poetry install
poetry run python telegram_bot/app.py
```

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request