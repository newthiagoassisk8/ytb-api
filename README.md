# 🎬 YouTube Video Downloader API

Essa é uma **API simples feita com FastAPI** que usa a biblioteca [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) para baixar vídeos do YouTube. Ela foi criada para ser utilizada por um app mobile em React Native como forma de praticar integração entre frontend e backend.

## ✨ O que ela faz

- Recebe o **ID de um vídeo do YouTube**.
- Usa o `yt-dlp` para **baixar o vídeo no formato MP4**.
- Gera um link temporário para que o app possa baixar o vídeo.
- O link é válido por 10 minutos e depois o vídeo é excluído automaticamente do servidor.

## 🔗 Endpoints principais

- `POST /download`: inicia o download de um vídeo a partir do ID e retorna o link para download.
- `GET /video/{id}`: entrega o vídeo, se o link ainda estiver válido.

## 📲 Projeto relacionado (Frontend)

Este backend foi desenvolvido para ser consumido por um aplicativo mobile React Native que você pode conferir aqui:

🔗 [daily-diet-app (branch youtube-video-downloader)](https://github.com/newthiagoassisk8/daily-diet-app/tree/youtube-video-downloader)

> **PS:** Sim, o nome do repositório parece estar em uma fase de identidade confusa — *não tem nada a ver com dieta*

---

Feita para estudos e experimentação com FastAPI, yt-dlp e integração com apps móveis. 🚀
