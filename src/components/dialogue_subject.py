import streamlit as st 
from src.database.db import create_subject
import time



@st.dialog("📚Create New Subject")
def create_new_sub(teacher_id):
    sub_code=st.text_input("Enter Subject Code",placeholder="E.g :CS101")
    sub_name=st.text_input("Enter Subject Name",placeholder="E.g :Computer Science")
    section=st.text_input("Enter Section")


    if st.button("Creat Subject Now",width="content"):
        response=None
        if not sub_code or not sub_name or not section:
            st.warning("Please fill all the fiels!")

        else:
            try:
                sub_data=create_subject(sub_code,sub_name,teacher_id,section)
            except Exception as e:
                st.error(f"Error:{str(e)}")


            if sub_data:
                st.toast("Subject Created Successfully!")
                time.sleep(2)
                st.session_state.current_teacher_tab="manage_subjects"
                st.rerun()
