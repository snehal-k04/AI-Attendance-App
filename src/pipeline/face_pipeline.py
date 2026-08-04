import dlib
import streamlit as st
import face_recognition_models
from sklearn.svm import SVC
from src.database.db import get_all_students
import numpy as np

@st.cache_resource
def load_dlib_models():

    detector=dlib.get_frontal_face_detector()

    sp=dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())

    face_rec=dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())



    return detector,sp,face_rec

@st.cache_resource
def get_face_embedding(np_image):

    detector,sp,face_rec=load_dlib_models()

    faces=detector(np_image)

    encodings=[]
    
    for face in faces:
        shape=sp(np_image,face)

        face_descripter=face_rec.compute_face_descriptor(np_image,shape,1)

        encodings.append(np.array(face_descripter))

    return encodings    


@st.cache_resource
def get_trained_model():
    X=[]
    y=[]
    

    student_db=get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        stu_embedding=student.get('face_embedding')
        
        X.append(np.array(stu_embedding))
        y.append(student.get('stu_id'))

    if len(X)==0:
        return 0

    model=SVC(kernel='linear',class_weight='balanced',probability=True)

    try:
       model.fit(X,y)
    except ValueError:
        pass

    return {'clf':model,'X':X,'y':y}


# for new entry
def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    return bool(model_data)


def predict_attendance(np_image):
    embeddings=get_face_embedding(np_image)

    detected_student={}


    model_data=get_trained_model()

    if not model_data:
        return detected_student,[],len(embeddings)

    model=model_data['clf']
    X_train=model_data['X']
    y_train=model_data['y']

    X_train = np.array(model_data['X'])
    y_train = np.array(model_data['y'])

    all_sid=sorted(list(set(y_train)))
    threshold_dist=0.45
    for embedding in embeddings:
        embedding=np.array(embedding).reshape(1,-1)



        if len(all_sid)>1:
           predicted_id=int(model.predict(embedding)[0])
        else:
            predicted_id=int(all_sid[0]) if all_sid else None


        same_stu_id=(y_train==predicted_id)
        actual_embedding=X_train[same_stu_id]
    
       
        match_dist=np.linalg.norm(actual_embedding-embedding,axis=1)
        best_dist=match_dist.min()
        
        if best_dist<=threshold_dist:
            detected_student[predicted_id]=True


    return detected_student,all_sid,len(embeddings)
        
        
