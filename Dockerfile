# ベースイメージ
FROM python:3.12-slim

# 環境変数（ログ即時出力など）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 必要ならビルドツールを追加
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# ワークディレクトリ
WORKDIR /app

# 依存関係インストール
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Dev Containers 用のユーザー作成（vscode）
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    chown -R $USERNAME:$USERNAME /app

# アプリ本体
COPY app ./app

# ポート公開
EXPOSE 8000

# 非 root で実行
USER $USERNAME

# デフォルト起動コマンド（dev は docker-compose で --reload に差し替え）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
