import random
import math
import streamlit as st

# ---------- Page Setup ----------
st.set_page_config(page_title="Tic-Tac-Toe • Streamlit Game", page_icon="🎮", layout="centered")

# ---------- Utils ----------
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6)              # diagonals
]

def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]  # 'X' or 'O'
    if all(cell for cell in board):
        return "Draw"
    return None

def available_moves(board):
    return [i for i, v in enumerate(board) if v == ""]

def minimax(board, player, ai, human, alpha=-math.inf, beta=math.inf):
    winner = check_winner(board)
    if winner == ai:   return (1, None)
    if winner == human:return (-1, None)
    if winner == "Draw": return (0, None)

    if player == ai:
        best_score, best_move = -math.inf, None
        for m in available_moves(board):
            board[m] = ai
            score, _ = minimax(board, human, ai, human, alpha, beta)
            board[m] = ""
            if score > best_score:
                best_score, best_move = score, m
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return (best_score, best_move)
    else:
        best_score, best_move = math.inf, None
        for m in available_moves(board):
            board[m] = human
            score, _ = minimax(board, ai, ai, human, alpha, beta)
            board[m] = ""
            if score < best_score:
                best_score, best_move = score, m
            beta = min(beta, score)
            if beta <= alpha:
                break
        return (best_score, best_move)

def ai_pick_move(board, ai, human, difficulty):
    moves = available_moves(board)
    if not moves:
        return None
    if difficulty == "Easy":
        return random.choice(moves)
    # "Hard" (perfect play via minimax)
    _, move = minimax(board[:], ai, ai, human)
    return move

def reset_game(human="X", difficulty="Easy"):
    st.session_state.board = [""] * 9
    st.session_state.human = human
    st.session_state.ai = "O" if human == "X" else "X"
    st.session_state.turn = "X"
    st.session_state.game_over = False
    st.session_state.difficulty = difficulty
    st.session_state.stats = st.session_state.get("stats", {"You": 0, "AI": 0, "Draw": 0})
    # If AI is X, let AI start
    if st.session_state.ai == "X":
        ai_move = ai_pick_move(st.session_state.board, st.session_state.ai, st.session_state.human, st.session_state.difficulty)
        if ai_move is not None:
            st.session_state.board[ai_move] = st.session_state.ai
            st.session_state.turn = "O"

# ---------- State ----------
if "board" not in st.session_state:
    reset_game()

# ---------- Sidebar (Settings) ----------
st.sidebar.title("⚙️ Settings")
col_s1, col_s2 = st.sidebar.columns(2)
human_choice = col_s1.selectbox("You play as", ["X", "O"], index=0 if st.session_state.human == "X" else 1)
difficulty_choice = col_s2.selectbox("Difficulty", ["Easy", "Hard"], index=0 if st.session_state.difficulty=="Easy" else 1)

if st.sidebar.button("New Game"):
    reset_game(human_choice, difficulty_choice)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Scoreboard")
st.sidebar.write(f"**You:** {st.session_state.stats['You']}  |  **AI:** {st.session_state.stats['AI']}  |  **Draw:** {st.session_state.stats['Draw']}")

# ---------- Title ----------
st.title("🎮 Tic-Tac-Toe")
st.caption("Built with Streamlit. Turn-based logic = perfect fit!")

# ---------- Status Message ----------
winner = check_winner(st.session_state.board)
if winner:
    st.session_state.game_over = True
    if winner == "Draw":
        st.success("It's a draw!")
    elif winner == st.session_state.human:
        st.success("You win! 🥳")
    else:
        st.error("AI wins! 🤖")
else:
    st.info(f"Turn: **{st.session_state.turn}** ({'You' if st.session_state.turn == st.session_state.human else 'AI'})")

# ---------- Board UI ----------
def handle_click(idx):
    if st.session_state.game_over:
        return
    if st.session_state.board[idx] != "":
        return
    if st.session_state.turn != st.session_state.human:
        return

    # Human move
    st.session_state.board[idx] = st.session_state.human
    st.session_state.turn = st.session_state.ai

    # Check after human move
    w = check_winner(st.session_state.board)
    if w:
        st.session_state.game_over = True
        if w == "Draw":
            st.session_state.stats["Draw"] += 1
        elif w == st.session_state.human:
            st.session_state.stats["You"] += 1
        else:
            st.session_state.stats["AI"] += 1
        return

    # AI move immediately in same run
    ai_move = ai_pick_move(st.session_state.board, st.session_state.ai, st.session_state.human, st.session_state.difficulty)
    if ai_move is not None:
        st.session_state.board[ai_move] = st.session_state.ai
        st.session_state.turn = st.session_state.human

    # Check after AI move
    w = check_winner(st.session_state.board)
    if w:
        st.session_state.game_over = True
        if w == "Draw":
            st.session_state.stats["Draw"] += 1
        elif w == st.session_state.human:
            st.session_state.stats["You"] += 1
        else:
            st.session_state.stats["AI"] += 1

# Draw grid (3x3)
for r in range(3):
    cols = st.columns(3, gap="small")
    for c in range(3):
        i = r * 3 + c
        label = st.session_state.board[i] if st.session_state.board[i] else " "
        # Use big, square-like buttons
        cols[c].button(
            label,
            key=f"cell_{i}",
            on_click=handle_click,
            args=(i,),
            help="Click to place your mark",
            use_container_width=True
        )

# ---------- Footer Controls ----------
col1, col2, col3 = st.columns(3)
if col1.button("🔁 Restart"):
    reset_game(st.session_state.human, st.session_state.difficulty)

if col2.button("🔄 Switch Sides"):
    new_human = "O" if st.session_state.human == "X" else "X"
    reset_game(new_human, st.session_state.difficulty)

if col3.button("🧠 Toggle Difficulty"):
    new_diff = "Hard" if st.session_state.difficulty == "Easy" else "Easy"
    reset_game(st.session_state.human, new_diff)

st.caption("Tip: Streamlit re-runs on each click, which makes turn-based games simple and stable.")
