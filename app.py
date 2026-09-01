import pandas as pd
import plotly.express as px
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Page
st.set_page_config(page_title="Campus Placement", layout="wide")

st.title("Campus Placement Dashboard")

# 1. Load dataset
df = pd.read_csv("placement_data.csv")

# 2. Prepare data
df["is_placed"] = (df["status"] == "Placed").astype(int)

features = [
    "ssc_p", "hsc_p", "degree_p",
    "backlogs", "internships", "projects",
    "certifications", "coding_score",
    "communication_score"
]

X = df[features]
y = df["is_placed"]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 5. Evaluate model
accuracy = accuracy_score(
    y_test,
    model.predict(X_test)
)

# Filters
st.sidebar.header("Filters")

level = st.sidebar.multiselect(
    "Level",
    df["level"].unique(),
    default=df["level"].unique()
)

spec = st.sidebar.multiselect(
    "Specialisation",
    df["specialisation"].unique(),
    default=df["specialisation"].unique()
)

workex = st.sidebar.selectbox(
    "Work Experience",
    ["All", "Yes", "No"]
)

low, high = st.sidebar.slider(
    "Degree %",
    40.0, 100.0, (40.0, 100.0)
)

# Filter data
view = df[
    df["level"].isin(level) &
    df["specialisation"].isin(spec) &
    df["degree_p"].between(low, high)
]

if workex != "All":
    view = view[view["workex"] == workex]

# KPIs
c1, c2, c3, c4 = st.columns(4)

c1.metric("Students", len(view))
c2.metric("Placement Rate", f"{view['is_placed'].mean():.0%}")
c3.metric("Median Package",
          f"₹{view['salary_lpa'].median():.2f} LPA")
c4.metric("Model Accuracy", f"{accuracy:.0%}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["Placement", "Marks", "Predict", "Data"]
)

# Placement
with tab1:

    data = view.groupby("specialisation")["is_placed"].mean()
    data = data.reset_index()

    data["is_placed"] *= 100

    fig = px.bar(
        data,
        x="specialisation",
        y="is_placed",
        labels={"is_placed": "Placement Rate (%)"}
    )

    st.plotly_chart(fig, width="stretch")

# Marks
with tab2:

    fig = px.box(
        view,
        x="status",
        y="degree_p",
        color="status"
    )

    st.plotly_chart(fig, width="stretch")

# Prediction
with tab3:

    st.write("Enter Student Details")

    ssc = st.slider("10th %", 40.0, 100.0, 78.0)
    hsc = st.slider("12th %", 40.0, 100.0, 75.0)
    degree = st.slider("Degree %", 40.0, 100.0, 72.0)

    backlogs = st.number_input("Arrears", 0, 10, 0)
    internships = st.number_input("Internships", 0, 5, 1)
    projects = st.number_input("Projects", 0, 10, 3)
    certifications = st.number_input("Certifications", 0, 10, 2)

    coding = st.slider("Coding Score", 0, 100, 62)
    communication = st.slider("Communication", 1.0, 10.0, 6.5)

    if st.button("Predict"):

        student = [[
            ssc,
            hsc,
            degree,
            backlogs,
            internships,
            projects,
            certifications,
            coding,
            communication
        ]]

        probability = model.predict_proba(student)[0][1]

        st.metric(
            "Placement Chance",
            f"{probability:.0%}"
        )

# Data
with tab4:

    st.dataframe(
        view.drop(columns="is_placed"),
        width="stretch"
    )
    
    st.download_button(
        "Download CSV",
        view.drop(columns="is_placed").to_csv(index=False),
        "placement_filtered.csv"
    )