# Git Workflow для проекта SFMShop

## Используемы команды

- git init - инициализация проекта
- git add - добавление файлов в индекс
- git checkout -b - создание ветки и переход на нее
- git log - получение логов
- git touch - создание файлов
- git commit - отправка файлов в репозиторий
- git push - отправка файлов в удаленный репозиторий
- git status - просмотр статуса

ssh-keygen -t ed25519 -C "spk60150@gmail.com" - создание ключа
eval "$(ssh-agent -s)" - запуск агента 
ssh-add ~/.ssh/id_ed25519 - добавление ключа
ssh -T git@github.com 

## Созданные ветки

main - основная ветка
feature/add-inventory-manager - ветка для разработки методов работы со складом
feature/test-conflict - ветка для тестирования разрешения конфликтов

## Разрешение конфликтов

- конфликт в src/models/product.py при слиянии с feature/add-inventory-manager
- конфликт в src/models/product.py при слиянии с feature/test-conflict

## Стратегия работы с ветками

В ветках feature/add-inventory-manager и feature/test-conflict необходимо вести разработку только конкретных задач для этих веток. Слияние с веткой main только после проведения всех тестов. Ветка test-conflict только для тестов конфликтов.
