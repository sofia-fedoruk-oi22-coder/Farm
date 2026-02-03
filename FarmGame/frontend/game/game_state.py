"""
Ігровий стан - керує всіма даними гри
Реалізує патерн Singleton для глобального доступу
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import random

from .constants import *


@dataclass
class AnimalData:
    """Дані про тварину"""
    id: int
    animal_type: str
    name: str
    age: int = 0
    health: float = 100.0
    hunger: float = 100.0
    happiness: float = 75.0
    is_alive: bool = True
    production_cooldown: int = 0
    breed: str = "default"
    
    # Статистика
    total_fed: int = 0
    total_produced: int = 0
    days_on_farm: int = 0
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict) -> 'AnimalData':
        return AnimalData(**data)


@dataclass
class ProductData:
    """Дані про продукт"""
    product_type: str
    amount: float
    quality: str = "normal"
    days_remaining: int = 30
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FeedData:
    """Дані про корм"""
    feed_type: str
    amount: float
    quality: float = 100.0
    days_remaining: int = 180
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass 
class BuildingData:
    """Дані про будівлю"""
    building_type: str
    name: str
    level: int = 1
    capacity: int = 10
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FarmerData:
    """Дані про фермера"""
    name: str
    money: float = 10000.0
    energy: float = 100.0
    max_energy: float = 100.0
    level: int = 1
    experience: float = 0.0
    
    # Навички
    skills: Dict[str, float] = field(default_factory=lambda: {
        "animal_care": 10.0,
        "feeding": 10.0,
        "milking": 5.0,
        "shearing": 5.0,
        "veterinary": 5.0,
        "trading": 10.0,
        "breeding": 5.0,
        "crafting": 5.0
    })
    
    # Статистика
    animals_fed: int = 0
    products_collected: int = 0
    animals_bought: int = 0
    animals_sold: int = 0
    total_earnings: float = 0.0
    total_spending: float = 0.0
    days_played: int = 0
    
    def to_dict(self) -> dict:
        return asdict(self)


class GameState:
    """
    Головний клас ігрового стану
    Зберігає всі дані гри та керує ігровою логікою
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton патерн"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        
        # Основні дані
        self.farm_name: str = "Моя Ферма"
        self.farmer: FarmerData = FarmerData(name="Фермер")
        
        # Колекції
        self.animals: List[AnimalData] = []
        self.products: Dict[str, ProductData] = {}
        self.feeds: Dict[str, FeedData] = {}
        self.buildings: List[BuildingData] = []
        self.achievements: Dict[str, bool] = {k: False for k in ACHIEVEMENTS}
        
        # Час
        self.current_day: int = 1
        self.current_hour: int = 6
        self.current_season: str = "spring"
        self.current_weather: str = "sunny"
        self.days_in_season: int = 0
        
        # Економіка
        self.daily_income: float = 0.0
        self.daily_expenses: float = 0.0
        self.reputation: int = 0
        
        # Історія подій
        self.events: List[str] = []
        self.notifications: List[Dict[str, Any]] = []
        
        # ID лічильник
        self._next_animal_id: int = 1
        
        # Час гри
        self.game_speed: float = 1.0
        self.time_accumulated: float = 0.0
    
    def new_game(self, farm_name: str, farmer_name: str):
        """Створення нової гри"""
        # Явно скидаємо всі поля (бо __init__ не спрацює через Singleton)
        self.farm_name = farm_name
        self.farmer = FarmerData(name=farmer_name)
        
        # Колекції - скидаємо повністю
        self.animals = []
        self.products = {}
        self.feeds = {}
        self.buildings = []
        self.achievements = {k: False for k in ACHIEVEMENTS}
        
        # Час - скидаємо
        self.current_day = 1
        self.current_hour = 6
        self.current_season = "spring"
        self.current_weather = "sunny"
        self.days_in_season = 0
        
        # Економіка - скидаємо
        self.daily_income = 0.0
        self.daily_expenses = 0.0
        self.reputation = 0
        
        # Історія подій - скидаємо
        self.events = []
        self.notifications = []
        
        # ID лічильник - скидаємо
        self._next_animal_id = 1
        
        # Час гри
        self.game_speed = 1.0
        self.time_accumulated = 0.0
        
        # Початкові будівлі
        self.buildings = [
            BuildingData("barn", "Сарай", 1, 10),
            BuildingData("coop", "Курник", 1, 20),
            BuildingData("stable", "Хлів", 1, 5),
            BuildingData("warehouse", "Склад", 1, 100)
        ]
        
        # Початкові корми
        self.feeds = {
            "hay": FeedData("hay", 50.0),
            "grain": FeedData("grain", 30.0),
            "mixed": FeedData("mixed", 20.0)
        }
        
        # Початкове повідомлення
        self.add_event(f"Ласкаво просимо на ферму '{farm_name}'!")
        self.add_notification("Підказка", "Почніть з купівлі тварин у магазині!")
    
    def update(self, dt: float):
        """Оновлення ігрового стану"""
        self.time_accumulated += dt * self.game_speed
        
        # Кожну "ігрову хвилину" (1 секунда реального часу = 1 година гри)
        if self.time_accumulated >= 1.0:
            self.time_accumulated -= 1.0
            self._advance_hour()
    
    def _advance_hour(self):
        """Просування часу на 1 годину"""
        self.current_hour += 1
        
        if self.current_hour >= 24:
            self.current_hour = 0
            self._advance_day()
        
        # Оновлення тварин кожну годину
        for animal in self.animals:
            if animal.is_alive:
                self._update_animal(animal)
    
    def _advance_day(self):
        """Просування часу на 1 день"""
        # Статистика
        self.farmer.days_played += 1
        self.current_day += 1
        self.days_in_season += 1
        
        # Зміна сезону
        if self.days_in_season >= 30:
            self._change_season()
        
        # Зміна погоди
        self._update_weather()
        
        # Старіння тварин
        for animal in self.animals:
            animal.age += 1
            animal.days_on_farm += 1
        
        # Старіння продуктів
        for product in list(self.products.values()):
            product.days_remaining -= 1
            if product.days_remaining <= 0:
                del self.products[product.product_type]
        
        # Старіння кормів
        for feed in list(self.feeds.values()):
            feed.days_remaining -= 1
            if feed.days_remaining <= 0 or feed.amount <= 0:
                del self.feeds[feed.feed_type]
        
        # Відновлення енергії
        self.farmer.energy = min(self.farmer.max_energy, self.farmer.energy + 30)
        
        # Перевірка досягнень
        self._check_achievements()
        
        # Подія нового дня
        season_name = SEASONS[self.current_season]["name"]
        weather_emoji = WEATHER_TYPES[self.current_weather]["emoji"]
        self.add_event(f"День {self.current_day}. {season_name}. {weather_emoji}")
    
    def _update_animal(self, animal: AnimalData):
        """Оновлення стану тварини"""
        # Голод зменшується
        animal.hunger -= 0.5
        animal.hunger = max(0, animal.hunger)
        
        # Щастя зменшується
        animal.happiness -= 0.2
        animal.happiness = max(0, animal.happiness)
        
        # Вплив голоду на здоров'я
        if animal.hunger < 20:
            animal.health -= 1
        
        # Вплив щастя на здоров'я
        if animal.happiness < 20:
            animal.health -= 0.5
        
        # Логіка хворіння залежно від умов
        self._apply_health_effects(animal)
        
        # Смерть
        if animal.health <= 0 or animal.hunger <= 0:
            animal.is_alive = False
            self.add_event(f"{animal.name} ({ANIMAL_TYPES[animal.animal_type]['name']}) помер(ла)!")
        
        # Зменшення кулдауну виробництва
        if animal.production_cooldown > 0:
            animal.production_cooldown -= 1
    
    def _apply_health_effects(self, animal: AnimalData):
        """Застосування впливу погоди та будівель на здоров'я"""
        # Базова ймовірність захворювання
        sickness_chance = 0.0
        
        # Вплив погоди
        weather_effects = {
            "sunny": 0.0,
            "cloudy": 0.005,
            "rainy": 0.015,
            "stormy": 0.025,
            "snowy": 0.02,
            "foggy": 0.01
        }
        sickness_chance += weather_effects.get(self.current_weather, 0.0)
        
        # Вплив сезону
        season_effects = {
            "spring": 0.005,
            "summer": 0.0,
            "autumn": 0.01,
            "winter": 0.015
        }
        sickness_chance += season_effects.get(self.current_season, 0.0)
        
        # Захист від будівель - кращі будівлі знижують ймовірність хворіння
        building_protection = self._get_building_protection(animal.animal_type)
        sickness_chance *= (1.0 - building_protection)
        
        # Випадкове захворювання
        import random
        if random.random() < sickness_chance:
            # Втрата здоров'я від хвороби
            health_loss = random.uniform(0.5, 2.0)
            animal.health = max(0, animal.health - health_loss)
    
    def _get_building_protection(self, animal_type: str) -> float:
        """Отримати рівень захисту від будівлі для типу тварини"""
        # Визначаємо, яка будівля потрібна для цього типу тварини
        building_map = {
            "cow": "barn",
            "pig": "barn",
            "sheep": "barn",
            "goat": "barn",
            "chicken": "coop",
            "duck": "coop",
            "rabbit": "coop",
            "horse": "stable"
        }
        
        building_type = building_map.get(animal_type, "barn")
        building = next((b for b in self.buildings if b.building_type == building_type), None)
        
        if not building:
            return 0.0  # Немає будівлі - немає захисту
        
        # Кожен рівень будівлі дає 10% захисту (максимум 80%)
        protection = min(0.8, building.level * 0.10)
        return protection
    
    def _change_season(self):
        """Зміна пори року"""
        self.days_in_season = 0
        seasons = ["spring", "summer", "autumn", "winter"]
        current_idx = seasons.index(self.current_season)
        self.current_season = seasons[(current_idx + 1) % 4]
        
        season_name = SEASONS[self.current_season]["name"]
        season_emoji = SEASONS[self.current_season]["emoji"]
        self.add_event(f"{season_emoji} Настала нова пора року: {season_name}!")
    
    def _update_weather(self):
        """Оновлення погоди"""
        # Ймовірності погоди залежно від сезону
        weather_weights = {
            "spring": {"sunny": 30, "cloudy": 30, "rainy": 30, "foggy": 10},
            "summer": {"sunny": 60, "cloudy": 20, "stormy": 15, "foggy": 5},
            "autumn": {"sunny": 20, "cloudy": 30, "rainy": 35, "foggy": 15},
            "winter": {"sunny": 15, "cloudy": 25, "snowy": 50, "foggy": 10}
        }
        
        weights = weather_weights.get(self.current_season, weather_weights["spring"])
        weather_types = list(weights.keys())
        probabilities = list(weights.values())
        
        self.current_weather = random.choices(weather_types, probabilities)[0]
    
    def _check_achievements(self):
        """Перевірка досягнень"""
        # Перша тварина
        if len(self.animals) >= 1 and not self.achievements["first_animal"]:
            self._unlock_achievement("first_animal")
        
        # 10 тварин
        if len(self.animals) >= 10 and not self.achievements["ten_animals"]:
            self._unlock_achievement("ten_animals")
        
        # 50 тварин
        if len(self.animals) >= 50 and not self.achievements["fifty_animals"]:
            self._unlock_achievement("fifty_animals")
        
        # Багатий фермер
        if self.farmer.money >= 100000 and not self.achievements["rich_farmer"]:
            self._unlock_achievement("rich_farmer")
        
        # Рік на фермі
        if self.farmer.days_played >= 365 and not self.achievements["year_passed"]:
            self._unlock_achievement("year_passed")
        
        # Всі типи тварин
        animal_types_on_farm = set(a.animal_type for a in self.animals if a.is_alive)
        if len(animal_types_on_farm) >= len(ANIMAL_TYPES) and not self.achievements["all_animals"]:
            self._unlock_achievement("all_animals")
        
        # Щасливі тварини
        living_animals = [a for a in self.animals if a.is_alive]
        if living_animals and all(a.happiness > 80 for a in living_animals):
            if not self.achievements["happy_animals"]:
                self._unlock_achievement("happy_animals")
    
    def _unlock_achievement(self, achievement_id: str):
        """Розблокувати досягнення"""
        if achievement_id in self.achievements and not self.achievements[achievement_id]:
            self.achievements[achievement_id] = True
            achievement = ACHIEVEMENTS[achievement_id]
            self.farmer.money += achievement["reward"]
            self.add_notification(
                f"Досягнення: {achievement['name']}",
                f"{achievement['description']}. Нагорода: {achievement['reward']} грн"
            )
    
    # ==================== Операції з тваринами ====================
    
    def buy_animal(self, animal_type: str, name: str) -> Optional[AnimalData]:
        """Купити тварину"""
        if animal_type not in ANIMAL_TYPES:
            return None
        
        price = ANIMAL_TYPES[animal_type]["price"]
        
        if self.farmer.money < price:
            self.add_notification("Помилка", "Недостатньо грошей!")
            return None
        
        # Перевірка місткості
        total_capacity = sum(b.capacity for b in self.buildings 
                           if b.building_type in ["barn", "coop", "stable"])
        living_animals = len([a for a in self.animals if a.is_alive])
        
        if living_animals >= total_capacity:
            self.add_notification("Помилка", "Недостатньо місця! Покращіть будівлі.")
            return None
        
        # Купуємо
        self.farmer.money -= price
        self.farmer.total_spending += price
        self.farmer.animals_bought += 1
        
        animal = AnimalData(
            id=self._next_animal_id,
            animal_type=animal_type,
            name=name
        )
        self._next_animal_id += 1
        self.animals.append(animal)
        
        emoji = ANIMAL_TYPES[animal_type]["emoji"]
        self.add_event(f"{emoji} Куплено {ANIMAL_TYPES[animal_type]['name']}: {name}")
        
        return animal
    
    def sell_animal(self, animal_id: int) -> float:
        """Продати тварину"""
        animal = next((a for a in self.animals if a.id == animal_id), None)
        if not animal or not animal.is_alive:
            return 0.0
        
        # Ціна залежить від стану
        base_price = ANIMAL_TYPES[animal.animal_type]["price"]
        price = base_price * (animal.health / 100) * 0.7
        
        self.farmer.money += price
        self.farmer.total_earnings += price
        self.farmer.animals_sold += 1
        
        self.animals.remove(animal)
        
        emoji = ANIMAL_TYPES[animal.animal_type]["emoji"]
        self.add_event(f"{emoji} Продано {animal.name} за {price:.0f} грн")
        
        return price
    
    def feed_animal(self, animal_id: int, feed_type: str) -> bool:
        """Погодувати тварину"""
        animal = next((a for a in self.animals if a.id == animal_id), None)
        if not animal or not animal.is_alive:
            return False
        
        if feed_type not in self.feeds or self.feeds[feed_type].amount < 1:
            self.add_notification("Помилка", "Недостатньо корму!")
            return False
        
        if self.farmer.energy < 5:
            self.add_notification("Помилка", "Недостатньо енергії!")
            return False
        
        # Годуємо
        self.feeds[feed_type].amount -= 1
        self.farmer.energy -= 5
        
        # Ефект годування
        feed_quality = self.feeds[feed_type].quality / 100
        animal.hunger = min(100, animal.hunger + 30 * feed_quality)
        animal.happiness = min(100, animal.happiness + 5 * feed_quality)
        animal.total_fed += 1
        
        self.farmer.animals_fed += 1
        
        return True
    
    def feed_all_animals(self) -> int:
        """Погодувати всіх голодних тварин"""
        fed_count = 0
        
        for animal in self.animals:
            if animal.is_alive and animal.hunger < 70:
                # Визначаємо улюблений корм
                preferred = self._get_preferred_feed(animal.animal_type)
                
                for feed_type in [preferred, "mixed", "hay", "grain"]:
                    if feed_type in self.feeds and self.feeds[feed_type].amount >= 1:
                        if self.feed_animal(animal.id, feed_type):
                            fed_count += 1
                            break
        
        if fed_count > 0:
            self.add_event(f"🍽️ Погодовано {fed_count} тварин")
        
        return fed_count
    
    def _get_preferred_feed(self, animal_type: str) -> str:
        """Отримати улюблений корм для тварини"""
        preferences = {
            "cow": "hay",
            "chicken": "grain",
            "pig": "mixed",
            "sheep": "grass",
            "goat": "branches",
            "duck": "grain",
            "rabbit": "carrots",
            "horse": "oats"
        }
        return preferences.get(animal_type, "mixed")
    
    def collect_product(self, animal_id: int) -> Optional[ProductData]:
        """Зібрати продукцію від тварини"""
        animal = next((a for a in self.animals if a.id == animal_id), None)
        if not animal or not animal.is_alive:
            return None
        
        if animal.production_cooldown > 0:
            return None
        
        if animal.hunger < 30 or animal.health < 20:
            return None
        
        if self.farmer.energy < 10:
            self.add_notification("Помилка", "Недостатньо енергії!")
            return None
        
        # Збираємо продукцію
        self.farmer.energy -= 10
        
        animal_info = ANIMAL_TYPES[animal.animal_type]
        product_type = animal.animal_type + "_product"
        
        # Кількість залежить від стану тварини
        base_amount = 1.0
        quality_multiplier = (animal.health / 100) * (animal.happiness / 100)
        amount = base_amount * quality_multiplier
        
        # Визначаємо якість
        if quality_multiplier >= 0.9:
            quality = "excellent"
        elif quality_multiplier >= 0.7:
            quality = "good"
        elif quality_multiplier >= 0.5:
            quality = "normal"
        else:
            quality = "poor"
        
        product = ProductData(product_type, amount, quality)
        
        # Додаємо до сховища
        if product_type in self.products:
            self.products[product_type].amount += amount
        else:
            self.products[product_type] = product
        
        # Оновлюємо кулдаун (24 години)
        animal.production_cooldown = 24
        animal.total_produced += 1
        
        self.farmer.products_collected += 1
        
        emoji = animal_info["product_emoji"]
        self.add_event(f"{emoji} Зібрано {animal_info['product']} від {animal.name}")
        
        return product
    
    def collect_all_products(self) -> int:
        """Зібрати всю продукцію"""
        collected = 0
        
        for animal in self.animals:
            if self.collect_product(animal.id):
                collected += 1
        
        return collected
    
    def pet_animal(self, animal_id: int):
        """Погладити тварину"""
        animal = next((a for a in self.animals if a.id == animal_id), None)
        if animal and animal.is_alive:
            animal.happiness = min(100, animal.happiness + 10)
            self.farmer.energy -= 2
    
    def heal_animal(self, animal_id: int) -> float:
        """Лікувати тварину"""
        animal = next((a for a in self.animals if a.id == animal_id), None)
        if not animal or not animal.is_alive:
            return 0.0
        
        cost = (100 - animal.health) * 5
        
        if self.farmer.money < cost:
            self.add_notification("Помилка", "Недостатньо грошей!")
            return 0.0
        
        self.farmer.money -= cost
        self.farmer.total_spending += cost
        animal.health = 100
        animal.happiness = min(100, animal.happiness + 10)
        
        self.add_event(f"💊 {animal.name} вилікувано! (-{cost:.0f} грн)")
        
        return cost
    
    # ==================== Операції з кормами ====================
    
    def buy_feed(self, feed_type: str, amount: float) -> bool:
        """Купити корм"""
        if feed_type not in FEED_TYPES:
            return False
        
        # Перевірка місткості складу
        warehouse_capacity = self._get_warehouse_capacity()
        current_feed_total = sum(feed.amount for feed in self.feeds.values())
        
        if current_feed_total + amount > warehouse_capacity:
            self.add_notification("Помилка", f"Недостатньо місця на складі! Місткість: {warehouse_capacity} кг")
            return False
        
        price = FEED_TYPES[feed_type]["price"] * amount
        
        if self.farmer.money < price:
            self.add_notification("Помилка", "Недостатньо грошей!")
            return False
        
        self.farmer.money -= price
        self.farmer.total_spending += price
        
        if feed_type in self.feeds:
            self.feeds[feed_type].amount += amount
        else:
            self.feeds[feed_type] = FeedData(feed_type, amount)
        
        emoji = FEED_TYPES[feed_type]["emoji"]
        self.add_event(f"{emoji} Куплено {FEED_TYPES[feed_type]['name']}: {amount} кг")
        
        return True
    
    def _get_warehouse_capacity(self) -> float:
        """Отримати загальну місткість складу для кормів"""
        warehouse = next((b for b in self.buildings if b.building_type == "warehouse"), None)
        if not warehouse:
            return 200.0  # Базова місткість без складу
        
        # Базова місткість + бонус за рівень
        return warehouse.capacity * 2.0  # capacity вже зростає з рівнем
    
    # ==================== Операції з продукцією ====================
    
    def sell_product(self, product_type: str, amount: float) -> float:
        """Продати продукцію"""
        if product_type not in self.products:
            return 0.0
        
        product = self.products[product_type]
        sell_amount = min(amount, product.amount)
        
        if sell_amount <= 0:
            return 0.0
        
        # Базова ціна
        base_price = 10.0  # TODO: визначити ціни для кожного типу
        
        # Множник якості
        quality_multipliers = {
            "poor": 0.5,
            "normal": 1.0,
            "good": 1.25,
            "excellent": 1.5
        }
        multiplier = quality_multipliers.get(product.quality, 1.0)
        
        # Торговий бонус
        trade_bonus = 1.0 + (self.farmer.skills["trading"] / 200)
        
        price = base_price * sell_amount * multiplier * trade_bonus
        
        product.amount -= sell_amount
        if product.amount <= 0:
            del self.products[product_type]
        
        self.farmer.money += price
        self.farmer.total_earnings += price
        self.daily_income += price
        
        self.add_event(f"💰 Продано продукцію за {price:.0f} грн")
        
        # Перевірка досягнення
        if not self.achievements["first_sale"]:
            self._unlock_achievement("first_sale")
        
        return price
    
    def sell_all_products(self) -> float:
        """Продати всю продукцію"""
        total = 0.0
        
        for product_type in list(self.products.keys()):
            total += self.sell_product(product_type, self.products[product_type].amount)
        
        return total
    
    # ==================== Будівлі ====================
    
    def upgrade_building(self, building_type: str) -> bool:
        """Покращити будівлю"""
        building = next((b for b in self.buildings if b.building_type == building_type), None)
        if not building:
            return False
        
        building_info = BUILDING_TYPES.get(building_type, {})
        base_cost = building_info.get("base_cost", 5000)
        multiplier = building_info.get("upgrade_cost_multiplier", 1.5)
        
        cost = base_cost * (multiplier ** building.level)
        
        if self.farmer.money < cost:
            self.add_notification("Помилка", "Недостатньо грошей!")
            return False
        
        self.farmer.money -= cost
        self.farmer.total_spending += cost
        building.level += 1
        building.capacity = int(building.capacity * 1.5)
        
        emoji = building_info.get("emoji", "🏠")
        self.add_event(f"{emoji} {building.name} покращено до рівня {building.level}!")
        
        return True
    
    # ==================== Утиліти ====================
    
    def add_event(self, message: str):
        """Додати подію в історію"""
        timestamp = f"[День {self.current_day}, {self.current_hour}:00]"
        self.events.append(f"{timestamp} {message}")
        
        # Обмежуємо розмір історії
        if len(self.events) > 100:
            self.events = self.events[-100:]
    
    def add_notification(self, title: str, message: str):
        """Додати сповіщення"""
        self.notifications.append({
            "title": title,
            "message": message,
            "time": datetime.now().isoformat()
        })
        
        # Обмежуємо кількість
        if len(self.notifications) > 20:
            self.notifications = self.notifications[-20:]
    
    def get_total_capacity(self) -> int:
        """Отримати загальну місткість для тварин"""
        return sum(b.capacity for b in self.buildings 
                   if b.building_type in ["barn", "coop", "stable"])
    
    def get_living_animals_count(self) -> int:
        """Отримати кількість живих тварин"""
        return len([a for a in self.animals if a.is_alive])
    
    def get_net_worth(self) -> float:
        """Отримати загальну вартість ферми"""
        worth = self.farmer.money
        
        # Вартість тварин
        for animal in self.animals:
            if animal.is_alive:
                worth += ANIMAL_TYPES[animal.animal_type]["price"] * (animal.health / 100) * 0.7
        
        # Вартість кормів
        for feed in self.feeds.values():
            worth += FEED_TYPES[feed.feed_type]["price"] * feed.amount
        
        # Вартість будівель
        for building in self.buildings:
            building_info = BUILDING_TYPES.get(building.building_type, {})
            base_cost = building_info.get("base_cost", 5000)
            worth += base_cost * building.level
        
        return worth
    
    # ==================== Збереження/Завантаження ====================
    
    def save_game(self) -> bool:
        """Зберегти гру"""
        try:
            data = {
                "farm_name": self.farm_name,
                "farmer": self.farmer.to_dict(),
                "animals": [a.to_dict() for a in self.animals],
                "products": {k: v.to_dict() for k, v in self.products.items()},
                "feeds": {k: v.to_dict() for k, v in self.feeds.items()},
                "buildings": [b.to_dict() for b in self.buildings],
                "achievements": self.achievements,
                "current_day": self.current_day,
                "current_hour": self.current_hour,
                "current_season": self.current_season,
                "current_weather": self.current_weather,
                "days_in_season": self.days_in_season,
                "reputation": self.reputation,
                "next_animal_id": self._next_animal_id,
                "saved_at": datetime.now().isoformat()
            }
            
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.add_notification("Збережено", "Гру успішно збережено!")
            return True
        except Exception as e:
            self.add_notification("Помилка", f"Не вдалося зберегти: {e}")
            return False
    
    def load_game(self) -> bool:
        """Завантажити гру"""
        if not os.path.exists(SAVE_FILE):
            return False
        
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.farm_name = data["farm_name"]
            self.farmer = FarmerData(**data["farmer"])
            self.animals = [AnimalData.from_dict(a) for a in data["animals"]]
            self.products = {k: ProductData(**v) for k, v in data["products"].items()}
            self.feeds = {k: FeedData(**v) for k, v in data["feeds"].items()}
            self.buildings = [BuildingData(**b) for b in data["buildings"]]
            self.achievements = data["achievements"]
            self.current_day = data["current_day"]
            self.current_hour = data["current_hour"]
            self.current_season = data["current_season"]
            self.current_weather = data["current_weather"]
            self.days_in_season = data["days_in_season"]
            self.reputation = data["reputation"]
            self._next_animal_id = data["next_animal_id"]
            
            self.add_notification("Завантажено", "Гру успішно завантажено!")
            return True
        except Exception as e:
            self.add_notification("Помилка", f"Не вдалося завантажити: {e}")
            return False
    
    def has_save_file(self) -> bool:
        """Перевірити наявність файлу збереження"""
        return os.path.exists(SAVE_FILE)
