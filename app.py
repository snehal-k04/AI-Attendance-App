import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.enroll_from_link import enroll_from_link


def login():
    st.set_page_config(
        page_title='TheAbsentee-Making Attendance faster using AI',
        page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2-alSeoTkg7ud9K9VvUq9NI6RUUOx9SQdDr_R0WXAng&s=10"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type']=None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            home_screen()


    join_code=st.query_params.get("join-code")
    if join_code:
        if st.session_state.login_type !='student':
           st.session_state.login_type='student'
           st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role')=='student':
            enroll_from_link(join_code)



       
login()



