# Dashboard App - Sistema de Exibição de Arquivos

## Descrição

O Dashboard App é um sistema web desenvolvido em Python com Flask que permite a exibição rotativa de vídeos, planilhas e PDFs em um dashboard moderno e colorido. O sistema inclui controle de acesso, gerenciamento de usuários e arquivos, com configuração personalizada de tempo de exibição.

## Funcionalidades

### 🎯 Dashboard de Exibição
- Exibição rotativa automática de arquivos
- Suporte para vídeos (MP4, AVI)
- Suporte para planilhas (Excel, CSV)
- Suporte para PDFs
- Controles de reprodução (Play/Pause, Anterior, Próximo)
- Barra de progresso com tempo restante
- Interface moderna e responsiva

### 👥 Sistema de Autenticação
- Login seguro com usuário e senha
- Controle de sessão
- Usuário administrador padrão (Admin/Admin)
- Diferentes níveis de permissão

### 📁 Gerenciamento de Arquivos
- Upload de arquivos via interface web
- Configuração individual de tempo de exibição
- Ativação/desativação de arquivos
- Edição e exclusão de arquivos
- Reordenação da sequência de exibição
- Controle de acesso por permissões

### 👤 Gerenciamento de Usuários
- Cadastro de novos usuários (apenas admin)
- Definição de papéis (Admin/Usuário)
- Controle de permissões de upload
- Edição e exclusão de usuários

## Tecnologias Utilizadas

- **Backend**: Python 3.11, Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticação**: Werkzeug Security
- **Upload**: Flask File Upload
- **Design**: CSS Gradients, Flexbox, Grid

## Estrutura do Projeto

```
dashboard_app/
├── src/
│   ├── main.py              # Aplicação principal
│   ├── models/
│   │   └── user.py          # Modelos do banco de dados
│   ├── routes/
│   │   ├── auth.py          # Rotas de autenticação
│   │   ├── user.py          # Rotas de usuários
│   │   └── files.py         # Rotas de arquivos
│   ├── static/
│   │   ├── index.html       # Interface principal
│   │   ├── styles.css       # Estilos CSS
│   │   └── script.js        # JavaScript
│   └── database/
│       └── app.db           # Banco SQLite
├── uploads/                 # Arquivos enviados
│   ├── videos/
│   ├── documents/
│   └── pdfs/
├── venv/                    # Ambiente virtual
└── requirements.txt         # Dependências
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou extraia o projeto**
   ```bash
   cd dashboard_app
   ```

2. **Ative o ambiente virtual**
   ```bash
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\\Scripts\\activate   # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python src/main.py
   ```

5. **Acesse a aplicação**
   - Abra o navegador e acesse: `http://localhost:5000`
   - Use as credenciais padrão: **Usuário: Admin** | **Senha: Admin**

## Uso do Sistema

### 1. Login
- Acesse a aplicação no navegador
- Use as credenciais do administrador padrão ou de um usuário cadastrado
- Após o login, você será redirecionado para o dashboard

### 2. Dashboard de Exibição
- A tela principal mostra os arquivos em rotação automática
- Use os controles para pausar, avançar ou retroceder
- O tempo de exibição é configurável por arquivo

### 3. Gerenciamento de Arquivos
- Clique em "Gerenciar Arquivos" no menu
- Use "Adicionar Arquivo" para fazer upload
- Configure o tempo de exibição (em segundos)
- Ative/desative arquivos conforme necessário
- Use os botões de edição e exclusão para gerenciar

### 4. Gerenciamento de Usuários (Apenas Admin)
- Clique em "Gerenciar Usuários" no menu
- Use "Adicionar Usuário" para criar novos usuários
- Defina o papel (Admin/Usuário) e permissões
- Controle quem pode fazer upload de arquivos

## Formatos Suportados

### Vídeos
- MP4 (recomendado)
- AVI

### Documentos
- Excel (.xlsx, .xls)
- CSV (.csv)
- OpenDocument Spreadsheet (.ods)

### PDFs
- Arquivos PDF (.pdf)

## Configurações

### Tempo de Exibição
- Configurável por arquivo (1-300 segundos)
- Padrão: 10 segundos
- Pode ser alterado durante o upload ou edição

### Permissões de Usuário
- **Admin**: Acesso total ao sistema
- **Usuário**: Acesso apenas ao dashboard
- **Permissão de Upload**: Pode ser concedida individualmente

### Tamanho de Arquivo
- Limite máximo: 500MB por arquivo
- Recomendado: Arquivos menores para melhor performance

## Segurança

- Senhas são armazenadas com hash seguro
- Controle de sessão ativo
- Validação de tipos de arquivo
- Proteção contra uploads maliciosos
- Controle de acesso baseado em papéis

## Solução de Problemas

### Erro de Banco de Dados
Se houver erro relacionado ao banco de dados:
```bash
rm src/database/app.db
python src/main.py
```

### Problemas de Upload
- Verifique se o arquivo está no formato suportado
- Confirme se o tamanho não excede 500MB
- Certifique-se de ter permissão de upload

### Problemas de Exibição
- Verifique se os arquivos estão ativos
- Confirme se há arquivos cadastrados no sistema
- Teste com diferentes tipos de arquivo

## Desenvolvimento

### Estrutura do Código
- **Models**: Definição das tabelas do banco de dados
- **Routes**: Endpoints da API REST
- **Static**: Arquivos frontend (HTML, CSS, JS)
- **Templates**: Não utilizados (SPA com JavaScript)

### API Endpoints
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/files/active` - Arquivos ativos
- `POST /api/upload` - Upload de arquivo
- `GET /api/users` - Listar usuários
- E outros...

## Licença

Este projeto foi desenvolvido como solução personalizada.

## Suporte

Para suporte ou dúvidas sobre o sistema, consulte a documentação ou entre em contato com o desenvolvedor.

---

**Dashboard App v1.0** - Sistema de Exibição de Arquivos Desenvolvido em Python/Flask

