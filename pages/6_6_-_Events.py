import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# st.title("PAGE IN PROGRESS!!")
# st.divider()
# st.header("Pitch Events (Mapped)")
# st.subheader("Defensive Actions")

a, b = st.columns(2)
a.image("images/globalrank.png")
b.image("images/teamratings.png")
#region BUTTONS
st.divider()
footer = st.empty()

with footer.container():
    col1, col2 = st.columns([0.05, 0.95])

    with col1:
        back = st.button("<-", key="back")
        if back:
            switch_page("5 - Comparison")
#endregion 