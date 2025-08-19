# idioms_game.py

import streamlit as st
import random
from PIL import Image
import time

st.set_page_config(page_title="Idioms Flip-Flop Game", layout="wide")

st.title("🎉 Idioms Flip-Flop Game 🎉")
st.markdown("Master English idioms with fun! Guess the idiom from the phrase or picture.")

# ---------------------------
# Predefined idioms database
# ---------------------------
idioms_data = {
    "Basic": [
        {"phrase": "It's raining ___", "idiom": "cats and dogs", "emoji": "🐱🐶"},
        {"phrase": "Break the ___", "idiom": "ice", "emoji": "🧊"},
        {"phrase": "Piece of ___", "idiom": "cake", "emoji": "🍰"},
        {"phrase": "Let the ___ out of the bag", "idiom": "cat", "emoji": "🐱"},
        {"phrase": "Hit the ___", "idiom": "sack", "emoji": "🛌"},
    ],
    "Difficult": [
        {"phrase": "Bite the ___", "idiom": "bullet", "emoji": "🔫"},
        {"phrase": "Burn the ___", "idiom": "midnight oil", "emoji": "🕯️🕛"},
        {"phrase": "Cry over spilled ___", "idiom": "milk", "emoji": "🥛"},
        {"phrase": "A blessing in ___", "idiom": "disguise", "emoji": "🎭"},
        {"phrase": "Hit the nail on the ___", "idiom": "head", "emoji": "🔨👤"},
    ],
    "Hard": [
        {"phrase": "Kick the ___", "idiom": "bucket", "emoji": "🪣💀"},
        {"phrase": "Burn your bridges ___", "idiom": "behind you", "emoji": "🔥🌉"},
        {"phrase": "The ball is in your ___", "idiom": "court", "emoji": "🎾🏟️"},
        {"phrase": "Barking up the wrong ___", "idiom": "tree", "emoji": "🐶🌳"},
        {"phrase": "Add fuel to the ___", "idiom": "fire", "emoji": "🔥⛽"},
    ]
}

# ---------------------------
# Select level
# ---------------------------
level = st.selectbox("Choose Level", ["Basic", "Difficult", "Hard"])
st.write(f"**Level selected:** {level}")

# ---------------------------
# Game logic
# ---------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = 0
if "shuffled" not in st.session_state or st.session_state.level != level:
    st.session_state.shuffled = random.sample(idioms_data[level], len(idioms_data[level]))
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.level = level

current_idiom = st.session_state.shuffled[st.session_state.current]

st.subheader("Phrase/Emoji Hint:")
flip = st.checkbox("Show Emoji Hint Instead of Phrase?")

if flip:
    st.write(current_idiom["emoji"])
else:
    st.write(current_idiom["phrase"])

user_input = st.text_input("Your Guess (Type the missing words)", "")

# ---------------------------
# Check answer
# ---------------------------
if st.button("Check Answer"):
    answer = current_idiom["idiom"].lower()
    guess = user_input.lower().strip()
    if guess == answer:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Incorrect! The answer is: **{current_idiom['idiom']}**")
    
    # Move to next idiom
    if st.session_state.current + 1 < len(st.session_state.shuffled):
        st.session_state.current += 1
    else:
        st.balloons()
        st.success(f"🎉 Level Completed! Your Score: {st.session_state.score}/{len(st.session_state.shuffled)}")
        if st.button("Restart Level"):
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.shuffled = random.sample(idioms_data[level], len(idioms_data[level]))

# ---------------------------
# Show score
# ---------------------------
st.write(f"**Current Score:** {st.session_state.score}")
st.write(f"**Idioms Left:** {len(st.session_state.shuffled) - st.session_state.current}")
