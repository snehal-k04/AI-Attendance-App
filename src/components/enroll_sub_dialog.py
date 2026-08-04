import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time


@st.dialog("Enroll to subject")
def enroll_sub():
    st.write("Enter the subject code provided by your teacher to enroll")
    join_code=st.text_input("Subject code",placeholder="e.g-CS101")
    
    if st.button("Enroll Now",width="content",key=f"enroll_{join_code}"):
        if join_code:
            res=supabase.table("subjects").select("sub_id","sub_code","sub_name").eq("sub_code",join_code).execute()
            if res.data:
                subject=res.data[0]
                student_id=st.session_state.student_data["stu_id"]

                check=supabase.table("subject_students").select("*").eq("subject_id",subject["sub_id"]).eq("student_id",student_id).execute()
                if check.data :
                    st.warning("You are already enrolled in this program")
                else:
                    try:
                       data=enroll_student_to_subject(student_id,subject["sub_id"])
                       if data:
                           st.toast("You are Successfully Enrolled 🎉")
                           time.sleep(2)
                           st.rerun()
                    except Exception as e:
                        st.error("Something went wrong!")

            else:
                st.error("Enter a valid subject code")
        else:
            st.warning("Please enter a subject code")


    
