import streamlit as st
import os
import tempfile
import uuid
import whisper
import yt_dlp
import time
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Transcrição de Vídeos",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Título e descrição
st.title("🎬 Transcrição de Vídeos")
st.markdown("""
Este aplicativo permite transcrever o conteúdo de áudio de vídeos para texto.
Você pode fazer upload de um arquivo de vídeo ou fornecer um link do YouTube ou Instagram.
""")

# Função para criar diretório temporário
@st.cache_resource
def get_temp_dir():
    temp_dir = tempfile.mkdtemp()
    return temp_dir

# Função para carregar o modelo Whisper
@st.cache_resource
def load_whisper_model(model_name="small"):
    with st.spinner(f"Carregando modelo de transcrição {model_name}..."):
        model = whisper.load_model(model_name)
    return model

# Função para baixar vídeo do YouTube
def download_youtube(url, temp_dir):
    try:
        # Gerar um nome de arquivo único
        output_id = str(uuid.uuid4())
        audio_path = os.path.join(temp_dir, f"{output_id}.mp3")
        
        # Configurações do yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(temp_dir, f"{output_id}.%(ext)s"),
            'quiet': True,
            'no_warnings': True
        }
        
        # Baixar o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return {
            'success': True,
            'file_path': audio_path,
            'message': 'Vídeo baixado com sucesso'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Erro ao baixar vídeo: {str(e)}'
        }

# Função para baixar vídeo do Instagram
def download_instagram(url, temp_dir):
    try:
        # Gerar um nome de arquivo único
        output_id = str(uuid.uuid4())
        audio_path = os.path.join(temp_dir, f"{output_id}.mp3")
        
        # Configurações do yt-dlp para Instagram
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(temp_dir, f"{output_id}.%(ext)s"),
            'quiet': True,
            'no_warnings': True
        }
        
        # Baixar o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return {
            'success': True,
            'file_path': audio_path,
            'message': 'Vídeo do Instagram baixado com sucesso'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Erro ao baixar vídeo do Instagram: {str(e)}'
        }

# Função para transcrever áudio
def transcribe_audio(audio_path, model, language=None):
    try:
        # Opções de transcrição
        options = {}
        if language:
            options["language"] = language
        
        # Realizar a transcrição
        result = model.transcribe(audio_path, **options)
        
        return {
            'success': True,
            'text': result["text"],
            'language': result.get("language", "desconhecido"),
            'segments': result.get("segments", []),
            'message': 'Transcrição concluída com sucesso'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Erro ao transcrever áudio: {str(e)}'
        }

# Inicializar o diretório temporário
temp_dir = get_temp_dir()

# Criar abas para diferentes métodos de entrada
tab1, tab2, tab3 = st.tabs(["Upload de Arquivo", "Link do YouTube", "Link do Instagram"])

# Lista de idiomas suportados
languages = {
    "": "Detectar automaticamente",
    "pt": "Português",
    "en": "Inglês",
    "es": "Espanhol",
    "fr": "Francês",
    "de": "Alemão",
    "it": "Italiano",
    "ja": "Japonês",
    "zh": "Chinês",
    "ru": "Russo"
}

# Aba de Upload de Arquivo
with tab1:
    st.header("Upload de Arquivo")
    uploaded_file = st.file_uploader("Escolha um arquivo de vídeo", type=["mp4", "avi", "mov", "mkv", "webm"])
    language_upload = st.selectbox("Idioma (opcional)", options=list(languages.keys()), format_func=lambda x: languages[x], key="language_upload")
    
    if uploaded_file is not None:
        if st.button("Transcrever Arquivo", key="btn_upload"):
            # Salvar o arquivo temporariamente
            with st.spinner("Processando o arquivo..."):
                # Criar um arquivo temporário
                temp_file = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Carregar o modelo Whisper
                model = load_whisper_model("small")
                
                # Transcrever o áudio
                with st.spinner("Transcrevendo o áudio..."):
                    result = transcribe_audio(temp_file, model, language_upload if language_upload else None)
                
                # Limpar o arquivo temporário
                try:
                    os.remove(temp_file)
                except:
                    pass
                
                # Exibir o resultado
                if result['success']:
                    st.success("Transcrição concluída com sucesso!")
                    st.subheader("Texto Transcrito:")
                    st.text_area("", value=result['text'], height=300, key="text_upload")
                    
                    # Opções para download
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download TXT",
                            data=result['text'],
                            file_name="transcricao.txt",
                            mime="text/plain"
                        )
                    with col2:
                        # Para PDF, precisaríamos de uma biblioteca adicional
                        # Por simplicidade, oferecemos apenas TXT no Streamlit
                        st.info("Download em PDF não disponível nesta versão")
                else:
                    st.error(f"Erro: {result.get('message', 'Falha na transcrição')}")

