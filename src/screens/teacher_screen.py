import streamlit as st
import pandas as pd
from src.ui.base_layout import authenticate_layout
from src.components.header import login_header
from src.components.footer import footer_layout
from src.ui.base_layout import reg_layout,dash_layout

from src.database.db import check_teacher_exist,create_teacher,teacher_login,get_teacher_subjects

from src.database.db import attendance_records

from src.components.dialogue_subject import create_new_sub

from src.components.share_sub_dialogue import share_sub_dialogue

from src.components.subject_card import display_card


from src.components.add_photo_dialog import add_photos_dialog

from src.components.face_dialog import face_dialog

from src.components.voice_dialog import voice_dialog

from src.pipeline.face_pipeline import predict_attendance

from src.database.config import supabase
from datetime import datetime

import io
import numpy as np
from PIL import Image





def teacher_screen():
    if "teacher_data" in st.session_state:
        login_dashboard()

    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()



def login_teacher(username,password):
    if not username or not password:
        return False
    else:
        teacher=teacher_login(username,password)
        if teacher:
            st.session_state.user_role='teacher'
            st.session_state.teacher_data=teacher
            st.session_state.is_logged_in=True
            return True
        else:
            st.error("Inavalid username and password combo")
            return False
    

def login_dashboard():
    teacher_data=st.session_state.teacher_data
    dash_layout()
    col1,col2=st.columns(2,gap='large')

    with col1:
        login_header()

    with col2:
        st.subheader("𝐖𝐄𝐋𝐂𝐎𝐌𝐄 !")
        st.subheader(f"{teacher_data['name']}")
        if st.button("Logout",type='secondary',shortcut='control+backspace',width='stretch'):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
    
    
    st.divider()

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'
        
    tab1,tab2,tab3=st.columns(3,gap='small')

    with tab1:
        type1='primary' if st.session_state.current_teacher_tab=='take_attendance' else 'tertiary'
        if st.button("Take Attendance",width='stretch' ,type=type1,icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab='take_attendance'
            st.rerun()

    with tab2:
        type2='primary' if st.session_state.current_teacher_tab=='manage_subjects' else 'tertiary'
        if st.button("Manage Subjects",width='stretch' ,type=type2,icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab='manage_subjects'
            st.rerun()

    with tab3:
        type3='primary' if st.session_state.current_teacher_tab=='attendance_records' else 'tertiary'
        if st.button("Attendance Records",width='stretch' ,type=type3,icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab='attendance_records'
            st.rerun()

    if st.session_state.current_teacher_tab=='take_attendance':
        take_attendance_screen()
    elif st.session_state.current_teacher_tab=='manage_subjects':
        manage_subjects_screen()
    elif st.session_state.current_teacher_tab=='attendance_records':
        attendance_records_screen()

    footer_layout()


def take_attendance_screen():
    
    st.divider()
    st.markdown('<h4 style="font-size:220px;">Take Attendance</h4>',unsafe_allow_html=True)
    
    teacher_data=st.session_state.teacher_data
    teacher_id=teacher_data["teach_id"]
    subjects=get_teacher_subjects(teacher_id)
    if not subjects:
        st.info("You have not created any subjects yet!")
    total_subject={f"{s["sub_name"]}-{s['sub_code']}":s['sub_id'] for s in subjects}
    
    col1,col2=st.columns([3,1])

    with col1:
        subject=st.selectbox(label="Select Subject",options=list(total_subject.keys()),placeholder="select the subject for taking attendance")
        if subject:
           selected_sub_id=total_subject[subject]
        else:
            return
    with col2:
       
        if st.button("Add Photos",icon=":material/add_circle:",width="stretch"):
            add_photos_dialog()

    st.space()
    with st.spinner("Loading the selected photos"):
        student_snaps=st.session_state.get("test_photos",[])
        if student_snaps:
            st.markdown('<h4 style="font-size:220px;">Added Photos </h4>', unsafe_allow_html=True)

            cols=st.columns(4,gap="xxlarge")
            for i,snap in enumerate(student_snaps):
                with cols[i%4]:
                    st.image(snap,width=200,caption=f"Photo {i+1}")
        
    
    st.divider()

    b1,b2,b3=st.columns(3)

    with b1:
        if st.button("Clear all photos",width=250,type="tertiary",icon=":material/delete:"):
            del st.session_state.test_photos
            st.rerun()
            
    with b2:
        if st.button("Run Face Analysis",width=250,type="tertiary",icon=":material/analytics:"):
           test_photos=st.session_state.get("test_photos",[])
           if not test_photos:
                st.error("No photos selected!") 
           else:
            all_detected_id={}
            with st.spinner("Deep scanning classroom photos..."):
                    for i,img in enumerate(test_photos):
                        img_np=np.array(img.convert("RGB"))
                        detected,_,_=predict_attendance(img_np)


                        if detected:
                            for sid in detected.keys():
                                student_id=int(sid)
                                all_detected_id.setdefault(student_id,[]).append(f"photo{i+1}")
                                    
                    enrolled_res=supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_sub_id).execute()
                    enrolled_students=enrolled_res.data
                    if not enrolled_students:
                        st.warning("No students enrolled in this course")
                    else:
                        results,attendance_logs=[],[]

                        current_timestamp= datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                                
                        for node in enrolled_students:
                            stu_id=node["student_id"]
                            students=node["students"]
                                        

                            sources=all_detected_id.get(int(students["stu_id"]),[])
                            is_present=len(sources)>0

                            results.append({
                                "Name":students["stu_name"],
                                "ID":stu_id,
                                "Source":",".join(sources) if is_present else "-" ,
                                "Status":"✅️Present" if is_present else "❌️Absent"
                            })

                                        
                            attendance_logs.append({
                                "timestamp":current_timestamp,
                                "subject_id":selected_sub_id,
                                "student_id":stu_id,
                                "is_present":bool(is_present)
                            })

                        face_dialog(pd.DataFrame(results),attendance_logs)       
            
    with b3:
        if st.button("Use Voice Attendance",width=250,type="tertiary",icon=":material/settings_voice:"):
           voice_dialog(selected_sub_id)     
        

   
def manage_subjects_screen():
    st.divider()
    col1,col2=st.columns(2,gap="large")

    teacher_data=st.session_state.teacher_data
   

    with col1:
        st.markdown('<h4 style="font-size:220px;">Manage Subjects</h4>',unsafe_allow_html=True)

    with col2:
        if st.button("Create New Subject",type="secondary",width="stretch"):
            create_new_sub( teacher_data['teach_id'])
            
    st.space()
    subjects=get_teacher_subjects( teacher_data['teach_id'])
    if subjects:
       for sub in subjects:
            stats=[
                 ("👥","Students",sub["total_students"]),
                 ("📆","Classes held",sub["total_classes"])
                ]
            
            
            def share_btn():
                if st.button(f"Share Code:{sub["sub_name"]}",key=f"share_{sub["sub_code"]}",icon=":material/share:"):
                    share_sub_dialogue(sub["sub_name"],sub["sub_code"])
            
            display_card(
                sub_code=sub["sub_code"],
                sub_name=sub["sub_name"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("You have not created any subject yet, Create One!")   

def attendance_records_screen():
    st.divider()
    st.markdown('<h4 style="font-size:28px;">Attendance Records</h4>',unsafe_allow_html=True)

    with st.spinner("Loading attendance records"):
        teacher=st.session_state.teacher_data
        teacher_id=teacher["teach_id"]
        try:
            logs=attendance_records(teacher_id)
            if not logs:
               return

            data=[]
            for l in logs:
                ts=l.get("timestamp")

                data.append({
                    "ts_group":ts.split(".")[0]  if ts else None,
                    "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
                    "Subject":l["subjects"]["sub_name"],
                    "Subject Code":l["subjects"]["sub_code"],
                    "is_present":bool(l.get("is_present",False))
                })

            df=pd.DataFrame(data)    

            summary=(
                df.groupby(["ts_group","Time","Subject","Subject Code"])
                .agg(
                    Present_Count=("is_present","sum"),
                    Total_Count=("is_present","count")
                )).reset_index()

            summary["Attendance Stats"]=(
                "✅" + summary["Present_Count"].astype(str) + "/" + summary["Total_Count"].astype(str) + "Students Present"
            )

            display_df=pd.DataFrame(summary.sort_values(by="ts_group",ascending=False)
                                    [["Time","Subject","Subject Code","Attendance Stats"]])

            st.dataframe(display_df,hide_index=True,width='stretch')
              
        except Exception as e:
            st.error(f"error {e}")

        
def teacher_screen_login():
    authenticate_layout()
    
    col1,col2=st.columns(2)

    with col1:
       login_header()
    
    with col2:
        if st.button("Back to Home page",width="stretch",shortcut="control+backspace" ,type="secondary",icon=":material/arrow_back:",icon_position="left"):
           st.session_state['login_type']=None
           st.rerun()
    

    st.title("Login using password")


    username=st.text_input("Enter your username" ,placeholder="example@23")
    
    password=st.text_input("Enter password" ,placeholder="Enter password",type="password")

    st.markdown("""<hr>""",unsafe_allow_html=True)

    column1,column2=st.columns(2,gap="xlarge")

    with column1:
           
           if  st.button("Login",shortcut="Enter",icon=':material/login:',width="stretch",icon_position="right",type="secondary"):
               success=login_teacher(username,password)
               teacher=st.session_state.get("teacher_data")
               if success:
                    st.toast(f"✨𝓦𝓮𝓵𝓬𝓸𝓂𝓮✨ {teacher['name']}")
                    import time
                    time.sleep(2)
                    st.rerun()
                   

    with column2:
        if st.button("Register Instead",width="stretch",icon=":material/app_registration:",icon_position="right",type="tertiary"):
            st.session_state.teacher_login_type='register'
            st.rerun()
        
    
    footer_layout()

def register_teacher(username,name,password,confirm_password):
    if not username or not name or not password or not confirm_password:
        return False,"All fields are required"

    if password!=confirm_password:
        return False,"Password doesn't match"

    if check_teacher_exist(username):
        return False,"Username already exist"
    
    
    else:
        try:
            create_teacher(username,password,name)
            return True,"Successfully created! Login in now"
        
        except Exception as e:
             return False, "Unexpected error"
            
            

def teacher_screen_register():
    reg_layout()
    col1,col2=st.columns(2)

    with col1:
       login_header()
    
    with col2:
         if st.button("Back to Home page",shortcut="control+backspace" ,type="secondary",icon=":material/arrow_back:",icon_position="left"):
            st.session_state['login_type']=None
            st.rerun()



    st.title("Register your teacher profile")

    teacher_user=st.text_input("Enter your username" ,placeholder="example@23")

    teacher_name=st.text_input("Enter your name" ,placeholder="E.g:Dan Johnson")

    teacher_pass=st.text_input("Enter password" ,placeholder="Enter password",type="password")

    teacher_conf_pass=st.text_input("Confirm password" ,placeholder="confirm password",type="password")

    st.markdown("""<hr>""",unsafe_allow_html=True)

    but1,but2=st.columns(2,gap="xlarge")

    with but1:
        if st.button("Register Now",shortcut="Enter",width="stretch",type="primary",icon=':material/passkey:'):
            success,messege=register_teacher(teacher_user,teacher_name,teacher_pass,teacher_conf_pass)
            if success:
                st.success(messege)
                import time
                time.sleep(5)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(messege)
    with but2:
        if st.button("Login Instead",width="stretch",type="primary",icon=':material/passkey:'):
            st.session_state.teacher_login_type='login'
            st.rerun()


    footer_layout()


       
