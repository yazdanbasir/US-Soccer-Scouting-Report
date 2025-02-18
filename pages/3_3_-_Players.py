import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide")
df = st.session_state.get("df", None)

st.title("Midfielder Scouting App")
st.divider()

#region Player Demographics
st.header("The Players")
# st.write("")

col1, col2, col3 = st.columns(3)

col1.subheader("Hal Hershfelt")
col1.image("images/hershfelt.jpg", use_container_width=True)

col2.subheader("Sam Coffey")
col2.image("images/coffey.jpg", use_container_width=True)

col3.subheader("Korbin Albert")
col3.image("images/albert.jpg", use_container_width=True)

demographics = pd.DataFrame({
    "Age": ["21", "26", "21"],
    "Team": ["Washington Spirit", "Portland Thorns", "Paris Saint Germain WFC"],
    "League": ["NWSL", "NWSL", "D1 Arkema"],
    "Appearances": ["28", "28", "29"],
    "USWNT Caps": ["3", "28", "22"],
})

demographics_transposed = demographics.T
# st.dataframe(demographics_transposed)
st.write("")
st.write("")
st.table(demographics_transposed)
#endregion Player Demographics

st.text("Sources: Official USWNT Roster, SofaScore")

#region BUTTONS
st.divider()
footer = st.empty()

with footer.container():
    col1, col2 = st.columns([0.05, 0.95])

    with col1:
        back = st.button("<-", key="back")
        if back:
            switch_page("2 - Overview")

    with col2:
        next = st.button("->", key="next")
        if next:
            switch_page("4 - Metrics")
#endregion 