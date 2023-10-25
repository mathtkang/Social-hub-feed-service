FROM python:3.11-slim

# python 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

# poetry 환경 변수 설정
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# poetry 명령을 컨테이너에서 사용 가능하도록 poetry 바이너리 경로를 환경 변수 path에 추가
ENV PATH="$POETRY_HOME/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# curl, poetry 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get install -y gcc \
    && apt-get install -y default-libmysqlclient-dev

# Copy the poetry files for dependency installation
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-root --no-ansi --no-dev

# 애플리케이션 코드 복사
COPY . /app

# Expose the port your Django app will run on (if needed)
EXPOSE 8000

# Command to run your application using Gunicorn (you may need to adjust this)
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
