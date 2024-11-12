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
def configurar_modelos (cliente, modelo, mensaje):
    return cliente.chat.completions.create(
        model = modelo,
        message = [{"role":"user", "content": mensaje}], 
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
          st.session_state.mensaje = [] #simula un historial


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

def actualizar_historial(rol,contenido,avatar):
    st.session_state.mensaje.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def actualizar_historial(rol,contenido,avatar):
    for mensaje in st.session_state.mensaje:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat ():         
    contenedordelchat = st.container (height= 4000, border = true)
    with contenedordelchat : mostrarhistorial()


elmodelo = configuracion_pagina()
st.write (f"seleccionaste  {elmodelo}") #imprime el dato en la pagina
cliente = crear_usuario_groq()
inicializar_estado()
mensaje = st.chat_input ("escribi tu solicitud")
#st.write (f"usuario: {mensaje }")

#
if mensaje:
    actualizar_historial ("user", mensaje, "🧑‍💻")
    chat_completo = configurar_modelos(cliente, modelo, mensaje) 
    actualizar_historial ("assistant", chat_completo, "🤖")
    print (mensaje)
