import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.title("Midfielder Scouting App")
st.divider()
st.header("Pitch Events (Mapped)")
st.subheader("Defensive Actions")

st.image("images/bokeh.png")


#region BUTTONS
st.divider()
footer = st.empty()

with footer.container():
    col1, col2 = st.columns([0.05, 0.95])

    with col1:
        back = st.button("<-", key="back")
        if back:
            switch_page("6 - End")
#endregion 