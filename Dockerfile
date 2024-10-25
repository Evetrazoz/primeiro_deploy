FROM python:3.10-slim




#definir o diretorio de traabalho no container
WORKDIR /app


#copiar os arquivos de requesitos para o conteiner
COPY requeriments.txt .

#instalar as dependencias
RUN pip install --no-cache-dir -r requeriments.txt

#copiar o projeto para dentro do container
COPY . .

#definir a variavel de ambiente para o django  usar o modo de producao
ENV DJANGO_SETTINGS_MODULE=core.settings

#coletar arquivos estaticos durante o build
RUN python manage.py collectstatic --noinput

#rodar as migracoes durante o build (so funcioanra se o banco de dados estiver acessivel)
RUN python manage.py migrate --noinput

#expor a porta que o container vai usar
EXPOSE 8000

#rodar o servidor gunicorn para produçao
CMD ["cunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]