<body>
    <div align="center">
        <img src="dox/res/main_screen.jpg" alt=".">
        <h1>Voice Assistant</h1>
    </div>
    <div align="center">
        <a href="https://github.com/xXxCLOTIxXx/xXxCLOTIxXx/blob/main/contacts.md">
            <img src="https://img.shields.io/badge/Контакты-Contacts-brightgreen" alt="Контакты">
        </a>
        <a href="https://github.com/xXxCLOTIxXx/xXxCLOTIxXx/blob/main/sponsor.md">
            <img src="https://img.shields.io/badge/Спонсировать-Donate-yellow" alt="Спонсировать">
        </a>
    </div>
    <div>
        <h2 align="center">По сборке:</h2>
        <ol>
            <li><strong>Скачивание модели:</strong>
                <p>Перейдите по следующей ссылке для скачивания модели речи: <a href="https://alphacephei.com/vosk/models" target="_blank">https://alphacephei.com/vosk/models</a></p>
                <p>Выберите подходящую модель для вашего проекта и скачайте её.</p>
            </li>
            <li><strong>Поместить модель в нужную папку:</strong>
                <p>После того как модель будет скачана, поместите её в папку: <code>assistant\server\system\stt\model\model_name</code>.</p>
                <p>Убедитесь, что модель находится в правильной директории, заменив <code>model_name</code> на vosk-model</p>
            </li>
            <li><strong>Сборка программы в EXE файл:</strong>
                <p>Чтобы собрать программу в исполняемый файл <code>.exe</code>, выполните следующие шаги:</p>
                <ul>
                    <li>Переместите файл <code>builder.py</code> в папку с проектом <code>assistant</code>.</li>
                    <li>Запустите файл <code>builder.py</code> с помощью Python. Для этого откройте командную строку или терминал в папке с файлом и выполните команду:</li>
                    <pre><code>python builder.py</code></pre>
                    <li>Дождитесь окончания процесса сборки. Программа создаст EXE файл в build директории.</li>
                </ul>
            </li>
        </ol>
        <p>Теперь ваш проект готов к использованию.</p>
      <div align="center">
      <a href="dox/main.md"><img src="https://img.shields.io/badge/Документация-Documentation-magenta" alt="Документация"></a>
      </div>
      </div>
    </body>
</html>
