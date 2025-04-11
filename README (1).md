Help
    
    curl -X http://127.0.0.1:5006/

Регистрация

    Запрос:
    curl -X POST http://127.0.0.1:5006/registration \
    -H "Content-Type: application/json" \
    -d '{"login": "testuser", "password": "P@$$w0rd","name":"TestName"}'
    
    Ответы:

    Успех:
        
        {'message': 'User created'}
    
    Не Удача:
    
        {'message': 'User no created'}