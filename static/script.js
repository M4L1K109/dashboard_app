// Estado global da aplicação
let currentUser = null;
let currentFiles = [];
let currentFileIndex = 0;
let isPlaying = true;
let displayTimer = null;
let progressTimer = null;
let currentDisplayTime = 10;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    checkSession();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Upload form
    document.getElementById('uploadForm').addEventListener('submit', handleUpload);
    
    // User form
    document.getElementById('userForm').addEventListener('submit', handleCreateUser);
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
}

// Autenticação
async function checkSession() {
    try {
        const response = await fetch('/api/auth/check-session');
        const data = await response.json();
        
        if (data.logged_in) {
            currentUser = data.user;
            showMainApp();
            loadActiveFiles();
        } else {
            showLoginModal();
        }
    } catch (error) {
        console.error('Erro ao verificar sessão:', error);
        showLoginModal();
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            hideLoginModal();
            showMainApp();
            loadActiveFiles();
        } else {
            showError('loginError', data.error);
        }
    } catch (error) {
        console.error('Erro no login:', error);
        showError('loginError', 'Erro de conexão');
    }
}

async function logout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
        currentUser = null;
        stopDisplay();
        showLoginModal();
        hideMainApp();
    } catch (error) {
        console.error('Erro no logout:', error);
    }
}

// Interface
function showLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
    document.getElementById('loginError').style.display = 'none';
}

function hideLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function showMainApp() {
    document.querySelector('.navbar').style.display = 'block';
    document.querySelector('.main-content').style.display = 'block';
    
    // Mostrar/ocultar links baseado no papel do usuário
    const adminLinks = document.querySelectorAll('.admin-only');
    const canManage = currentUser && (currentUser.role === 'admin' || currentUser.can_upload);
    
    adminLinks.forEach(link => {
        link.style.display = canManage ? 'flex' : 'none';
    });
    
    showDashboard();
}

function hideMainApp() {
    document.querySelector('.navbar').style.display = 'none';
    document.querySelector('.main-content').style.display = 'none';
}

function showDashboard() {
    hideAllSections();
    document.getElementById('dashboardSection').style.display = 'block';
}

function showManageFiles() {
    hideAllSections();
    document.getElementById('manageFilesSection').style.display = 'block';
    loadFiles();
}

function showManageUsers() {
    hideAllSections();
    document.getElementById('manageUsersSection').style.display = 'block';
    loadUsers();
}

function hideAllSections() {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
}

function toggleNav() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('active');
}

// Dashboard - Exibição de arquivos
async function loadActiveFiles() {
    try {
        const response = await fetch('/api/files/active');
        const data = await response.json();
        
        if (response.ok) {
            currentFiles = data;
            currentFileIndex = 0;
            
            if (currentFiles.length > 0) {
                displayCurrentFile();
                if (isPlaying) {
                    startAutoRotation();
                }
            } else {
                showNoFiles();
            }
        }
    } catch (error) {
        console.error('Erro ao carregar arquivos:', error);
        showNoFiles();
    }
}

function displayCurrentFile() {
    if (currentFiles.length === 0) {
        showNoFiles();
        return;
    }
    
    const file = currentFiles[currentFileIndex];
    const fileDisplay = document.getElementById('fileDisplay');
    const fileName = document.getElementById('currentFileName');
    
    fileName.textContent = file.original_name;
    currentDisplayTime = file.display_time;
    
    // Limpar conteúdo anterior
    fileDisplay.innerHTML = '';
    
    // Criar elemento baseado no tipo de arquivo
    let content;
    
    if (file.file_type === 'video') {
        content = document.createElement('video');
        content.src = `/api/serve/${file.filename}`;
        content.controls = true;
        content.autoplay = true;
        content.muted = true; // Para permitir autoplay
        content.className = 'file-content';
    } else if (file.file_type === 'pdf') {
        content = document.createElement('iframe');
        content.src = `/api/serve/${file.filename}`;
        content.className = 'file-content';
    } else if (file.file_type === 'document') {
        content = document.createElement('div');
        content.className = 'file-content';
        content.innerHTML = `
            <div class="document-preview">
                <i class="fas fa-file-excel"></i>
                <h3>${file.original_name}</h3>
                <p>Documento Excel/CSV</p>
                <a href="/api/serve/${file.filename}" target="_blank" class="btn btn-primary">
                    <i class="fas fa-download"></i> Abrir Documento
                </a>
            </div>
        `;
    }
    
    fileDisplay.appendChild(content);
    
    // Iniciar timer de progresso
    startProgressTimer();
}

