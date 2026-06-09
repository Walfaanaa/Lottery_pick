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

if "members" not in st.session_state:
    st.session_state.members = None


# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Load data
df = pd.read_csv(uploaded_file)

st.success("File loaded successfully!")

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# extra safety mapping
df.rename(columns={
    "memberid": "member_id",
    "member_id_": "member_id"
}, inplace=True)

st.subheader("📄 Data Preview")
st.dataframe(df)

st.write("📌 Columns Detected:", list(df.columns))


# =========================
# VALIDATION
# =========================
if "member_id" not in df.columns:
    st.error("❌ No 'member_id' column found in uploaded file.")
    st.stop()

members = df["member_id"].dropna().astype(str).tolist()

if len(members) == 0:
    st.error("❌ No valid member IDs found.")
    st.stop()

st.session_state.members = members


# =========================
# LOTTERY PANEL
# =========================
st.subheader("🎯 Lottery Draw Panel")

col1, col2 = st.columns(2)

with col1:
    st.write(f"👥 Total Members: **{len(members)}**")
    st.write(f"🏆 Winners Selected: **{len(st.session_state.winners)}**")

with col2:
    draw_btn = st.button("🎲 Draw Winner")


# =========================
# DRAW LOGIC (NO DUPLICATES)
# =========================
if draw_btn:
    remaining = list(set(members) - set(st.session_state.winners))

    if len(remaining) == 0:
        st.warning("⚠️ No more eligible members left!")
    else:
        winner = random.choice(remaining)
        st.session_state.winners.append(winner)

        st.success(f"🏆 Winner: {winner}")


# =========================
# WINNER HISTORY (UPDATED)
# =========================
st.subheader("📜 Winners History")

if len(st.session_state.winners) == 0:
    st.info("No winners yet.")
else:
    history_df = pd.DataFrame({
        "No": range(1, len(st.session_state.winners) + 1),
        "Lottery Number": st.session_state.winners
    })
    st.table(history_df)
