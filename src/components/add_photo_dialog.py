import streamlit as st
import io
from PIL import Image

@st.dialog("📸 Capture or Upload Photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")
   

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab='camera'

    col1,col2=st.columns(2,gap="small")

    with col1:
        ty1='primary' if st.session_state.photo_tab == "camera" else "tertiary"
        if st.button("📷 Camera",type=ty1,width="stretch"):
           st.session_state.photo_tab='camera'
           
           
    with col2:
        ty2='primary' if st.session_state.photo_tab=='upload' else 'tertiary'
        if st.button("📂 Upload",type=ty2,width="stretch"):
            st.session_state.photo_tab='upload'

    if 'test_photos' not in st.session_state:
        st.session_state.test_photos=[]
           
    if st.session_state.photo_tab=='camera':
        cam_photo=st.camera_input(label="Take a snapshot",key="dialog_cam",width=600)
        
        if cam_photo:
            st.session_state.test_photos.append(Image.open(cam_photo))
            st.toast("Photo Captured")
            st.rerun()

            
    if st.session_state.photo_tab=='upload':
        st.write("Choose image files")
        upload_photos=st.file_uploader("Upload images",accept_multiple_files=True,key="dialog_upload",type=["jpg","jpeg","png"]) 

        if upload_photos: 
            for photo in upload_photos:
                st.session_state.test_photos.append(Image.open(photo))
            st.toast("Photos uploaded successfully")
            st.rerun()

    st.divider()
    if st.button("Done",width="stretch"):
        st.rerun()