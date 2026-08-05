import streamlit as st

def home_layout():

    st.markdown("""   
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400..800&family=Fredoka:wght@300..700&family=Work+Sans:ital,wght@0,100..900;1,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Croissant+One&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Viga&display=swap');                             

.stApp{
background-color:#E8E4F3 !important ;        
}

#MainMenu,header,footer{
visibility:hidden;
}
                
div[data-testid="stFullScreenFrame"] img {
    width: 150px !important;
    margin-left: 280px !important;
    margin-top:-25px !important;
}
           
.block-container{
padding:1.5rem ;
}    
                         
h1{
margin-top:-20px !important;
border:none !important;
padding-bottom:30px !important;
margin-left:20px !important;
text-align: center !important ;
color:#4A1942 !important;
font-family: "Viga", sans-serif !important;
font-style: normal !important; 
line-height:35px !important;
transform:scaleX(1.5) !important;
}
                
#teacher img, #student img {
    width: 1300px !important;
    height: 229px !important;
    object-fit: cover !important;
    border-radius: 10% !important;  
}

#student ,#teacher{
color:#0D0100 !important;
background-color:#D9E4F5 !important;
text-align:center !important;
height:280px !important;
border-radius:100px !important;
box-shadow: 10px 10px 30px #0D0100 !important;
} 
                
#student h3, #teacher h3 {
font-family: "Croissant One", serif !important;
}            

button[kind="primary"]{
margin-left:50px !important;
background-color:#E8613C !important;
font-weight:bold !important;
color:white !important;
transition:1s  ease-in-out !important;
border :none ! important;
margin-top:-15px !important;
font-family: "Nunito", sans-serif !important;
}
                
button[kind="primary"]:hover{
transform:scale(1.1) !important;
box-shadow: 5px 5px 20px black !important;

}

</style>
""",unsafe_allow_html=True)


def authenticate_layout():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gravitas+One&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Tilt+Prism&display=swap');
.stApp{           
    background-color:#D9E4F5 !important;

}
                
div[data-testid="stFullScreenFrame"] img {
    width: 120px !important;
    margin-left: 20px !important;
}
                
#MainMenu,header,footer{
visibility:hidden;
}
                
h1{
text-align:center !important;
margin-top:-50px !important;
margin-bottom:20px !important;}
                
button[kind="secondary"]{
background-color:#E90164 !important;
color:white  !important;
margin-top:30px !important;
border-radius:100px !important;
transition:1s  ease-in-out !important;
}
                              
button[kind="secondary"]:hover{
transform:scale(0.9) !important;
box-shadow: 5px 5px 20px #000000 !important;
}

button[kind="tertiary"]{
background-color:purple !important;
color:white !important;
margin-top:30px !important;
border-radius:100px !important;
transition:1s  ease-in-out !important;
}
                
button[kind="tertiary"]:hover{
transform:scale(0.9) !important;
box-shadow: 5px 5px 20px #000000 !important;
}
                

.block-container{
padding:1.5rem;
}
                
button[data-testid="stCameraInputButton"]{
background-color:blue !important;
color:white !important;
border-radius:100px !important;
transition:1s !important;
}
                
button[data-testid="stCameraInputButton"]:hover{
transform:scale(0.9) !important;
}
                
h2{
font-family: "Tilt Prism", sans-serif !important;
margin-right:-70px !important;
margin-left:-10px !important;
}

.foot{
color:red !important;
}
</style>
""",unsafe_allow_html=True)
    


    
def reg_layout():

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gravitas+One&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Tilt+Prism&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
.stApp{           
    background-color:#D9E4F5 !important;

}
                
div[data-testid="stFullScreenFrame"] img {
    width: 120px !important;
    margin-left: 20px !important;
}

h1{
text-align:center !important;
margin-top:-50px !important;
margin-bottom:20px !important;}
                
button[kind="primary"]{
background-color:#07998B !important;
color:black !important;

margin-top:30px !important;
border-radius:100px !important;
transition:1s  ease-in-out !important;

}
                               
button[kind="primary"]:hover{
transform:scale(0.9) !important;
box-shadow: 5px 5px 20px #D70564 !important;
} 

button[kind="secondary"]{
background-color:#E90164 !important;
color:black !important;
margin-top:30px !important;
border-radius:100px !important;
transition:1s  ease-in-out !important;
margin-left:20px !important;

}
                
button[kind="secondary"]:hover{
transform:scale(0.9) !important;
box-shadow: 5px 5px 20px #000000 !important;
}              

#MainMenu,header,footer{
visibility:hidden;
}

.block-container{
padding:1.5rem;
}
                
h2{
font-family: "Tilt Prism", sans-serif !important;
margin-right:-70px !important;
margin-left:-10px !important;
}
.foot{
color:red !important;
}
</style>
""",unsafe_allow_html=True)



def dash_layout():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Satisfy&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Tilt+Prism&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Work+Sans:ital,wght@0,100..900;1,100..900&display=swap');
.stApp{           
    background-color:#D9E4F5 !important

}             
.st-emotion-cache-uwwqev.e1xxut3m0 {
margin-left:80px !important;
}

.st-emotion-cache-13gev4o{
margin-left:-50px !important;
margin-top:10px !important;}
    
button[kind="primary"]{
background-color:#0235a3 !important;
color:white !important;
margin-top:40px !important;
border-radius:100px !important;
transition:1s  ease-in-out !important;

}
                

                
button[kind="tertiary"]{
background-color:#000000 !important;
color:white !important;
margin-top:40px !important;
border-radius:100px !important;
transition:1s  ease-in-out !important;

}
                
button[kind="tertiary"]:hover{
transform:scale(0.9) !important;
box-shadow: 5px 5px 20px #000000 !important;         
}
                
h1{
margin-left:100px !important;
font-size:30px !important;
line-height:1.5 !important;
font-family: "Racing Sans One", sans-serif !important;
} 
                                       
h3{
color:#3220ba !important;
font-family: "Satisfy", cursive !important;
font-size:35px !important;
margin-left:50px !important;
padding-bottom:0px !important;
padding-top:0px !important;
}
                
h4{
font-family: "Work Sans", sans-serif !important;
color:black !important;
font-size:30px !important;
margin-left:10px !important;
margin-top:10px !important;               
}
                
button[kind="secondary"]{
background-color:#E90164 !important;
color:black !important;
border-radius:100px !important;
transition:1s  ease-in-out !important;
margin-top:25px !important;
margin-left:5px !important;
margin-bottom:-30px !important;
}
                
button[kind="secondary"]:hover{
transform:scale(0.9) !important;
box-shadow: 5px 5px 20px #000000 !important;
}              

#MainMenu,header,footer{
visibility:hidden;
}

.block-container{
padding:1.5rem;
}
                
h2{
font-family: "Tilt Prism", sans-serif !important;

margin-right:-70px !important;
margin-left:-10px !important;}

div[data-testid="stFullScreenFrame"] img {
    width: 120px !important;
    margin-left: -5px !important;
}

.foot{
color:red !important;
}
</style>
""",unsafe_allow_html=True)


