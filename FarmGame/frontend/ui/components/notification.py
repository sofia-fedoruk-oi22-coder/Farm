"""
Система сповіщень
"""

import pygame
from typing import List, Tuple, Optional
from dataclasses import dataclass
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game.constants import COLORS, FONT_SIZES, get_font


@dataclass
class Notification:
    """Дані сповіщення"""
    title: str
    message: str
    notification_type: str = "info"  # info, success, warning, error
    duration: float = 3.0
    time_remaining: float = 3.0
    alpha: int = 255


class NotificationPopup:
    """
    Popup сповіщення
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        notification: Notification
    ):
        self.notification = notification
        self.width = width
        self.height = 70
        self.rect = pygame.Rect(x, y, width, self.height)
        
        # Анімація
        self.offset_x = width  # Починаємо за межами екрану
        self.target_offset_x = 0
        self.alpha = 0
        self.target_alpha = 255
        
        # Шрифти
        self.title_font = get_font(FONT_SIZES["normal"], bold=True)
        self.message_font = get_font(FONT_SIZES["small"])
    
    def update(self, dt: float) -> bool:
        """Оновлення, повертає False якщо сповіщення закінчилось"""
        # Анімація появи
        offset_diff = self.target_offset_x - self.offset_x
        self.offset_x += offset_diff * dt * 10
        
        alpha_diff = self.target_alpha - self.alpha
        self.alpha += alpha_diff * dt * 10
        
        # Зменшення часу
        self.notification.time_remaining -= dt
        
        # Анімація зникнення
        if self.notification.time_remaining <= 0.5:
            self.target_offset_x = self.width
            self.target_alpha = 0
        
        return self.notification.time_remaining > 0
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        if self.alpha <= 0:
            return
        
        # Колір залежно від типу
        colors = {
            "info": COLORS["info"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "error": COLORS["danger"]
        }
        color = colors.get(self.notification.notification_type, COLORS["info"])
        
        # Позиція з анімацією
        draw_x = int(self.rect.x + self.offset_x)
        draw_rect = pygame.Rect(draw_x, self.rect.y, self.width, self.height)
        
        # Поверхня з прозорістю
        popup_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Тінь
        shadow_rect = pygame.Rect(3, 3, self.width - 3, self.height - 3)
        pygame.draw.rect(popup_surface, (0, 0, 0, 50), shadow_rect, border_radius=10)
        
        # Фон
        bg_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(popup_surface, (*COLORS["panel"], int(self.alpha * 0.95)), bg_rect, border_radius=10)
        
        # Кольорова смужка зліва
        stripe_rect = pygame.Rect(0, 0, 6, self.height)
        pygame.draw.rect(popup_surface, (*color, int(self.alpha)), stripe_rect, 
                        border_top_left_radius=10, border_bottom_left_radius=10)
        
        # Іконка
        icons = {
            "info": "",
            "success": "",
            "warning": "",
            "error": ""
        }
        icon = icons.get(self.notification.notification_type, "")
        icon_surface = self.title_font.render(icon, True, color)
        icon_surface.set_alpha(int(self.alpha))
        popup_surface.blit(icon_surface, (15, 15))
        
        # Заголовок
        title_surface = self.title_font.render(self.notification.title, True, COLORS["text"])
        title_surface.set_alpha(int(self.alpha))
        popup_surface.blit(title_surface, (45, 12))
        
        # Повідомлення
        message_surface = self.message_font.render(self.notification.message, True, COLORS["text_secondary"])
        message_surface.set_alpha(int(self.alpha))
        popup_surface.blit(message_surface, (45, 38))
        
        # Прогрес бар
        progress = self.notification.time_remaining / self.notification.duration
        progress_width = int((self.width - 20) * progress)
        progress_rect = pygame.Rect(10, self.height - 5, progress_width, 3)
        pygame.draw.rect(popup_surface, (*color, int(self.alpha * 0.7)), progress_rect, border_radius=2)
        
        surface.blit(popup_surface, draw_rect)


class NotificationManager:
    """
    Менеджер сповіщень
    """
    
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        max_notifications: int = 5
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_notifications = max_notifications
        
        self.notifications: List[NotificationPopup] = []
        self.notification_width = 350
        self.notification_height = 70
        self.padding = 10
        self.margin_right = 20
        self.margin_top = 80
    
    def add(
        self,
        title: str,
        message: str,
        notification_type: str = "info",
        duration: float = 3.0
    ):
        """Додати сповіщення"""
        # Очищення від емодзі (залишаємо лише символи з кодом < 8192)
        # Це збереже кирилицю, латиницю та основні розділові знаки
        clean_title = "".join(c for c in title if ord(c) < 8192)
        clean_message = "".join(c for c in message if ord(c) < 8192)
        
        notification = Notification(
            title=clean_title,
            message=clean_message,
            notification_type=notification_type,
            duration=duration,
            time_remaining=duration
        )
        
        x = self.screen_width - self.notification_width - self.margin_right
        y = self.margin_top + len(self.notifications) * (self.notification_height + self.padding)
        
        popup = NotificationPopup(x, y, self.notification_width, notification)
        self.notifications.append(popup)
        
        # Обмеження кількості
        while len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)
            self._reposition_notifications()
    
    def add_info(self, title: str, message: str):
        """Додати інформаційне сповіщення"""
        self.add(title, message, "info")
    
    def add_success(self, title: str, message: str):
        """Додати успішне сповіщення"""
        self.add(title, message, "success")
    
    def add_warning(self, title: str, message: str):
        """Додати попередження"""
        self.add(title, message, "warning")
    
    def add_error(self, title: str, message: str):
        """Додати помилку"""
        self.add(title, message, "error")
    
    def _reposition_notifications(self):
        """Перепозиціонувати сповіщення"""
        for i, popup in enumerate(self.notifications):
            popup.rect.y = self.margin_top + i * (self.notification_height + self.padding)
    
    def update(self, dt: float):
        """Оновлення"""
        # Оновлюємо всі сповіщення
        for popup in self.notifications[:]:
            if not popup.update(dt):
                self.notifications.remove(popup)
                self._reposition_notifications()
    
    def draw(self, surface: pygame.Surface):
        """Відмальовка"""
        for popup in self.notifications:
            popup.draw(surface)
    
    def clear(self):
        """Очистити всі сповіщення"""
        self.notifications.clear()
