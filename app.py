import streamlit as st
import numpy as np
import json
from pathlib import Path
import time

BOARD_SIZE = 20
SCORE_FILE = "score.json"

st.set_page_config(page_title="五子棋 AI 挑戰版", layout="wide")
st.markdown("""

""", unsafe_allow_html=True)

def load_score():
    if Path(SCORE_FILE).exists():
        try:
            with open(SCORE_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"player":0,"ai":0}

def save_score(score):
    with open(SCORE_FILE,"w",encoding="utf-8") as f:
        json.dump(score,f)

if (
    "board" not in st.session_state
    or not isinstance(st.session_state.board, np.ndarray)
    or st.session_state.board.shape != (BOARD_SIZE, BOARD_SIZE)
):
    st.session_state.board = np.zeros(
        (BOARD_SIZE, BOARD_SIZE),
        dtype=int
    )

if "turn" not in st.session_state:
    st.session_state.turn = 1

if "winner" not in st.session_state:
    st.session_state.winner = None

if "score" not in st.session_state:
    st.session_state.score = load_score()

def reset_board():
    st.session_state.board = np.zeros(
        (BOARD_SIZE, BOARD_SIZE),
        dtype=int
    )

    st.session_state.turn = 1
    st.session_state.winner = None

def check_win(board, r, c, p):
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for dr,dc in dirs:
        cnt = 1
        rr,cc = r+dr,c+dc
        while 0<=rr<BOARD_SIZE and 0<=cc<BOARD_SIZE and board[rr,cc]==p:
            cnt+=1; rr+=dr; cc+=dc
        rr,cc = r-dr,c-dc
        while 0<=rr<BOARD_SIZE and 0<=cc<BOARD_SIZE and board[rr,cc]==p:
            cnt+=1; rr-=dr; cc-=dc
        if cnt>=5:
            return True
    return False

def score_point(board,r,c,p):
    dirs=[(1,0),(0,1),(1,1),(1,-1)]
    total=0
    for dr,dc in dirs:
        cnt=1
        for s in (1,-1):
            rr,cc=r+dr*s,c+dc*s
            while 0<=rr<BOARD_SIZE and 0<=cc<BOARD_SIZE and board[rr,cc]==p:
                cnt+=1
                rr+=dr*s
                cc+=dc*s
        if cnt>=5: total+=100000
        elif cnt==4: total+=10000
        elif cnt==3: total+=1000
        elif cnt==2: total+=100
    return total

def ai_move():
    board = st.session_state.board
    best=None
    best_score=-1

    occupied=np.argwhere(board!=0)
    if len(occupied)==0:
        return BOARD_SIZE//2, BOARD_SIZE//2

    candidates=set()
    for r,c in occupied:
        for dr in range(-2,3):
            for dc in range(-2,3):
                nr,nc=r+dr,c+dc
                if 0<=nr<BOARD_SIZE and 0<=nc<BOARD_SIZE and board[nr,nc]==0:
                    candidates.add((nr,nc))

    for r,c in candidates:
        attack=score_point(board,r,c,2)
        defend=score_point(board,r,c,1)*1.2
        score=attack+defend
        if score>best_score:
            best_score=score
            best=(r,c)
    return best

st.title("🎮 五子棋 AI 挑戰版")

st.caption("玩家：⚫　AI：⚪")

c1,c2,c3,c4=st.columns(4)
with c1:
    st.metric("玩家", st.session_state.score["player"])
with c2:
    st.metric("AI", st.session_state.score["ai"])

with c3:
    if st.button("重新開始"):
        reset_board()
        st.rerun()

with c4:
    if st.button("全部重置"):
    
        st.session_state.clear()
    
        st.session_state.board = np.zeros(
            (BOARD_SIZE, BOARD_SIZE),
            dtype=int
        )
    
        st.session_state.turn = 1
        st.session_state.winner = None
    
        st.session_state.score = {
            "player": 0,
            "ai": 0
        }
    
        save_score(st.session_state.score)
    
        st.rerun()

if st.session_state.winner:
    st.success(st.session_state.winner)

board = st.session_state.board

if board.shape != (BOARD_SIZE, BOARD_SIZE):
    st.session_state.board = np.zeros(
        (BOARD_SIZE, BOARD_SIZE),
        dtype=int
    )
    st.rerun()

board = st.session_state.board

for r in range(BOARD_SIZE):
    cols=st.columns(BOARD_SIZE)
    for c in range(BOARD_SIZE):
        v=board[r,c]
        txt="·"
        if v==1: txt="⚫"
        elif v==2: txt="⚪"

        if cols[c].button(txt,key=f"{r}_{c}",disabled=(st.session_state.winner is not None)):
            if board[r,c]==0 and st.session_state.turn==1:
                board[r,c]=1

                if check_win(board,r,c,1):
                    st.session_state.score["player"]+=1
                    save_score(st.session_state.score)
                    st.session_state.winner="🎉 玩家獲勝"
                    st.rerun()

                move = ai_move()
                
                if move is not None:
                    ar, ac = move
                    board[ar, ac] = 2
                
                    if check_win(board, ar, ac, 2):
                        st.session_state.score["ai"] += 1
                        save_score(st.session_state.score)
                        st.session_state.winner = "🤖 AI獲勝"

                st.rerun()
