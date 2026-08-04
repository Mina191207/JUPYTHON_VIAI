import asyncio
import edge_tts

TEXT = "Xin chào"

VOICE = "vi-VN-HoaiMyNeural"

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save("test.mp3")
    print("Done")

asyncio.run(main())