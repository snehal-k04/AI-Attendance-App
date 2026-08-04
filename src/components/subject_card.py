import streamlit as st


def display_card(sub_code,sub_name,section,stats=None,footer_callback=None):
    html=f"""
      <div style="border:thick double #121413;margin-left:20px;padding-bottom:10px;background-color:white;border-radius:10px;">
      <h4>{sub_name}</h4>
      
      <p style="margin-left:10px;">Code:{sub_code}|Section:{section}</p>
      """
    if stats:
        for icon,label,value in stats:
            html+=f"""<span style="margin-left:20px;background-color:#E2E6EA;">{icon}{value}{label}</span>"""
    html+=f"""</div>"""


    st.markdown(html,unsafe_allow_html=True)


    if footer_callback:
        footer_callback()