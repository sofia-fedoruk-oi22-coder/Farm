"""
Константи гри
"""

# Інформація про гру
GAME_TITLE = "Ферма"
GAME_SUBTITLE = "Курсова робота з ООП"
VERSION = "1.0.0"

# Розміри екрану
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Кольори
COLORS = {
    "background": (135, 206, 235),      # Небесно-блакитний
    "grass": (34, 139, 34),             # Зелена трава
    "dirt": (139, 90, 43),              # Земля
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (220, 20, 60),
    "green": (50, 205, 50),
    "blue": (65, 105, 225),
    "yellow": (255, 215, 0),
    "orange": (255, 165, 0),
    "brown": (139, 69, 19),
    "gray": (128, 128, 128),
    "light_gray": (200, 200, 200),
    "dark_gray": (64, 64, 64),
    "gold": (255, 215, 0),
    "wood": (160, 82, 45),
    
    # Кольори UI
    "panel": (245, 245, 220),            # Бежевий
    "panel_light": (255, 250, 240),      # Світлий бежевий
    "panel_dark": (210, 180, 140),       # Темний бежевий
    "button": (100, 149, 237),           # Васильковий
    "button_hover": (65, 105, 225),      # Синій
    "button_text": (255, 255, 255),
    "text": (51, 51, 51),
    "text_secondary": (102, 102, 102),
    "text_light": (200, 200, 200),
    
    # Акценти
    "accent": (76, 175, 80),              # Зелений акцент
    "accent_light": (129, 199, 132),      # Світло-зелений
    "accent_dark": (56, 142, 60),         # Темно-зелений
    "primary": (100, 149, 237),           # Основний колір (васильковий)
    "primary_light": (130, 170, 255),     # Світло-синій
    "primary_dark": (65, 105, 225),       # Темно-синій
    "secondary": (255, 193, 7),           # Жовтий
    "secondary_light": (255, 224, 130),   # Світло-жовтий
    "secondary_dark": (255, 160, 0),      # Темно-жовтий
    
    # Кольори станів
    "health": (220, 20, 60),
    "hunger": (255, 165, 0),
    "happiness": (255, 215, 0),
    "energy": (30, 144, 255),
    
    # Сповіщення
    "success": (76, 175, 80),
    "warning": (255, 152, 0),
    "error": (244, 67, 54),
    "danger": (244, 67, 54),        # Те саме що error
    "info": (33, 150, 243),
    
    # Сезони
    "spring": (144, 238, 144),
    "summer": (255, 255, 102),
    "autumn": (255, 165, 0),
    "winter": (240, 248, 255),
    
    # Інші
    "transparent": (0, 0, 0, 0),
    "overlay": (0, 0, 0, 128),
    "shadow": (0, 0, 0, 64),
    "border": (139, 90, 43),
    "selected": (100, 200, 255),
    "dark": (30, 30, 30),
    "light": (250, 250, 250)
}

# Розміри тайлів
TILE_SIZE = 64

# Типи тварин
ANIMAL_TYPES = {
    "cow": {
        "name": "Корова",
        "emoji": "🐄",
        "price": 15000,
        "product": "Молоко",
        "product_emoji": "🥛"
    },
    "chicken": {
        "name": "Курка",
        "emoji": "🐔",
        "price": 150,
        "product": "Яйця",
        "product_emoji": "🥚"
    },
    "pig": {
        "name": "Свиня",
        "emoji": "🐷",
        "price": 3000,
        "product": "Сало",
        "product_emoji": "🥓"
    },
    "sheep": {
        "name": "Вівця",
        "emoji": "🐑",
        "price": 2000,
        "product": "Вовна",
        "product_emoji": "🧶"
    },
    "goat": {
        "name": "Коза",
        "emoji": "🐐",
        "price": 1800,
        "product": "Козине молоко",
        "product_emoji": "🥛"
    },
    "duck": {
        "name": "Качка",
        "emoji": "🦆",
        "price": 100,
        "product": "Качині яйця",
        "product_emoji": "🥚"
    },
    "rabbit": {
        "name": "Кролик",
        "emoji": "🐰",
        "price": 200,
        "product": "Хутро",
        "product_emoji": "🧥"
    },
    "horse": {
        "name": "Кінь",
        "emoji": "🐴",
        "price": 25000,
        "product": "Робота",
        "product_emoji": "⚙️"
    }
}

# Типи кормів
FEED_TYPES = {
    "hay": {"name": "Сіно", "emoji": "🌾", "price": 10, "nutrition": 25},
    "grain": {"name": "Зерно", "emoji": "🌾", "price": 15, "nutrition": 30},
    "corn": {"name": "Кукурудза", "emoji": "🌽", "price": 12, "nutrition": 28},
    "mixed": {"name": "Комбікорм", "emoji": "🥣", "price": 25, "nutrition": 40},
    "grass": {"name": "Трава", "emoji": "🌿", "price": 5, "nutrition": 15},
    "vegetables": {"name": "Овочі", "emoji": "🥕", "price": 20, "nutrition": 35},
    "oats": {"name": "Овес", "emoji": "🌾", "price": 18, "nutrition": 32},
    "carrots": {"name": "Морква", "emoji": "🥕", "price": 8, "nutrition": 20},
    "premium": {"name": "Преміум корм", "emoji": "⭐", "price": 50, "nutrition": 50}
}

