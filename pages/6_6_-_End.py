import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("Midfielder Scouting App")
st.divider()

st.header("League and Team Rankings")
st.subheader("NWSL vs D1 Arkema")

a, b = st.columns(2)
a.image("images/globalrank.png")
b.image("images/teamratings.png")

st.write("Source: Opta/Opta Analyst")
st.divider()

st.image("images/table.png")
st.write("Source: SofaScore")

#region BUTTONS
st.divider()
footer = st.empty()

with footer.container():
    col1, col2 = st.columns([0.05, 0.95])

    with col1:
        back = st.button("<-", key="back")
        if back:
            switch_page("5 - Comparison")

    with col2:
        next = st.button("->", key="next")
        if next:
            switch_page("7 - Events")
#endregion 