const socket = io.connect('http://' + document.domain + ':' + location.port);

// Элементы интерфейса
const commandList = document.getElementById('commandList');
const keywordInput = document.getElementById('keyword');
const actionSelect = document.getElementById('action');
const detailsInput = document.getElementById('detailsInput');
const addCommandButton = document.getElementById('addCommand');
const backButton = document.getElementById('backButton');

actionSelect.addEventListener('change', () => {
    updateDetailsInput();
});

function updateDetailsInput() {
    const action = actionSelect.value;
    detailsInput.innerHTML = '';

    if (action === 'open_file' || action === 'run_file') {
        const button = document.createElement('button');
        button.textContent = 'Выбрать файл';
        button.className = 'fileSelectButton';
        button.id = 'fileSelectButton';

        const filePathDisplay = document.createElement('span');
        filePathDisplay.className = 'filePathDisplay';
        filePathDisplay.id = 'filePathDisplay';
        filePathDisplay.textContent = 'Файл не выбран';

        button.addEventListener('click', () => {
            socket.emit('select_file');
        });

        detailsInput.appendChild(button);
        detailsInput.appendChild(filePathDisplay);
    } else {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'messageInput';
        input.id = 'actionDetails';

        if (action === 'open_page') {
            input.placeholder = 'Введите URL страницы';
        } else if (action === 'answer_msg') {
            input.placeholder = 'Введите ответ бота.';
        } else if (action === 'console_command') {
            input.placeholder = 'Введите консольную команду.';
        }

        detailsInput.appendChild(input);
    }
}

// Обработка событий сокета
socket.on('file_selected', (data) => {
    const filePathDisplay = document.getElementById('filePathDisplay');
    if (filePathDisplay) {
        filePathDisplay.textContent = data.file_path || 'Файл не выбран';
        filePathDisplay.dataset.filePath = data.file_path; // Сохранение пути для дальнейшего использования
    }
});

socket.on('file_selected_error', (data) => {
    alert(data.message || 'Произошла ошибка при выборе файла!');
});

// Добавление команды
addCommandButton.addEventListener('click', () => {
    const keyword = keywordInput.value.trim();
    const action = actionSelect.value;

    let details = '';
    if (action === 'open_file' || action === 'run_file') {
        const filePathDisplay = document.getElementById('filePathDisplay');
        details = filePathDisplay?.dataset.filePath || '';
    } else {
        details = document.getElementById('actionDetails')?.value || '';
    }

    if (!keyword || !details) {
        alert('Заполните все поля!');
        return;
    }

    const commandData = {
        keyword: keyword,
        args: {
            type: action,
            url: action === 'open_page' ? details : undefined,
            path: (action === 'open_file' || action === 'run_file') ? details : undefined,
            answer_msg: action === 'answer_msg' ? details : undefined,
            command: action === 'console_command' ? details : undefined
        }
    };

    socket.emit('add_command', commandData);

    keywordInput.value = '';
    detailsInput.innerHTML = '';
    updateDetailsInput();
});



function deleteCommand(keyword) {
    socket.emit('delete_command', { keyword });
}

function executeCommand(keyword) {
    socket.emit('execute_command', { keyword });
}


socket.on('commands_list', (commands) => {
    commandList.innerHTML = '';
    commands.forEach(command => {
        const commandDiv = document.createElement('div');
        commandDiv.className = 'command';
        commandDiv.innerHTML = `
            <span>${command.keyword}</span>
            <div>
                <button onclick="executeCommand('${command.keyword}')">Выполнить</button>
                <button onclick="deleteCommand('${command.keyword}')">Удалить</button>
            </div>
        `;
        commandList.appendChild(commandDiv);
    });
});


backButton.addEventListener('click', () => {
    history.back();
});


socket.emit('get_commands');
updateDetailsInput();
