import streamlit as st
import pywhatkit as kit
import pyautogui
import time

st.set_page_config(page_title="Painel WhatsApp", layout="centered")
st.title("📲 Painel de Envio no WhatsApp")

st.markdown("Cole os nomes e números no formato: `Nome | +55Número`")

entrada = st.text_area("📋 Lista de contatos", height=200, placeholder="Ex:\nJoão | +5511987654321\nMaria | +5592912345678")

mensagem_modelo = st.text_area("✏️ Mensagem personalizada (use {nome})", 
                               "Olá {nome}, tudo bem? 😄")

enviar = st.button("🚀 Enviar mensagens")

if enviar:
    if not entrada.strip():
        st.warning("⚠️ Nenhum contato informado.")
    else:
        linhas = entrada.strip().split('\n')
        resultados = []

        with st.spinner("Enviando mensagens... não feche o navegador e não mexa no teclado!"):
            for linha in linhas:
                try:
                    if '|' not in linha:
                        resultados.append((linha, '', '❌ Formato inválido'))
                        continue

                    partes = linha.strip().split('|')
                    if len(partes) < 2:
                        resultados.append((linha, '', '❌ Dados incompletos'))
                        continue

                    nome = partes[0].strip()
                    telefone = partes[1].strip().replace(" ", "").replace("-", "")
                    if not telefone.startswith('+'):
                        telefone = '+55' + telefone

                    mensagem = mensagem_modelo.replace("{nome}", nome)

                    st.write(f"➡️ Enviando para {nome} ({telefone})...")

                    kit.sendwhatmsg_instantly(telefone, mensagem, wait_time=10, tab_close=False)
                    time.sleep(10)
                    pyautogui.press("enter")

                    resultados.append((nome, telefone, "✅ Enviado"))
                    time.sleep(5)

                except Exception as e:
                    resultados.append((linha, '', f"❌ Erro: {str(e)}"))

        st.success("✅ Finalizado!")
        st.subheader("📊 Relatório de envio:")
        for nome, telefone, status in resultados:
            st.write(f"{nome} | {telefone} → {status}")
if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://localhost:8501")
