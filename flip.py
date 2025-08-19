# ultimate_idioms_game.py
import streamlit as st
import random
from PIL import Image
import time
from pathlib import Path

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(page_title="Ultimate Idioms Game 🎉", layout="wide")

st.title("🎉 Ultimate Idioms Learning Game 🎉")
st.markdown("""
Master English idioms effectively!  
Flip cards, see images, listen to audio, complete stories, and score points. 🚀
""")

# ---------------------------
# File Paths for Images and Audio
# ---------------------------
image_folder = Path("images")  # Place your idiom images here
audio_folder = Path("audio")   # Place your idiom audio files here (.mp3)

# ---------------------------
# Predefined Idioms Database
# ---------------------------
# Each idiom has: phrase, idiom answer, image, audio, example sentence
idioms_data = {
    "Basic": [
        {"phrase": "It's raining ___", "idiom": "cats and dogs", "image": image_folder/"cats_and_dogs.jpg", "audio": audio_folder/"cats_and_dogs.mp3", "story": "It’s raining ___, take your umbrella!"},
        {"phrase": "Break the ___", "idiom": "ice", "image": image_folder/"ice.jpg", "audio": audio_folder/"ice.mp3", "story": "John was nervous, but he decided to break the ___ by telling a joke."},
        {"phrase": "Piece of ___", "idiom": "cake", "image": image_folder/"cake.jpg", "audio": audio_folder/"cake.mp3", "story": "The test was a piece of ___; everyone finished early."},
    ],
    "Difficult": [
        {"phrase": "Bite the ___", "idiom": "bullet", "image": image_folder/"bullet.jpg", "audio": audio_folder/"bullet.mp3", "story": "I didn’t want to tell her the truth, but I had to bite the ___."},
        {"phrase": "Burn the ___", "idiom": "midnight oil", "image": image_folder/"candle.jpg", "audio": audio_folder/"midnight_oil.mp3", "story": "She burned the ___ to finish the project on time."},
    ],
    "Hard": [
        {"phrase": "Kick the ___", "idiom": "bucket", "image": image_folder/"bucket.jpg", "audio": audio_folder/"bucket.mp3", "story": "The old tree finally kicked the ___ during the storm."},
        {"phrase": "Barking up the wrong ___", "idiom": "tree", "image": image_folder/"tree.jpg", "audio": audio_folder/"tree.mp3", "story": "He is barking up the wrong ___ by blaming her for the mistake."},
    ]
}

# ---------------------------
# Level Selection
# ---------------------------
level = st.selectbox("Choose Level", ["Basic", "Difficult", "Hard"])
st.write(f"**Level selected:** {level}")

# ---------------------------
# Session State Initialization
# ---------------------------
if "score" not in st.session_state or st.session_state.get("level") != level:
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.shuffled = random.sample(idioms_data[level], len(idioms_data[level]))
    st.session_state.level = level
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

current_idiom = st.session_state.shuffled[st.session_state.current]

# ---------------------------
# Flip-Flop Card Display
# ---------------------------
st.subheader("Flip the Card for Hint")
flip = st.checkbox("Show Image Hint Instead of Phrase?")

card_placeholder = st.empty()

def show_card(flipped=False):
    """Display either phrase or image based on flip state."""
    if flipped:
        try:
            img = Image.open(current_idiom["image"])
            card_placeholder.image(img, caption=current_idiom["idiom"], use_column_width=True)
        except:
            card_placeholder.write("🖼️ Image not found!")
    else:
        card_placeholder.markdown(
            f"<div style='background-color:#fef9f9;border-radius:15px;padding:40px;text-align:center;font-size:28px;"
            f"box-shadow:5px 5px 15px #aaa;'>{current_idiom['phrase']}</div>", unsafe_allow_html=True
        )

show_card(flipped=False if not flip else True)

# ---------------------------
# Context Story Hint
# ---------------------------
st.subheader("Context Story Hint")
st.write(current_idiom["story"])

# ---------------------------
# Audio Pronunciation
# ---------------------------
st.subheader("Listen to the Idiom Pronunciation")
try:
    audio_file = open(current_idiom["audio"], "rb")
    st.audio(audio_file.read(), format='audio/mp3')
except:
    st.write("🔊 Audio not found!")

# ---------------------------
# User Input & Progress
# ---------------------------
user_input = st.text_input("Your Guess (Type the missing words)", "")
progress = st.progress(st.session_state.current / len(st.session_state.shuffled))

# ---------------------------
# Check Answer & Update Score
# ---------------------------
if st.button("Check Answer"):
    guess = user_input.lower().strip()
    correct = current_idiom["idiom"].lower()
    
    if guess == correct:
        st.success("✅ Correct! +1 Point 🎉")
        st.session_state.score += 1
        st.session_state.leaderboard.append((current_idiom["idiom"], "Correct"))
    else:
        st.error(f"❌ Incorrect! The answer is: **{current_idiom['idiom']}**")
        st.session_state.leaderboard.append((current_idiom["idiom"], "Incorrect"))
    
    # Animated flip effect
    for i in range(2):
        show_card(flipped=not flip)
        time.sleep(0.3)
    
    # Move to next idiom or finish level
    if st.session_state.current + 1 < len(st.session_state.shuffled):
        st.session_state.current += 1
        user_input = ""
    else:
        st.balloons()
        st.success(f"🎉 Level Completed! Your Score: {st.session_state.score}/{len(st.session_state.shuffled)}")
        st.subheader("🏆 Leaderboard")
        for idiom, result in st.session_state.leaderboard:
            st.write(f"{idiom}: {result}")
        if st.button("Restart Level"):
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.shuffled = random.sample(idioms_data[level], len(idioms_data[level]))
            st.session_state.leaderboard = []

# ---------------------------
# Display Score & Remaining Idioms
# ---------------------------
st.write(f"**Current Score:** {st.session_state.score}")
st.write(f"**Idioms Left:** {len(st.session_state.shuffled) - st.session_state.current}")
