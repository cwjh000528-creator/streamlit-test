import streamlit as st
import numpy as np

BOARD_SIZE = 15

st.set_page_config(page_title="五子棋", layout="wide")

if "board" not in st.session_state:
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

if "player" not in st.session_state:
    st.session_state.player = 1

if "winner" not in st.session_state:
    st.session_state.winner = None


def check_winner(board, row, col, player):
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for dr, dc in directions:
        count = 1

        r, c = row + dr, col + dc
        while (
            0 <= r < BOARD_SIZE
            and 0 <= c < BOARD_SIZE
            and board[r][c] == player
        ):
            count += 1
            r += dr
            c += dc

        r, c = row - dr, col - dc
        while (
            0 <= r < BOARD_SIZE
            and 0 <= c < BOARD_SIZE
            and board[r][c] == player
        ):
            count += 1
            r -= dr
            c -= dc

        if count >= 5:
            return True

    return False


st.title("🎮 五子棋")

if st.button("重新開始"):
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.player = 1
    st.session_state.winner = None
    st.rerun()

if st.session_state.winner:
    st.success(f"🎉 玩家 {st.session_state.winner} 獲勝")

player_name = "⚫ 黑棋" if st.session_state.player == 1 else "⚪ 白棋"
st.write(f"目前玩家：{player_name}")

for r in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)

    for c in range(BOARD_SIZE):

        value = st.session_state.board[r][c]

        if value == 1:
            label = "⚫"
        elif value == 2:
            label = "⚪"
        else:
            label = "➕"

        if cols[c].button(label, key=f"{r}_{c}"):

            if (
                value == 0
                and st.session_state.winner is None
            ):

                player = st.session_state.player

                st.session_state.board[r][c] = player

                if check_winner(
                    st.session_state.board,
                    r,
                    c,
                    player,
                ):
                    st.session_state.winner = player

                else:
                    st.session_state.player = (
                        2 if player == 1 else 1
                    )

                st.rerun()
```

