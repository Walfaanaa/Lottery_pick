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
# GITHUB DEFAULT FILE
# =========================
DEFAULT_GITHUB_CSV = (
    "https://raw.githubusercontent.com/"
    "Walfaanaa/Lottery_pick/main/"
    "lottery_assignment%20(1).csv"
)

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
    "Select Data Source",
    [
        "GitHub CSV",
        "Upload CSV"
    ]
)

df = None

# =========================
# GITHUB SOURCE
# =========================
if source == "GitHub CSV":

    github_url = st.sidebar.text_input(
        "GitHub Raw CSV URL",
        value=DEFAULT_GITHUB_CSV
    )

    try:
        df = pd.read_csv(github_url)

        st.success(
            "✅ Lottery data loaded from GitHub"
        )

    except Exception as e:
        st.error(
            f"❌ Unable to load GitHub file: {e}"
        )
        st.stop()

# =========================
# UPLOAD SOURCE
# =========================
else:

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            st.success(
                "✅ CSV uploaded successfully"
            )

        except Exception as e:
            st.error(
                f"❌ Error reading CSV: {e}"
            )
            st.stop()

    else:
        st.info(
            "Upload a CSV file to continue."
        )
        st.stop()

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# =========================
# VALIDATION
# =========================
required_columns = [
    "member_id",
    "lottery_number_1",
    "lottery_number_2"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "❌ Missing required columns:\n\n"
        + ", ".join(missing_columns)
    )

    st.write("Detected Columns:")
    st.write(list(df.columns))

    st.stop()

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Data Preview")

st.dataframe(
    df,
    use_container_width=True
)

# =========================
# CREATE LOTTERY POOL
# =========================
lottery_pool = pd.concat([
    df["lottery_number_1"],
    df["lottery_number_2"]
]).dropna().tolist()

# =========================
# DASHBOARD
# =========================
st.subheader("🎯 Lottery Draw Panel")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "👥 Members",
        len(df)
    )

with c2:
    st.metric(
        "🎟️ Lottery Numbers",
        len(lottery_pool)
    )

with c3:
    st.metric(
        "🏆 Winners Drawn",
        len(st.session_state.winners)
    )

# =========================
# DRAW BUTTON
# =========================
draw_btn = st.button(
    "🎲 DRAW WINNER",
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
        num
        for num in lottery_pool
        if num not in used_numbers
    ]

    if len(available_numbers) == 0:

        st.warning(
            "⚠️ No lottery numbers remaining."
        )

    else:

        # Select one random number
        winning_number = random.choice(
            available_numbers
        )

        # Match back to owner
        winner_row = df[
            (df["lottery_number_1"] == winning_number)
            |
            (df["lottery_number_2"] == winning_number)
        ].iloc[0]

        winner_id = winner_row["member_id"]

        st.session_state.winners.append({
            "member_id": winner_id,
            "lottery_number": winning_number
        })

        st.balloons()

        st.success(
            f"🏆 WINNER MEMBER ID: {winner_id}"
        )

        st.info(
            f"🎟️ WINNING LOTTERY NUMBER: {winning_number}"
        )

# =========================
# LATEST WINNER
# =========================
if len(st.session_state.winners) > 0:

    latest = st.session_state.winners[-1]

    st.subheader("🥇 Latest Winner")

    a, b = st.columns(2)

    with a:
        st.metric(
            "Member ID",
            latest["member_id"]
        )

    with b:
        st.metric(
            "Lottery Number",
            latest["lottery_number"]
        )

# =========================
# WINNER HISTORY
# =========================
st.subheader("📜 Winners History")

if len(st.session_state.winners) == 0:

    st.info(
        "No winners drawn yet."
    )

else:

    history_df = pd.DataFrame(
        st.session_state.winners
    )

    history_df.insert(
        0,
        "No",
        range(
            1,
            len(history_df) + 1
        )
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

# =========================
# DOWNLOAD HISTORY
# =========================
if len(st.session_state.winners) > 0:

    csv = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Winners History",
        csv,
        "winners_history.csv",
        "text/csv"
    )

# =========================
# RESET
# =========================
st.divider()

if st.button(
    "🔄 Reset Draw History"
):

    st.session_state.winners = []

    st.success(
        "✅ Winner history cleared."
    )

    st.rerun()
