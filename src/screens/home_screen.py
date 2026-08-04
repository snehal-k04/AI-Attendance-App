import streamlit as st
from src.ui.base_layout import home_layout
from src.components.footer import footer_layout
from src.components.header import header_layout

def home_screen():
    home_layout()
    header_layout()
    
    tea_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbZn-WkhIun0hLEFqtIv3GL2l3Qjzqit7zN0oCZW_9xw&s=10"
    stu_url="https://png.pngtree.com/png-clipart/20250209/original/pngtree-a-group-of-people-cute-style-cartoon-style-college-student-graduation-png-image_20399531.png"
    
    col1,col2=st.columns(2,gap="xxlarge")

    with col1:
        st.markdown(f"""<div id="student"><bold><h3>I'm <br> Student</h3></bold> <img src="{stu_url}"></div>""",unsafe_allow_html=True)
        if st.button("Student portal",type="primary" ,icon=':material/arrow_outward:',icon_position="right"):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.markdown(f"""<div id="teacher"><bold><h3>I'm <br> Teacher</h3></bold> <img src="{tea_url}"></div>""",unsafe_allow_html=True)
        if st.button("Teacher portal" ,type="primary",icon=':material/arrow_outward:',icon_position="right"):
            st.session_state['login_type']='teacher'
            st.rerun()


    footer_layout()