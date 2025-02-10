# Sistema de Gerenciamento de Salas de Reunião

Um sistema completo para gerenciamento de salas de reunião, desenvolvido com FastAPI e SQLite, utilizando padrões de projeto e boas práticas de desenvolvimento.

## Escolha do Banco de Dados

O projeto utiliza SQLite como banco de dados:

### Justificativa
- **Domínio da aplicação**: O sistema gerencia um conjunto definido de entidades (salas, reservas e usuários) com isso o volume de dados que pode ser previsível
- **Simplicidade**: Por ser arquivo único, elimina a necessidade de configuração de servidor de banco de dados, simplificando desenvolvimento e compartilhamento para validação da atividade

## Funcionalidades

- Cadastro e autenticação de usuários
- Gerenciamento de salas de reunião
- Sistema de reservas com verificação de disponibilidade
- Controle de estados das salas (Disponível, Parcialmente Disponível, Indisponível)
- API RESTful completa com documentação Swagger

## Pré-requisitos

- Python 3.12 ou superior
- Docker e Docker Compose (opcional)
- Sistema operacional: Windows, Linux ou macOS

## Instalação

### Usando Docker (Recomendado)

1. Clone o repositório:
```bash
git clone https://github.com/brunobortolucci/teste-pratico-myside.git
cd teste-pratico-myside
```

2. Execute com Docker Compose:
```bash
docker-compose up --build
```

A aplicação estará disponível em: http://localhost:8000

### Usando Python local

1. Clone o repositório:
```bash
git clone https://github.com/brunobortolucci/teste-pratico-myside.git
cd teste-pratico-myside
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações do banco de dados:
```bash
alembic upgrade head
```

5. Inicie o servidor:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Obs**: Se utilizar o vscode, aqui está uma configuração para debug local
```bash
{
  "configurations": [
    {
      "name": "Depurador do Python: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload"
      ],
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      },
      "envFile": "${workspaceFolder}/.env"
    }
  ]
}
```

## Documentação da API

Após iniciar o servidor, acesse:

- Swagger UI: http://localhost:8000/docs

### Fluxo básico de uso

1. Crie um novo usuário:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

2. Faça login para obter o token:
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

3. Use o token nas requisições de reserva de sala (Criar/apagar):
```bash
curl -X POST http://localhost:8000/reservations/ \
  -H "Authorization: Bearer seu_token" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": "id_da_sala",
    "start_time": "2025-02-10T14:00:00",
    "end_time": "2025-02-10T15:00:00"
  }'
```

## Sistema de Observação e Logging

O projeto implementa o padrão Observer para monitoramento e logging de eventos relacionados às reservas. Este sistema permite:

### Funcionalidades do Observer Pattern
- Sistema de logging estruturado para diferentes tipos de eventos
- Notificações simuladas de email
- Detecção e registro de conflitos de reservas

### Tipos de Observers Implementados

1. **LoggingObserver**
   - Registra todas as operações de reserva
   - Mantém histórico detalhado de criações e cancelamentos
   - Nível de log: INFO

2. **EmailObserver**
   - Simula o envio de notificações por email
   - Registra tentativas de comunicação com usuários
   - Nível de log: INFO

3. **ConflictObserver**
   - Monitora e registra conflitos de horários
   - Alerta sobre sobreposições de reservas
   - Nível de log: WARNING

### Sistema de Logging

O sistema utiliza logging estruturado com as seguintes características:
- Logs persistentes em arquivo (`reservations.log`)
- Saída simultânea em console para desenvolvimento
- Diferentes níveis de log (DEBUG, INFO, WARNING, ERROR)
- Formato de log detalhado incluindo timestamp
- Configuração flexível por tipo de observer

Exemplo de log:
```log
2025-02-10 14:30:22,123 - LoggingObserver - INFO - Reserva criada | Sala: 123 | Usuário: 456 | Início: 2025-02-10 15:00:00 | Fim: 2025-02-10 16:00:00
2025-02-10 14:30:22,124 - EmailObserver - INFO - Email enviado | Confirmação de reserva para usuário 456 | Sala 123
2025-02-10 14:30:22,125 - ConflictObserver - WARNING - Conflito detectado | Sala: 123 | Período conflitante: 2025-02-10 15:00:00 - 2025-02-10 16:00:00
```

## Testes

### Testes de Integração Automatizados

O projeto inclui testes de integração automatizados que são executados no GitHub Actions. Estes testes:

1. Constroem a aplicação em um container Docker
2. Inicializam o banco de dados
3. Executam um fluxo completo de testes incluindo:
   - Registro de usuário
   - Autenticação
   - Criação de sala
   - Criação de reserva
   - Verificação de disponibilidade
   - Listagem de reservas
   - Remove uma reserva

Para verificar os testes de integração consulte o arquivo:

```bash
.github/workflows/integration-test.yml
```

## 📁 Estrutura do Projeto

```
.
├── src/
│   ├── api/
│   │   └── routes/          # Rotas da API
│   ├── domain/
│   │   ├── entities/        # Entidades do domínio
│   │   ├── models/          # Modelos Pydantic
│   │   └── states/          # Estados das salas
│   └── infrastructure/
│       ├── database/        # Configuração do banco
│       ├── repositories/    # Repositórios
│       └── security/        # Autenticação e segurança
├── migrations/              # Migrações Alembic
├── .github/
│   └── workflows/          # GitHub Actions workflows
├── docker-compose.yml      # Configuração Docker
├── docker-compose-test.yml # Configuração Docker para testes
└── README.md              # Este arquivo
```

## Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Python-Jose](https://python-jose.readthedocs.io/)
- [Passlib](https://passlib.readthedocs.io/)
- [Docker](https://www.docker.com/)

## Padrões de Projeto

- [State Pattern](https://refactoring.guru/pt-br/design-patterns/state): Para gerenciamento de estados das salas
- [Observer Pattern](https://refactoring.guru/pt-br/design-patterns/observer): Para notificar mudança de estados das reservas
- [Factory Pattern](https://refactoring.guru/pt-br/design-patterns/factory-method): Para criação de objetos
