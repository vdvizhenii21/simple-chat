# Simple Chat

## Тестове завдання: Чат.

## Технічні вимоги:
- Docker
- docker-compose

### Запуск проекту.

**Для запуску проекту протрібно виконати команд:**
```
./dc.sh up -d --build
```

**Після цього потрібно залити дамп бази, за допомогою команди:**
```
cat backup.sql | docker exec -i simple-chat-db-1 psql -U postgres -d postgres
```
**Таким чином ми завантажимо тестові данні. В системі є 4 юзери:**
- test1, test2, test3, test4.
**Пароль для кожного: rbcA88zz1**

### Створення суперюзера робиться за допмогою команди:
```
./manage.sh creatsuperuser
```

### Авторизація в системі.
```
// POST запит, з тілом username та password.

http://localhost:8085/jwt-auth/jwt/create/

```