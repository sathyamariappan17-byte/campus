import streamlit as st
st.title("hellow students!!!have a great day ahead")
st.header("Dashboard Building")
st.subheader("Using Streamlit")
st.text("Today is a great day!!!")
st.markdown("### This is a markdown")
st.success("Success")
st.info("Information")
st.warning("Warning")
st.error("Error")
exp = ZeroDivisionError("Trying to divide by Zero")
st.exception(exp)
st.write("Text with write")
st.write(range(10))
st.write(list(range(10)))
from PIL import Image
img = Image.open("rabbit.jpg")
st.image(img, width=200)
if st.checkbox("Show/Hide"):
    st.text("Showing the widget")
status = st.radio("Select Gender:", ['Male', 'Female'])
if status == 'Male':
    st.success("Male")
else:
    st.success("Female")