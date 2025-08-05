# 🚀 Instruções Rápidas - Dashboard App

## Como Executar

1. **Abra o terminal na pasta do projeto**
   ```bash
   cd dashboard_app
   ```

2. **Ative o ambiente virtual**
   ```bash
   source venv/bin/activate
   ```

3. **Execute a aplicação**
   ```bash
   python src/main.py
   ```

4. **Acesse no navegador**
   - URL: `http://localhost:5000`
   - **Usuário**: Admin
   - **Senha**: Admin

## 📋 Funcionalidades Principais

### ✅ Login e Autenticação
- Sistema seguro com usuário/senha
- Usuário admin padrão: Admin/Admin
- Controle de permissões

### ✅ Dashboard de Exibição
- Rotação automática de arquivos
- Controles: Play/Pause, Anterior, Próximo
- Tempo configurável por arquivo
- Suporte: Vídeos (MP4, AVI), Planilhas (Excel, CSV), PDFs

### ✅ Gerenciamento de Arquivos
- Upload via interface web
- Configuração de tempo de exibição
- Ativar/desativar arquivos
- Editar e excluir arquivos

### ✅ Gerenciamento de Usuários
- Cadastro de novos usuários (apenas admin)
- Controle de permissões de upload
- Papéis: Admin e Usuário

## 🎨 Design
- Interface moderna e colorida
- Responsivo para desktop e mobile
- Gradientes e animações suaves

## 📁 Formatos Suportados
- **Vídeos**: MP4, AVI
- **Planilhas**: Excel (.xlsx, .xls), CSV
- **PDFs**: Arquivos PDF

## ⚙️ Configurações
- Tempo de exibição: 1-300 segundos
- Tamanho máximo: 500MB por arquivo
- Rotação automática configurável

## 🔧 Solução Rápida de Problemas

**Erro de banco de dados?**
```bash
rm src/database/app.db
python src/main.py
```

**Não consegue fazer upload?**
- Verifique se tem permissão de upload
- Confirme o formato do arquivo
- Verifique o tamanho (máx 500MB)

**Arquivos não aparecem no dashboard?**
- Verifique se estão ativos
- Confirme se há arquivos cadastrados

---
**Pronto para usar! 🎉**

