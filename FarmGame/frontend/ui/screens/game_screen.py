"""
Головний ігровий екран
"""

import pygame
import math
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES,
    ANIMAL_TYPES, SEASONS, WEATHER_TYPES, get_font, get_emoji_font
)
from game.game_state import GameState, AnimalData
from ..components.button import Button, IconButton
from ..components.panel import Panel
from ..components.progress_bar import ProgressBar, EnergyBar
from ..components.text import Text
from ..components.animal_card import AnimalCard
from ..components.notification import NotificationManager


class GameScreen:
    """
    Головний ігровий екран з усіма панелями та елементами
    """
    
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_state = GameState()
        
        # Менеджер сповіщень
        self.notification_manager = NotificationManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Скроллінг списку тварин
        self.animal_scroll_offset = 0
        self.max_scroll = 0
        
        # Вибрана тварина
        self.selected_animal: Optional[AnimalData] = None
        
        # Анімаційний час
        self.time = 0.0
        
        self._create_ui()
    
    def _create_ui(self):
        """Створення UI елементів"""
        # ===== Верхня панель (статус) =====
        self.top_panel = Panel(
            0, 0, SCREEN_WIDTH, 70,
            color=COLORS["panel_dark"],
            border_radius=0,
            shadow=False
        )
        
        # ===== Ліва панель (тварини) =====
        self.animals_panel = Panel(
            10, 80, 350, SCREEN_HEIGHT - 90,
            header="Tварини",
            header_color=COLORS["primary"]
        )
        
        # ===== Права панель (дії) =====
        self.actions_panel = Panel(
            SCREEN_WIDTH - 260, 80, 250, 300,
            header="Дії",
            header_color=COLORS["secondary"]
        )
        
        # ===== Панель інформації про вибрану тварину =====
        self.info_panel = Panel(
            SCREEN_WIDTH - 260, 400, 250, SCREEN_HEIGHT - 410,
            header="Інформація",
            header_color=COLORS["info"]
        )
        
        # ===== Кнопки навігації =====
        button_y = 15
        
        self.btn_shop = Button(
            SCREEN_WIDTH - 480, button_y, 100, 40,
            "Магазин",
            self._on_shop,
            color=COLORS["success"]
        )
        
        self.btn_inventory = Button(
            SCREEN_WIDTH - 370, button_y, 110, 40,
            "Інвентар",
            self._on_inventory,
            color=COLORS["warning"]
        )
        
        self.btn_settings = IconButton(
            SCREEN_WIDTH - 160, button_y, 40, "S",
            self._on_settings,
            color=COLORS["gray"],
            tooltip="Налаштування"
        )
        
        self.btn_save = IconButton(
            SCREEN_WIDTH - 110, button_y, 40, "Z",  # З для Зберегти або S для Save (але S вже зайнято)
            self._on_save,
            color=COLORS["info"],
            tooltip="Зберегти гру"
        )
        
        self.btn_menu = IconButton(
            SCREEN_WIDTH - 60, button_y, 40, "M",  # M для Меню
            self._on_menu,
            color=COLORS["secondary"],
            tooltip="Головне меню"
        )
        
        # ===== Кнопки швидких дій =====
        action_content = self.actions_panel.get_content_rect()
        
        self.btn_feed_all = Button(
            action_content.x, action_content.y,
            action_content.width, 45,
            "Погодувати всіх",
            self._on_feed_all,
            color=COLORS["warning"]
        )
        
        self.btn_collect_all = Button(
            action_content.x, action_content.y + 55,
            action_content.width, 45,
            "Зібрати все",
            self._on_collect_all,
            color=COLORS["success"]
        )
        
        self.btn_sell_products = Button(
            action_content.x, action_content.y + 110,
            action_content.width, 45,
            "Продати продукцію",
            self._on_sell_products,
            color=COLORS["primary"]
        )
        
        self.btn_heal_all = Button(
            action_content.x, action_content.y + 165,
            action_content.width, 45,
            "Лікувати хворих",
            self._on_heal_all,
            color=COLORS["danger"]
        )
        
        # ===== Бар енергії =====
        self.energy_bar = EnergyBar(
            action_content.x, action_content.y + 220,
            action_content.width, 25,
            self.game_state.farmer.energy
        )
        
        # ===== Картки тварин =====
        self.animal_cards: List[AnimalCard] = []
        self._refresh_animal_cards()
    
    def _refresh_animal_cards(self):
        """Оновити список карток тварин"""
        self.animal_cards.clear()
        
        content_rect = self.animals_panel.get_content_rect()
        card_width = content_rect.width - 20
        card_height = 180  # Збільшено з 150 для кращого відображення
        card_spacing = 10
        
        for i, animal in enumerate(self.game_state.animals):
            if not animal.is_alive:
                continue
            
            y = content_rect.y + i * (card_height + card_spacing) - self.animal_scroll_offset
            
            card = AnimalCard(
                content_rect.x + 5,
                y,
                card_width,
                card_height,
                animal,
                on_click=self._on_animal_click,
                on_feed=self._on_feed_animal,
                on_collect=self._on_collect_animal
            )
            self.animal_cards.append(card)
        
        # Обчислюємо максимальний скрол
        total_height = len(self.animal_cards) * (card_height + card_spacing)
        self.max_scroll = max(0, total_height - content_rect.height + 50)
    
    # ===== Обробники подій =====
    
    def _on_shop(self):
        self.game_engine.change_screen("shop")
    
    def _on_inventory(self):
        self.game_engine.change_screen("inventory")
    
    def _on_settings(self):
        self.game_engine.change_screen("settings")
    
    def _on_save(self):
        if self.game_state.save_game():
            self.notification_manager.add_success("Збережено", "Гру успішно збережено!")
        else:
            self.notification_manager.add_error("Помилка", "Не вдалося зберегти гру")
    
    def _on_menu(self):
        # Автозбереження
        self.game_state.save_game()
        self.game_engine.change_screen("main_menu")
    
    def _on_feed_all(self):
        count = self.game_state.feed_all_animals()
        if count > 0:
            self.notification_manager.add_success("Годування", f"Погодовано {count} тварин!")
        else:
            self.notification_manager.add_warning("Годування", "Немає голодних тварин або корму")
    
    def _on_collect_all(self):
        count = self.game_state.collect_all_products()
        if count > 0:
            self.notification_manager.add_success("Збір", f"Зібрано продукцію від {count} тварин!")
        else:
            self.notification_manager.add_info("Збір", "Немає продукції для збору")
    
    def _on_sell_products(self):
        total = self.game_state.sell_all_products()
        if total > 0:
            self.notification_manager.add_success("Продаж", f"Продано на {total:.0f} грн!")
        else:
            self.notification_manager.add_info("Продаж", "Немає продукції для продажу")
    
    def _on_heal_all(self):
        healed = 0
        total_cost = 0
        
        for animal in self.game_state.animals:
            if animal.is_alive and animal.health < 50:
                cost = self.game_state.heal_animal(animal.id)
                if cost > 0:
                    healed += 1
                    total_cost += cost
        
        if healed > 0:
            self.notification_manager.add_success("Лікування", f"Вилікувано {healed} тварин за {total_cost:.0f} грн")
        else:
            self.notification_manager.add_info("Лікування", "Немає хворих тварин")
    
    def _on_animal_click(self, card: AnimalCard):
        self.selected_animal = card.animal
        for c in self.animal_cards:
            c.selected = (c.animal.id == card.animal.id)
    
    def _on_feed_animal(self, animal_id: int):
        # Автовибір корму
        for feed_type in self.game_state.feeds.keys():
            if self.game_state.feed_animal(animal_id, feed_type):
                animal = next((a for a in self.game_state.animals if a.id == animal_id), None)
                if animal:
                    self.notification_manager.add_success("Годування", f"{animal.name} погодовано!")
                return
        
        self.notification_manager.add_warning("Годування", "Немає корму!")
    
    def _on_collect_animal(self, animal_id: int):
        product = self.game_state.collect_product(animal_id)
        if product:
            animal = next((a for a in self.game_state.animals if a.id == animal_id), None)
            if animal:
                self.notification_manager.add_success("Збір", f"Зібрано продукцію від {animal.name}!")
        else:
            self.notification_manager.add_info("Збір", "Продукція ще не готова")
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій"""
        # Скролінг
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if self.animals_panel.rect.collidepoint(mouse_pos):
                self.animal_scroll_offset -= event.y * 30
                self.animal_scroll_offset = max(0, min(self.max_scroll, self.animal_scroll_offset))
                self._refresh_animal_cards()
        
        # Кнопки навігації
        if self.btn_shop.handle_event(event): return
        if self.btn_inventory.handle_event(event): return
        if self.btn_settings.handle_event(event): return
        if self.btn_save.handle_event(event): return
        if self.btn_menu.handle_event(event): return
        
        # Кнопки дій
        if self.btn_feed_all.handle_event(event): return
        if self.btn_collect_all.handle_event(event): return
        if self.btn_sell_products.handle_event(event): return
        if self.btn_heal_all.handle_event(event): return
        
        # Картки тварин
        for card in self.animal_cards:
            card.handle_event(event)
        
        # ESC - пауза
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_engine.toggle_pause()
    
    def update(self, dt: float):
        """Оновлення"""
        self.time += dt
        
        # Оновлення ігрового стану
        self.game_state.update(dt)
        
        # Оновлення сповіщень
        self.notification_manager.update(dt)
        
        # Синхронізуємо сповіщення з game_state
        while self.game_state.notifications:
            notif = self.game_state.notifications.pop(0)
            self.notification_manager.add_info(notif['title'], notif['message'])
        
        # Оновлення енергії
        self.energy_bar.set_value(self.game_state.farmer.energy)
        self.energy_bar.update(dt)
        
        # Оновлення кнопок
        self.btn_shop.update(dt)
        self.btn_inventory.update(dt)
        self.btn_settings.update(dt)
        self.btn_save.update(dt)
        self.btn_menu.update(dt)
        
        self.btn_feed_all.update(dt)
        self.btn_collect_all.update(dt)
        self.btn_sell_products.update(dt)
        self.btn_heal_all.update(dt)
        
        # Оновлення карток
        for card in self.animal_cards:
            # Синхронізуємо дані
            animal = next((a for a in self.game_state.animals if a.id == card.animal.id), None)
            if animal:
                card.set_animal(animal)
            card.update(dt)
        
        # Періодичне оновлення списку
        if int(self.time) % 5 == 0 and self.time - int(self.time) < dt:
            self._refresh_animal_cards()
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Фон
        self._draw_background(surface)
        
        # Панелі
        self.top_panel.draw(surface)
        self.animals_panel.draw(surface)
        self.actions_panel.draw(surface)
        self.info_panel.draw(surface)
        
        # Верхня панель - інформація
        self._draw_top_bar(surface)
        
        # Кнопки навігації
        self.btn_shop.draw(surface)
        self.btn_inventory.draw(surface)
        self.btn_settings.draw(surface)
        self.btn_save.draw(surface)
        self.btn_menu.draw(surface)
        
        # Кнопки дій
        self.btn_feed_all.draw(surface)
        self.btn_collect_all.draw(surface)
        self.btn_sell_products.draw(surface)
        self.btn_heal_all.draw(surface)
        
        # Енергія
        self.energy_bar.draw(surface)
        
        # Картки тварин (з відсіканням)
        self._draw_animal_cards(surface)
        
        # Інформація про вибрану тварину
        self._draw_selected_animal_info(surface)
        
        # Сповіщення
        self.notification_manager.draw(surface)
    
    def _draw_background(self, surface: pygame.Surface):
        """Відмальовка фону"""
        # Основний колір
        surface.fill(COLORS["background"])
        
        # Декоративні елементи
        season = self.game_state.current_season
        season_color = SEASONS[season]["color"]
        
        # Градієнт знизу
        gradient_rect = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
        for y in range(gradient_rect.height):
            alpha = int(50 * (y / gradient_rect.height))
            color = (*season_color, alpha)
            line_surface = pygame.Surface((SCREEN_WIDTH, 1), pygame.SRCALPHA)
            line_surface.fill(color)
            surface.blit(line_surface, (0, SCREEN_HEIGHT - 200 + y))
    
    def _draw_top_bar(self, surface: pygame.Surface):
        """Відмальовка верхньої панелі"""
        font = get_font(FONT_SIZES["normal"], bold=True)
        small_font = get_font(FONT_SIZES["small"])
        
        x = 20
        y = 15
        
        # Гроші
        money_text = font.render(f"{self.game_state.farmer.money:.0f} грн", True, COLORS["success"])
        surface.blit(money_text, (x, y))
        
        # День
        x += 150
        day_text = font.render(f"День {self.game_state.current_day}", True, COLORS["text"])
        surface.blit(day_text, (x, y))
        
        # Час
        x += 100
        hour = self.game_state.current_hour
        time_text = font.render(f"{hour:02d}:00", True, COLORS["text"])
        surface.blit(time_text, (x, y))
        
        # Сезон
        x += 80
        season = self.game_state.current_season
        season_info = SEASONS[season]
        season_text = font.render(f"{season_info['name']}", True, season_info["color"])
        surface.blit(season_text, (x, y))
        
        # Погода
        x += 100
        weather = self.game_state.current_weather
        weather_info = WEATHER_TYPES[weather]
        weather_text = font.render(f"{weather_info['name']}", True, COLORS["text"])
        surface.blit(weather_text, (x, y))
        
        # Кількість тварин
        x += 100
        living = self.game_state.get_living_animals_count()
        capacity = self.game_state.get_total_capacity()
        animals_text = font.render(f"{living}/{capacity}", True, COLORS["text"])
        surface.blit(animals_text, (x, y))
        
        # Друга лінія
        x = 20
        y += 30
        
        # Ім'я фермера
        farmer_text = small_font.render(f"{self.game_state.farmer.name}", True, COLORS["text_secondary"])
        surface.blit(farmer_text, (x, y))
        
        # Рівень
        x += 150
        level_text = small_font.render(f"Рівень {self.game_state.farmer.level}", True, COLORS["text_secondary"])
        surface.blit(level_text, (x, y))
    
    def _draw_animal_cards(self, surface: pygame.Surface):
        """Відмальовка карток тварин з відсіканням"""
        content_rect = self.animals_panel.get_content_rect()
        
        # Створюємо область відсікання
        clip_rect = pygame.Rect(content_rect.x, content_rect.y, content_rect.width, content_rect.height)
        old_clip = surface.get_clip()
        surface.set_clip(clip_rect)
        
        for card in self.animal_cards:
            # Малюємо тільки видимі картки
            if card.rect.bottom > content_rect.top and card.rect.top < content_rect.bottom:
                card.draw(surface)
        
        surface.set_clip(old_clip)
        
        # Індикатор скролу
        if self.max_scroll > 0:
            scroll_height = max(30, content_rect.height * content_rect.height // (content_rect.height + self.max_scroll))
            scroll_y = content_rect.y + int((self.animal_scroll_offset / self.max_scroll) * (content_rect.height - scroll_height))
            
            pygame.draw.rect(surface, COLORS["gray"], 
                           (content_rect.right - 5, scroll_y, 4, scroll_height),
                           border_radius=2)
    
    def _draw_selected_animal_info(self, surface: pygame.Surface):
        """Інформація про вибрану тварину"""
        content_rect = self.info_panel.get_content_rect()
        font = get_font(FONT_SIZES["small"])
        
        if not self.selected_animal:
            text = font.render("Виберіть тварину", True, COLORS["text_secondary"])
            text_rect = text.get_rect(center=(content_rect.centerx, content_rect.centery))
            surface.blit(text, text_rect)
            return
        
        animal = self.selected_animal
        animal_info = ANIMAL_TYPES.get(animal.animal_type, {})
        
        y = content_rect.y + 10
        x = content_rect.x + 10
        line_height = 22
        
        # Emoji та ім'я
        emoji_font = get_emoji_font(32)
        emoji_surface = emoji_font.render(animal_info.get('emoji', '🐾'), True, COLORS["text"])
        surface.blit(emoji_surface, (x, y))
        
        name_font = get_font(FONT_SIZES["normal"], bold=True)
        name_surface = name_font.render(animal.name, True, COLORS["text"])
        surface.blit(name_surface, (x + 45, y + 5))
        
        y += 50
        
        # Інформація
        info_lines = [
            f"Тип: {animal_info.get('name', animal.animal_type)}",
            f"Вік: {animal.age} днів",
            f"Здоров'я: {animal.health:.0f}%",
            f"Голод: {animal.hunger:.0f}%",
            f"Щастя: {animal.happiness:.0f}%",
            f"Днів на фермі: {animal.days_on_farm}",
            f"Разів погодовано: {animal.total_fed}",
            f"Продукції зібрано: {animal.total_produced}"
        ]
        
        for line in info_lines:
            text = font.render(line, True, COLORS["text"])
            surface.blit(text, (x, y))
            y += line_height
