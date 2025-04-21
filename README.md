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

## 🚀 Executando o Projeto

Para rodar este projeto, certifique-se de que você está utilizando o **Python 3.11** e que possui um **ambiente virtual** ativado.

Após instalar as dependências necessárias, execute o seguinte comando:

```bash
uvicorn main:app --host 0.0.0.0 --port 8006
```

Esse comando inicia a aplicação utilizando o `uvicorn`, tornando-a acessível em todas as interfaces de rede (`0.0.0.0`) na porta `8006`.

> 💡 Dica: para criar e ativar um ambiente virtual, utilize os comandos abaixo:

```bash
python3.11 -m venv venv
source venv/bin/activate  # No Linux/macOS
venv\Scripts\activate     # No Windows
```

Feita para estudos e experimentação com FastAPI, yt-dlp e integração com apps móveis. 🚀
