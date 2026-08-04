import streamlit as st
from src.pipeline.voice_pipeline import process_bulk_audio
import pandas as pd
from datetime import datetime
from src.database.config import supabase
from src.database.db import save_logs
import time


@st.dialog("🎙️Voice Attendance")
def voice_dialog(selected_sub_id):
    st.markdown("""
<p>Record audio of students saying <b>'I am present'</b>.The AI will recognize enrolled voices.</p>
""",unsafe_allow_html=True)
    audio=st.audio_input("Record classroom audio")
    audio_bytes=audio.getvalue() if audio else None
    if 'attendance' not in st.session_state:
        st.session_state.attendance='report'

        
    if st.button("Analyze Voice Attendance",type="primary"):
        if audio_bytes:
            st.session_state.attendance='report'
        
    

            if st.session_state.attendance=='report':
                with st.spinner("Loading attendance report"):
                    candidate_dict={}
                    enrolled_res=supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_sub_id).execute()
                    enrolled_students=enrolled_res.data

                    for stu in enrolled_students:
                        student=stu["students"]
                        student_id=student["stu_id"]
                        voice_embed=student["voice_embedding"]
                        if voice_embed and student_id:
                           candidate_dict[student_id]=voice_embed

                    current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    identified_result=process_bulk_audio(audio_bytes,candidate_dict)
                    if identified_result is None:
                        identified_result={}

                    results,attendance_logs=[],[]

                    for stu in enrolled_students:
                        student=stu["students"]
                        is_present=False
                        score=None
                        for sid,match_score in identified_result.items():
                            if student["stu_id"]==sid:
                               is_present=True 
                               score=match_score  
                               break

                           

                        results.append({

                        "Name":student["stu_name"],
                        "ID":student["stu_id"],
                        "Score":score if score else "-",     
                        "Status":"✅️Present" if is_present else "❌️Absent"
                        })

                        attendance_logs.append({
                        "timestamp":current_timestamp,
                        "subject_id":selected_sub_id,
                        "student_id":student["stu_id"],
                        "is_present":is_present
                        })

                    if "voice_result" not in st.session_state:
                        st.session_state.voice_result=results
                    if "voice_logs" not in st.session_state:
                        st.session_state.voice_logs=attendance_logs   

        if not audio_bytes:
            st.error("Record your Audio")


    if "voice_result" in st.session_state:
        with st.spinner("Loading Attendance report"):
            results=st.session_state.voice_result
            st.dataframe(pd.DataFrame(results),hide_index=True)

        

        c1,c2=st.columns(2,gap="small")

        with c1:
            if st.button("Discard",width="stretch",type='tertiary'):
               del st.session_state.voice_result
               del st.session_state.voice_logs
               st.rerun()

        with c2:
            if st.button("Confirm & Save",width="stretch",type="primary"):
               logs=st.session_state.voice_logs
               if logs:
                    try:
                       save_logs(logs)
                       st.toast("Attendance Saved 🎉")
                       time.sleep(1)
                       del st.session_state.voice_result
                       del st.session_state.voice_logs
                       st.rerun()
                    except Exception as e:
                       st.error("Failed To Sync")   