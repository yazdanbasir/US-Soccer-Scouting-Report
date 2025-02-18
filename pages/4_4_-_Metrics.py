import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

st.set_page_config(layout="wide")
st.title("Midfielder Scouting App")
st.divider()
st.header("Performance Metrics (Raw Values)")
st.subheader("Defensive and Offensive")

df = pd.read_csv("cdm_data.csv")

#region BAR NEW ----------------------------------------------------
playerColors = {
    "Hal Hershfelt": {"bar": "#FFB300", "text": "#FFFFFF"},
    "Samantha Coffey": {"bar": "#d43e3e", "text": "#FFFFFF"},
    "Korbin Albert": {"bar": "#0052cc", "text": "#FFFFFF"}
}

defensiveColumns = [
    "pressure_applied_per_90",
    "tackles_made_per_90",
    "tackle_win_percentage"
]

offensiveColumns = [
    "progressive_pass_per_90",
    "final_third_entry_pass_per_90",
    "pass_completion_under_pressure_per_90",
    "shot_assist_op_per_90",
    "progressive_carries_per_90"
]

allColumns = defensiveColumns + offensiveColumns

aliases = {
    "pressure_applied_per_90": "Pressures Applied /90",
    "tackles_made_per_90": "Tackles Made /90",
    "tackle_win_percentage": "Tackle Win %",
    "progressive_pass_per_90": "Progressive Passes /90",
    "final_third_entry_pass_per_90": "Final Third Entry Passes /90",
    "pass_completion_under_pressure_per_90": "Pass Completion Under Pressure /90",
    "shot_assist_op_per_90": "Shot Assists in Open Play /90",
    "progressive_carries_per_90": "Progressive Carries /90"
}

options = st.selectbox(
    "Which area would you like to visualize?",
    ("Defensive", "Offensive", "All"),
    index=0
)

if options == "Defensive":
    selectedColumns = defensiveColumns
elif options == "Offensive":
    selectedColumns = offensiveColumns
else:
    selectedColumns = allColumns

selectedAliases = [aliases[col] for col in selectedColumns]

selectedStats = st.pills(
    "Filter Individual Charts/Stats", 
    options=selectedAliases, 
    selection_mode="multi",
    default=selectedAliases
)

filtered_columns = [col for col, al in zip(selectedColumns, selectedAliases) if al in selectedStats]
filtered_aliases = [al for al in selectedAliases if al in selectedStats]

# Check if at least one stat is selected.
if not filtered_columns:
    st.info("Please select at least one stat to display the chart.")
else:
    players = df["player_name"].tolist()
    fig = make_subplots(
        rows=1, cols=len(filtered_columns), 
        shared_yaxes=False,  # Independent y-axes per chart
        horizontal_spacing=0.08  # Adjust spacing between subplots
    )

    # Add traces for each stat (chart) and for each player
    for i, (col, alias) in enumerate(zip(filtered_columns, filtered_aliases)):
        for player in players:
            stat_value = df[df["player_name"] == player][col].values[0]
            fig.add_trace(go.Bar(
                name=player,                    
                x=[alias],                      
                y=[stat_value],
                marker_color=playerColors[player]["bar"],
                text=[f'{stat_value:.2g}'],
                textposition="auto",
                textfont=dict(color=playerColors[player]["text"]),
                showlegend=(i == 0), # Only show the legend in the first subplot
                legendgroup=player # Group traces by player for unified filtering
            ), row=1, col=i+1)

    fig.update_layout(
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        width=250 * len(filtered_columns),  # Adjust width based on number of charts
        height=500,
    )

    st.plotly_chart(fig)
#endregion

#region METRICS ----------------------------------------------------
players = df["player_name"].tolist()

if not filtered_columns:
    st.info("Please select at least one stat to display the power scores.")
else:
    percentileColumnMap = {
        'pressure_applied_per_90': 'pressure_applied_percentile',
        'tackles_made_per_90': 'tackles_made_percentile',
        'tackle_win_percentage': 'tackle_win_percentage_percentile',
        'progressive_pass_per_90': 'progressive_pass_percentile',
        'final_third_entry_pass_per_90': 'final_third_entry_pass_percentile',
        'pass_completion_under_pressure_per_90': 'pass_completion_under_pressure_percentile',
        'shot_assist_op_per_90': 'shot_assist_op_percentile',
        'progressive_carries_per_90': 'progressive_carries_percentile'
    }

    # Initialize session state to store previous ratings
    if "previousRatings" not in st.session_state:
        st.session_state["previousRatings"] = {player: None for player in players}

    playerRatings = {}

    for player in players:
        percentileColumns = [percentileColumnMap[col] for col in selectedColumns if col in percentileColumnMap]
        numberOfPercentiles = len(percentileColumns)

        playerRow = df[df["player_name"].str.strip().str.lower() == player.strip().lower()]

        if playerRow.empty:
            raise ValueError(f"Player {player} not found in dataset!")

        playerData = playerRow.iloc[0]
        stats = [playerData[col] for col in percentileColumns]
        avgPercentile = sum(stats) / numberOfPercentiles
        playerRatings[player] = avgPercentile

    # Calculate deltas and update previousRatings in session state
    deltas = {}
    for player, currentValue in playerRatings.items():
        previousValue = st.session_state["previousRatings"].get(player)
        delta = 0 if previousValue is None else currentValue - previousValue
        deltas[player] = delta
        st.session_state["previousRatings"][player] = currentValue  # Update session state

    st.text("Power Scores calculated through total defensive and/or offensive metrics:")
    a, x, y, z, b = st.columns(5)

    x.metric("Hershfelt", value=f"{playerRatings.get('Hal Hershfelt', 0):.0f}", delta=f"{deltas.get('Hal Hershfelt', 0):+.0f}", border=True)
    y.metric("Coffey", value=f"{playerRatings.get('Samantha Coffey', 0):.0f}", delta=f"{deltas.get('Samantha Coffey', 0):+.0f}", border=True)
    z.metric("Albert", value=f"{playerRatings.get('Korbin Albert', 0):.0f}", delta=f"{deltas.get('Korbin Albert', 0):+.0f}", border=True)
#endregion

#region BUTTONS ----------------------------------------------------
st.divider()
footer = st.empty()

with footer.container():
    col1, col2 = st.columns([0.05, 0.95])

    with col1:
        back = st.button("<-", key="back")
        if back:
            switch_page("3 - Players")

    with col2:
        next = st.button("->", key="next")
        if next:
            switch_page("5 - Comparison")
#endregion 