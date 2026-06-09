import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="EGSA Lottery System",
    page_icon="🎟️",
    layout="wide"
)

# =========================
# PASSWORDS
# =========================

PASSWORD_ASSIGN = "EGSA_ASSIGN_2026"
PASSWORD_DRAW = "EGSA_DRAW_2026"
PASSWORD_RESET = "EGSA_RESET_2026"

# =========================
# FILES
# =========================

ASSIGNMENT_FILE = "lottery_assignment.csv"
HISTORY_FILE = "lottery_history.csv"

# =========================
# INIT FILES
# =========================

if not os.path.exists(ASSIGNMENT_FILE):
    pd.DataFrame(columns=["Member ID", "Lottery Number 1", "Lottery Number 2"]).to_csv(
        ASSIGNMENT_FILE, index=False
    )

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["Round", "Draw Date", "Winning Number", "Member ID"]).to_csv(
        HISTORY_FILE, index=False
    )

# =========================
# UPLOAD SECTION
# =========================

st.sidebar.header("📂 Member Upload")

uploaded_file = st.sidebar.file_uploader("Upload Member CSV", type=["csv"])

MEMBER_IDS = []
DATA_SOURCE = "generate"

if uploaded_file is not None:

    member_df = pd.read_csv(uploaded_file)

    if "Member ID" not in member_df.columns:
        st.error("CSV must contain 'Member ID' column")
        st.stop()

    MEMBER_IDS = member_df["Member ID"].dropna().tolist()
    DATA_SOURCE = "upload"

    st.sidebar.success(f"{len(MEMBER_IDS)} members loaded.")

# =========================
# AUTO MODE IF NO UPLOAD
# =========================

if DATA_SOURCE == "generate" and len(MEMBER_IDS) == 0:
    MEMBER_IDS = [f"AUTO_{i}" for i in range(1, 11)]

# =========================
# LOTTERY GENERATOR FUNCTION
# =========================

def generate_lottery(member_ids):
    total_numbers = len(member_ids) * 2
    numbers = list(range(1, total_numbers + 1))
    random.shuffle(numbers)

    data = []

    for m in member_ids:
        data.append({
            "Member ID": m,
            "Lottery Number 1": numbers.pop(),
            "Lottery Number 2": numbers.pop()
        })

    return pd.DataFrame(data)

# =========================
# TITLE
# =========================

st.title("🎟️ EGSA Lottery System (FIXED AUTO VERSION)")

tab1, tab2, tab3 = st.tabs(["Assign Numbers", "Draw Lottery", "Round Control"])

# =========================
# TAB 1 - ASSIGN (AUTO FIXED)
# =========================

with tab1:

    st.subheader("Assign Lottery Numbers")

    assign_pass = st.text_input("Enter Assign Password", type="password")

    if assign_pass == PASSWORD_ASSIGN:

        df = pd.read_csv(ASSIGNMENT_FILE)

        already_assigned = (
            len(df) > 0
            and "Lottery Number 1" in df.columns
            and df["Lottery Number 1"].notna().any()
        )

        if already_assigned:
            st.success("Lottery already assigned.")
            st.dataframe(df, use_container_width=True, hide_index=True)

        else:

            if len(MEMBER_IDS) == 0:
                st.warning("No members found.")
                st.stop()

            # =========================
            # AUTO ASSIGN (NO BUTTON NEEDED)
            # =========================

            st.info("Generating lottery automatically...")

            df = generate_lottery(MEMBER_IDS)

            df.to_csv(ASSIGNMENT_FILE, index=False)

            st.success("Lottery assigned successfully!")

            st.dataframe(df, use_container_width=True, hide_index=True)

# =========================
# TAB 2 - DRAW
# =========================

with tab2:

    st.subheader("🎯 Draw Lottery")

    draw_pass = st.text_input("Enter Draw Password", type="password")

    if draw_pass == PASSWORD_DRAW:

        df = pd.read_csv(ASSIGNMENT_FILE)
        history_df = pd.read_csv(HISTORY_FILE)

        if df.empty:

            st.error("No lottery assigned yet. Upload CSV or generate first.")
            st.stop()

        if st.button("Draw Winner"):

            max_number = int(
                max(df["Lottery Number 1"].max(), df["Lottery Number 2"].max())
            )

            winning_number = random.randint(1, max_number)

            winner = df[
                (df["Lottery Number 1"] == winning_number)
                | (df["Lottery Number 2"] == winning_number)
            ]

            if winner.empty:
                st.error("No winner found.")
            else:

                member_id = winner.iloc[0]["Member ID"]

                st.success("🎉 Winner Selected")
                st.metric("Winning Number", winning_number)
                st.metric("Member ID", member_id)

                round_no = 1 if len(history_df) == 0 else int(history_df["Round"].max()) + 1

                new_row = pd.DataFrame([{
                    "Round": round_no,
                    "Draw Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Winning Number": winning_number,
                    "Member ID": member_id
                }])

                history_df = pd.concat([history_df, new_row], ignore_index=True)
                history_df.to_csv(HISTORY_FILE, index=False)

        st.subheader("📜 Draw History")

        st.dataframe(history_df, use_container_width=True, hide_index=True)

# =========================
# TAB 3 - RESET
# =========================

with tab3:

    st.subheader("🔄 Round Control")

    reset_pass = st.text_input("Enter Reset Password", type="password")

    if reset_pass == PASSWORD_RESET:

        if st.button("Start New Round"):

            empty_df = pd.DataFrame(columns=[
                "Member ID",
                "Lottery Number 1",
                "Lottery Number 2"
            ])

            empty_df.to_csv(ASSIGNMENT_FILE, index=False)

            st.success("New round started successfully!")
            st.info("History preserved.")

    elif reset_pass:
        st.error("Wrong Reset Password")
