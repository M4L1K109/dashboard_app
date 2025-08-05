# Estrutura do Projeto - Dashboard Web App

## Estrutura de Pastas
```
dashboard_app/
├── app.py                 # Aplicação principal Flask
├── config.py             # Configurações
├── models.py             # Modelos do banco de dados
├── auth.py               # Sistema de autenticação
├── database.db           # Banco SQLite
├── uploads/              # Pasta para arquivos enviados
│   ├── videos/
│   ├── documents/
│   └── pdfs/
├── static/               # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── uploads/         # Arquivos públicos
└── templates/            # Templates HTML
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── manage_files.html
    ├── manage_users.html
    └── upload.html
```

## Banco de Dados - Modelos

### Tabela Users
- id (Primary Key)
- username (Unique)
- password (Hash)
- role (admin/user)
- can_upload (Boolean)
- created_at

### Tabela Files
- id (Primary Key)
- filename
- original_name
- file_type (video/document/pdf)
- file_path
- display_time (segundos)
- is_active (Boolean)
- upload_order
- uploaded_by (Foreign Key -> Users)
- uploaded_at

### Tabela Settings
- id (Primary Key)
- key
- value
- description

## Funcionalidades Principais

### Dashboard (/)
- Exibição rotativa de arquivos
- Controle automático de tempo
- Interface moderna e colorida
- Responsivo

### Gerenciamento de Arquivos (/manage-files)
- Upload de arquivos (AVI, MP4, Excel, CSV, PDF)
- Configuração de tempo de exibição
- Editar/Apagar arquivos
- Reordenar sequência
- Ativar/Desativar arquivos

### Gerenciamento de Usuários (/manage-users)
- Cadastro de novos usuários
- Editar permissões
- Definir quem pode fazer upload
- Apagar usuários

### Autenticação
- Login/Logout
- Controle de sessão
- Proteção de rotas administrativas