# Aba de Link do YouTube
with tab2:
    st.header("Link do YouTube")
    youtube_url = st.text_input("URL do vídeo do YouTube", key="youtube_url")
    language_youtube = st.selectbox("Idioma (opcional)", options=list(languages.keys()), format_func=lambda x: languages[x], key="language_youtube")
    
    if youtube_url:
        if st.button("Transcrever do YouTube", key="btn_youtube"):
            # Validação básica da URL
            if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
                st.error("URL inválida do YouTube")
            else:
                # Baixar o vídeo
                with st.spinner("Baixando vídeo do YouTube..."):
                    download_result = download_youtube(youtube_url, temp_dir)
                
                if not download_result['success']:
                    st.error(f"Erro: {download_result.get('message', 'Falha ao baixar vídeo')}")
                else:
                    # Carregar o modelo Whisper
                    model = load_whisper_model("small")
                    
                    # Transcrever o áudio
                    with st.spinner("Transcrevendo o áudio..."):
                        audio_path = download_result['file_path']
                        transcription_result = transcribe_audio(audio_path, model, language_youtube if language_youtube else None)
                    
                    # Limpar o arquivo temporário
                    try:
                        os.remove(audio_path)
                    except:
                        pass
                    
                    # Exibir o resultado
                    if transcription_result['success']:
                        st.success("Transcrição concluída com sucesso!")
                        st.subheader("Texto Transcrito:")
                        st.text_area("", value=transcription_result['text'], height=300, key="text_youtube")
                        
                        # Opções para download
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                label="Download TXT",
                                data=transcription_result['text'],
                                file_name="transcricao.txt",
                                mime="text/plain"
                            )
                        with col2:
                            st.info("Download em PDF não disponível nesta versão")
                    else:
                        st.error(f"Erro: {transcription_result.get('message', 'Falha na transcrição')}")

# Aba de Link do Instagram
with tab3:
    st.header("Link do Instagram")
    instagram_url = st.text_input("URL do vídeo do Instagram", key="instagram_url")
    language_instagram = st.selectbox("Idioma (opcional)", options=list(languages.keys()), format_func=lambda x: languages[x], key="language_instagram")
    
    if instagram_url:
        if st.button("Transcrever do Instagram", key="btn_instagram"):
            # Validação básica da URL
            if "instagram.com" not in instagram_url:
                st.error("URL inválida do Instagram")
            else:
                # Baixar o vídeo
                with st.spinner("Baixando vídeo do Instagram..."):
                    download_result = download_instagram(instagram_url, temp_dir)
                
                if not download_result['success']:
                    st.error(f"Erro: {download_result.get('message', 'Falha ao baixar vídeo')}")
                else:
                    # Carregar o modelo Whisper
                    model = load_whisper_model("small")
                    
                    # Transcrever o áudio
                    with st.spinner("Transcrevendo o áudio..."):
                        audio_path = download_result['file_path']
                        transcription_result = transcribe_audio(audio_path, model, language_instagram if language_instagram else None)
                    
                    # Limpar o arquivo temporário
                    try:
                        os.remove(audio_path)
                    except:
                        pass
                    
                    # Exibir o resultado
                    if transcription_result['success']:
                        st.success("Transcrição concluída com sucesso!")
                        st.subheader("Texto Transcrito:")
                        st.text_area("", value=transcription_result['text'], height=300, key="text_instagram")
                        
                        # Opções para download
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                label="Download TXT",
                                data=transcription_result['text'],
                                file_name="transcricao.txt",
                                mime="text/plain"
                            )
                        with col2:
                            st.info("Download em PDF não disponível nesta versão")
                    else:
                        st.error(f"Erro: {transcription_result.get('message', 'Falha na transcrição')}")

# Informações adicionais
st.markdown("---")
st.markdown("""
### Notas:
- A transcrição pode levar alguns minutos, dependendo do tamanho do vídeo
- Para vídeos do YouTube e Instagram, algumas restrições podem exigir autenticação
- A qualidade da transcrição varia conforme a clareza do áudio
""")

# Rodapé
st.markdown("---")
st.caption("Aplicativo de Transcrição de Vídeos | Desenvolvido com Streamlit")
