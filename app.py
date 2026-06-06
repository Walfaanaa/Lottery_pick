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
# MEMBERS
# =========================

MEMBER_IDS = [
    1001, 1002, 1003, 1004, 1005,
    1006, 1007, 1008, 1009, 1010,
    1011, 1012, 1013, 1014, 1015,
    1016, 1017, 1018, 1019, 1020,
    1022, 1023, 1024, 1025, 1026
]

# =========================
# AUTO CREATE FILES
# =========================

if not os.path.exists(ASSIGNMENT_FILE):
    pd.DataFrame(columns=[
        "Member ID", "Lottery Number 1", "Lottery Number 2"
    ]).to_csv(ASSIGNMENT_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=[
        "Round", "Draw Date", "Winning Number", "Member ID"
    ]).to_csv(HISTORY_FILE, index=False)

# =========================
# TITLE
# =========================

st.title("🎟️ EGSA Lottery System (Stable Version)")

tab1, tab2, tab3 = st.tabs(["Assign Numbers", "Draw Lottery", "Round Control"])

# =========================
# TAB 1 - ASSIGN
# =========================

with tab1:

    st.subheader("Assign Lottery Numbers")

    assign_pass = st.text_input("Enter Assign Password", type="password")

    if assign_pass == PASSWORD_ASSIGN:

        df = pd.read_csv(ASSIGNMENT_FILE)

        if len(df) > 0 and "Lottery Number 1" in df.columns and df["Lottery Number 1"].notna().any():
            st.success("Lottery already assigned.")
            st.dataframe(df, use_container_width=True, hide_index=True)

        else:

            if st.button("Generate Numbers"):

                numbers = list(range(1, 51))
                random.shuffle(numbers)

                data = []

                for m in MEMBER_IDS:
                    data.append({
                        "Member ID": m,
                        "Lottery Number 1": numbers.pop(),
                        "Lottery Number 2": numbers.pop()
                    })

                df = pd.DataFrame(data)
                df.to_csv(ASSIGNMENT_FILE, index=False)

                st.success("Lottery numbers generated successfully!")
                st.dataframe(df, use_container_width=True, hide_index=True)

# =========================
# TAB 2 - DRAW (WITH DOWNLOAD)
# =========================

with tab2:

    st.subheader("🎯 Draw Lottery")

    draw_pass = st.text_input("Enter Draw Password", type="password")

    if draw_pass == PASSWORD_DRAW:

        df = pd.read_csv(ASSIGNMENT_FILE)
        history_df = pd.read_csv(HISTORY_FILE)

        if "Round" not in history_df.columns:
            history_df["Round"] = 0

        if st.button("Draw Winner"):

            if df.empty or "Lottery Number 1" not in df.columns:
                st.error("Please generate lottery first.")
            else:

                winning_number = random.randint(1, 50)

                winner = df[
                    (df["Lottery Number 1"] == winning_number) |
                    (df["Lottery Number 2"] == winning_number)
                ]

                if winner.empty:
                    st.error("No winner found.")
                else:
                    member_id = winner.iloc[0]["Member ID"]

                    st.success("🎉 Winner Selected")
                    st.metric("Winning Number", winning_number)
                    st.metric("Member ID", member_id)

                    if len(history_df) == 0:
                        round_no = 1
                    else:
                        round_no = int(history_df["Round"].max()) + 1

                    new_row = pd.DataFrame([{
                        "Round": round_no,
                        "Draw Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Winning Number": winning_number,
                        "Member ID": member_id
                    }])

                    history_df = pd.concat([history_df, new_row], ignore_index=True)
                    history_df.to_csv(HISTORY_FILE, index=False)

        # =========================
        # DOWNLOAD SECTION
        # =========================

        st.subheader("📥 Download CSV Files")

        assignment_df = pd.read_csv(ASSIGNMENT_FILE)
        history_df = pd.read_csv(HISTORY_FILE)

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="⬇️ Download Assignment CSV",
                data=assignment_df.to_csv(index=False).encode("utf-8"),
                file_name="lottery_assignment.csv",
                mime="text/csv"
            )

        with col2:
            st.download_button(
                label="⬇️ Download History CSV",
                data=history_df.to_csv(index=False).encode("utf-8"),
                file_name="lottery_history.csv",
                mime="text/csv"
            )

    elif draw_pass:
        st.error("Wrong Draw Password")

    st.subheader("📜 Draw History")
    st.dataframe(pd.read_csv(HISTORY_FILE), use_container_width=True, hide_index=True)

# =========================
# TAB 3 - RESET
# =========================

with tab3:

    st.subheader("🔄 Round Control")

    reset_pass = st.text_input("Enter Reset Password", type="password")

    if reset_pass == PASSWORD_RESET:

        if st.button("Start New Round"):

            empty_df = pd.DataFrame(columns=[
                "Member ID", "Lottery Number 1", "Lottery Number 2"
            ])
            empty_df.to_csv(ASSIGNMENT_FILE, index=False)

            st.success("New round started successfully!")
            st.info("History is preserved safely.")

    elif reset_pass:
        st.error("Wrong Reset Password")
