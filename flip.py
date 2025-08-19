# advanced_idioms_game.py

import streamlit as st
import random
from PIL import Image
import time
from pathlib import Path

st.set_page_config(page_title="Advanced Idioms Flip-Flop Game 🎉", layout="wide")

st.title("🎉 Advanced Idioms Flip-Flop Game 🎉")
st.markdown("""
Master English idioms effectively!  
Flip the cards, see **images**, guess the idioms, earn points, and climb levels! 🚀
""")

# ---------------------------
# Predefined idioms database with local images
# ---------------------------
# Make sure you have an 'images' folder with named images corresponding to idioms
# Example: cats_and_dogs.jpg, ice.jpg, cake.jpg, etc.
image_folder = Path("images")

idioms_data = {
    "Basic": [
        {"phrase": "It's raining ___", "idiom": "cats and dogs", "image": image_folder/"cats_and_dogs.jpg"},
        {"phrase": "Break the ___", "idiom": "ice", "image": image_folder/"ice.jpg"},
        {"phrase": "Piece of ___", "idiom": "cake", "image": image_folder/"cake.jpg"},
        {"phrase": "Let the ___ out of the bag", "idiom": "cat", "image": image_folder/"cat.jpg"},
        {"phrase": "Hit the ___", "idiom": "sack", "image": image_folder/"bed.jpg"},
    ],
    "Difficult": [
        {"phrase": "Bite the ___", "idiom": "bullet", "image": image_folder/"bullet.jpg"},
        {"phrase": "Burn the ___", "idiom": "midnight oil", "image": image_folder/"candle.jpg"},
        {"phrase": "Cry over spilled ___", "idiom": "milk", "image": image_folder/"milk.jpg"},
        {"phrase": "A blessing in ___", "idiom": "disguise", "image": image_folder/"mask.jpg"},
        {"phrase": "Hit the nail on the ___", "idiom": "head", "image": image_folder/"hammer.jpg"},
    ],
    "Hard": [
        {"phrase": "Kick the ___", "idiom": "bucket", "image": image_folder/"bucket.jpg"},
        {"phrase": "Burn your bridges ___", "idiom": "behind you", "image": image_folder/"fire.jpg"},
        {"phrase": "The ball is in your ___", "idiom": "court", "image": image_folder/"tennis_court.jpg"},
        {"phrase": "Barking up the wrong ___", "idiom": "tree", "image": image_folder/"tree.jpg"},
        {"phrase": "Add fuel to the ___", "idiom": "fire", "image": image_folder/"fire.jpg"},
    ]
}

# ---------------------------
# Select level
# ---------------------------
level = st.selectbox("Choose Level", ["Basic", "Difficult", "Hard"])
st.write(f"**Level selected:** {level}")

# ---------------------------
# Initialize session state
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
# Game UI
# ---------------------------
st.subheader("Flip the Card for Hint")
flip = st.checkbox("Show Image Hint Instead of Phrase?")

card_placeholder = st.empty()

def show_card(flipped=False):
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

# User input
user_input = st.text_input("Your Guess (Type the missing words)", "")

# Progress bar
progress = st.progress(st.session_state.current / len(st.session_state.shuffled))

# ---------------------------
# Check answer
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
    
    # Animated card flip
    for i in range(2):
        show_card(flipped=not flip)
        time.sleep(0.3)
    
    # Move to next idiom or finish
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
# Display score and remaining
# ---------------------------
st.write(f"**Current Score:** {st.session_state.score}")
st.write(f"**Idioms Left:** {len(st.session_state.shuffled) - st.session_state.current}")
