import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("Midfielder Scouting App")
st.divider() 

a, b, c=st.columns([0.01,1,0.01])
# Using B column to center image
b.image("images/cover.jpg", use_container_width=True)

#region BUTTONS
footer = st.empty()

with footer.container():
    col1, col2, col3 = st.columns([1, 45, 1])

    with col1:
        next = st.button("->", key="next")
        if next:
            switch_page("2 - Overview")
#endregion 