# Сезони
SEASONS = {
    "spring": {"name": "Весна", "emoji": "🌸", "days": 30, "color": (144, 238, 144)},
    "summer": {"name": "Літо", "emoji": "☀️", "days": 30, "color": (255, 255, 102)},
    "autumn": {"name": "Осінь", "emoji": "🍂", "days": 30, "color": (255, 165, 0)},
    "winter": {"name": "Зима", "emoji": "❄️", "days": 30, "color": (240, 248, 255)}
}

# Погода
WEATHER_TYPES = {
    "sunny": {"name": "Сонячно", "emoji": "☀️"},
    "cloudy": {"name": "Хмарно", "emoji": "☁️"},
    "rainy": {"name": "Дощ", "emoji": "🌧️"},
    "stormy": {"name": "Шторм", "emoji": "⛈️"},
    "snowy": {"name": "Сніг", "emoji": "🌨️"},
    "foggy": {"name": "Туман", "emoji": "🌫️"}
}

# Будівлі
BUILDING_TYPES = {
    "barn": {
        "name": "Сарай",
        "emoji": "🏠",
        "base_capacity": 10,
        "base_cost": 5000,
        "upgrade_cost_multiplier": 1.5
    },
    "coop": {
        "name": "Курник",
        "emoji": "🏡",
        "base_capacity": 20,
        "base_cost": 2000,
        "upgrade_cost_multiplier": 1.4
    },
    "stable": {
        "name": "Хлів",
        "emoji": "🏚️",
        "base_capacity": 5,
        "base_cost": 8000,
        "upgrade_cost_multiplier": 1.6
    },
    "warehouse": {
        "name": "Склад",
        "emoji": "🏭",
        "base_capacity": 100,
        "base_cost": 3000,
        "upgrade_cost_multiplier": 1.3
    },
    "refrigerator": {
        "name": "Холодильник",
        "emoji": "❄️",
        "base_capacity": 50,
        "base_cost": 10000,
        "upgrade_cost_multiplier": 1.5
    }
}

# Досягнення
ACHIEVEMENTS = {
    "first_animal": {
        "name": "Перший друг",
        "description": "Купіть свою першу тварину",
        "reward": 100
    },
    "ten_animals": {
        "name": "Маленька ферма",
        "description": "Маєте 10 тварин на фермі",
        "reward": 500
    },
    "fifty_animals": {
        "name": "Велика ферма",
        "description": "Маєте 50 тварин на фермі",
        "reward": 2000
    },
    "first_sale": {
        "name": "Перший продаж",
        "description": "Продайте свою першу продукцію",
        "reward": 50
    },
    "rich_farmer": {
        "name": "Багатий фермер",
        "description": "Накопичіть 100,000 грн",
        "reward": 5000
    },
    "year_passed": {
        "name": "Рік на фермі",
        "description": "Проведіть цілий рік на фермі",
        "reward": 1000
    },
    "all_animals": {
        "name": "Ноїв ковчег",
        "description": "Маєте по одній тварині кожного типу",
        "reward": 3000
    },
    "happy_animals": {
        "name": "Щасливі тварини",
        "description": "Всі тварини мають щастя > 80%",
        "reward": 1500
    }
}

# Шрифти
FONT_SIZES = {
    "tiny": 14,
    "small": 18,
    "normal": 20,
    "medium": 24,
    "large": 32,
    "title": 48,
    "huge": 72
}

# Анімації
ANIMATION_SPEED = 0.1
FADE_SPEED = 5

# Звуки (шляхи до файлів)
SOUNDS = {
    "click": "assets/sounds/click.wav",
    "coin": "assets/sounds/coin.wav",
    "animal": "assets/sounds/animal.wav",
    "success": "assets/sounds/success.wav",
    "error": "assets/sounds/error.wav",
    "ambient": "assets/sounds/ambient.wav"
}

# Збереження
SAVE_FILE = "savegame.json"

# Шрифти з підтримкою кирилиці та емодзі
# На Windows найкраще використовувати Segoe UI для обох
UNIVERSAL_FONTS = [
    "Segoe UI",            # Windows - підтримує і кирилицю і багато емодзі
    "Arial Unicode MS",    # Універсальний 
    "DejaVu Sans",         # Linux
    "Noto Sans",           # Крос-платформний
    "Tahoma",              # Windows fallback
    "Ubuntu",              # Linux
    "Verdana",             # Має підтримку кирилиці
]

def get_font(size, bold=False):
    """Отримати шрифт з підтримкою кирилиці"""
    import pygame
    for font_name in UNIVERSAL_FONTS:
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            if font:
                return font
        except:
            continue
    # Fallback на системний шрифт
    return pygame.font.SysFont(None, size, bold=bold)

def get_emoji_font(size):
    """Отримати шрифт з підтримкою емодзі"""
    import pygame
    # Спочатку пробуємо спеціальні емодзі-шрифти
    emoji_fonts = [
        "Segoe UI Emoji",      # Windows - кольорові емодзі
        "Segoe UI Symbol",     # Windows - символи
        "Apple Color Emoji",   # macOS
        "Noto Color Emoji",    # Linux
    ]
    for font_name in emoji_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            if font:
                return font
        except:
            continue
    # Fallback на Segoe UI
    try:
        return pygame.font.SysFont("Segoe UI", size)
    except:
        pass
    return pygame.font.SysFont(None, size)
