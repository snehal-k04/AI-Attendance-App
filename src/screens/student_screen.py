import streamlit as st
from src.ui.base_layout import dash_layout,authenticate_layout
from src.components.header import login_header
import numpy as np
from PIL import Image
from src.components.footer import footer_layout

from src.pipeline.face_pipeline import predict_attendance,get_face_embedding,train_classifier


from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject

from src.pipeline.voice_pipeline import get_voice_embedding


from src.components.enroll_sub_dialog import enroll_sub

from src.components.subject_card import display_card




def login_dashboard():
    student_data=st.session_state.student_data
    student_id=student_data["stu_id"]


    dash_layout()
    col1,col2=st.columns(2,gap='large')

    with col1:
        login_header()

    with col2:
        st.subheader(f"Welcome {student_data['stu_name']}")
        if st.button("Logout",type='secondary',shortcut='control+backspace',width='stretch'):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data
            st.rerun()

    sec1,sec2=st.columns(2)

    with sec1:
        st.title("Your Enrolled Subjects")

    with sec2:
        if st.button("Enroll to subject",width="stretch",type="tertiary"):
            enroll_sub()
            
    st.divider()
    with st.spinner("Loading your enrolled subjects"):
        subjects=get_student_subjects(student_id)
        logs=get_student_attendance(student_id)

    stats_map={}

    for log in logs:
        sub_id=log["subject_id"]

        if sub_id not in stats_map:
            stats_map[sub_id]={"total":0,"attended":0}

        stats_map[sub_id]['total']+=1

        if log.get('is_present'):
            stats_map[sub_id]["attended"]+=1

            
    cols=st.columns(2)

    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sub_id=sub["sub_id"]
        stats=stats_map.get(sub_id,{"total":0,"attended":0})

        def unenroll_btn():
            if st.button("Unenroll from this course",width=200,type="tertiary",key=f"unenroll_{sub_id}"):
                unenroll_student_to_subject(student_id,sub_id)
        with cols[i%2]:
            display_card(
                sub["sub_code"],
                sub["sub_name"],
                sub["section"],
                stats=[("📅","Total classes",stats["total"]),("✅","Attended",stats["attended"])],
                footer_callback=unenroll_btn
                    )
                    
    footer_layout()
    
def  student_screen():
    
    if 'student_data' in st.session_state:
        login_dashboard()
        return


   
    authenticate_layout()
    
    col1,col2=st.columns(2,gap="large")

    with col1:
         login_header()

    
    with col2:
        button=st.button("Go to home page" ,type="secondary",shortcut="control+backspace")

        if button :
            st.session_state['login_type']=None
            st.rerun()
    
    st.title("Login with FaceID")


    photo_source=st.camera_input("Position your face in center",width=600)
    show_registration=False


    if photo_source:
        img=np.array(Image.open(photo_source))
        with st.spinner('AI is Scanning...'):
            detected_students,all_sub_id,num_faces=predict_attendance(img)

            if num_faces==0:
                st.error("Face not detected!")

            elif num_faces>1:
                st.error("Many faces found!")

            else:
                if detected_students:
                    sub_id=list(detected_students.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['stu_id']==sub_id ),None)
                    
                    st.session_state.user_role='student'
                    st.session_state.is_logged_in=True
                    st.session_state.student_data=student
                    st.rerun()

                else:
                    st.info("Face not found, You must be a new student!")
                    show_registration=True
                
                    if show_registration:
                        with st.container(border=True):
                            st.space()
                            st.title("Register new profile")
                            new_name=st.text_input("Enter your name",placeholder="E.g Akash Kumar")
                            st.divider()
                            st.subheader("Optional:Voice Enrollement")
                            st.info("Enroll your voice for voice only attendance")     

                            try:            
                                audio_data=st.audio_input("Record a short phrase like I am present,My name is akash")

                            except Exception as e:
                                st.error("Failed to detect audio") 
                                
                                
                            if st.button("Create Account",type="primary"):
                                audio_data=None
                                if new_name:
                                    with st.spinner("Creating account..."):

                                        img=np.array(Image.open(photo_source)) 
                                        encodings=get_face_embedding(img) 
                                        if encodings:
                                            face_embedding=encodings[0].tolist()

                                        voice_embedding=None
                                        if audio_data:
                                            voice_embedding=get_voice_embedding(audio_data.read())
                                        


                            
                                        response=create_student(new_name,face_embedding,voice_embedding)
                                        
                                        if response:
                                            train_classifier()
                                            st.session_state.user_role='student'
                                            st.session_state.is_logged_in=True
                                            st.session_state.student_data=response[0]
                                            st.toast(f"Profile created! Hi {new_name}")
                                            st.rerun()

    footer_layout()