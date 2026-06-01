## APM Project Structure

### Root Directory
- [apm.py](https://github.com/aaalllexxx/APM/blob/master/apm.py) — Главная точка входа APM
- [helpers.py](https://github.com/aaalllexxx/APM/blob/master/helpers.py) — Вспомогательные функции и UI-классы
- [win2lin.py](https://github.com/aaalllexxx/APM/blob/master/win2lin.py) — Кроссплатформенная абстракция
- [json_dict.py](https://github.com/aaalllexxx/APM/blob/master/json_dict.py) — JSON-файл как Python-объект
- [config.json](https://github.com/aaalllexxx/APM/blob/master/config.json) — Конфигурация APM
- [config_template.json](https://github.com/aaalllexxx/APM/blob/master/config_template.json) — Шаблон конфигурации проекта
- [requirements.txt](https://github.com/aaalllexxx/APM/blob/master/requirements.txt) — Зависимости Python
- [apm.bat](https://github.com/aaalllexxx/APM/blob/master/apm.bat) — Запуск APM (Windows)
- [apm.sh](https://github.com/aaalllexxx/APM/blob/master/apm.sh) — Запуск APM (Linux/macOS)
- [apm.ps1](https://github.com/aaalllexxx/APM/blob/master/apm.ps1) — Запуск APM (PowerShell)

### modules/
- [config.py](https://github.com/aaalllexxx/APM/blob/master/modules/config.py) — Создание файла конфигурации проекта
- [create.py](https://github.com/aaalllexxx/APM/blob/master/modules/create.py) — Создание нового проекта
- [delete.py](https://github.com/aaalllexxx/APM/blob/master/modules/delete.py) — Удаление проекта
- [develop.py](https://github.com/aaalllexxx/APM/blob/master/modules/develop.py) — Создание шаблонов модулей и экранов
- [docs.py](https://github.com/aaalllexxx/APM/blob/master/modules/docs.py) — Открытие документации
- [env.py](https://github.com/aaalllexxx/APM/blob/master/modules/env.py) — Выполнение команд в окружении APM
- [goto.py](https://github.com/aaalllexxx/APM/blob/master/modules/goto.py) — Переход в директорию проекта
- [init.py](https://github.com/aaalllexxx/APM/blob/master/modules/init.py) — Регистрация проекта AEngine
- [install.py](https://github.com/aaalllexxx/APM/blob/master/modules/install.py) — Установка программных модулей
- [list.py](https://github.com/aaalllexxx/APM/blob/master/modules/list.py) — Просмотр зарегистрированных проектов
- [modules.py](https://github.com/aaalllexxx/APM/blob/master/modules/modules.py) — Просмотр списка модулей проекта
- [remove.py](https://github.com/aaalllexxx/APM/blob/master/modules/remove.py) — Удаление загруженного модуля
- [run.py](https://github.com/aaalllexxx/APM/blob/master/modules/run.py) — Запуск проекта AEngine
- [select.py](https://github.com/aaalllexxx/APM/blob/master/modules/select.py) — Выбор проекта как глобального
- [unregister.py](https://github.com/aaalllexxx/APM/blob/master/modules/unregister.py) — Удаление проекта из реестра
- [update.py](https://github.com/aaalllexxx/APM/blob/master/modules/update.py) — Обновление APM
- [upgrade.py](https://github.com/aaalllexxx/APM/blob/master/modules/upgrade.py) — Обновление AEngineApps в проекте

### scripts/
- [setup.bat](https://github.com/aaalllexxx/APM/blob/master/scripts/setup.bat) — Установка APM (Windows)
- [setup.sh](https://github.com/aaalllexxx/APM/blob/master/scripts/setup.sh) — Установка APM (Linux/macOS)
- [delete.bat](https://github.com/aaalllexxx/APM/blob/master/scripts/delete.bat) — Удаление APM (Windows)
- [delete.sh](https://github.com/aaalllexxx/APM/blob/master/scripts/delete.sh) — Удаление APM (Linux/macOS)
