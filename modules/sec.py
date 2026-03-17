import os
import sys
import importlib.util

__help__ = "Управление безопасностью и подписью проекта (sec)"

def run(base_dir, gconf_path="", args=None):
    """
    Bridge to the sec package.
    Redirects calls to AEngine/sec/init.py or specific submodules.
    """
    if args is None:
        args = []
        
    # Путь к директории sec (на уровень выше APM)
    sec_dir = os.path.abspath(os.path.join(base_dir, "..", "sec"))
    
    if not os.path.exists(sec_dir):
        print(f"[!] Директория sec не найдена: {sec_dir}")
        print(f"    Проверьте структуру проекта AEngine.")
        return

    # Добавляем sec в sys.path чтобы внутренние импорты работали
    if sec_dir not in sys.path:
        sys.path.insert(0, sec_dir)

    # args[0] is 'sec', args[1] is the subcommand
    subcommand = args[1] if len(args) > 1 else "init"
    
    # Пытаемся найти файл подкоманды
    cmd_file = os.path.join(sec_dir, f"{subcommand}.py")
    if not os.path.exists(cmd_file):
        # Если файла нет, пробуем init.py (основной инсталлятор)
        cmd_file = os.path.join(sec_dir, "init.py")
    
    if os.path.exists(cmd_file):
        try:
            # Загрузка через importlib.util (без deprecated load_module)
            spec = importlib.util.spec_from_file_location(f"sec.{subcommand}", cmd_file)
            if spec is None or spec.loader is None:
                print(f"[!] Не удалось загрузить модуль: {cmd_file}")
                return
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"sec.{subcommand}"] = module
            spec.loader.exec_module(module)
            
            if hasattr(module, "run"):
                # Передаем управление модулю, пропуская 'sec' и имя подкоманды
                module.run(base_dir, gconf_path=gconf_path, args=args[2:])
            else:
                print(f"[!] В модуле {os.path.basename(cmd_file)} не найдена функция run()")
        except ModuleNotFoundError as e:
            import traceback
            print(f"[!] Ошибка зависимости 'sec {subcommand}': отсутствует модуль '{e.name}'")
            print(f"    Установите его: pip install {e.name}")
            traceback.print_exc()
        except Exception as e:
            import traceback
            print(f"[!] Ошибка при выполнении 'sec {subcommand}':")
            traceback.print_exc()
    else:
        print(f"[!] Команда 'sec {subcommand}' не найдена.")
        print(f"    Доступные подкоманды: init, sign, unsign, add_admin, logs, remove")
