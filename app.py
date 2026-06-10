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
# DATA SOURCE
# =========================
st.sidebar.header("📂 Data Source")

source = st.sidebar.radio(
    "Choose Source",
    ["Upload CSV", "GitHub CSV"]
)

df = None

# =========================
# OPTION 1: UPLOAD FILE
# =========================
if source == "Upload CSV":

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

# =========================
# OPTION 2: GITHUB FILE
# =========================
else:

    github_url = st.text_input(
        "GitHub Raw CSV URL",
        placeholder="https://raw.githubusercontent.com/user/repo/main/members.csv"
    )

    if github_url:
        try:
            df = pd.read_csv(github_url)
            st.success("✅ GitHub CSV loaded successfully!")
        except Exception as e:
            st.error(f"Failed to load GitHub file: {e}")

# =========================
# STOP IF NO DATA
# =========================
if df is None:
    st.info("Upload a CSV or provide a GitHub CSV URL.")
    st.stop()

# =========================
# CLEAN COLUMNS
# =========================
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

st.success("✅ Data Loaded")

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Data Preview")
st.dataframe(df, use_container_width=True)

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
        f"❌ Missing columns: {', '.join(missing_cols)}"
    )
    st.stop()

# =========================
# LOTTERY POOL
# =========================
lottery_pool = pd.concat([
    df["lottery_number_1"],
    df["lottery_number_2"]
]).dropna().tolist()

# =========================
# PANEL
# =========================
st.subheader("🎯 Lottery Draw Panel")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🎟️ Total Numbers",
        len(lottery_pool)
    )

    st.metric(
        "🏆 Winners",
        len(st.session_state.winners)
    )

with col2:
    draw_btn = st.button(
        "🎲 Draw Winner",
        use_container_width=True
    )

# =========================
# DRAW
# =========================
if draw_btn:

    used_numbers = [
        x["lottery_number"]
        for x in st.session_state.winners
    ]

    available_numbers = [
        x for x in lottery_pool
        if x not in used_numbers
    ]

    if not available_numbers:
        st.warning("⚠️ No numbers remaining.")
    else:

        winning_number = random.choice(
            available_numbers
        )

        winner_row = df[
            (df["lottery_number_1"] == winning_number) |
            (df["lottery_number_2"] == winning_number)
        ].iloc[0]

        winner_id = winner_row["member_id"]

        st.session_state.winners.append({
            "member_id": winner_id,
            "lottery_number": winning_number
        })

        st.balloons()

        st.success(
            f"🏆 Winner Member ID: {winner_id}"
        )

        st.info(
            f"🎟️ Winning Number: {winning_number}"
        )

# =========================
# HISTORY
# =========================
st.subheader("📜 Winners History")

if st.session_state.winners:

    history_df = pd.DataFrame(
        st.session_state.winners
    )

    history_df.insert(
        0,
        "No",
        range(1, len(history_df)+1)
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:
    st.info("No winners yet.")

# =========================
# RESET
# =========================
if st.button("🔄 Reset Draw History"):

    st.session_state.winners = []
    st.success("History Cleared")
    st.rerun()
