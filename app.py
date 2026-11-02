"""Streamlit front-end for the Student Pass/Fail Predictor.

Run:  streamlit run app.py
"""
import streamlit as st

from src.predict import load_model, predict

st.set_page_config(page_title="Student Pass Predictor", page_icon="🎓")


@st.cache_resource
def get_model():
    return load_model()


st.title("🎓 Student Pass / Fail Predictor")
st.write("A small ML demo (Logistic Regression) for the MLOps lab experiments.")

col1, col2 = st.columns(2)
with col1:
    study_hours = st.slider("Study hours per day", 0.0, 10.0, 4.0, 0.5)
    attendance = st.slider("Attendance (%)", 40, 100, 75)
with col2:
    previous_score = st.slider("Previous exam score", 20, 100, 60)
    extra_classes = st.radio("Attends extra classes?", ["yes", "no"], horizontal=True)

if st.button("Predict", type="primary"):
    label, prob = predict(get_model(), study_hours, attendance,
                          previous_score, extra_classes)
    if label == "Pass":
        st.success(f"Prediction: **{label}**  (probability of passing: {prob:.0%})")
    else:
        st.error(f"Prediction: **{label}**  (probability of passing: {prob:.0%})")
    st.progress(prob)

st.caption("Model version 1.1 – added by feature branch")
