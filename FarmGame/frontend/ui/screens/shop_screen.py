"""
Екран магазину
"""

import pygame
from typing import Dict, List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES,
    ANIMAL_TYPES, FEED_TYPES, get_font, get_emoji_font
)
from game.game_state import GameState
from ..components.button import Button, IconButton
from ..components.panel import Panel
from ..components.text import Text
from ..components.input_field import InputField
from ..components.notification import NotificationManager


class ShopScreen:
    """
    Магазин для купівлі тварин та кормів
    """
    
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_state = GameState()
        
        # Менеджер сповіщень
        self.notification_manager = NotificationManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Вкладка: animals або feeds
        self.current_tab = "animals"
        
        # Вибраний елемент
        self.selected_item: Optional[str] = None
        
        # Скролінг
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Для покупки тварини
        self.animal_name = ""
        
        # Шрифти
        self.title_font = get_font(FONT_SIZES["large"], bold=True)
        self.font = get_font(FONT_SIZES["medium"])
        self.emoji_font = get_emoji_font(48)
        
        self._create_ui()
    
    def _create_ui(self):
        """Створення UI"""
        # Верхня панель
        self.top_panel = Panel(
            0, 0, SCREEN_WIDTH, 70,
            color=COLORS["panel_dark"],
            border_radius=0,
            shadow=False
        )
        
        # Панель товарів
        self.items_panel = Panel(
            10, 80, SCREEN_WIDTH - 320, SCREEN_HEIGHT - 90,
            color=COLORS["panel"]
        )
        
        # Панель покупки
        self.buy_panel = Panel(
            SCREEN_WIDTH - 300, 80, 290, SCREEN_HEIGHT - 90,
            header="Покупка",
            header_color=COLORS["success"]
        )
        
        # Вкладки
        self.btn_animals_tab = Button(
            20, 15, 150, 40,
            "Тварини",
            lambda: self._set_tab("animals"),
            color=COLORS["primary"]
        )
        
        self.btn_feeds_tab = Button(
            180, 15, 150, 40,
            "Корми",
            lambda: self._set_tab("feeds"),
            color=COLORS["secondary"]
        )
        
        # Кнопка назад
        self.btn_back = Button(
            SCREEN_WIDTH - 130, 15, 120, 40,
            "← Назад",
            self._on_back,
            color=COLORS["gray"]
        )
        
        # Поле вводу імені тварини
        buy_content = self.buy_panel.get_content_rect()
        
        self.name_label = Text(
            buy_content.x + 10,
            buy_content.y + 200,
            "Ім'я тварини:",
            font_size=FONT_SIZES["small"]
        )
        
        self.name_input = InputField(
            buy_content.x + 10,
            buy_content.y + 225,
            buy_content.width - 20,
            40,
            placeholder="Введіть ім'я..."
        )
        
        # Кнопка купити
        self.btn_buy = Button(
            buy_content.x + 10,
            buy_content.y + buy_content.height - 120,
            buy_content.width - 20,
            50,
            "Купити",
            self._on_buy,
            color=COLORS["success"],
            font_size=FONT_SIZES["large"]
        )
        
        # Гроші
        self.money_font = get_font(FONT_SIZES["large"], bold=True)
        
        self._update_tab_buttons()
    
    def _set_tab(self, tab: str):
        """Змінити вкладку"""
        self.current_tab = tab
        self.selected_item = None
        self.scroll_offset = 0
        self._update_tab_buttons()
    
    def _update_tab_buttons(self):
        """Оновити стиль кнопок вкладок"""
        if self.current_tab == "animals":
            self.btn_animals_tab.color = COLORS["primary"]
            self.btn_animals_tab.border_width = 3
            self.btn_animals_tab.border_color = COLORS["white"]
            self.btn_feeds_tab.color = COLORS["secondary"]
            self.btn_feeds_tab.border_width = 0
        else:
            self.btn_animals_tab.color = COLORS["secondary"]
            self.btn_animals_tab.border_width = 0
            self.btn_feeds_tab.color = COLORS["primary"]
            self.btn_feeds_tab.border_width = 3
            self.btn_feeds_tab.border_color = COLORS["white"]
    
    def _on_back(self):
        """Повернутися до гри"""
        self.game_engine.change_screen("game")
    
    def _on_buy(self):
        """Купити вибраний товар"""
        if not self.selected_item:
            self.notification_manager.add_warning("Помилка", "Виберіть товар!")
            return
        
        if self.current_tab == "animals":
            self._buy_animal()
        else:
            self._buy_feed()
    
    def _buy_animal(self):
        """Купити тварину"""
        name = self.name_input.get_text().strip()
        if not name:
            name = f"{ANIMAL_TYPES[self.selected_item]['name']} #{len(self.game_state.animals) + 1}"
        
        animal = self.game_state.buy_animal(self.selected_item, name)
        
        if animal:
            self.notification_manager.add_success(
                "Покупка",
                f"Куплено {ANIMAL_TYPES[self.selected_item]['name']}: {name}!"
            )
            self.name_input.clear()
        else:
            self.notification_manager.add_error("Помилка", "Не вдалося купити тварину")
    
    def _buy_feed(self):
        """Купити корм"""
        amount = 10  # Купуємо по 10 кг
        
        if self.game_state.buy_feed(self.selected_item, amount):
            self.notification_manager.add_success(
                "Покупка",
                f"Куплено {amount} кг {FEED_TYPES[self.selected_item]['name']}!"
            )
        else:
            self.notification_manager.add_error("Помилка", "Не вдалося купити корм")
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій"""
        # Скролінг
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.items_panel.rect.collidepoint(mouse_pos):
                self.scroll_offset -= event.y * 30
                self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
        
        # Клік на товар
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.items_panel.rect.collidepoint(mouse_pos):
                self._handle_item_click(mouse_pos)
        
        # Кнопки
        self.btn_animals_tab.handle_event(event)
        self.btn_feeds_tab.handle_event(event)
        self.btn_back.handle_event(event)
        self.btn_buy.handle_event(event)
        
        # Поле вводу
        self.name_input.handle_event(event)
        
        # ESC - назад
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._on_back()
    
    def _handle_item_click(self, mouse_pos):
        """Обробка кліку на товар"""
        content_rect = self.items_panel.get_content_rect()
        
        items = ANIMAL_TYPES if self.current_tab == "animals" else FEED_TYPES
        
        card_height = 100
        card_spacing = 10
        cols = 3
        card_width = (content_rect.width - (cols + 1) * 10) // cols
        
        for i, item_id in enumerate(items.keys()):
            col = i % cols
            row = i // cols
            
            x = content_rect.x + 10 + col * (card_width + 10)
            y = content_rect.y + 10 + row * (card_height + card_spacing) - self.scroll_offset
            
            item_rect = pygame.Rect(x, y, card_width, card_height)
            
            if item_rect.collidepoint(mouse_pos) and y > content_rect.y - card_height:
                self.selected_item = item_id
                return
    
    def update(self, dt: float):
        """Оновлення"""
        # Кнопки
        self.btn_animals_tab.update(dt)
        self.btn_feeds_tab.update(dt)
        self.btn_back.update(dt)
        self.btn_buy.update(dt)
        
        # Поле вводу
        self.name_input.update(dt)
        
        # Сповіщення
        self.notification_manager.update(dt)
        
        # Синхронізація сповіщень
        while self.game_state.notifications:
            notif = self.game_state.notifications.pop(0)
            self.notification_manager.add_info(notif['title'], notif['message'])
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Фон
        surface.fill(COLORS["background"])
        
        # Панелі
        self.top_panel.draw(surface)
        self.items_panel.draw(surface)
        self.buy_panel.draw(surface)
        
        # Заголовок
        title_font = get_font(FONT_SIZES["huge"], bold=True)
        title = title_font.render("Магазин", True, COLORS["text"])
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 15))
        
        # Гроші
        money_font = get_font(FONT_SIZES["large"], bold=True)
        money_text = money_font.render(
            f"{self.game_state.farmer.money:.0f} грн",
            True, COLORS["success"]
        )
        surface.blit(money_text, (SCREEN_WIDTH - 300, 20))
        
        # Вкладки
        self.btn_animals_tab.draw(surface)
        self.btn_feeds_tab.draw(surface)
        self.btn_back.draw(surface)
        
        # Товари
        self._draw_items(surface)
        
        # Панель покупки
        self._draw_buy_panel(surface)
        
        # Сповіщення
        self.notification_manager.draw(surface)
    
    def _draw_items(self, surface: pygame.Surface):
        """Відмальовка товарів"""
        content_rect = self.items_panel.get_content_rect()
        
        items = ANIMAL_TYPES if self.current_tab == "animals" else FEED_TYPES
        
        card_height = 100
        card_spacing = 10
        cols = 3
        card_width = (content_rect.width - (cols + 1) * 10) // cols
        
        # Обчислюємо max_scroll
        rows = (len(items) + cols - 1) // cols
        total_height = rows * (card_height + card_spacing)
        self.max_scroll = max(0, total_height - content_rect.height + 20)
        
        # Відсікання
        old_clip = surface.get_clip()
        surface.set_clip(content_rect)
        
        font = get_font(FONT_SIZES["normal"], bold=True)
        small_font = get_font(FONT_SIZES["small"])
        emoji_font = get_emoji_font(28)
        
        for i, (item_id, item_info) in enumerate(items.items()):
            col = i % cols
            row = i // cols
            
            x = content_rect.x + 10 + col * (card_width + 10)
            y = content_rect.y + 10 + row * (card_height + card_spacing) - self.scroll_offset
            
            # Пропускаємо невидимі
            if y < content_rect.y - card_height or y > content_rect.bottom:
                continue
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            
            # Фон картки
            bg_color = COLORS["panel_dark"]
            if item_id == self.selected_item:
                bg_color = COLORS["primary_light"]
            
            pygame.draw.rect(surface, bg_color, card_rect, border_radius=10)
            pygame.draw.rect(surface, COLORS["border"], card_rect, width=2, border_radius=10)
            
            # Emoji
            emoji = item_info.get('emoji', '📦')
            emoji_surface = emoji_font.render(emoji, True, COLORS["text"])
            surface.blit(emoji_surface, (x + 10, y + 10))
            
            # Назва
            name = item_info.get('name', item_id)
            name_surface = font.render(name, True, COLORS["text"])
            surface.blit(name_surface, (x + 50, y + 10))
            
            # Ціна
            price = item_info.get('price', 0)
            price_color = COLORS["success"] if self.game_state.farmer.money >= price else COLORS["danger"]
            price_surface = small_font.render(f"{price} грн", True, price_color)
            surface.blit(price_surface, (x + 10, y + 40))
            
            # Додаткова інформація
            if self.current_tab == "animals":
                product = item_info.get('product', '')
                product_surface = small_font.render(f"{product}", True, COLORS["text_secondary"])
                surface.blit(product_surface, (x + 10, y + 60))
            else:
                nutrition = item_info.get('nutrition', 0)
                nutrition_surface = small_font.render(f"+{nutrition}", True, COLORS["text_secondary"])
                surface.blit(nutrition_surface, (x + 10, y + 60))
            
            # Індикатор вибору
            if item_id == self.selected_item:
                pygame.draw.rect(surface, COLORS["primary"], card_rect, width=3, border_radius=10)
        
        surface.set_clip(old_clip)
    
    def _draw_buy_panel(self, surface: pygame.Surface):
        """Відмальовка панелі покупки"""
        content_rect = self.buy_panel.get_content_rect()
        font = get_font(FONT_SIZES["normal"])
        small_font = get_font(FONT_SIZES["small"])
        emoji_font = get_emoji_font(48)
        
        if not self.selected_item:
            # Підказка
            hint = font.render("Виберіть товар", True, COLORS["text_secondary"])
            hint_rect = hint.get_rect(center=(content_rect.centerx, content_rect.centery))
            surface.blit(hint, hint_rect)
            return
        
        items = ANIMAL_TYPES if self.current_tab == "animals" else FEED_TYPES
        item_info = items.get(self.selected_item, {})
        
        y = content_rect.y + 10
        
        # Emoji
        emoji = item_info.get('emoji')
        emoji_surface = emoji_font.render(emoji, True, COLORS["text"])
        emoji_rect = emoji_surface.get_rect(centerx=content_rect.centerx)
        surface.blit(emoji_surface, (emoji_rect.x, y))
        
        y += 60
        
        # Назва
        name = item_info.get('name', self.selected_item)
        name_font = get_font(FONT_SIZES["large"], bold=True)
        name_surface = name_font.render(name, True, COLORS["text"])
        name_rect = name_surface.get_rect(centerx=content_rect.centerx)
        surface.blit(name_surface, (name_rect.x, y))
        
        y += 40
        
        # Ціна
        price = item_info.get('price', 0)
        price_color = COLORS["success"] if self.game_state.farmer.money >= price else COLORS["danger"]
        emoji_font_normal = get_font(FONT_SIZES["normal"])
        price_surface = emoji_font_normal.render(f"Ціна: {price} грн", True, price_color)
        price_rect = price_surface.get_rect(centerx=content_rect.centerx)
        surface.blit(price_surface, (price_rect.x, y))
        
        y += 30
        
        # Деталі
        emoji_font_small = get_font(FONT_SIZES["small"])
        if self.current_tab == "animals":
            product = item_info.get('product', '')
            product_emoji = item_info.get('product_emoji')
            detail_surface = emoji_font_small.render(f"Продукція: {product}", True, COLORS["text_secondary"])
        else:
            nutrition = item_info.get('nutrition', 0)
            detail_surface = emoji_font_small.render(f"Поживність: +{nutrition}", True, COLORS["text_secondary"])
        
        detail_rect = detail_surface.get_rect(centerx=content_rect.centerx)
        surface.blit(detail_surface, (detail_rect.x, y))
        
        # Поле імені (тільки для тварин)
        if self.current_tab == "animals":
            self.name_label.draw(surface)
            self.name_input.draw(surface)
        
        # Кнопка купити
        self.btn_buy.draw(surface)