function showNoFiles() {
    const fileDisplay = document.getElementById('fileDisplay');
    fileDisplay.innerHTML = `
        <div class="no-files">
            <i class="fas fa-folder-open"></i>
            <p>Nenhum arquivo para exibir</p>
        </div>
    `;
    
    document.getElementById('currentFileName').textContent = '-';
    document.getElementById('timeRemaining').textContent = '-';
    document.getElementById('progressFill').style.width = '0%';
}

function startAutoRotation() {
    if (currentFiles.length <= 1) return;
    
    displayTimer = setTimeout(() => {
        nextFile();
    }, currentDisplayTime * 1000);
}

function stopAutoRotation() {
    if (displayTimer) {
        clearTimeout(displayTimer);
        displayTimer = null;
    }
}

function startProgressTimer() {
    stopProgressTimer();
    
    let timeElapsed = 0;
    const totalTime = currentDisplayTime;
    
    progressTimer = setInterval(() => {
        timeElapsed += 0.1;
        const progress = (timeElapsed / totalTime) * 100;
        const timeRemaining = Math.max(0, totalTime - timeElapsed);
        
        document.getElementById('progressFill').style.width = `${Math.min(progress, 100)}%`;
        document.getElementById('timeRemaining').textContent = `${Math.ceil(timeRemaining)}s`;
        
        if (timeElapsed >= totalTime) {
            stopProgressTimer();
        }
    }, 100);
}

function stopProgressTimer() {
    if (progressTimer) {
        clearInterval(progressTimer);
        progressTimer = null;
    }
}

function togglePlayPause() {
    isPlaying = !isPlaying;
    const btn = document.getElementById('playPauseBtn');
    
    if (isPlaying) {
        btn.innerHTML = '<i class="fas fa-pause"></i> Pausar';
        startAutoRotation();
        startProgressTimer();
    } else {
        btn.innerHTML = '<i class="fas fa-play"></i> Reproduzir';
        stopAutoRotation();
        stopProgressTimer();
    }
}

function nextFile() {
    if (currentFiles.length === 0) return;
    
    stopAutoRotation();
    stopProgressTimer();
    
    currentFileIndex = (currentFileIndex + 1) % currentFiles.length;
    displayCurrentFile();
    
    if (isPlaying) {
        startAutoRotation();
    }
}

function previousFile() {
    if (currentFiles.length === 0) return;
    
    stopAutoRotation();
    stopProgressTimer();
    
    currentFileIndex = currentFileIndex === 0 ? currentFiles.length - 1 : currentFileIndex - 1;
    displayCurrentFile();
    
    if (isPlaying) {
        startAutoRotation();
    }
}

function stopDisplay() {
    stopAutoRotation();
    stopProgressTimer();
}

// Gerenciamento de arquivos
async function loadFiles() {
    try {
        showLoading();
        const response = await fetch('/api/files');
        const data = await response.json();
        
        if (response.ok) {
            displayFiles(data);
        } else {
            console.error('Erro ao carregar arquivos:', data.error);
        }
    } catch (error) {
        console.error('Erro ao carregar arquivos:', error);
    } finally {
        hideLoading();
    }
}

function displayFiles(files) {
    const grid = document.getElementById('filesGrid');
    
    if (files.length === 0) {
        grid.innerHTML = '<p>Nenhum arquivo encontrado.</p>';
        return;
    }
    
    grid.innerHTML = files.map(file => `
        <div class="file-card ${file.is_active ? 'active' : 'inactive'}">
            <div class="file-header">
                <div>
                    <i class="fas ${getFileIcon(file.file_type)} file-icon ${file.file_type}"></i>
                    <h3>${file.original_name}</h3>
                </div>
                <span class="status-badge ${file.is_active ? 'active' : 'inactive'}">
                    ${file.is_active ? 'Ativo' : 'Inativo'}
                </span>
            </div>
            
            <div class="file-info-item">
                <label>Tipo:</label>
                <span>${getFileTypeLabel(file.file_type)}</span>
            </div>
            
            <div class="file-info-item">
                <label>Tempo de Exibição:</label>
                <span>${file.display_time}s</span>
            </div>
            
            <div class="file-info-item">
                <label>Enviado por:</label>
                <span>${file.uploader_name}</span>
            </div>
            
            <div class="file-info-item">
                <label>Data:</label>
                <span>${formatDate(file.uploaded_at)}</span>
            </div>
            
            <div class="file-actions">
                <button class="btn btn-sm btn-warning" onclick="editFile(${file.id})">
                    <i class="fas fa-edit"></i> Editar
                </button>
                <button class="btn btn-sm ${file.is_active ? 'btn-secondary' : 'btn-success'}" 
                        onclick="toggleFileActive(${file.id})">
                    <i class="fas fa-${file.is_active ? 'pause' : 'play'}"></i> 
                    ${file.is_active ? 'Desativar' : 'Ativar'}
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteFile(${file.id})">
                    <i class="fas fa-trash"></i> Excluir
                </button>
            </div>
        </div>
    `).join('');
}

