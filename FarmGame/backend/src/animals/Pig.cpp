/**
 * @file Pig.cpp
 * @brief Реалізація класу Pig
 */

#include "animals/Pig.hpp"
#include <algorithm>
#include <random>

namespace FarmGame {

Pig::Pig(const std::string& name, int age, PigBreed breed)
    : Animal(name, age)
    , breed_(breed)
    , weight_(50.0)
    , meatQuality_(70.0)
    , truffleSkill_(0.0)
    , trufflesFound_(0)
{
    initializeBreedStats();
}

void Pig::initializeBreedStats() {
    switch (breed_) {
        case PigBreed::LANDRACE:
            meatQuality_ = 80.0;
            weight_ = 60.0;
            break;
        case PigBreed::YORKSHIRE:
            meatQuality_ = 75.0;
            weight_ = 55.0;
            truffleSkill_ = 30.0;  // Може шукати трюфелі
            break;
        case PigBreed::DUROC:
            meatQuality_ = 85.0;
            weight_ = 50.0;
            break;
        case PigBreed::HAMPSHIRE:
            meatQuality_ = 90.0;
            weight_ = 55.0;
            break;
        case PigBreed::BERKSHIRE:
            meatQuality_ = 95.0;  // Найкраща якість
            weight_ = 45.0;
            truffleSkill_ = 60.0;  // Найкращі для пошуку трюфелів
            break;
    }
}

std::string Pig::getBreedName() const {
    switch (breed_) {
        case PigBreed::LANDRACE: return "Ландрас";
        case PigBreed::YORKSHIRE: return "Йоркшир";
        case PigBreed::DUROC: return "Дюрок";
        case PigBreed::HAMPSHIRE: return "Гемпшир";
        case PigBreed::BERKSHIRE: return "Беркшир";
        default: return "Невідома";
    }
}

double Pig::produce() {
    if (!canProduce()) return 0.0;
    
    // Свині можуть шукати трюфелі
    if (canFindTruffles()) {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<> dis(0.0, 100.0);
        
        if (dis(gen) < truffleSkill_) {
            productionCooldown_ = 24;
            trufflesFound_++;
            stats_.totalProduced++;
            // Повернути ціну трюфеля
            return 1.0;  // 1 трюфель
        }
    }
    
    // Інакше - виробництво добрива
    double manure = weight_ * 0.05 * calculateProductionBonus();
    productionCooldown_ = 12;
    stats_.totalProduced++;
    
    return manure;
}

double Pig::getProductPrice() const {
    // Якщо свиня може знаходити трюфелі
    if (canFindTruffles()) {
        return 500.0;  // Ціна трюфеля
    }
    return 2.0;  // Ціна добрива за кг
}

double Pig::getBasePrice() const {
    double basePrice = 3000.0;
    
    switch (breed_) {
        case PigBreed::LANDRACE:
            basePrice = 3500.0;
            break;
        case PigBreed::YORKSHIRE:
            basePrice = 3200.0;
            break;
        case PigBreed::DUROC:
            basePrice = 4000.0;
            break;
        case PigBreed::HAMPSHIRE:
            basePrice = 4500.0;
            break;
        case PigBreed::BERKSHIRE:
            basePrice = 5500.0;
            break;
    }
    
    // Вартість також залежить від ваги
    basePrice += weight_ * 50.0;
    
    return basePrice;
}

std::unique_ptr<Animal> Pig::clone() const {
    auto pig = std::make_unique<Pig>(name_, age_, breed_);
    pig->health_ = health_;
    pig->hunger_ = hunger_;
    pig->happiness_ = happiness_;
    pig->weight_ = weight_;
    pig->meatQuality_ = meatQuality_;
    pig->truffleSkill_ = truffleSkill_;
    return pig;
}

bool Pig::searchTruffles() {
    if (!canFindTruffles() || productionCooldown_ > 0) return false;
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 100.0);
    
    double chance = truffleSkill_ * calculateProductionBonus();
    
    if (dis(gen) < chance) {
        trufflesFound_++;
        productionCooldown_ = 24;
        stats_.totalProduced++;
        happiness_ = std::min(100.0, happiness_ + 15.0);  // Свиня радіє
        return true;
    }
    
    // Пошук стомлює
    hunger_ -= 10.0;
    productionCooldown_ = 6;
    return false;
}

double Pig::slaughter() {
    if (!isAlive_) return 0.0;
    
    // Розрахувати кількість м'яса
    double meat = weight_ * 0.7;  // ~70% від ваги - м'ясо
    
    // Якість м'яса впливає на ціну
    double qualityMultiplier = meatQuality_ / 100.0;
    double value = meat * 80.0 * qualityMultiplier;  // 80 грн/кг
    
    isAlive_ = false;
    
    return value;
}

void Pig::update(double deltaTime) {
    Animal::update(deltaTime);
    
    if (!isAlive_) return;
    
    // Свині набирають вагу
    if (hunger_ > 70.0) {
        gainWeight(0.1 * deltaTime);
    }
    
    // Тренування навички пошуку трюфелів
    if (truffleSkill_ > 0 && happiness_ > 60.0) {
        truffleSkill_ = std::min(100.0, truffleSkill_ + 0.01 * deltaTime);
    }
}

bool Pig::feed(double feedQuality, double amount) {
    if (!Animal::feed(feedQuality, amount)) return false;
    
    // Годування впливає на набір ваги
    gainWeight(amount * feedQuality * 0.3);
    
    // Комбікорм покращує якість м'яса
    if (feedQuality > 0.8) {
        meatQuality_ = std::min(100.0, meatQuality_ + 0.2);
    }
    
    return true;
}

void Pig::onFed(double quality, double amount) {
    // Свині люблять їсти
    happiness_ = std::min(100.0, happiness_ + 5.0);
}

double Pig::calculateProductionBonus() const {
    double bonus = Animal::calculateProductionBonus();
    
    // Беркширські свині краще знаходять трюфелі
    if (breed_ == PigBreed::BERKSHIRE && canFindTruffles()) {
        bonus *= 1.3;
    }
    
    return bonus;
}

void Pig::gainWeight(double amount) {
    // Максимальна вага залежить від породи
    double maxWeight = 200.0;
    switch (breed_) {
        case PigBreed::LANDRACE:
            maxWeight = 250.0;
            break;
        case PigBreed::DUROC:
            maxWeight = 220.0;
            break;
        default:
            maxWeight = 200.0;
    }
    
    weight_ = std::min(maxWeight, weight_ + amount);
}

} // namespace FarmGame
