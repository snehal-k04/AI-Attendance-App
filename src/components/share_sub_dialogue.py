import streamlit as st
import segno
import io

@st.dialog("🔁Share subject link")
def share_sub_dialogue(sub_name,sub_code):
    url="http://localhost:8501"
    join_link=f"{url}/?join-code={sub_code}"

    qr=segno.make(join_link)
    st.header(f"For joining {sub_name}")
    st.space()
    qr_code=io.BytesIO()

    qr.save(qr_code,kind="png",border=1,scale=5)

    col1,col2=st.columns(2,gap="small")
    with col1:
        st.text("🔗Copy the following Link")
        st.code(join_link)
        st.text("OR Copy code below")
        st.code(sub_code)
        st.info("copy this code to share on whatsapp and email")

    with col2:
        st.text("⛶Scan to join")
        st.image(qr_code.getvalue(),caption="QRCODE for class joining",width="content")

        
