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
# SIDEBAR UPLOAD
# =========================

st.sidebar.header("📂 Member Upload")

uploaded_file = st.sidebar.file_uploader("Upload Member CSV", type=["csv"])

MEMBER_IDS = []

if uploaded_file is not None:

    df_upload = pd.read_csv(uploaded_file)

    if "Member ID" not in df_upload.columns:
        st.error("CSV must contain 'Member ID' column")
        st.stop()

    MEMBER_IDS = df_upload["Member ID"].dropna().astype(str).tolist()

    st.sidebar.success(f"{len(MEMBER_IDS)} members loaded.")

# ❗ STRICT MODE: NO FILE = STOP SYSTEM (NO GENERATION)
if uploaded_file is None:
    st.warning("Please upload a Member CSV file. No auto-generated data is allowed.")
    st.stop()

# =========================
# HELPER FUNCTION
# =========================

def generate_lottery(member_ids):

    total_numbers = len(member_ids) * 2
    numbers = list(range(1, total_numbers + 1))
    random.shuffle(numbers)

    data = []

    for m in member_ids:
        data.append({
            "Member ID": str(m),
            "Lottery Number 1": int(numbers.pop()),
            "Lottery Number 2": int(numbers.pop())
        })

    return pd.DataFrame(data)

# =========================
# TITLE
# =========================

st.title("🎟️ EGSA Lottery System (STRICT MODE - NO AUTO GENERATION)")

tab1, tab2, tab3 = st.tabs(["Assign Numbers", "Draw Lottery", "Round Control"])

# =========================
# TAB 1 - ASSIGN
# =========================

with tab1:

    st.subheader("Assign Lottery Numbers")

    assign_pass = st.text_input("Enter Assign Password", type="password")

    if assign_pass == PASSWORD_ASSIGN:

        df = pd.read_csv(ASSIGNMENT_FILE)

        already_assigned = (
            not df.empty
            and "Lottery Number 1" in df.columns
            and df["Lottery Number 1"].notna().any()
        )

        if already_assigned:
            st.success("Lottery already assigned.")
            st.dataframe(df, use_container_width=True, hide_index=True)

        else:

            if len(MEMBER_IDS) == 0:
                st.error("No members found in uploaded file.")
                st.stop()

            st.info("Assigning lottery numbers from uploaded file...")

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
            st.error("No lottery assigned yet.")
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

                member_id = str(winner.iloc[0]["Member ID"])

                st.success("🎉 Winner Selected")
                st.metric("Winning Number", int(winning_number))
                st.metric("Member ID", member_id)

                round_no = 1 if history_df.empty else int(history_df["Round"].max()) + 1

                new_row = pd.DataFrame([{
                    "Round": int(round_no),
                    "Draw Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Winning Number": int(winning_number),
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
            st.info("Assignment reset. No data was generated.")

    elif reset_pass:
        st.error("Wrong Reset Password")
