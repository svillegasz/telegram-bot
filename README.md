# Telegram Bot with Vertex AI

A Python-based Telegram bot built with `python-telegram-bot` that integrates with Google Cloud's Vertex AI agent engine to provide intelligent, context-aware conversations.

## Features

- **AI-Powered Conversations**: Uses Vertex AI Agent Engines for intelligent responses
- **Session Management**: Manages separate conversation sessions per user using agent.create_session()
- **Personalized Greetings**: Greets users by their first and last name from their Telegram profile
- **Error Handling**: Graceful error handling with user-friendly messages
- **Typing Indicators**: Shows typing action while processing responses
- **Environment-based Configuration**: Secure token and credentials management using `.env` files
- **Comprehensive Logging**: Track bot activity, agent interactions, and errors
- **Dual Mode Support**: Works in both polling (development) and webhook (production) modes

## Prerequisites

- Python 3.13 or higher
- Poetry (Python dependency manager) [(installation guide)](https://python-poetry.org/docs/#installation)
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Google Cloud Platform account with:
  - Vertex AI API enabled
  - A deployed Agent Engine
  - Service account with appropriate permissions (Vertex AI User role)

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

### 1. Set Up Google Cloud Authentication

Before configuring the bot, set up Google Cloud authentication:

```bash
# Option 1: Use service account key file (recommended for production)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

# Option 2: Use application default credentials (good for development)
gcloud auth application-default login
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with the following configuration:

#### For Development (Polling Mode - Default)

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_MODE=polling

# Vertex AI Configuration
VERTEX_AI_PROJECT_ID=your-gcp-project-id
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_AGENT_ID=your-reasoning-engine-agent-id
```

#### For Production (Webhook Mode)

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_MODE=webhook
WEBHOOK_URL=https://yourdomain.com
PORT=8443

# Vertex AI Configuration
VERTEX_AI_PROJECT_ID=your-gcp-project-id
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_AGENT_ID=your-reasoning-engine-agent-id
```

**Configuration Options:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | - | Your bot token from [@BotFather](https://t.me/botfather) |
| `BOT_MODE` | No | `polling` | Bot operation mode: `polling` (development) or `webhook` (production) |
| `WEBHOOK_URL` | Only for webhook mode | - | Public HTTPS URL where Telegram will send updates |
| `PORT` | Only for webhook mode | `8443` | Port for webhook server (443, 80, 88, or 8443) |
| `VERTEX_AI_PROJECT_ID` | Yes | - | Your Google Cloud project ID |
| `VERTEX_AI_LOCATION` | No | `us-central1` | Vertex AI region (e.g., `us-central1`, `us-east1`, `europe-west1`) |
| `VERTEX_AI_AGENT_ID` | Yes | - | Your deployed Agent Engine ID |

**⚠️ Important**: Never commit your `.env` file or service account keys to version control. They're already listed in `.gitignore`.

### 3. Create Your Vertex AI Agent

To use this bot, you need a deployed Agent Engine in Vertex AI. Here's how to create one:

1. **Enable Vertex AI API** in your GCP project
2. **Create an Agent Engine** using the Vertex AI console or SDK
3. **Deploy the agent** and note the agent ID
4. **Grant permissions**: Ensure your service account has the "Vertex AI User" role

For detailed instructions on creating Vertex AI agents, refer to the [Vertex AI Agent Builder documentation](https://cloud.google.com/vertex-ai/docs/agents).

## Bot Modes

The bot supports two operation modes:

### Polling Mode (Development) 🔄

**When to use:** Local development, testing, or when you don't have a public server

**Pros:**
- Easy to set up
- Works on localhost
- No SSL certificate required
- Great for development

**Cons:**
- Bot constantly checks for updates (less efficient)
- Not recommended for production

**Configuration:**
```env
BOT_MODE=polling
```

### Webhook Mode (Production) 🚀

**When to use:** Production deployment with a public server

**Pros:**
- More efficient (Telegram pushes updates to your server)
- Better for production
- Lower server load

**Cons:**
- Requires HTTPS with valid SSL certificate
- Needs public server with accessible domain
- More complex setup

**Configuration:**
```env
BOT_MODE=webhook
WEBHOOK_URL=https://yourdomain.com
PORT=8443
```

**Requirements for Webhook Mode:**
- ✅ Public domain with HTTPS
- ✅ Valid SSL certificate (Let's Encrypt works great)
- ✅ Server accessible from internet
- ✅ Open port (443, 80, 88, or 8443)

## Usage

### Start the Bot

Run the bot using Poetry:

```bash
poetry run python telegram_bot/app.py
```

The bot will start in the configured mode (polling by default) and respond to commands.

**You should see:**
```
INFO - Starting bot in POLLING mode (development)
```
or
```
INFO - Starting bot in WEBHOOK mode
INFO - Webhook URL: https://yourdomain.com/webhook
INFO - Port: 8443
```

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Initiates conversation and creates a new session |
| Any text | Sends message to Vertex AI agent and receives intelligent response |
| Unknown commands | Bot responds with "Sorry, I didn't understand that command." |

### Testing Your Bot

1. Open Telegram and search for your bot by username
2. Send `/start` - you should receive a personalized greeting from the AI assistant
3. Send any text message - the bot will process it with Vertex AI and respond intelligently
4. Continue the conversation - the agent maintains context within the session
5. Send `/start` again to delete the old session and create a new one

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
- `google-cloud-aiplatform` (==1.110.0): Google Cloud AI Platform client with Agent Engines support

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

## Switching Between Modes

To switch between polling and webhook modes, simply update the `BOT_MODE` variable in your `.env` file:

**Switch to Polling (Development):**
```env
BOT_MODE=polling
```

**Switch to Webhook (Production):**
```env
BOT_MODE=webhook
WEBHOOK_URL=https://yourdomain.com
PORT=8443
```

Restart the bot after changing the configuration.

## 🧪 Testing Webhooks Locally

### Using the Included Utilities

This project includes helpful scripts for testing webhooks locally, especially useful for Mac ARM with Netskope:

#### Quick Setup with ngrok
```bash
# Automated setup (checks installation, configures, starts ngrok)
./scripts/quick_ngrok_setup.sh
```

#### Manage Webhooks
```bash
# Interactive webhook management tool
poetry run python scripts/webhook_manager.py
```

**Features:**
- ✅ View current webhook status and errors
- ✅ Set webhook URL (automatically adds /webhook path)
- ✅ Delete webhook to return to polling mode
- ✅ Step-by-step ngrok instructions

### Manual Webhook Testing

**Step 1: Install ngrok**
```bash
brew install ngrok
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

**Step 2: Start bot**
```bash
poetry run python telegram_bot/app.py
```

**Step 3: Start ngrok**
```bash
ngrok http 8443
```

**Step 4: Set webhook**
```bash
poetry run python scripts/webhook_manager.py
# Select option 2 and enter your ngrok HTTPS URL
```

### Detailed Documentation

For comprehensive guides on local webhook testing with Netskope considerations:
- **Webhook testing guide**: [`docs/LOCAL_WEBHOOK_TESTING.md`](docs/LOCAL_WEBHOOK_TESTING.md)
- **Scripts documentation**: [`scripts/README.md`](scripts/README.md)

## Troubleshooting

### "TELEGRAM_BOT_TOKEN not found" Error

**Problem**: The bot can't find your token.

**Solution**: 
- Ensure `.env` file exists in the project root
- Verify `TELEGRAM_BOT_TOKEN` is set correctly in `.env`
- No spaces around the `=` sign in `.env`

### "VERTEX_AI_PROJECT_ID not found" Error

**Problem**: Vertex AI configuration is missing.

**Solution**:
- Ensure `.env` file contains `VERTEX_AI_PROJECT_ID` and `VERTEX_AI_AGENT_ID`
- Verify your Google Cloud project ID is correct
- Check that the agent ID matches your deployed Reasoning Engine

### "Failed to load agent" Error

**Problem**: Cannot connect to Vertex AI agent.

**Solution**:
- Verify your Google Cloud credentials are set up correctly
- Check that Vertex AI API is enabled in your GCP project
- Ensure the agent ID is correct and the agent is deployed
- Verify your service account has "Vertex AI User" permissions
- Confirm the `VERTEX_AI_LOCATION` matches where your agent is deployed
- Check agent ID format: should be just the agent ID, not the full resource path

### Authentication Errors

**Problem**: Google Cloud authentication failures.

**Solution**:
```bash
# Check current authentication
gcloud auth list

# Re-authenticate if needed
gcloud auth application-default login

# Or set service account key
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

### "WEBHOOK_URL is required when BOT_MODE=webhook" Error

**Problem**: Webhook mode is enabled but URL is not configured.

**Solution**:
- Add `WEBHOOK_URL` to your `.env` file with a valid HTTPS URL
- Or switch to polling mode if you don't have a public server

### Bot Doesn't Respond (Polling Mode)

**Problem**: Bot is running but doesn't reply to messages.

**Solution**:
- Verify your token is correct
- Check if you're messaging the correct bot
- Ensure the bot is running (check console for logs)
- Check your internet connection

### Webhook Not Receiving Updates

**Problem**: Bot running in webhook mode but not receiving messages.

**Solution**:
- Verify `WEBHOOK_URL` is accessible from the internet
- Ensure you're using HTTPS (not HTTP)
- Check if the SSL certificate is valid
- Verify the port is open and not blocked by firewall
- Check server logs for incoming requests from Telegram
- Test webhook URL: `https://yourdomain.com/webhook` should be accessible

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