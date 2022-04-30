import streamlit as st
from pydub import AudioSegment, silence
import speech_recognition as sr
import os
recog=sr.Recognizer()
final_result=""
st.markdown("<h1 style='text-align: center;'>Audio To Text Converter</h1>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)
audio=st.file_uploader("Upload Your Audio File", type=['mp3', 'wav'])
if audio:
    st.audio(audio)
    audio_segment=AudioSegment.from_file(audio)
    chunks=silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS-20, keep_silence=100)
    for index,chunk in enumerate(chunks):
        chunk.export(str(index)+".wav", format="wav")
        with sr.AudioFile(str(index)+".wav") as source:
            recorded=recog.record(source)
            try:
                text=recog.recognize_google(recorded)
                final_result=final_result+" "+text
                print(text)
            except:
                print("None")
                final_result=final_result+" Unaudible"
    with st.form("Result"): 
        result=st.text_area("TEXT", value=final_result) 
        d_btn=st.form_submit_button("Download")    
        if d_btn:
            envir_var=os.environ
            usr_loc=envir_var.get('USERPROFILE')
            loc=usr_loc+"\Downloads\\transcript.txt"
            with open(loc, 'w') as file:
                file.write(result)
        