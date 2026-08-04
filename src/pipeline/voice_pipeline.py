from resemblyzer  import VoiceEncoder,preprocess_wav
import librosa
import io
import streamlit as st
import numpy as np



@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    
    try:
        encoder=load_voice_encoder()

        audio_file,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)

        norm_audio=preprocess_wav(audio_file)

        voice_embedding=encoder.embed_utterance(norm_audio)

        return voice_embedding.tolist()
    
    except Exception as e:
           st.error("voice Recognise error")
           return None
        

def identify_speaker(new_embedding,candidate_dict,threshold=0.50):

    #candidate_dict: {sid,voice_embed} for all_students
    if new_embedding is None or not candidate_dict:
      return None,0.0

    best_score=-1.0
    best_sid=None

    for sid,stored_embedding in candidate_dict.items():

        match_score=np.dot(stored_embedding,new_embedding)

        if match_score>=best_score:
            best_score=match_score
            best_sid=sid

    if best_score>=threshold:
        return best_sid,best_score

    return None,best_score


def process_bulk_audio(audio_bytes,candidate_dict,threshold=0.50):
    
    try:

        encoder=load_voice_encoder()
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments=librosa.effects.split(audio,top_db=30)

        identified_result={}
        for start,end in segments:
            if (end-start)<sr*0.5:
                continue
            segment=audio[start:end]
            audio_norm=preprocess_wav(segment)

            embedding=encoder.embed_utterance(audio_norm)

            sid,score=identify_speaker(embedding,candidate_dict,threshold)
            


            if sid not in identified_result or score>identified_result[sid]:
                identified_result[sid]=score

        return identified_result 
    except Exception as e:
        st.error(f"error {e}")
