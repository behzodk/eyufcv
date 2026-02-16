# Telegram Bot for Data Collection

This bot collects user information (FISH, University, Workplace, Position) and a CV, then forwards it to a specified Telegram group.

## Setup

1.  Ensure you have Python installed.
2.  Dependencies are installed in `./libs`.

## Running the Bot

Due to permission issues with global Python installation and virtual environments on your system, please run the bot using the following command which uses a local library path and passes configuration directly:

```bash
PYTHONPATH=./libs TELEGRAM_BOT_TOKEN='8471497744:AAFv69c0twtmvZ_8QEoXc4wOjO4IM_camYI' TELEGRAM_CHAT_ID='-5232704220' python3 bot.py
```

## Usage

1.  Start the bot with `/start`.
2.  Answer the questions step-by-step.
3.  Upload the CV (document) at the end.
4.  The bot will send the compiled information to the group.

## Troubleshooting

-   **Conflict Error**: If you see "terminated by other getUpdates request", ensure no other instance of the bot is running. Check your terminal processes.
-   **.env Warning**: You can ignore the `.env file not found` warning if you use the command above.
