# Instruções para Deploy no Streamlit Cloud

## O que é o Streamlit Cloud?

O Streamlit Cloud é uma plataforma gratuita que permite hospedar aplicativos Streamlit na nuvem sem necessidade de conhecimentos avançados de programação ou infraestrutura.

## Pré-requisitos

1. Uma conta GitHub (gratuita)
2. Uma conta no Streamlit Cloud (gratuita)

## Passo a Passo para Deploy

### 1. Criar uma conta no GitHub

Se você ainda não tem uma conta no GitHub:
1. Acesse [github.com](https://github.com)
2. Clique em "Sign up" e siga as instruções para criar uma conta gratuita

### 2. Criar um novo repositório no GitHub

1. Após fazer login no GitHub, clique no botão "+" no canto superior direito
2. Selecione "New repository"
3. Dê um nome ao repositório (ex: "app-transcricao-videos")
4. Deixe o repositório como "Public"
5. Clique em "Create repository"

### 3. Fazer upload dos arquivos para o GitHub

1. No seu novo repositório, clique no link "uploading an existing file"
2. Arraste os arquivos do aplicativo ou clique para selecionar:
   - `app.py`
   - `requirements.txt`
3. Clique em "Commit changes"

### 4. Criar uma conta no Streamlit Cloud

1. Acesse [streamlit.io/cloud](https://streamlit.io/cloud)
2. Clique em "Sign up" e siga as instruções
3. Recomendamos fazer login com sua conta GitHub para facilitar a integração

### 5. Deploy do aplicativo

1. Após fazer login no Streamlit Cloud, clique em "New app"
2. Selecione o repositório que você acabou de criar
3. Na seção "Main file path", digite: `app.py`
4. Clique em "Deploy!"

O Streamlit Cloud irá automaticamente:
- Detectar o arquivo requirements.txt
- Instalar todas as dependências necessárias
- Iniciar o aplicativo

### 6. Acessar o aplicativo

Após o deploy ser concluído (pode levar alguns minutos), você receberá um URL público para o seu aplicativo, algo como:
```
https://username-app-transcricao-videos-randomstring.streamlit.app
```

Este URL pode ser compartilhado com qualquer pessoa para usar o aplicativo.

## Observações Importantes

1. **Recursos Gratuitos**: O plano gratuito do Streamlit Cloud tem algumas limitações:
   - O aplicativo "adormece" após inatividade
   - Recursos computacionais limitados
   - Tempo de processamento pode ser maior para vídeos longos

2. **Dependências**: O arquivo requirements.txt já inclui todas as dependências necessárias.

3. **FFmpeg**: O Streamlit Cloud já tem o FFmpeg instalado, então não há necessidade de instalação adicional.

4. **Problemas Comuns**:
   - Se o deploy falhar, verifique os logs para identificar o problema
   - Alguns vídeos do YouTube ou Instagram podem exigir autenticação
   - Para vídeos muito longos, o processamento pode exceder o tempo limite do Streamlit Cloud

## Suporte

Se você encontrar problemas durante o deploy:
1. Verifique os logs de erro no Streamlit Cloud
2. Consulte a [documentação oficial do Streamlit](https://docs.streamlit.io/)
3. Busque ajuda na [comunidade do Streamlit](https://discuss.streamlit.io/)
