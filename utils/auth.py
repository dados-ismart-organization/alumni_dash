
import streamlit as st
import time

def check_microsoft_login():
    """Autenticação via login da Microsoft e verificação do domínio."""
    # Verifica se o usuário está logado (isso vai depender da implementação do login que você usa)
    if not st.session_state.get("user_logged_in", False):  # Verifica se o usuário está logado
        st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold;'>🔐 Bem-vindo(a) ao Dashboard da Educação Básica</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 18px;'>Para acessar as informações, faça login com sua conta institucional.</div>", unsafe_allow_html=True)
        st.write("")
       
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.write("")
            st.button("🔓 Acessar com minha conta Microsoft",
                      on_click=login_microsoft,  # Função de login que você implementou
                      help="Clique para entrar com seu e-mail do Ismart",
                      use_container_width=True)
            st.write("")

        # Para simular o login, coloque um sleep ou outro método para impedir que o usuário continue enquanto não houver login
        st.stop()
 
    # Se o usuário estiver logado, então checa o email
    email_usuario = st.session_state.get("user_email", "")  # Recupera o email do usuário da sessão
 
    if not email_usuario.endswith("@ismart.org.br"):
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<div style='text-align: center; font-size: 20px; font-weight: bold;'>⛔ Acesso não autorizado</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 16px;'>Apenas usuários com e-mail institucional (@ismart.org.br) podem acessar este dashboard.</div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 14px;'>Caso precise de ajuda, entre em contato com o <b>time de dados</b>!</div>", unsafe_allow_html=True)
            st.write("")
            st.button("↩️ Tentar novamente", on_click=logout, use_container_width=True)
        st.stop()
 
    return True

def login_microsoft():
    """Função de login com a conta Microsoft."""
    # Este código precisa ser implementado de acordo com a biblioteca de autenticação que você está utilizando
    # Exemplo: St.auth ou integração com algum serviço de autenticação.
    # Após o login bem-sucedido, armazene os dados do usuário na sessão:
    
    st.session_state["user_logged_in"] = True
    st.session_state["user_email"] = "usuario@ismart.org.br"  # Simulando um login bem-sucedido
    
    st.success("Login bem-sucedido!")


def logout():
    """Realiza logout da conta Microsoft e limpa a sessão."""
    if st.session_state.get("user_logged_in", False):
        st.session_state["user_logged_in"] = False
        st.session_state.pop("user_email", None)
   
    # Limpa variáveis da sessão
    keys_to_remove = ["auth_success_shown", "autenticado"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
   
    st.toast("🔒 Você foi desconectado com sucesso!", icon="🔒")
    time.sleep(0.5)
