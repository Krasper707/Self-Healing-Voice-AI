import speech_recognition as sr
import requests
import pygame
import os
import time
import asyncio
import edge_tts
import random
import threading
import tempfile
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
pygame.mixer.init()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

FILLER_PHRASES = ["Let me check that for you.", "One second, looking into it."]

async def generate_audio(text, filename):
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
    await communicate.save(filename)

def pre_generate_fillers():
    if not os.path.exists("fillers"):
        os.makedirs("fillers")
    for i, phrase in enumerate(FILLER_PHRASES):
        filename = f"fillers/filler_{i}.mp3"
        if not os.path.exists(filename):
            asyncio.run(generate_audio(phrase, filename))

def play_filler():
    random_idx = random.randint(0, len(FILLER_PHRASES) - 1)
    pygame.mixer.music.load(f"fillers/filler_{random_idx}.mp3")
    pygame.mixer.music.play()

def main():
    pre_generate_fillers()
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("\nReady! Start talking (Say 'quit' to exit).\n")
        
        while True:
            try:
                print("🎙️ Listening...")
                audio_data = r.listen(source, phrase_time_limit=10)
                print("Groq Whisper Transcribing...")
                
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                    temp_audio.write(audio_data.get_wav_data())
                    temp_path = temp_audio.name

                with open(temp_path, "rb") as file:
                    transcription = groq_client.audio.transcriptions.create(
                        file=("temp.wav", file.read()),
                        model="whisper-large-v3",
                        temperature=0.0
                    )
                user_text = transcription.text
                os.remove(temp_path)
                
                if not user_text: continue
                print(f"\nYou: {user_text}")
                if user_text.lower().replace(".", "") in["quit", "exit"]: break

                # --- LATENCY MASKING TIMEOUT 
                api_result = {}
                def call_backend():
                    try:
                        res = requests.post("http://localhost:8000/voice-chat", json={"query": user_text})
                        api_result["text"] = res.json().get("response", "")
                    except:
                        api_result["text"] = "Server error."

                api_thread = threading.Thread(target=call_backend)
                api_thread.start()
                api_thread.join(timeout=0.5)

                if api_thread.is_alive():
                    print("API > 500ms. Playing filler audio...")
                    play_filler()
                    api_thread.join()
                    while pygame.mixer.music.get_busy(): time.sleep(0.1)
                else:
                    print("Fast-Fail Triggered. Skipping filler.")

                # --- EDGE TTS 
                bot_text = api_result.get("text", "")
                print(f"Bot: {bot_text}")
                
                temp_audio_file = "response.mp3"
                asyncio.run(generate_audio(bot_text, temp_audio_file))
                
                pygame.mixer.music.load(temp_audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy(): time.sleep(0.1)
                
                pygame.mixer.music.unload()
                if os.path.exists(temp_audio_file): os.remove(temp_audio_file) 
                print("-" * 50)

            except Exception as e:
                pass 

if __name__ == "__main__":
    main()