/**
 * @file Animal.cpp
 * @brief Реалізація базового класу Animal
 */

#include "animals/Animal.hpp"
#include <sstream>
#include <algorithm>

namespace FarmGame {

int Animal::nextId_ = 1;

Animal::Animal(const std::string& name, int age)
    : name_(name)
    , age_(age)
    , health_(100.0)
    , hunger_(100.0)
    , happiness_(75.0)
    , state_(AnimalState::HEALTHY)
    , isAlive_(true)
    , productionCooldown_(0)
    , id_(nextId_++)
    , birthTime_(std::time(nullptr))
{
    stats_ = AnimalStats();
}

bool Animal::feed(double feedQuality, double amount) {
    if (!isAlive_) return false;
    
    // Розрахувати ефективність годування
    double efficiency = feedQuality * 0.7 + 0.3;
    double hungerIncrease = amount * 20.0 * efficiency;
    
    double oldHunger = hunger_;
    hunger_ = std::min(100.0, hunger_ + hungerIncrease);
    
    // Покращити здоров'я якщо корм якісний
    if (feedQuality > 0.8) {
        health_ = std::min(100.0, health_ + 2.0);
    }
    
    // Покращити щастя
    happiness_ = std::min(100.0, happiness_ + 5.0 * feedQuality);
    
    // Виклик обробника
    onFed(feedQuality, amount);
    
    // Оновити статистику
    stats_.totalFed++;
    
    // Оновити стан
    updateState();
    
    return true;
}

void Animal::update(double deltaTime) {
    if (!isAlive_) return;
    
    // Зменшення ситості з часом
    hunger_ -= 0.1 * deltaTime;
    hunger_ = std::max(0.0, hunger_);
    
    // Зменшення щастя з часом
    happiness_ -= 0.05 * deltaTime;
    happiness_ = std::max(0.0, happiness_);
    
    // Вплив голоду на здоров'я
    if (hunger_ < 20.0) {
        health_ -= 0.2 * deltaTime;
    }
    
    // Вплив щастя на здоров'я
    if (happiness_ < 20.0) {
        health_ -= 0.1 * deltaTime;
    }
    
    // Смерть від голоду або хвороби
    if (health_ <= 0.0 || hunger_ <= 0.0) {
        isAlive_ = false;
        state_ = AnimalState::SICK;
        return;
    }
    
    // Зменшення кулдауну виробництва
    if (productionCooldown_ > 0) {
        productionCooldown_--;
    }
    
    updateState();
}

double Animal::heal() {
    if (!isAlive_) return 0.0;
    
    double cost = (100.0 - health_) * 2.0;  // Вартість залежить від стану
    health_ = 100.0;
    happiness_ = std::min(100.0, happiness_ + 10.0);
    
    if (state_ == AnimalState::SICK) {
        state_ = AnimalState::HEALTHY;
    }
    
    return cost;
}

void Animal::pet() {
    if (!isAlive_) return;
    
    happiness_ = std::min(100.0, happiness_ + 10.0);
    
    // Невеликий бонус до здоров'я
    health_ = std::min(100.0, health_ + 1.0);
}

bool Animal::canProduce() const {
    return isAlive_ && 
           productionCooldown_ <= 0 && 
           hunger_ > 30.0 && 
           health_ > 20.0;
}

double Animal::getCurrentValue() const {
    // Базова ціна * модифікатори
    double value = getBasePrice();
    value *= (health_ / 100.0);
    value *= (0.5 + happiness_ / 200.0);
    
    // Старі тварини коштують менше
    double ageFactor = 1.0;
    if (age_ > 365 * 5) {  // Більше 5 років
        ageFactor = 0.5;
    } else if (age_ > 365 * 3) {
        ageFactor = 0.75;
    }
    value *= ageFactor;
    
    return value;
}

std::string Animal::getStateString() const {
    switch (state_) {
        case AnimalState::HEALTHY: return "Здорова";
        case AnimalState::HUNGRY: return "Голодна";
        case AnimalState::SICK: return "Хвора";
        case AnimalState::PRODUCING: return "Виробляє";
        case AnimalState::SLEEPING: return "Спить";
        case AnimalState::HAPPY: return "Щаслива";
        default: return "Невідомо";
    }
}

void Animal::ageOneDay() {
    age_++;
    stats_.daysOnFarm++;
    
    // Природне старіння впливає на здоров'я
    if (age_ > 365 * 7) {  // Більше 7 років
        health_ -= 0.5;
    }
}

std::string Animal::getInfo() const {
    std::ostringstream oss;
    oss << "=== " << getTypeName() << " ===" << std::endl;
    oss << "Ім'я: " << name_ << std::endl;
    oss << "ID: " << id_ << std::endl;
    oss << "Вік: " << (age_ / 365) << " років " << (age_ % 365) << " днів" << std::endl;
    oss << "Здоров'я: " << static_cast<int>(health_) << "%" << std::endl;
    oss << "Ситість: " << static_cast<int>(hunger_) << "%" << std::endl;
    oss << "Щастя: " << static_cast<int>(happiness_) << "%" << std::endl;
    oss << "Стан: " << getStateString() << std::endl;
    oss << "Продукція: " << getProductName() << std::endl;
    oss << "Вартість: " << getCurrentValue() << " грн" << std::endl;
    return oss.str();
}

void Animal::onFed(double quality, double amount) {
    // Базова реалізація - нічого
    // Похідні класи можуть перевизначити
}

void Animal::onStateChanged(AnimalState oldState, AnimalState newState) {
    // Базова реалізація
}

double Animal::calculateProductionBonus() const {
    double bonus = 1.0;
    bonus *= (health_ / 100.0);
    bonus *= (0.7 + happiness_ / 300.0);
    bonus *= (0.8 + hunger_ / 500.0);
    return bonus;
}

void Animal::updateState() {
    AnimalState oldState = state_;
    
    if (health_ < 30.0) {
        state_ = AnimalState::SICK;
    } else if (hunger_ < 30.0) {
        state_ = AnimalState::HUNGRY;
    } else if (happiness_ > 80.0 && health_ > 80.0) {
        state_ = AnimalState::HAPPY;
    } else {
        state_ = AnimalState::HEALTHY;
    }
    
    if (oldState != state_) {
        onStateChanged(oldState, state_);
    }
}

} // namespace FarmGame
