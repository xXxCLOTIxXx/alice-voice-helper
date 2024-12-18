const socket = io.connect('http://' + document.domain + ':' + location.port);


const tabs = document.querySelectorAll('.tab-button');
const contents = document.querySelectorAll('.tab-content');
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

const synthesisType = document.getElementById('synthesis-type');
const voiceSelection = document.getElementById('voice-selection');
const voiceList = document.getElementById('voice-list');

synthesisType.addEventListener('change', () => {
    if (['pyttsx3', 'silero'].includes(synthesisType.value)) {
        voiceSelection.style.display = 'block';
        socket.emit('get_models', { type: synthesisType.value });
    } else {
        voiceSelection.style.display = 'none';
    }
});

socket.on('update_models', data => {
    voiceList.innerHTML = '';
    data.models.forEach(
        model => {
        const option = document.createElement('option');
        option.value = model;
        option.textContent = model;
        voiceList.appendChild(option);
    });
    if (data.current) {
        voiceList.value = data.current;
    }
});

const dialogModelSelect = document.getElementById('dialog-model-select');
const tokenField = document.getElementById('token-field');

dialogModelSelect.addEventListener('change', () => {
    tokenField.style.display = dialogModelSelect.value === 'chatgpt' ? 'block' : 'none';
});

document.getElementById('apply-button').addEventListener('click', () => {
    const settings = {
        synthesis: {
            type: synthesisType.value,
            voice: voiceList.value
        },
        input_output: {
            volume: document.getElementById('volume-slider').value,
            speak: document.getElementById('speak-checkbox').checked,
            listen: document.getElementById('listen-checkbox').checked,
        },
        dialog_model: {
            model: dialogModelSelect.value,
            token: document.getElementById('chatgpt-token').value,
            dialog_mode: document.getElementById('dialog_mode').checked
        },
        other: {
            names: document.getElementById('names-list').value,
            initial_prompt: document.getElementById('initial-prompt').value
        }
    };

    socket.emit('update_settings', settings);
});

document.getElementById('reset-button').addEventListener('click', () => {
    socket.emit('reset_settings');
    location.reload()
});

window.onload = () => {
    getSettingsData();
};

function getSettingsData() {
    socket.emit('get_settings_data');
}

socket.on('settings_data', (data) => {
    const settings = JSON.parse(data);
    console.log(settings);

    document.getElementById('synthesis-type').value = settings.synthesis.type || 'gtts';
    document.getElementById('volume-slider').value = settings.input_output.volume || 50;
    document.getElementById('speak-checkbox').checked = settings.input_output.speak || false;
    document.getElementById('listen-checkbox').checked = settings.input_output.listen || false;
    document.getElementById('dialog-model-select').value = settings.dialog_model.model || 'g4f';
    document.getElementById('chatgpt-token').value = settings.dialog_model.token || null;
    document.getElementById('dialog_mode').checked = settings.dialog_model.dialog_mode || false;

    document.getElementById('names-list').value = settings.other.names || '';
    document.getElementById('initial-prompt').value = settings.other.initial_prompt || '';
    document.getElementById('voice-list').value = settings.synthesis.voice || null;
    
    if (['pyttsx3', 'silero'].includes(synthesisType.value)) {
        voiceSelection.style.display = 'block';
        socket.emit('get_models', { type: synthesisType.value });
    }

    if (settings.dialog_model.model === 'chatgpt') {
        console.log(dialogModelSelect.value);
        tokenField.style.display = 'block';
    }    
});
