## Деплой

Клонируйте репозиторий:
```bash
git clone https://github.com/iamshelldy/menu-django-app.git
cd menu-django-app
```

Запустите контейнер, используя `Dockerfile`:
```bash
docker build -t myapp .
docker run -p 8000:8000 myapp
```
или `docker-compose.yml`:
```bash
docker-compose up --build
```

## Данные учетной записи суперпользователя

Имя пользователя: `admin`\
Пароль: `admin`
