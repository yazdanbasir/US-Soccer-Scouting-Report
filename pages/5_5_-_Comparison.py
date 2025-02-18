import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from mplsoccer import PyPizza, FontManager
import matplotlib.pyplot as plt
import pandas as pd

st.title("Midfielder Scouting App")
st.divider()
st.header("Performance Metrics (Compared)")
st.subheader("Percentile Rank vs NWSL #6s in 2024")

#region RADAR CHART 
df = pd.read_csv("cdm_data.csv")

font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Italic.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab[wght].ttf')

options = ["Hal Hershfelt", "Sam Coffey", "Korbin Albert"]
defaultSelection = ["Hal Hershfelt"]
# selection = st.pills("Players", options, default=defaultSelection, selection_mode="multi")
selection = st.segmented_control("Players", options, default=defaultSelection, selection_mode="multi")

@st.cache_resource(show_spinner=False)
def generate_chart(selection):
    playerIndexes = {
        "Hal Hershfelt": 0,
        "Sam Coffey": 1,
        "Korbin Albert": 2
    }
    playerColors = {
        "Hal Hershfelt": {"slice": "#FFB300", "text": "#000000"},  # Darker Yellow with Black text
        "Sam Coffey":    {"slice": "#d43e3e", "text": "#FFFFFF"},  # Darker Red with White text
        "Korbin Albert": {"slice": "#0052cc", "text": "#FFFFFF"}   # Blue with White text
    }
    # teams = {
    #     "Hal Hershfelt": "Washington Spirit",
    #     "Sam Coffey": "Portland Thorns",
    #     "Korbin Albert": "PSG WFC"
    # }
    params = [
        "Progessive Passes",
        "Final Third Entry Passes",
        "Pass Completion Under Pressure",
        "Shot Assist (Open Play)",
        "Progressive Carries",
        "Pressures Applied",
        "Tackes Made",
        "Tackles Won %"
    ]
    
    selected_values = []
    for player in selection:
        idx = playerIndexes[player]
        vals = [
            df["progressive_pass_percentile"].iloc[idx],
            df["final_third_entry_pass_percentile"].iloc[idx],
            df["pass_completion_under_pressure_percentile"].iloc[idx],
            df["shot_assist_op_percentile"].iloc[idx],
            df["progressive_carries_percentile"].iloc[idx],
            df["pressure_applied_percentile"].iloc[idx],
            df["tackles_made_percentile"].iloc[idx],
            df["tackle_win_percentage_percentile"].iloc[idx]
        ]
        selected_values.append(vals)
    mainValues = selected_values[0]
    
    #PyPizza with dark theme settings.
    baker = PyPizza(
        params=params,
        background_color="#0f1117",
        straight_line_color="#000000",
        straight_line_lw=1,
        last_circle_color="#000000",
        last_circle_lw=1,
        other_circle_lw=0,
        inner_circle_size=20
    )
    
    # Common styling.
    kwargs_slices = dict(edgecolor="#000000", zorder=2, linewidth=1)
    kwargs_params = dict(color="#F2F2F2", fontsize=11, fontproperties=font_normal.prop, va="center")
    kwargs_values = dict(
        color="#F2F2F2", fontsize=11,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(edgecolor="#000000", facecolor="cornflowerblue", boxstyle="round,pad=0.2", lw=1)
    )
    
    # Create the figure based on the number of players.
    if len(selection) == 1:
        # Single player: use that player's constant color for all slices.
        player = selection[0]
        sliceColor = playerColors[player]["slice"]
        textColor = playerColors[player]["text"]
        singleSliceColors = [sliceColor] * len(params)
        singleTextColors = [textColor] * len(params)
        
        fig, ax = baker.make_pizza(
            mainValues,
            figsize=(8, 8.5),
            color_blank_space="same",
            slice_colors=singleSliceColors,
            value_colors=singleTextColors,
            value_bck_colors=singleSliceColors,
            blank_alpha=0.4,
            kwargs_slices=kwargs_slices,
            kwargs_params=kwargs_params,
            kwargs_values=kwargs_values
        )
    
    elif len(selection) == 2:
        # Two players: each series uses its player's constant color.
        mainPlayer = selection[0]
        comparePlayer = selection[1]
        mainColor = playerColors[mainPlayer]["slice"]
        comparisonColor = playerColors[comparePlayer]["slice"]
        twoMainSliceColors = [mainColor] * len(params)
        
        mainValues_kwargs = dict(
            color=playerColors[mainPlayer]["text"], fontsize=11, fontproperties=font_normal.prop, zorder=3,
            bbox=dict(edgecolor="#000000", facecolor=mainColor, boxstyle="round,pad=0.2", lw=1)
        )
        compare_values_kwargs = dict(
            color=playerColors[comparePlayer]["text"], fontsize=11, fontproperties=font_normal.prop, zorder=3,
            bbox=dict(edgecolor="#000000", facecolor=comparisonColor, boxstyle="round,pad=0.2", lw=1)
        )
        compare_kwargs = dict(facecolor=comparisonColor, edgecolor="#000000", zorder=2, linewidth=1)
        
        fig, ax = baker.make_pizza(
            mainValues,
            compare_values=selected_values[1],
            figsize=(8, 8.5),
            color_blank_space="same",
            slice_colors=twoMainSliceColors,
            value_colors=[playerColors[mainPlayer]["text"]] * len(params),
            blank_alpha=0.4,
            kwargs_slices=kwargs_slices,
            kwargs_compare=compare_kwargs,
            kwargs_params=kwargs_params,
            kwargs_values=mainValues_kwargs,
            kwargs_compare_values=compare_values_kwargs
        )
        
        fig.text(
            0.47, 0.93,
            mainPlayer,
            size=14,
            ha="right",
            fontproperties=font_bold.prop,
            color=mainColor
        )
        fig.text(
            0.50, 0.93,
            "vs",
            size=14,
            ha="center",
            fontproperties=font_bold.prop,
            color="#F2F2F2"
        )
        fig.text(
            0.53, 0.93,
            comparePlayer,
            size=14,
            ha="left",
            fontproperties=font_bold.prop,
            color=comparisonColor
        )
    
    else:
        fig, ax = plt.subplots(figsize=(8, 8.5))
        ax.text(
            0.5, 0.5,
            "Please select 1 or 2 players to display the chart",
            ha="center",
            va="center",
            fontsize=14
        )
    return fig

if not selection:
    st.info("Please select 1 or 2 players to display the chart")
elif len(selection) > 2:
    st.info("Please select 1 or 2 players to display the chart")
else:
    # Convert selection to a tuple for caching
    sel_tuple = tuple(selection)
    fig = generate_chart(sel_tuple)
    st.pyplot(fig, use_container_width=True)
#endregion

#region BUTTONS
st.divider()
footer = st.empty()

with footer.container():
    col1, col2 = st.columns([0.05, 0.95])

    with col1:
        back = st.button("<-", key="back")
        if back:
            switch_page("4 - Metrics")

    with col2:
        next = st.button("->", key="next")
        if next:
            switch_page("6 - End")
#endregion 