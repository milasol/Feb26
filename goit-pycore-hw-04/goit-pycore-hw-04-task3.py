import sys
from pathlib import Path
from colorama import Fore, Style, init

# Ініціалізація colorama для підтримки Windows
init(autoreset=True)

def visualize_directory_structure(path: Path, indent: str = ""):
    
    try:
        # Отримуємо відсортований список вмісту (спочатку папки, потім файли)
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        
        for i, item in enumerate(items):
            # Визначаємо символи для візуалізації структури (Box Drawing)
            is_last = (i == len(items) - 1)
            connector = "┗ " if is_last else "┣ "
            
            if item.is_dir():
                # Виводимо папку синім кольором
                print(f"{indent}{connector}{Fore.BLUE}{Style.BRIGHT}📂 {item.name}{Style.RESET_ALL}")
                
                # Підготовка відступу для вкладених елементів
                new_indent = indent + ("  " if is_last else "┃ ")
                visualize_directory_structure(item, new_indent)
            else:
                # Виводимо файл зеленим кольором
                print(f"{indent}{connector}{Fore.GREEN}📜 {item.name}{Style.RESET_ALL}")
                
    except PermissionError:
        print(f"{indent}{Fore.RED}[Відмовлено в доступі]{Style.RESET_ALL}")

def main():
    # Перевіряємо, чи передано аргумент командного рядка
    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}Будь ласка, вкажіть шлях до директорії як аргумент.")
        print(f"Приклад: python hw03.py /шлях/до/директорії")
        return

    # Отримуємо шлях та перетворюємо його на об'єкт Path
    root_path = Path(sys.argv[1])

    # Валідація шляху
    if not root_path.exists():
        print(f"{Fore.RED}Помилка: Шлях '{root_path}' не існує.")
        return
    if not root_path.is_dir():
        print(f"{Fore.RED}Помилка: '{root_path}' не є директорією.")
        return

    # Виведення кореневої папки
    print(f"{Fore.CYAN}{Style.BRIGHT}📦 {root_path.name}{Style.RESET_ALL}")
    visualize_directory_structure(root_path)

if __name__ == "__main__":
    main()