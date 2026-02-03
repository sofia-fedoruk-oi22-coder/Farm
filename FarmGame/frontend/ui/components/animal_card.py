"""
Картка тварини
"""

import pygame
from typing import Tuple, Callable, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, FONT_SIZES, ANIMAL_TYPES, get_font, get_emoji_font
from game.game_state import AnimalData


class AnimalCard:
    """
    Картка для відображення інформації про тварину
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        animal: AnimalData,
        on_click: Callable[['AnimalCard'], None] = None,
        on_feed: Callable[[int], None] = None,
        on_collect: Callable[[int], None] = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.animal = animal
        self.on_click = on_click
        self.on_feed = on_feed
        self.on_collect = on_collect
        
        # Стан
        self.hovered = False
        self.selected = False
        
        # Анімація
        self.scale = 1.0
        self.target_scale = 1.0
        self.animation_time = 0.0
        
        # Шрифти
        self.title_font = get_font(FONT_SIZES["normal"], bold=True)
        self.font = get_font(FONT_SIZES["small"])
        self.emoji_font = get_emoji_font(32)  # Для emoji тварини
        self.icon_font = get_emoji_font(20)   # Для іконок статус барів
        
        # Кнопки
        self._create_buttons()
    
    def _create_buttons(self):
        """Створити кнопки дій"""
        button_size = 35
        button_spacing = 5
        
        # Кнопка збору (права)
        self.collect_button_rect = pygame.Rect(
            self.rect.right - button_size - 10,
            self.rect.y + 10,
            button_size,
            button_size
        )
        
        # Кнопка годування (ліворуч від кнопки збору)
        self.feed_button_rect = pygame.Rect(
            self.collect_button_rect.x - button_size - button_spacing,
            self.rect.y + 10,
            button_size,
            button_size
        )
    
    def set_animal(self, animal: AnimalData):
        """Встановити тварину"""
        self.animal = animal
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обробка подій"""
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = self.rect.collidepoint(event.pos)
            
            if self.hovered and not was_hovered:
                self.target_scale = 1.02
            elif not self.hovered and was_hovered:
                self.target_scale = 1.0
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.feed_button_rect.collidepoint(event.pos):
                if self.on_feed:
                    self.on_feed(self.animal.id)
                return True
            
            elif self.collect_button_rect.collidepoint(event.pos):
                if self.on_collect:
                    self.on_collect(self.animal.id)
                return True
            
            elif self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click(self)
                return True
        
        return False
    
    def update(self, dt: float):
        """Оновлення"""
        self.animation_time += dt
        
        # Анімація масштабу
        scale_diff = self.target_scale - self.scale
        self.scale += scale_diff * dt * 10
        
        # Оновлення позицій кнопок
        self._create_buttons()
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка картки"""
        if not self.animal:
            return
        
        # Фон
        bg_color = COLORS["panel"] if not self.selected else COLORS["primary_light"]
        if self.hovered:
            bg_color = tuple(min(255, c + 20) for c in bg_color)
        
        # Тінь
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, (0, 0, 0, 80), shadow_rect, border_radius=10)
        
        # Основний прямокутник
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=10)
        
        # Рамка
        border_color = COLORS["primary"] if self.selected else COLORS["border"]
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=10)
        
        # Індикатор живий/мертвий
        status_color = COLORS["success"] if self.animal.is_alive else COLORS["danger"]
        status_rect = pygame.Rect(self.rect.right - 15, self.rect.y + 5, 10, 10)
        pygame.draw.circle(surface, status_color, status_rect.center, 5)
        
        # Emoji тварини
        animal_info = ANIMAL_TYPES.get(self.animal.animal_type, {})
        emoji = animal_info.get("emoji", "🐾")
        
        emoji_surface = self.emoji_font.render(emoji, True, COLORS["text"])
        emoji_x = self.rect.x + 20
        emoji_y = self.rect.y + 20
        surface.blit(emoji_surface, (emoji_x, emoji_y))
        
        # Ім'я
        name_surface = self.title_font.render(self.animal.name, True, COLORS["text"])
        surface.blit(name_surface, (emoji_x + 45, emoji_y + 5))
        
        # Вік
        age_text = f"Вік: {self.animal.age} дн."
        age_surface = self.font.render(age_text, True, COLORS["text_secondary"])
        surface.blit(age_surface, (emoji_x + 45, emoji_y + 30))
        
        # Статус бари
        bar_x = self.rect.x + 20
        bar_y = emoji_y + 65
        bar_width = self.rect.width - 40
        bar_height = 14
        
        # Здоров'я
        self._draw_status_bar(surface, bar_x, bar_y, bar_width, bar_height,
                             self.animal.health, "❤️", self._get_health_color())
        
        # Голод
        self._draw_status_bar(surface, bar_x, bar_y + 22, bar_width, bar_height,
                             self.animal.hunger, "🍽️", self._get_hunger_color())
        
        # Щастя
        self._draw_status_bar(surface, bar_x, bar_y + 44, bar_width, bar_height,
                             self.animal.happiness, "😊", self._get_happiness_color())
        
        # Кнопки дій (тільки якщо тварина жива)
        if self.animal.is_alive:
            self._draw_action_buttons(surface)
    
    def _draw_status_bar(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        value: float,
        icon: str,
        color: Tuple[int, int, int]
    ):
        """Відмальовка статус бару"""
        # Іконка
        icon_surface = self.icon_font.render(icon, True, COLORS["text"])
        surface.blit(icon_surface, (x, y - 3))
        
        # Фон бару
        bar_x = x + 30  # Збільшено відступ для іконки
        bar_width = width - 30
        bar_rect = pygame.Rect(bar_x, y, bar_width, height)
        pygame.draw.rect(surface, COLORS["panel_dark"], bar_rect, border_radius=height//2)
        
        # Заповнення
        fill_width = int((value / 100) * bar_width)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, y, fill_width, height)
            pygame.draw.rect(surface, color, fill_rect, border_radius=height//2)
    
    def _draw_action_buttons(self, surface: pygame.Surface):
        """Відмальовка кнопок дій"""
        # Кнопка годування
        pygame.draw.rect(surface, COLORS["warning"], self.feed_button_rect, border_radius=5)
        feed_icon = self.icon_font.render("🍽️", True, COLORS["white"])
        icon_x = self.feed_button_rect.x + (self.feed_button_rect.width - feed_icon.get_width()) // 2
        icon_y = self.feed_button_rect.y + (self.feed_button_rect.height - feed_icon.get_height()) // 2
        surface.blit(feed_icon, (icon_x, icon_y))
        
        # Кнопка збору (якщо кулдаун = 0)
        if self.animal.production_cooldown == 0:
            pygame.draw.rect(surface, COLORS["success"], self.collect_button_rect, border_radius=5)
        else:
            pygame.draw.rect(surface, COLORS["gray"], self.collect_button_rect, border_radius=5)
        
        animal_info = ANIMAL_TYPES.get(self.animal.animal_type, {})
        product_emoji = animal_info.get("product_emoji", "📦")
        collect_icon = self.icon_font.render(product_emoji, True, COLORS["white"])
        icon_x = self.collect_button_rect.x + (self.collect_button_rect.width - collect_icon.get_width()) // 2
        icon_y = self.collect_button_rect.y + (self.collect_button_rect.height - collect_icon.get_height()) // 2
        surface.blit(collect_icon, (icon_x, icon_y))
    
    def _get_health_color(self) -> Tuple[int, int, int]:
        """Колір здоров'я"""
        if self.animal.health > 60:
            return COLORS["success"]
        elif self.animal.health > 30:
            return COLORS["warning"]
        return COLORS["danger"]
    
    def _get_hunger_color(self) -> Tuple[int, int, int]:
        """Колір голоду"""
        if self.animal.hunger > 50:
            return COLORS["success"]
        elif self.animal.hunger > 25:
            return COLORS["warning"]
        return COLORS["danger"]
    
    def _get_happiness_color(self) -> Tuple[int, int, int]:
        """Колір щастя"""
        if self.animal.happiness > 60:
            return COLORS["info"]
        elif self.animal.happiness > 30:
            return COLORS["warning"]
        return COLORS["danger"]
