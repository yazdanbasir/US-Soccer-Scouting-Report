import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

# st.set_page_config(layout="wide")
df = st.session_state.get("df", None)

st.title("Midfielder Scouting App")
st.divider()
st.header("Dataset Overview")

df = pd.read_csv("cdm_data.csv")
columnsToShade = df.columns[6:]
highlight_max_props = "background-color: rgba(144, 238, 144, 0.4);"
highlight_min_props = "background-color: rgba(240, 128, 128, 0.4);"
shadedDF = df.style.highlight_max(props=highlight_max_props, subset=columnsToShade, axis=0)\
                    .highlight_min(props=highlight_min_props, subset=columnsToShade, axis=0)
st.dataframe(shadedDF)

# # Assign color based on which value it is
# def shades(val, maxValue, minValue):
#     if val == maxValue:
#         return "background-color: rgba(144, 238, 144,0.4);"  
#     elif val == minValue:
#         return "background-color: rgba(240, 128, 128,0.4);"
#     else:
#         return "background-color: rgba(255, 255, 0,0.5);"

# shadedDF = df.style.apply(
#     lambda col: [shades(val, col.max(), col.min()) for val in col],
#     subset=columnsToShade
# )

# st.dataframe(shadedDF)

#region BUTTONS
st.divider()
footer = st.empty()

with footer.container():
    col1, col2 = st.columns([0.05, 0.95])

    with col1:
        back = st.button("<-", key="back")
        if back:
            switch_page("1 - Home")

    with col2:
        next = st.button("->", key="next")
        if next:
            switch_page("3 - Players")
#endregion 