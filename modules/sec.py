import os
import sys
from importlib.machinery import SourceFileLoader

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
        print(f"[!] Директория {sec_dir} не найдена. Проверьте структуру проекта.")
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
            loader = SourceFileLoader(f"sec.{subcommand}", cmd_file)
            module = loader.load_module()
            if hasattr(module, "run"):
                # Передаем управление модулю, пропуская 'sec' и имя подкоманды
                # Теперь 'logs.py' получит ['analyze', ...]
                module.run(base_dir, gconf_path=gconf_path, args=args[2:])
            else:
                print(f"[!] В модуле {cmd_file} не найдена функция run()")
        except Exception as e:
            import traceback
            print(f"[!] Ошибка при выполнении sec {subcommand}: {e}")
            traceback.print_exc()
    else:
        print(f"[!] Команда sec {subcommand} не найдена.")
