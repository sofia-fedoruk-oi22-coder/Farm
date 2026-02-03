/**
 * @file Cow.cpp
 * @brief Реалізація класу Cow
 */

#include "animals/Cow.hpp"
#include <algorithm>
#include <random>

namespace FarmGame {

Cow::Cow(const std::string& name, int age, CowBreed breed)
    : Animal(name, age)
    , breed_(breed)
    , milkQuality_(70.0)
    , milkProduction_(15.0)
    , isPregnant_(false)
    , pregnancyDays_(0)
    , lactationPeriod_(305)
{
    initializeBreedStats();
}

void Cow::initializeBreedStats() {
    switch (breed_) {
        case CowBreed::HOLSTEIN:
            milkProduction_ = 25.0;  // Найбільше молока
            milkQuality_ = 65.0;
            break;
        case CowBreed::JERSEY:
            milkProduction_ = 15.0;
            milkQuality_ = 90.0;     // Найкраща якість
            break;
        case CowBreed::ANGUS:
            milkProduction_ = 8.0;   // М'ясна порода
            milkQuality_ = 60.0;
            break;
        case CowBreed::HEREFORD:
            milkProduction_ = 12.0;
            milkQuality_ = 70.0;
            break;
        case CowBreed::SIMMENTAL:
            milkProduction_ = 18.0;
            milkQuality_ = 75.0;
            break;
    }
}

std::string Cow::getBreedName() const {
    switch (breed_) {
        case CowBreed::HOLSTEIN: return "Голштинська";
        case CowBreed::JERSEY: return "Джерсі";
        case CowBreed::ANGUS: return "Ангус";
        case CowBreed::HEREFORD: return "Херефорд";
        case CowBreed::SIMMENTAL: return "Симентальська";
        default: return "Невідома";
    }
}

double Cow::produce() {
    if (!canProduce()) return 0.0;
    
    // Розрахувати виробництво молока
    double production = milkProduction_ * calculateProductionBonus();
    
    // Бонус від лактації
    if (lactationPeriod_ > 200) {
        production *= 1.2;
    }
    
    // Встановити кулдаун (раз на день)
    productionCooldown_ = 24;
    
    // Оновити статистику
    stats_.totalProduced++;
    stats_.totalEarnings += production * getProductPrice();
    
    return production;
}

double Cow::getProductPrice() const {
    // Базова ціна молока за літр
    double basePrice = 15.0;
    
    // Множник якості
    double qualityMultiplier = 0.5 + (milkQuality_ / 100.0);
    
    return basePrice * qualityMultiplier;
}

double Cow::getBasePrice() const {
    double basePrice = 15000.0;  // Базова ціна корови
    
    switch (breed_) {
        case CowBreed::HOLSTEIN:
            basePrice = 20000.0;
            break;
        case CowBreed::JERSEY:
            basePrice = 25000.0;
            break;
        case CowBreed::ANGUS:
            basePrice = 30000.0;
            break;
        case CowBreed::HEREFORD:
            basePrice = 22000.0;
            break;
        case CowBreed::SIMMENTAL:
            basePrice = 28000.0;
            break;
    }
    
    return basePrice;
}

std::unique_ptr<Animal> Cow::clone() const {
    auto cow = std::make_unique<Cow>(name_, age_, breed_);
    cow->health_ = health_;
    cow->hunger_ = hunger_;
    cow->happiness_ = happiness_;
    cow->milkQuality_ = milkQuality_;
    cow->milkProduction_ = milkProduction_;
    return cow;
}

void Cow::update(double deltaTime) {
    Animal::update(deltaTime);
    
    if (!isAlive_) return;
    
    // Оновити вагітність
    if (isPregnant_) {
        updatePregnancy();
    }
    
    // Зменшення періоду лактації
    if (lactationPeriod_ > 0) {
        lactationPeriod_--;
    }
}

bool Cow::feed(double feedQuality, double amount) {
    if (!Animal::feed(feedQuality, amount)) return false;
    
    // Якісний корм покращує якість молока
    if (feedQuality > 0.8) {
        milkQuality_ = std::min(100.0, milkQuality_ + 0.5);
    }
    
    return true;
}

void Cow::onFed(double quality, double amount) {
    // Сіно особливо добре для корів
    if (amount > 2.0) {
        milkProduction_ = std::min(milkProduction_ + 0.1, 35.0);
    }
}

double Cow::calculateProductionBonus() const {
    double bonus = Animal::calculateProductionBonus();
    
    // Додатковий бонус для певних порід
    if (breed_ == CowBreed::HOLSTEIN) {
        bonus *= 1.1;
    }
    
    return bonus;
}

void Cow::breed() {
    if (canBreed()) {
        isPregnant_ = true;
        pregnancyDays_ = 0;
    }
}

void Cow::updatePregnancy() {
    if (!isPregnant_) return;
    
    pregnancyDays_++;
    
    // Вагітність корови ~283 дні
    if (pregnancyDays_ >= 283) {
        isPregnant_ = false;
        pregnancyDays_ = 0;
        lactationPeriod_ = 305;  // Новий період лактації
        // Тут можна додати народження теляти
    }
}

bool Cow::canBreed() const {
    return isAlive_ && 
           !isPregnant_ && 
           age_ >= 365 * 2 &&  // Мінімум 2 роки
           health_ > 70.0 &&
           hunger_ > 50.0;
}

} // namespace FarmGame
