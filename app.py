import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Mental Health in Tech Survey",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_mental_health_survey.csv")

df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("🧠 Mental Health in Tech Survey Dashboard")

st.write(
    "An interactive dashboard exploring mental health treatment, "
    "workplace attitudes, and employer support among technology professionals."
)

st.divider()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Dashboard Filters")

country_options = ["All"] + sorted(df["Country"].unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", country_options)

gender_options = ["All"] + sorted(df["Gender"].unique().tolist())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

# -----------------------------
# KEY METRICS
# -----------------------------
st.subheader("📌 Key Metrics")

total_respondents = len(filtered_df)

if total_respondents > 0:
    treatment_rate = (
        filtered_df["treatment"].eq("Yes").mean() * 100
    )

    benefits_rate = (
        filtered_df["benefits"].eq("Yes").mean() * 100
    )

    average_age = filtered_df["Age"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Respondents", total_respondents)
    col2.metric("Treatment Rate", f"{treatment_rate:.1f}%")
    col3.metric("Employer Benefits", f"{benefits_rate:.1f}%")
    col4.metric("Average Age", f"{average_age:.1f}")

    st.divider()

    # -----------------------------
    # TREATMENT DISTRIBUTION
    # -----------------------------
    st.subheader("📊 Mental Health Treatment")

    treatment_counts = filtered_df["treatment"].value_counts()

    fig1, ax1 = plt.subplots()
    treatment_counts.plot(kind="bar", ax=ax1)

    ax1.set_title("Mental Health Treatment Distribution")
    ax1.set_xlabel("Sought Treatment")
    ax1.set_ylabel("Number of Respondents")
    ax1.tick_params(axis="x", rotation=0)

    st.pyplot(fig1)

    # -----------------------------
    # FAMILY HISTORY VS TREATMENT
    # -----------------------------
    st.subheader("👨‍👩‍👧 Family History vs Treatment")

    family_treatment = pd.crosstab(
        filtered_df["family_history"],
        filtered_df["treatment"]
    )

    fig2, ax2 = plt.subplots()
    family_treatment.plot(kind="bar", ax=ax2)

    ax2.set_title("Family History vs Mental Health Treatment")
    ax2.set_xlabel("Family History")
    ax2.set_ylabel("Number of Respondents")
    ax2.tick_params(axis="x", rotation=0)

    st.pyplot(fig2)

    # -----------------------------
    # WORK INTERFERENCE
    # -----------------------------
    st.subheader("💼 Mental Health and Work Interference")

    work_counts = filtered_df["work_interfere"].value_counts()

    fig3, ax3 = plt.subplots()
    work_counts.plot(kind="bar", ax=ax3)

    ax3.set_title("Frequency of Mental Health Interference at Work")
    ax3.set_xlabel("Work Interference")
    ax3.set_ylabel("Number of Respondents")
    ax3.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    st.pyplot(fig3)

    # -----------------------------
    # EMPLOYER BENEFITS
    # -----------------------------
    st.subheader("🏢 Employer Mental Health Benefits")

    benefits_counts = filtered_df["benefits"].value_counts()

    fig4, ax4 = plt.subplots()
    benefits_counts.plot(kind="bar", ax=ax4)

    ax4.set_title("Employer-Provided Mental Health Benefits")
    ax4.set_xlabel("Benefits Available")
    ax4.set_ylabel("Number of Respondents")
    ax4.tick_params(axis="x", rotation=0)

    st.pyplot(fig4)

    # -----------------------------
    # SUPERVISOR COMFORT
    # -----------------------------
    st.subheader("🗣️ Comfort Discussing Mental Health with Supervisors")

    supervisor_counts = filtered_df["supervisor"].value_counts()

    fig5, ax5 = plt.subplots()
    supervisor_counts.plot(kind="bar", ax=ax5)

    ax5.set_title("Willingness to Discuss Mental Health with Supervisor")
    ax5.set_xlabel("Response")
    ax5.set_ylabel("Number of Respondents")
    ax5.tick_params(axis="x", rotation=0)

    st.pyplot(fig5)

    # -----------------------------
    # AGE DISTRIBUTION
    # -----------------------------
    st.subheader("👥 Age Distribution")

    fig6, ax6 = plt.subplots()

    ax6.hist(filtered_df["Age"], bins=15, edgecolor="black")
    ax6.set_title("Age Distribution of Respondents")
    ax6.set_xlabel("Age")
    ax6.set_ylabel("Number of Respondents")

    st.pyplot(fig6)

    # -----------------------------
    # KEY INSIGHTS
    # -----------------------------
    st.divider()
    st.subheader("🔍 Key Insights")

    st.markdown("""
    - Approximately half of the survey respondents reported seeking mental health treatment.
    - Treatment-seeking was more common among respondents with a family history of mental illness.
    - Respondents reporting greater mental health interference at work were more likely to have sought treatment.
    - Employer-provided mental health benefits were associated with higher treatment-seeking rates.
    - Employees showed mixed levels of comfort discussing mental health issues with their supervisors.
    - Workplace awareness and accessibility of mental health support remain important areas for organizations.
    """)

else:
    st.warning("No respondents match the selected filters.")

st.divider()

st.caption(
    "Mental Health in Tech Survey | Exploratory Data Analysis & Streamlit Dashboard"
)
