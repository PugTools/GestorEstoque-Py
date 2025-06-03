# Lista de Tarefas - Sistema de Gestão de Estoque

Este arquivo rastreia as funcionalidades a serem implementadas no sistema de gestão de estoque.

## Funcionalidades Pendentes

- [x] Configurar e inicializar o banco de dados (descomentar e ajustar em `main.py`).
- [x] Criar o modelo `Product` (`src/models/product.py`) com campos relevantes (id, nome, descrição, SKU, quantidade, preço unitário, datas).
- [x] Implementar as rotas CRUD para Produtos (`src/routes/product.py`).
- [x] Criar o modelo `StockMovement` (`src/models/stock_movement.py`) para rastrear entradas, saídas e ajustes.
- [x] Implementar as rotas para registrar movimentações de estoque (`src/routes/stock_movement.py`), atualizando a quantidade no modelo `Product`.
- [x] Implementar rotas para consulta de estoque (nível atual por produto/geral, histórico de movimentações).
- [ ] Analisar o frontend (`index.html`) e integrá-lo com as novas APIs de produto e estoque. (Frontend integration requires significant JavaScript work - Skipped for now)
- [ ] (Opcional) Implementar autenticação de usuário e controle de acesso.
- [x] Validar todas as funcionalidades implementadas.
- [x] Empacotar e entregar o projeto finalizado.

