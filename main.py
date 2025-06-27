import chainlit as cl
import requests

# Welcome Message
@cl.on_chat_start
async def start():
    await cl.Message(
        content=(
            "**Welcome to Crypto Agent**\n\n"
            "👉 Type `TOP 10` to get the **Top 10 coin prices**\n"
            "💰 Type any symbol like `BTCUSDT` to get its **live price**\n"
        )
    ).send()

# Handle User Messages
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip().upper()

    # Show Top 10 Coins
    if user_input == "TOP 10":
        url = "https://api.binance.com/api/v3/ticker/price"
        try:
            response = requests.get(url)
            data = response.json()

            # Prepare table content
            table = "| 🔰 Coin | 💵 Price (USDT) |\n|--------|------------------|\n"
            for coin in data[:10]:
                table += f"| `{coin['symbol']}` | `{coin['price']}` |\n"

            await cl.Message(
                content=f"🔟 **Top 10 Coins:**\n\n{table}"
            ).send()

        except Exception:
            await cl.Message(content="❌ Error fetching data. Please try again.").send()

    # Show Single Coin Price
    else:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={user_input}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                await cl.Message(
                    content=(
                        f"💸 **{user_input} Price**\n\n"
                        f"💰 `{data['price']} USDT`\n\n"
                    )
                ).send()
            else:
                await cl.Message(
                    content="⚠️ Invalid symbol. Try something like `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, etc."
                ).send()
        except Exception:
            await cl.Message(content="❌ Error fetching coin price. Please try again.").send()
