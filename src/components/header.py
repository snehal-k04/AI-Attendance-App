import streamlit as st


def header_layout():
    st.image("src/ui/image.svg",width =78)
    
    st.markdown("""
        <h1 style="color:#0D0100">The<br>Absentee</h1>
    
        """,unsafe_allow_html=True)
    
    


def login_header():
    col1,col2=st.columns(2,gap="xxsmall")

    with col1:
        st.image("src/ui/image.svg",width=70)


    with col2:
        st.markdown("""
    <h2 style="color:#0D0100">The<br>Absentee</h2>

    """,unsafe_allow_html=True)

    st.space()