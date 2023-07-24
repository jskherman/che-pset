import datetime as dt

import altair as alt
import gspread
import pandas as pd
import streamlit as st

if not st.session_state["auth"]:
    st.error("&ensp; **You are unauthorized to see this page.** Please login.", icon="🔒")
    st.stop()

st.set_page_config(page_title="Analytics :: Problem Set Generator", page_icon="📊")