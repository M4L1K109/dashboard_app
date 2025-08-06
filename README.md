# Dashboard App - Deploy no Render com PostgreSQL

## Sobre o Projeto
Dashboard App é uma aplicação web desenvolvida em Flask que permite upload e exibição rotativa de arquivos (vídeos, planilhas e PDFs) em um dashboard moderno e responsivo.

## Funcionalidades
- 📊 Dashboard com rotação automática de arquivos
- 📁 Upload de vídeos (AVI, MP4), planilhas (Excel, CSV) e PDFs
- 👥 Sistema de gerenciamento de usuários
- 🔐 Autenticação e controle de permissões
- ⚙️ Configurações personalizáveis
- 📱 Interface responsiva e moderna

## Estrutura do Projeto
```
dashboard_app/
├── app.py                    # Aplicação principal Flask
├── requirements.txt          # Dependências Python
├── runtime.txt              # Versão do Python
├── Procfile                 # Comando de execução
├── src/
│   ├── models/
│   │   └── user.py          # Modelos do banco de dados
│   └── routes/
│       ├── auth.py          # Rotas de autenticação
│       ├── files.py         # Rotas de gerenciamento de arquivos
│       └── user.py          # Rotas de gerenciamento de usuários
├── static/
│   ├── index.html           # Interface principal
│   ├── styles.css           # Estilos CSS
│   └── script.js            # JavaScript
├── uploads/                 # Pasta para arquivos enviados
└── database/               # Pasta para banco SQLite (desenvolvimento)
```

## Deploy no Render com PostgreSQL

### 1. Preparação do Repositório
1. Faça upload deste arquivo ZIP para seu repositório Git (GitHub, GitLab, etc.)
2. Extraia os arquivos na raiz do repositório
3. Faça commit e push dos arquivos

### 2. Criar Banco PostgreSQL no Render
**IMPORTANTE**: Você deve criar o banco PostgreSQL ANTES de configurar o Web Service.

1. No dashboard do Render, clique em "New +" e selecione "PostgreSQL"
2. Configure o banco:
   - **Name**: dashboard-app-db (ou nome de sua escolha)
   - **Database**: dashboard_app
   - **User**: dashboard_user (será criado automaticamente)
   - **Region**: Escolha a mesma região do seu Web Service
3. Clique em "Create Database"
4. **Anote a URL de conexão** que será fornecida (você precisará dela no próximo passo)

### 3. Configurar Web Service no Render
1. No dashboard do Render, clique em "New +" e selecione "Web Service"
2. Conecte seu repositório Git
3. Configure as seguintes opções:

**Configurações Básicas:**
- **Name**: dashboard-app (ou nome de sua escolha)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Configurações Avançadas:**
- **Python Version**: 3.11.0 (definido no runtime.txt)
- **Auto-Deploy**: Yes (para deploy automático em commits)

### 4. Configurar Variáveis de Ambiente
Configure as seguintes variáveis de ambiente no Render:

**Obrigatórias:**
- **DATABASE_URL**: Cole a URL de conexão do PostgreSQL criado no passo 2
- **SECRET_KEY**: Uma chave secreta segura (ex: `minha_chave_super_secreta_2024`)

**Opcionais:**
- **PORT**: 5000 (geralmente não é necessário, o Render define automaticamente)

### 5. Exemplo de Configuração
Suas variáveis de ambiente devem ficar assim:
```
DATABASE_URL=postgresql://dashboard_user:senha@dpg-xxxxx-a.oregon-postgres.render.com/dashboard_app
SECRET_KEY=minha_chave_super_secreta_2024
```

### 6. Deploy e Primeiro Acesso
1. Clique em "Create Web Service" para iniciar o deploy
2. Aguarde o build e deploy completarem (pode levar alguns minutos)
3. Acesse a URL fornecida pelo Render
4. Faça login com as credenciais padrão:
   - **Usuário**: Admin
   - **Senha**: Admin
5. **IMPORTANTE**: Altere a senha padrão imediatamente!

## Solução de Problemas

### Erro "unable to open database file"
Este erro indica que o SQLite não pode ser usado no Render. Certifique-se de:
1. Ter criado o banco PostgreSQL no Render
2. Configurado corretamente a variável `DATABASE_URL`
3. A URL do banco estar no formato correto

### Erro de conexão com PostgreSQL
Verifique se:
1. O banco PostgreSQL está ativo no Render
2. A variável `DATABASE_URL` está configurada corretamente
3. O banco e o Web Service estão na mesma região

### Build falha
Verifique se:
1. O arquivo `requirements.txt` está presente na raiz do projeto
2. Todas as dependências estão listadas corretamente
3. A versão do Python está especificada no `runtime.txt`

## Uso da Aplicação

### Dashboard Principal
- Acesse a página inicial para ver o dashboard
- Os arquivos são exibidos em rotação automática
- Use os controles para pausar/retomar a rotação

### Gerenciamento de Arquivos
1. Faça login como administrador
2. Clique em "Gerenciar Arquivos"
3. Faça upload de vídeos, planilhas ou PDFs
4. Configure o tempo de exibição de cada arquivo
5. Ative/desative arquivos conforme necessário

### Gerenciamento de Usuários
1. Acesse "Gerenciar Usuários" (apenas administradores)
2. Crie novos usuários
3. Defina permissões (admin/usuário)
4. Configure quem pode fazer upload

## Tipos de Arquivo Suportados
- **Vídeos**: .avi, .mp4
- **Planilhas**: .xlsx, .xls, .csv
- **Documentos**: .pdf

## Configurações
- Tempo padrão de exibição: 10 segundos
- Tamanho máximo de arquivo: 500MB
- Rotação automática: Ativada por padrão

## Desenvolvimento Local

### Pré-requisitos
- Python 3.11+
- PostgreSQL (opcional, pode usar SQLite)

### Instalação
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure as variáveis de ambiente (opcional para SQLite local)
4. Execute: `python app.py`

## Segurança
- ✅ Use PostgreSQL em produção (incluído nesta versão)
- ✅ Configure uma SECRET_KEY forte
- ✅ Altere a senha padrão do administrador
- ✅ HTTPS automático no Render
- ✅ Monitore uploads e usuários regularmente

## Custos no Render
- **Web Service**: Gratuito para uso básico, $7/mês para instâncias dedicadas
- **PostgreSQL**: Gratuito para bancos pequenos, $7/mês para bancos maiores
- **Armazenamento**: Incluído nos planos

## Suporte
Para dúvidas ou problemas:
1. Verifique os logs no dashboard do Render
2. Confirme se o banco PostgreSQL está ativo
3. Verifique se todas as variáveis de ambiente estão configuradas
4. Teste a conexão com o banco

---

**Dashboard App** - Sistema de Exibição de Arquivos
Versão otimizada para PostgreSQL no Render 🚀

