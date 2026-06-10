import streamlit as st
import pandas as pd
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EGSA Lottery System",
    page_icon="🎟️",
    layout="wide"
)

st.title("🎟️ EGSA Lottery System")

# =========================
# SESSION STATE
# =========================
if "winners" not in st.session_state:
    st.session_state.winners = []

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is None:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# =========================
# LOAD CSV
# =========================
df = pd.read_csv(uploaded_file)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

st.success("✅ File loaded successfully!")

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Data Preview")
st.dataframe(df)

st.write("📌 Columns Detected:")
st.write(list(df.columns))

# =========================
# VALIDATION
# =========================
required_columns = [
    "member_id",
    "lottery_number_1",
    "lottery_number_2"
]

missing_cols = [
    col for col in required_columns
    if col not in df.columns
]

if missing_cols:
    st.error(
        f"❌ Missing required columns: {', '.join(missing_cols)}"
    )
    st.stop()

# =========================
# CREATE LOTTERY POOL
# =========================
lottery_pool = pd.concat([
    df["lottery_number_1"],
    df["lottery_number_2"]
]).dropna().tolist()

total_numbers = len(lottery_pool)

# =========================
# LOTTERY PANEL
# =========================
st.subheader("🎯 Lottery Draw Panel")

col1, col2 = st.columns(2)

with col1:
    st.metric("🎟️ Total Lottery Numbers", total_numbers)
    st.metric("🏆 Winners Drawn", len(st.session_state.winners))

with col2:
    draw_btn = st.button(
        "🎲 Draw Winner",
        use_container_width=True
    )

# =========================
# DRAW LOGIC
# =========================
if draw_btn:

    used_numbers = [
        winner["lottery_number"]
        for winner in st.session_state.winners
    ]

    available_numbers = [
        num for num in lottery_pool
        if num not in used_numbers
    ]

    if len(available_numbers) == 0:
        st.warning("⚠️ No lottery numbers remaining!")
    else:

        # Randomly select ONE lottery number
        winning_number = random.choice(
            available_numbers
        )

        # Find member owning that number
        winner_row = df[
            (df["lottery_number_1"] == winning_number) |
            (df["lottery_number_2"] == winning_number)
        ].iloc[0]

        winner_member = winner_row["member_id"]

        # Save history
        st.session_state.winners.append({
            "member_id": winner_member,
            "lottery_number": winning_number
        })

        # Display result
        st.balloons()

        st.success(
            f"🏆 Winner Member ID: {winner_member}"
        )

        st.info(
            f"🎟️ Winning Lottery Number: {winning_number}"
        )

# =========================
# CURRENT WINNER
# =========================
if len(st.session_state.winners) > 0:

    latest = st.session_state.winners[-1]

    st.subheader("🥇 Latest Winner")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Member ID",
            latest["member_id"]
        )

    with c2:
        st.metric(
            "Winning Number",
            latest["lottery_number"]
        )

# =========================
# WINNERS HISTORY
# =========================
st.subheader("📜 Winners History")

if len(st.session_state.winners) == 0:
    st.info("No winners yet.")
else:

    history_df = pd.DataFrame(
        st.session_state.winners
    )

    history_df.insert(
        0,
        "No",
        range(1, len(history_df) + 1)
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

# =========================
# RESET BUTTON
# =========================
st.divider()

if st.button("🔄 Reset Draw History"):

    st.session_state.winners = []

    st.success(
        "Winner history cleared successfully!"
    )

    st.rerun()
