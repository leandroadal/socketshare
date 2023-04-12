# Definindo a imagem base
FROM python:3.11.2
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=D:\Programação\Projetos\Python\socketshare\venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY requirements.txt .

COPY . /app

RUN pip install -r requirements.txt

# Expondo a porta 5000
EXPOSE 8081


# Iniciando o servidor
CMD ["python", "server/socket_server.py"]
