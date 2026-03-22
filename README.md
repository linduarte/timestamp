# ⏳ TimeStamp App - NiceGUI Edition

O **TimeStamp** é uma aplicação moderna de registro e controle de tempo desenvolvida com **Python** e o framework **NiceGUI**. Esta ferramenta foi projetada para oferecer uma interface reativa, leve e intuitiva para o gerenciamento de registros temporais (check-ins, logs de eventos ou controle de jornada).

## 🌟 Destaques do Projeto

Este projeto demonstra o poder do NiceGUI em transformar scripts Python em aplicações web profissionais de página única (SPA), com foco em:
* **Interface Reativa:** Atualizações de estado instantâneas sem recarregamento de página.
* **Componentização:** Uso de cards, diálogos e inputs estilizados com Tailwind CSS.
* **Persistência de Dados:** Organização de registros com data e hora precisos.

## 🚀 Funcionalidades

* **Registro Instantâneo:** Captura de timestamp com um único clique.
* **Visualização em Tempo Real:** Listagem dinâmica dos registros realizados.
* **Exportação de Dados:** Possibilidade de extração dos logs para análise externa.
* **Layout Responsivo:** Adaptável a desktops e dispositivos móveis através da grade flexível do NiceGUI.

## 🛠️ Tecnologias Utilizadas

* [Python 3.10+](https://www.python.org/)
* [NiceGUI](https://nicegui.io/) - Framework para UI baseada em Web.
* [Asyncio](https://docs.python.org/3/library/asyncio.html) - Para operações assíncronas não bloqueantes.
* [Tailwind CSS](https://tailwindcss.com/) - Estilização integrada nativamente ao framework.

## 📦 Estrutura de Arquivos

```text
├── main.py              # Ponto de entrada da aplicação e definição da UI
├── services/            # Lógica de negócio e manipulação de tempo
├── static/              # Ativos estáticos (CSS customizado, ícones)
└── requirements.txt     # Dependências do projeto

Testando o commit com assinatura