import streamlit as st
from groq import Groq


st.set_page_config(page_title="la superIA", page_icon="🤓") #titulo de la pag

st.title ("mi primer aplicacion usando streamlit")

nombre = st.text_input("cual es tu nombre")

if st.button("mandar un saludo"):
    st.write(f"hola {nombre}! gracias por acompañarnos el dia de hoy")


modelo = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#conectar a la api, creando un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq( api_key = clave_secreta)

#usuario = usuario de groq
def configurar_modelos (cliente, modelo, mensajedeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajedeEntrada}], 
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
          st.session_state.mensajes = [] #simula un historial


#? creando funcion con diseño de la pagina
def configuracion_pagina():
    st.title("la superIA")
    st.sidebar.title ("esta es una barra lateral")
    seleccion = st.sidebar.selectbox(
        "que modelo deseas utilizar",
        modelo,
        index = 0 #datodefecto
    )
    return seleccion #devuelve el dato

def generar_respuestas(chat_completo):
    respuesta_completa = "" #Texto vacio
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa 

def actualizar_historial(rol,contenido,avatar):
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])
            

def area_chat ():         
    contenedordelchat = st.container (height= 400, border = True)
    with contenedordelchat : mostrar_historial()

def main(): 
    elmodelo = configuracion_pagina()
    cliente = crear_usuario_groq()
    inicializar_estado()
    area_chat() 
    mensaje = st.chat_input ("escribi tu solicitud")

    if mensaje:
        actualizar_historial ("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelos(cliente, elmodelo, mensaje) 
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
            st.rerun()

                

if __name__ == "__main__":
    main()
