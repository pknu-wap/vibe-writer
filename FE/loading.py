import time
import streamlit as st

button_col = st.columns([1, 2, 1])[1]
with button_col:
    start_button = st.button("Start", use_container_width=True)

progress_col = st.columns([1, 2, 1])[1]
progress_box = progress_col.empty()

spinner_col = st.columns([1, 2, 1])[1]

if start_button:
    progress_bar = progress_box.progress(0, text="0%")

    with spinner_col:
        with st.spinner("Loading", show_time=True):
            for step in range(100):
                time.sleep(0.03)
                percent = step + 1
                progress_bar.progress(percent, text=f"{percent}%")