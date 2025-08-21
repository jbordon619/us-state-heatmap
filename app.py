import streamlit as st
import plotly.express as px
from helper import load_and_validate

st.title("🇺🇸 U.S. State Heatmap Generator")
uploaded = st.file_uploader("Upload a CSV with a state column and a numeric value column", type="csv")

if uploaded:
    try:
        df = load_and_validate(uploaded)

        cscale = st.selectbox("Colour scale", ["Viridis", "Blues", "Reds", "Greens"])

        fig = px.choropleth(
            df,
            locations="state",  # 2-letter abbreviations
            locationmode="USA-states",
            color="value",
            scope="usa",
            color_continuous_scale=cscale,
            hover_name="state_raw",  # Full or raw user input
            hover_data={"value": True},
        )

        st.plotly_chart(fig, use_container_width=True)

        st.download_button("Download PNG", fig.to_image(format="png"), "heatmap.png")

    except Exception as e:
        st.error(str(e))
else:
    st.info("Awaiting CSV upload…")
