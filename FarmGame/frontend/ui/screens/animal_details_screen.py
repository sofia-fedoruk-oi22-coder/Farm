"""
Екран деталей тварини
"""

import pygame
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONT_SIZES,
    ANIMAL_TYPES, FEED_TYPES, get_font, get_emoji_font
)
from game.game_state import GameState, AnimalData
from ..components.button import Button
from ..components.panel import Panel
from ..components.progress_bar import HealthBar, HungerBar, HappinessBar
from ..components.text import Text
from ..components.notification import NotificationManager


class AnimalDetailsScreen:
    """
    Детальна інформація про тварину
    """
    
    def __init__(self, game_engine, animal_id: int = None):
        self.game_engine = game_engine
        self.game_state = GameState()
        self.animal_id = animal_id
        
        # Менеджер сповіщень
        self.notification_manager = NotificationManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self._create_ui()
    
    def set_animal(self, animal_id: int):
        """Встановити тварину для перегляду"""
        self.animal_id = animal_id
        self._create_ui()
    
    @property
    def animal(self) -> Optional[AnimalData]:
        """Отримати поточну тварину"""
        if self.animal_id is None:
            return None
        return next((a for a in self.game_state.animals if a.id == self.animal_id), None)
    
    def _create_ui(self):
        """Створення UI"""
        center_x = SCREEN_WIDTH // 2
        
        # Головна панель
        panel_width = 700
        panel_height = 550
        self.main_panel = Panel(
            center_x - panel_width // 2,
            SCREEN_HEIGHT // 2 - panel_height // 2,
            panel_width,
            panel_height,
            color=COLORS["panel"]
        )
        
        content_rect = self.main_panel.get_content_rect()
        
        # Кнопка назад
        self.btn_back = Button(
            content_rect.x + 10,
            content_rect.y + 10,
            100, 40,
            "← Назад",
            self._on_back,
            color=COLORS["gray"]
        )
        
        # Кнопки дій
        action_y = content_rect.y + panel_height - 150
        button_width = (panel_width - 80) // 4
        
        self.btn_feed = Button(
            content_rect.x + 10,
            action_y,
            button_width, 50,
            "🍽️ Годувати",
            self._on_feed,
            color=COLORS["warning"]
        )
        
        self.btn_collect = Button(
            content_rect.x + 20 + button_width,
            action_y,
            button_width, 50,
            "📦 Зібрати",
            self._on_collect,
            color=COLORS["success"]
        )
        
        self.btn_pet = Button(
            content_rect.x + 30 + button_width * 2,
            action_y,
            button_width, 50,
            "❤️ Погладити",
            self._on_pet,
            color=COLORS["info"]
        )
        
        self.btn_heal = Button(
            content_rect.x + 40 + button_width * 3,
            action_y,
            button_width, 50,
            "💊 Лікувати",
            self._on_heal,
            color=COLORS["danger"]
        )
        
        # Кнопка продажу
        self.btn_sell = Button(
            content_rect.x + 10,
            action_y + 60,
            panel_width - 40, 45,
            "💰 Продати тварину",
            self._on_sell,
            color=COLORS["danger"]
        )
        
        # Прогрес бари
        bar_x = content_rect.x + 200
        bar_y = content_rect.y + 200
        bar_width = panel_width - 250
        
        self.health_bar = HealthBar(bar_x, bar_y, bar_width, 25)
        self.hunger_bar = HungerBar(bar_x, bar_y + 40, bar_width, 25)
        self.happiness_bar = HappinessBar(bar_x, bar_y + 80, bar_width, 25)
    
    def _on_back(self):
        self.game_engine.change_screen("game")
    
    def _on_feed(self):
        if not self.animal:
            return
        
        # Автовибір корму
        for feed_type in self.game_state.feeds.keys():
            if self.game_state.feed_animal(self.animal_id, feed_type):
                self.notification_manager.add_success("Годування", f"{self.animal.name} погодовано!")
                return
        
        self.notification_manager.add_warning("Помилка", "Немає корму!")
    
    def _on_collect(self):
        if not self.animal:
            return
        
        product = self.game_state.collect_product(self.animal_id)
        if product:
            self.notification_manager.add_success("Збір", f"Зібрано продукцію!")
        else:
            self.notification_manager.add_info("Збір", "Продукція ще не готова")
    
    def _on_pet(self):
        if not self.animal:
            return
        
        self.game_state.pet_animal(self.animal_id)
        self.notification_manager.add_success("Увага", f"{self.animal.name} щасливіший!")
    
    def _on_heal(self):
        if not self.animal:
            return
        
        cost = self.game_state.heal_animal(self.animal_id)
        if cost > 0:
            self.notification_manager.add_success("Лікування", f"{self.animal.name} вилікувано!")
        else:
            self.notification_manager.add_info("Лікування", "Тварина здорова")
    
    def _on_sell(self):
        if not self.animal:
            return
        
        price = self.game_state.sell_animal(self.animal_id)
        if price > 0:
            self.notification_manager.add_success("Продаж", f"Продано за {price:.0f} грн!")
            self._on_back()
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій"""
        self.btn_back.handle_event(event)
        self.btn_feed.handle_event(event)
        self.btn_collect.handle_event(event)
        self.btn_pet.handle_event(event)
        self.btn_heal.handle_event(event)
        self.btn_sell.handle_event(event)
        
        # ESC - назад
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._on_back()
    
    def update(self, dt: float):
        """Оновлення"""
        self.btn_back.update(dt)
        self.btn_feed.update(dt)
        self.btn_collect.update(dt)
        self.btn_pet.update(dt)
        self.btn_heal.update(dt)
        self.btn_sell.update(dt)
        
        # Оновлення барів
        if self.animal:
            self.health_bar.set_value(self.animal.health)
            self.hunger_bar.set_value(self.animal.hunger)
            self.happiness_bar.set_value(self.animal.happiness)
        
        self.health_bar.update(dt)
        self.hunger_bar.update(dt)
        self.happiness_bar.update(dt)
        
        self.notification_manager.update(dt)
        
        # Синхронізація сповіщень
        while self.game_state.notifications:
            notif = self.game_state.notifications.pop(0)
            self.notification_manager.add_info(notif['title'], notif['message'])
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        # Фон
        surface.fill(COLORS["background"])
        
        # Панель
        self.main_panel.draw(surface)
        
        content_rect = self.main_panel.get_content_rect()
        
        # Кнопка назад
        self.btn_back.draw(surface)
        
        if not self.animal:
            font = get_font(FONT_SIZES["large"])
            text = font.render("Тварину не знайдено", True, COLORS["text_secondary"])
            text_rect = text.get_rect(center=(content_rect.centerx, content_rect.centery))
            surface.blit(text, text_rect)
            return
        
        animal = self.animal
        animal_info = ANIMAL_TYPES.get(animal.animal_type, {})
        
        # Emoji тварини (великий)
        emoji_font = get_emoji_font(72)
        emoji = animal_info.get('emoji', '🐾')
        emoji_surface = emoji_font.render(emoji, True, COLORS["text"])
        surface.blit(emoji_surface, (content_rect.x + 30, content_rect.y + 60))
        
        # Ім'я та тип
        title_font = get_font(FONT_SIZES["huge"], bold=True)
        name_surface = title_font.render(animal.name, True, COLORS["text"])
        surface.blit(name_surface, (content_rect.x + 150, content_rect.y + 60))
        
        type_font = get_font(FONT_SIZES["large"])
        type_surface = type_font.render(animal_info.get('name', animal.animal_type), True, COLORS["text_secondary"])
        surface.blit(type_surface, (content_rect.x + 150, content_rect.y + 110))
        
        # Статус
        status_text = "🟢 Живий" if animal.is_alive else "🔴 Мертвий"
        status_color = COLORS["success"] if animal.is_alive else COLORS["danger"]
        status_font = get_font(FONT_SIZES["normal"], bold=True)
        status_surface = status_font.render(status_text, True, status_color)
        surface.blit(status_surface, (content_rect.x + 150, content_rect.y + 145))
        
        # Прогрес бари
        bar_x = content_rect.x + 200
        bar_y = content_rect.y + 200
        
        label_font = get_font(FONT_SIZES["normal"])
        
        # Здоров'я
        health_label = label_font.render("❤️ Здоров'я:", True, COLORS["text"])
        surface.blit(health_label, (content_rect.x + 30, bar_y))
        self.health_bar.draw(surface)
        
        # Голод
        emoji_font_normal = get_font(FONT_SIZES["normal"])
        hunger_label = emoji_font_normal.render("🍽️ Ситість:", True, COLORS["text"])
        surface.blit(hunger_label, (content_rect.x + 30, bar_y + 40))
        self.hunger_bar.draw(surface)
        
        # Щастя
        happiness_label = label_font.render("😊 Щастя:", True, COLORS["text"])
        surface.blit(happiness_label, (content_rect.x + 30, bar_y + 80))
        self.happiness_bar.draw(surface)
        
        # Статистика
        stats_y = bar_y + 130
        small_font = get_font(FONT_SIZES["small"])
        emoji_font_small = get_font(FONT_SIZES["small"])
        
        stats = [
            f"📅 Вік: {animal.age} днів",
            f"🏠 Днів на фермі: {animal.days_on_farm}",
            f"🍽️ Разів погодовано: {animal.total_fed}",
            f"📦 Продукції зібрано: {animal.total_produced}",
            f"⏳ Кулдаун: {animal.production_cooldown} год."
        ]
        
        for i, stat in enumerate(stats):
            stat_surface = emoji_font_small.render(stat, True, COLORS["text"])
            x = content_rect.x + 30 + (i % 2) * 300
            y = stats_y + (i // 2) * 25
            surface.blit(stat_surface, (x, y))
        
        # Кнопки дій
        self.btn_feed.draw(surface)
        self.btn_collect.draw(surface)
        self.btn_pet.draw(surface)
        self.btn_heal.draw(surface)
        self.btn_sell.draw(surface)
        
        # Сповіщення
        self.notification_manager.draw(surface)
