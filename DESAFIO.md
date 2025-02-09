Teste Prático: Sistema de Gerenciamento de Reservas de Salas de Reunião
O objetivo deste teste é avaliar sua capacidade de criar soluções considerando integrações, lógica de negócios, boas práticas e documentação.

Descrição do Desafio
Você foi contratado para desenvolver uma API para o sistema de gerenciamento de reservas de salas de reunião de uma empresa. O sistema deve permitir que usuários:
Cadastrem salas de reunião.
Verifiquem a disponibilidade de salas em horários específicos.
Reservem salas disponíveis.
Cancelam reservas.
O sistema deve garantir que não existam conflitos de reservas e que uma sala não possa ser reservada por mais de um usuário no mesmo horário.

Requisitos do Sistema
1. Funcionalidades da API

Cadastrar Sala de Reunião:
Endpoint: POST /rooms
Body da requisição (JSON):
 {
  "name": "Sala A",
  "capacity": 10,
  "location": "Andar 1"
}
Retorno esperado: Código HTTP 201 e os detalhes da sala criada.

Listar Salas:
Endpoint: GET /rooms
Retorno esperado: Lista de todas as salas cadastradas.

Consultar Disponibilidade:
Endpoint: GET /rooms/{id}/availability
Parâmetros: start_time, end_time (e.g., ?start_time=2025-01-22T14:00:00&end_time=2025-01-22T16:00:00)
Retorno esperado: Indicação se a sala está disponível no período solicitado.

Reservar uma Sala:
Endpoint: POST /reservations
Body da requisição (JSON):
 {
  "room_id": 1,
  "user_name": "João Silva",
  "start_time": "2025-01-22T14:00:00",
  "end_time": "2025-01-22T16:00:00"
}
Retorno esperado: Código HTTP 201 e os detalhes da reserva criada.
Regras de negócio:
O horário de início deve ser anterior ao de término.
O período reservado não pode conflitar com outras reservas da mesma sala.

Cancelar Reserva:
Endpoint: DELETE /reservations/{id}
Retorno esperado: Código HTTP 204.

Listar Reservas de uma Sala:
Endpoint: GET /rooms/{id}/reservations
Parâmetros opcionais: date (e.g., ?date=2025-01-22)
Retorno esperado: Lista das reservas feitas para a sala no dia especificado (ou todas, caso a data não seja fornecida).

Requisitos Técnicos
Use Python com Django Rest Framework (DRF) ou FastAPI.
Banco de dados: Utilize o banco de dados mais indicado para esse tipo de aplicação e justifique sua escolha.
Implemente validações completas (e.g., checar conflitos de horário, capacidade mínima, etc.).
Inclua documentação automática (Swagger, Redoc ou outro à sua escolha).
Registre logs para ações principais (e.g., criação de reservas, conflitos detectados, etc.).
Inclua um README detalhado com as instruções para rodar o projeto e usar a API.

Diferenciais (opcional)
Autenticação e Autorização: Implemente um sistema básico para autenticar usuários, permitindo que apenas o criador de uma reserva possa cancelá-la.
Paginação: Adicione paginação nos endpoints que retornam listas.
Notificações: Envie notificações simuladas (por console ou log) ao criar ou cancelar reservas.
Teste de Performance: Teste a aplicação com dados de carga e ajuste para garantir escalabilidade.
Docker: Containerize a aplicação para facilitar o setup.
Testes Automatizados: Implemente testes unitários e de integração para os endpoints principais.
CI/CD: Configure pipelines de integração contínua (GitHub Actions ou outra ferramenta).

Entrega
Suba o código em um repositório público no GitHub.
Inclua no README:
Descrição do projeto.
Instruções de setup e execução.
Detalhes sobre a API (endpoints e exemplos de uso).
Envie o link do repositório para isabelle.oliveira@myside.com.br

Critérios de Avaliação
Organização do código e clareza.
Implementação correta das regras de negócio.
Estrutura do projeto e boas práticas.
Qualidade da documentação e do README.
Complexidade e implementação de itens diferenciais.
Boa sorte no desenvolvimento! 🚀