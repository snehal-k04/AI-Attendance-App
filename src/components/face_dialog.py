import streamlit as st
from src.database.db import save_logs


@st.dialog("📋Attendance Report")
def face_dialog(result,logs):
    st.text("Please review the detected attendance before confirming.Absent students are automatically marked as well.")
    st.dataframe(
    result, hide_index=True, width='stretch')


    c1,c2=st.columns(2,gap="small")

    with c1:
        if st.button("Discard",type="tertiary",width='stretch'):
            del st.session_state.test_photos
            st.rerun()
    with c2:
        if st.button("Confirm & Save",type="primary",width='stretch'):
            try:
               save_logs(logs)
               st.toast("Report Saved 🎉")
               import time
               time.sleep(1)
               del st.session_state.test_photos
               st.rerun()
            except Exception as e:
               st.error("Sync Failed")