function getFileIcon(type) {
    switch (type) {
        case 'video': return 'fa-video';
        case 'document': return 'fa-file-excel';
        case 'pdf': return 'fa-file-pdf';
        default: return 'fa-file';
    }
}

function getFileTypeLabel(type) {
    switch (type) {
        case 'video': return 'Vídeo';
        case 'document': return 'Planilha';
        case 'pdf': return 'PDF';
        default: return 'Arquivo';
    }
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('pt-BR');
}

// Upload de arquivos
function showUploadModal() {
    document.getElementById('uploadModal').style.display = 'block';
    document.getElementById('uploadForm').reset();
    document.getElementById('uploadProgress').style.display = 'none';
}

function closeUploadModal() {
    document.getElementById('uploadModal').style.display = 'none';
}

async function handleUpload(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('uploadProgressFill');
    const progressText = document.getElementById('uploadProgressText');
    
    try {
        progressDiv.style.display = 'block';
        
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressFill.style.width = percentComplete + '%';
                progressText.textContent = Math.round(percentComplete) + '%';
            }
        });
        
        xhr.addEventListener('load', function() {
            if (xhr.status === 201) {
                closeUploadModal();
                loadFiles();
                loadActiveFiles(); // Recarregar dashboard
                showSuccessMessage('Arquivo enviado com sucesso!');
            } else {
                const error = JSON.parse(xhr.responseText);
                alert('Erro: ' + error.error);
            }
        });
        
        xhr.addEventListener('error', function() {
            alert('Erro de conexão durante o upload');
        });
        
        xhr.open('POST', '/api/upload');
        xhr.send(formData);
        
    } catch (error) {
        console.error('Erro no upload:', error);
        alert('Erro no upload: ' + error.message);
    }
}

// Gerenciamento de usuários
async function loadUsers() {
    try {
        showLoading();
        const response = await fetch('/api/users');
        const data = await response.json();
        
        if (response.ok) {
            displayUsers(data);
        } else {
            console.error('Erro ao carregar usuários:', data.error);
        }
    } catch (error) {
        console.error('Erro ao carregar usuários:', error);
    } finally {
        hideLoading();
    }
}

function displayUsers(users) {
    const grid = document.getElementById('usersGrid');
    
    if (users.length === 0) {
        grid.innerHTML = '<p>Nenhum usuário encontrado.</p>';
        return;
    }
    
    grid.innerHTML = users.map(user => `
        <div class="user-card">
            <div class="user-header">
                <div>
                    <i class="fas fa-user user-icon ${user.role}"></i>
                    <h3>${user.username}</h3>
                </div>
                <span class="status-badge ${user.role}">
                    ${user.role === 'admin' ? 'Admin' : 'Usuário'}
                </span>
            </div>
            
            <div class="user-info-item">
                <label>Pode fazer upload:</label>
                <span>${user.can_upload ? 'Sim' : 'Não'}</span>
            </div>
            
            <div class="user-info-item">
                <label>Criado em:</label>
                <span>${formatDate(user.created_at)}</span>
            </div>
            
            <div class="user-actions">
                <button class="btn btn-sm btn-warning" onclick="editUser(${user.id})">
                    <i class="fas fa-edit"></i> Editar
                </button>
                <button class="btn btn-sm ${user.can_upload ? 'btn-secondary' : 'btn-success'}" 
                        onclick="toggleUserUpload(${user.id})">
                
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)