import streamlit as st
import os
from PIL import Image

st.write('<h1 style="font-family: serif;"><i>The Infinity School</i></h1>', unsafe_allow_html=True)

st.markdown("""
    Que tal lembrar alguns momentos que a escola do infinito proporcionou esse ano?
    
    Tem de tudo um pouco Hallowen, Festa das cores e muita **aula**.
""")


st.divider()
st.markdown("""
    **Antes de tudo, alguns dos mestres que tive a honra de acompanhar ao longo desse ano**:
            
    - [Nator Junior](https://www.linkedin.com/in/nator-junior-carvalho-da-costa-77b13768/)  
    - [Andre Severo](https://www.linkedin.com/in/andre-severo-21a681209/)  
    - [Carlos Souza](https://www.linkedin.com/in/carlos-sousa-793b4526/)  
    - [Lynda Inês](https://www.linkedin.com/in/lyndainesaraujo/)  
    - [Káthia Rocha](https://www.linkedin.com/in/k%C3%A1thia-rocha-a8b7b61ba/)
""")
st.divider()

def resize_image(img):
    semana_tech = Image.open(f"./imgs/{img}")

    image_width, image_height = semana_tech.size

    image_resized = semana_tech.resize((int(image_width/2),int(image_height/2)))

    return image_resized

st.markdown("""
    #### Algumas das aulas que dei esse ano:
""")

img1 = resize_image("semana_tech.jpeg")

st.image(img1)

img2 = resize_image("aula.jpeg")
st.image(img2)

st.divider()

st.markdown("""
    #### Também teve muita monitoria!
""")

st.image("./imgs/monitoria.jpg")
st.divider()
st.header("Se liga em alguns dos eventos!!!")

videos = os.listdir("./videos")
videos = [i.replace('.mp4', "") for i in videos]
selected = st.selectbox("**Veja aqui alguns dos melhores momentos**", videos)

if selected != None:
    st.video(f"./videos/{selected}.mp4")

