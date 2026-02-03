# Farm Game - Гра "Ферма"

## Структура проекту

```
FarmGame/
├── frontend/                   # Python фронтенд
│   ├── game/                  # Ігрова логіка
│   │   ├── game_engine.py    # Головний ігровий движок
│   │   ├── game_state.py     # Стан гри (Singleton)
│   │   └── constants.py      # Константи гри
│   ├── ui/                    # Графічний інтерфейс
│   │   ├── screens/          # Екрани гри
│   │   │   ├── main_menu.py
│   │   │   ├── game_screen.py
│   │   │   ├── shop_screen.py
│   │   │   ├── inventory_screen.py
│   │   │   └── settings_screen.py
│   │   └── components/       # UI компоненти
│   │       ├── button.py
│   │       ├── panel.py
│   │       ├── progress_bar.py
│   │       └── ...
│   └── main.py               # Точка входу
├── backend/                    # C++ бекенд (опціонально)
│   ├── include/              # Заголовні файли
│   └── src/                  # Реалізація
├── requirements.txt           # Залежності Python
└── README.md                  # Документація
```

---

## Принципи ООП реалізовані в проекті

### 1. Інкапсуляція
- Приховування внутрішньої реалізації класів
- Використання `@property` декораторів
- Private атрибути з `_` префіксом

### 2. Наслідування  
- Базовий клас `AnimalData` → спеціалізовані типи
- Ієрархія UI компонентів: `Button` → `IconButton`, `ImageButton`
- `ProgressBar` → `HealthBar`, `HungerBar`, `HappinessBar`

### 3. Поліморфізм
- Віртуальні методи `handle_event()`, `update()`, `draw()` для всіх екранів
- Єдиний інтерфейс для різних типів тварин
- Фабричний метод для створення тварин

### 4. Абстракція
- Абстрактні екрани з обов'язковими методами
- Інтерфейс `Storage` для різних типів сховищ
- Шаблони дизайну: Singleton, Factory, Observer


## Встановлення та запуск

### Крок 1: Клонування або завантаження
```bash
cd FarmGame
```

### Крок 2: Створення віртуального середовища (рекомендовано)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# або
source venv/bin/activate  # Linux/macOS
```

### Крок 3: Встановлення залежностей
```bash
pip install -r requirements.txt
```

### Крок 4: Запуск гри
```bash
cd frontend
python main.py
```

---