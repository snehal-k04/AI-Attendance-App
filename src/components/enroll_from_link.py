import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_sub
import time

@st.dialog("Quick Enrollement")
def enroll_from_link(code):
    response=supabase.table("subjects").select("*").eq("sub_code",code).execute()
    if not response.data:
        st.error("Subject not Found!")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return
    subject=response.data[0]
    sub_id=subject["sub_id"]
    student_data=st.session_state.student_data
    student_id=student_data["stu_id"]
    check=supabase.table("subject_students").select("*").eq("student_id",student_id).eq("subject_id",sub_id).execute()
    if check.data:
        st.info("You are already enrolled")
        if st.button("Got it!"):
            st.query_params.clear()
            st.rerun()
        return
    
    st.markdown(f"Would you like to enroll in {subject["sub_name"]}")

    col1,col2=st.columns(2,gap="medium")
    
    with col1:
        if st.button("No thanks"):
            st.query_params.clear()
            st.rerun()
    
    with col2:
        if st.button("Yes, Enroll Now!"):
            enroll_student_sub(sub_id,student_id)
            st.success("Joined successfully 🎉")
            time.sleep(1)
            st.query_params.clear()
            st.rerun()