import streamlit as st
import speech_recognition as sr
import edge_tts
import asyncio
import io
import wave
import uuid

def show_voice():
    st.set_page_config(
        page_title="Voice Assistant",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Voice Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container(height=600)

    # Render history
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and "audio" in msg:
                    st.audio(msg["audio"], format="audio/mp3")

        audio_value = st.audio_input("🎤 Tell me what you want to ask", sample_rate=48000)

        if audio_value:
            audio_bytes = audio_value.read()

            # Speech to text
            try:
                with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                    frames = wf.readframes(wf.getnframes())
                    sample_rate = wf.getframerate()
                    sample_width = wf.getsampwidth()

                recognizer = sr.Recognizer()
                audio_data = sr.AudioData(frames, sample_rate, sample_width)

                user_text = recognizer.recognize_google(
                    audio_data,
                    language="vi-VN"
                )

            except sr.UnknownValueError:
                st.error("Voice not recognized")
                st.stop()

            except sr.RequestError:
                st.error("Speech recognition service unavailable (quota/network).")
                st.stop()

            except Exception as e:
                st.error("Audio processing error")
                print("STT ERROR:", e)
                st.stop()

            # Show user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_text
            })

            with st.chat_message("user"):
                st.markdown(user_text)

            # Assistant response (sau này thay bằng RAG)
            assistant_text = f"You just said: **{user_text}**."

            # Text-to-Speech (async safe)
            async def tts_to_bytes(text):
                communicate = edge_tts.Communicate(
                    text=text,
                    voice="vi-VN-HoaiMyNeural",
                    rate="-10%",
                    volume="-5%"
                )
                audio_stream = io.BytesIO()
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_stream.write(chunk["data"])
                audio_stream.seek(0)
                return audio_stream

            try:
                audio_buffer = asyncio.run(tts_to_bytes(assistant_text))
            except RuntimeError:
                # Fix event loop issue in Streamlit
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                audio_buffer = loop.run_until_complete(tts_to_bytes(assistant_text))

            # Render assistant
            with st.chat_message("assistant"):
                st.markdown(assistant_text)
                st.audio(audio_buffer, format="audio/mp3")

            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_text,
                "audio": audio_buffer
            })
