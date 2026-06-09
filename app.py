import streamlit as st
import pandas as pd
import random
from datetime import datetime

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
    st.session_state.members = []
    
if "loaded" not in st.session_state:
    st.session_state.loaded = False


# =========================
# UPLOAD FILE (ONLY SOURCE)
# =========================
uploaded_file = st.file_uploader(
    "📥 Drag & Drop CSV File Here",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("✅ File loaded successfully!")

    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df)

    # =========================
    # VALIDATION
    # =========================
    if "member_id" not in df.columns:
        st.error("❌ CSV must contain 'member_id' column.")
        st.stop()

    # IMPORTANT: keep exact values (NO GENERATION)
    members = df["member_id"].dropna().astype(str).tolist()

    if len(members) == 0:
        st.error("❌ No valid members found.")
        st.stop()

    st.session_state.members = members
    st.session_state.loaded = True


# Stop if no file
if not st.session_state.loaded:
    st.warning("Please upload a CSV file to continue.")
    st.stop()


# =========================
# LOTTERY PANEL
# =========================
st.subheader("🎯 Lottery Draw Panel")

remaining = list(set(st.session_state.members) - set(st.session_state.winners))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Members", len(st.session_state.members))

with col2:
    st.metric("🏆 Winners", len(st.session_state.winners))

with col3:
    st.metric("🎯 Remaining", len(remaining))


draw_btn = st.button("🎲 Draw Winner", use_container_width=True)


# =========================
# DRAW LOGIC (NO DUPLICATES)
# =========================
if draw_btn:
    if len(remaining) == 0:
        st.warning("⚠️ No more eligible members left!")
    else:
        winner = random.choice(remaining)

        st.session_state.winners.append(winner)

        st.success(f"🏆 Winner Selected: {winner}")


# =========================
# WINNER HISTORY
# =========================
st.subheader("📜 Winners History")

if st.session_state.winners:
    history_df = pd.DataFrame({
        "No": list(range(1, len(st.session_state.winners) + 1)),
        "Winner ID": st.session_state.winners,
        "Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(st.session_state.winners)
    })

    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No winners yet.")
