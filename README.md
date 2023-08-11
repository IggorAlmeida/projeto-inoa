# projeto-inoa


```bash
# Clone este repositório
$ git clone <https://github.com/IggorAlmeida/projeto-inoa.git>

# Acesse a pasta do projeto no terminal
$ cd projeto-inoa

# Crie um virtualenviroment
$ python3 -m venv venv

# Ative o virtualenviroment
$ soucer venv/bin/activate

# Instale as dependências
$ pip install requirements.txt

# Execute o makemigrations
$ python manage.py makemigration

# Aplique as migrações
$ python manage.py migrate

# Execute o comando de desenvolvimento
$ python manage.py runserver

# Em outro terminal execute o comando de desenvolvimento
$ celery -A core worker -l INFO

# Em outro terminal execute o comando de desenvolvimento
$ celery -A core.celery beat


