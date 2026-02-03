"""
Компонент кнопки з анімаціями та ефектами
"""

import pygame
from typing import Callable, Optional, Tuple
import sys
import os

# Додаємо шлях до game модуля
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, FONT_SIZES, get_font


class Button:
    """
    Стильна кнопка з анімаціями
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: Optional[Callable] = None,
        color: Tuple[int, int, int] = None,
        hover_color: Tuple[int, int, int] = None,
        text_color: Tuple[int, int, int] = None,
        font_size: int = None,
        border_radius: int = 10,
        border_width: int = 0,
        border_color: Tuple[int, int, int] = None,
        enabled: bool = True,
        icon: str = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        
        # Кольори
        self.color = color or COLORS["primary"]
        self.hover_color = hover_color or COLORS["primary_dark"]
        self.text_color = text_color or COLORS["white"]
        self.disabled_color = COLORS["gray"]
        
        # Стиль
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color or COLORS["dark"]
        
        # Стан
        self.enabled = enabled
        self.hovered = False
        self.pressed = False
        self.icon = icon
        
        # Анімація
        self.animation_offset = 0
        self.scale = 1.0
        self.target_scale = 1.0
        
        # Шрифт
        font_size = font_size or FONT_SIZES["normal"]
        self.font = get_font(font_size, bold=True)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обробка подій миші"""
        if not self.enabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = self.rect.collidepoint(event.pos)
            
            if self.hovered and not was_hovered:
                self.target_scale = 1.05
            elif not self.hovered and was_hovered:
                self.target_scale = 1.0
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                self.animation_offset = 2
                self.target_scale = 0.95
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.pressed and self.rect.collidepoint(event.pos):
                    self.pressed = False
                    self.animation_offset = 0
                    self.target_scale = 1.0
                    if self.callback:
                        self.callback()
                    return True
                self.pressed = False
                self.animation_offset = 0
        
        return False
    
    def update(self, dt: float):
        """Оновлення анімації"""
        # Плавна анімація масштабу
        scale_diff = self.target_scale - self.scale
        self.scale += scale_diff * dt * 10
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка кнопки"""
        # Визначаємо колір
        if not self.enabled:
            current_color = self.disabled_color
        elif self.pressed:
            current_color = self.hover_color
        elif self.hovered:
            current_color = self.hover_color
        else:
            current_color = self.color
        
        # Масштабування прямокутника
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2 + self.animation_offset
        
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Тінь
        if not self.pressed:
            shadow_rect = scaled_rect.copy()
            shadow_rect.y += 4
            pygame.draw.rect(surface, (0, 0, 0, 80), shadow_rect, border_radius=self.border_radius)
        
        # Основний прямокутник
        pygame.draw.rect(surface, current_color, scaled_rect, border_radius=self.border_radius)
        
        # Рамка
        if self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, scaled_rect, 
                           width=self.border_width, border_radius=self.border_radius)
        
        # Градієнтний ефект зверху
        if self.enabled and not self.pressed:
            highlight_rect = pygame.Rect(
                scaled_rect.x + 4,
                scaled_rect.y + 2,
                scaled_rect.width - 8,
                scaled_rect.height // 3
            )
            s = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (255, 255, 255, 40), s.get_rect(), border_radius=self.border_radius)
            surface.blit(s, highlight_rect)
        
        # Іконка та текст
        text_surface = self.font.render(self.text, True, self.text_color)
        
        if self.icon:
            icon_surface = self.font.render(self.icon + " ", True, self.text_color)
            total_width = icon_surface.get_width() + text_surface.get_width()
            icon_x = scaled_rect.centerx - total_width // 2
            text_x = icon_x + icon_surface.get_width()
            y = scaled_rect.centery - text_surface.get_height() // 2
            surface.blit(icon_surface, (icon_x, y))
            surface.blit(text_surface, (text_x, y))
        else:
            text_rect = text_surface.get_rect(center=scaled_rect.center)
            surface.blit(text_surface, text_rect)
    
    def set_position(self, x: int, y: int):
        """Встановити позицію"""
        self.rect.x = x
        self.rect.y = y
    
    def set_center(self, x: int, y: int):
        """Встановити центр"""
        self.rect.centerx = x
        self.rect.centery = y


class ImageButton(Button):
    """
    Кнопка з зображенням
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        callback: Optional[Callable] = None,
        hover_image_path: str = None,
        scale: float = 1.0
    ):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * scale),
             int(self.original_image.get_height() * scale))
        )
        
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
            self.hover_image = pygame.transform.scale(
                self.hover_image,
                (int(self.hover_image.get_width() * scale),
                 int(self.hover_image.get_height() * scale))
            )
        else:
            self.hover_image = self._brighten_image(self.original_image)
        
        width = self.original_image.get_width()
        height = self.original_image.get_height()
        
        super().__init__(x, y, width, height, "", callback)
        self.current_image = self.original_image
    
    def _brighten_image(self, image: pygame.Surface) -> pygame.Surface:
        """Створити освітлене зображення"""
        bright = image.copy()
        bright.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_ADD)
        return bright
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка кнопки з зображенням"""
        if self.hovered:
            self.current_image = self.hover_image
        else:
            self.current_image = self.original_image
        
        # Масштабування
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_image = pygame.transform.scale(self.current_image, (scaled_width, scaled_height))
        
        x = self.rect.centerx - scaled_width // 2
        y = self.rect.centery - scaled_height // 2 + self.animation_offset
        
        surface.blit(scaled_image, (x, y))


class IconButton(Button):
    """
    Кругла кнопка з іконкою (emoji)
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        icon: str,
        callback: Optional[Callable] = None,
        color: Tuple[int, int, int] = None,
        tooltip: str = None
    ):
        super().__init__(x, y, size, size, icon, callback, color, font_size=size // 2)
        self.size = size
        self.tooltip = tooltip
        self.tooltip_visible = False
        self.border_radius = size // 2  # Робимо круглою
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка круглої кнопки"""
        # Визначаємо колір
        if not self.enabled:
            current_color = self.disabled_color
        elif self.pressed:
            current_color = self.hover_color
        elif self.hovered:
            current_color = self.hover_color
        else:
            current_color = self.color
        
        center = (self.rect.centerx, self.rect.centery + self.animation_offset)
        radius = int(self.size // 2 * self.scale)
        
        # Тінь
        if not self.pressed:
            shadow_center = (center[0], center[1] + 3)
            pygame.draw.circle(surface, (0, 0, 0), shadow_center, radius)
        
        # Коло
        pygame.draw.circle(surface, current_color, center, radius)
        
        # Іконка
        icon_surface = self.font.render(self.text, True, self.text_color)
        icon_rect = icon_surface.get_rect(center=center)
        surface.blit(icon_surface, icon_rect)
        
        # Tooltip
        if self.hovered and self.tooltip:
            self._draw_tooltip(surface)
    
    def _draw_tooltip(self, surface: pygame.Surface):
        """Відмальовка підказки"""
        font = get_font(FONT_SIZES["small"])
        text_surface = font.render(self.tooltip, True, COLORS["white"])
        
        padding = 8
        tooltip_rect = pygame.Rect(
            self.rect.centerx - text_surface.get_width() // 2 - padding,
            self.rect.top - text_surface.get_height() - padding * 2 - 5,
            text_surface.get_width() + padding * 2,
            text_surface.get_height() + padding * 2
        )
        
        pygame.draw.rect(surface, COLORS["dark"], tooltip_rect, border_radius=5)
        surface.blit(text_surface, (tooltip_rect.x + padding, tooltip_rect.y + padding))
