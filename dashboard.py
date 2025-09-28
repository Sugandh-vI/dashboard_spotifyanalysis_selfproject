import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("spotify_churn_dataset.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Ensure churn column is numeric
if df['is_churned'].dtype == object:
    df['is_churned'] = df['is_churned'].map({"Yes": 1, "No": 0})

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.title("Spotify Churn Dashboard 🎵")

# Sidebar filters
st.sidebar.header("Filters")
countries = st.sidebar.multiselect("Select Country", options=df['country'].unique(), default=df['country'].unique())
genders = st.sidebar.multiselect("Select Gender", options=df['gender'].unique(), default=df['gender'].unique())
subscription_types = st.sidebar.multiselect("Select Subscription Type", options=df['subscription_type'].unique(), default=df['subscription_type'].unique())

# Apply filters
filtered_df = df[
    (df['country'].isin(countries)) &
    (df['gender'].isin(genders)) &
    (df['subscription_type'].isin(subscription_types))
]

st.write(f"Number of rows after filtering: {len(filtered_df)}")

# -------------------------------
# Summary Metrics
# -------------------------------
st.subheader("Summary Metrics")
if not filtered_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", len(filtered_df))
    col2.metric("Total Churned", filtered_df['is_churned'].sum())
    col3.metric("Average Listening Time (hrs)", round(filtered_df['listening_time'].mean(),2))
else:
    st.warning("No data available for the selected filters.")

# -------------------------------
# Churn rate by subscription type
# -------------------------------
if not filtered_df.empty:
    churn_rate_sub = filtered_df.groupby("subscription_type")["is_churned"].mean().reset_index()
    churn_rate_sub.rename(columns={"is_churned": "churn_rate"}, inplace=True)
    st.subheader("Churn Rate by Subscription Type")
    st.bar_chart(churn_rate_sub.set_index("subscription_type"))

# -------------------------------
# Churn rate by device type
# -------------------------------
if not filtered_df.empty:
    churn_rate_device = filtered_df.groupby("device_type")["is_churned"].mean().reset_index()
    churn_rate_device.rename(columns={"is_churned": "churn_rate"}, inplace=True)
    st.subheader("Churn Rate by Device Type")
    st.bar_chart(churn_rate_device.set_index("device_type"))

# -------------------------------
# Scatter plot: songs_played_per_day vs listening_time
# -------------------------------
if not filtered_df.empty:
    st.subheader("Songs Played per Day vs Listening Time")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=filtered_df,
        x="songs_played_per_day",
        y="listening_time",
        hue="is_churned",
        palette={0: "green", 1: "red"},
        alpha=0.7,
        ax=ax
    )
    ax.set_xlabel("Songs Played per Day")
    ax.set_ylabel("Listening Time (hours)")
    ax.legend(title="Churned", labels=["No", "Yes"])
    st.pyplot(fig)

# -------------------------------
# Scatter plot: skip_rate vs songs_played_per_day
# -------------------------------
if not filtered_df.empty:
    st.subheader("Skip Rate vs Songs Played per Day")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=filtered_df,
        x="songs_played_per_day",
        y="skip_rate",
        hue="is_churned",
        palette={0: "green", 1: "red"},
        alpha=0.7,
        ax=ax
    )
    ax.set_xlabel("Songs Played per Day")
    ax.set_ylabel("Skip Rate")
    ax.legend(title="Churned", labels=["No", "Yes"])
    st.pyplot(fig)

# -------------------------------
# Show raw data
# -------------------------------
st.subheader("Filtered Data")
st.dataframe(filtered_df)

