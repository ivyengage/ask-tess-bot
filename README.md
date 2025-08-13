# Ivy Benefits Bot

AI-powered benefits expert for Slack integration with your enrollment team.

## Quick Setup for Railway

### 1. Environment Variables
In Railway, add these environment variables:

- `SLACK_BOT_TOKEN` - Your Slack bot token (starts with xoxb-)
- `OPENAI_API_KEY` - Your OpenAI API key (starts with sk-)
- `SLACK_SIGNING_SECRET` - Your Slack app signing secret

### 2. Slack App Configuration
After deployment, update your Slack app's Event Subscriptions URL to:
`https://your-railway-app-url.railway.app/slack/events`

### 3. Bot Events to Subscribe To
In your Slack app settings, subscribe to these bot events:
- `app_mention`
- `message.channels`

### 4. Required Slack Permissions
Your bot needs these OAuth scopes:
- `app_mentions:read`
- `channels:history`
- `chat:write`
- `files:read`
- `users:read`

## Usage

1. Add the bot to your private enrollment channels
2. Mention the bot with your benefits questions:
   `@Ivy Benefits Expert What is the deductible for ABC Company's medical plan?`

## Features

- Responds only when @mentioned
- Identifies employer group from channel name
- Provides GPT-4 powered responses
- Professional formatting with citations
- Multi-channel support

## Support

For issues or questions, refer to the implementation guide provided with this bot.

