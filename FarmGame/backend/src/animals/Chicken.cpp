/**
 * @file Chicken.cpp
 * @brief Реалізація класу Chicken
 */

#include "animals/Chicken.hpp"
#include <algorithm>
#include <random>

namespace FarmGame {

Chicken::Chicken(const std::string& name, int age, ChickenBreed breed)
    : Animal(name, age)
    , breed_(breed)
    , eggQuality_(70.0)
    , eggsPerDay_(1)
    , isBroody_(false)
    , incubationDays_(0)
    , chicks_(0)
    , eggsCollected_(0)
{
    initializeBreedStats();
}

void Chicken::initializeBreedStats() {
    switch (breed_) {
        case ChickenBreed::LEGHORN:
            eggsPerDay_ = 1;
            eggQuality_ = 75.0;
            break;
        case ChickenBreed::RHODE_ISLAND:
            eggsPerDay_ = 1;
            eggQuality_ = 80.0;
            break;
        case ChickenBreed::PLYMOUTH:
            eggsPerDay_ = 1;
            eggQuality_ = 70.0;
            break;
        case ChickenBreed::SUSSEX:
            eggsPerDay_ = 1;
            eggQuality_ = 85.0;
            break;
        case ChickenBreed::ORPINGTON:
            eggsPerDay_ = 1;
            eggQuality_ = 90.0;  // Великі яйця
            break;
    }
}

std::string Chicken::getBreedName() const {
    switch (breed_) {
        case ChickenBreed::LEGHORN: return "Леггорн";
        case ChickenBreed::RHODE_ISLAND: return "Род-Айленд";
        case ChickenBreed::PLYMOUTH: return "Плімутрок";
        case ChickenBreed::SUSSEX: return "Сассекс";
        case ChickenBreed::ORPINGTON: return "Орпінгтон";
        default: return "Невідома";
    }
}

double Chicken::produce() {
    if (!canProduce()) return 0.0;
    
    // Шанс знести яйце
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    
    double productionChance = 0.8 * calculateProductionBonus();
    
    if (dis(gen) > productionChance) {
        return 0.0;  // Сьогодні яєць немає
    }
    
    // Кількість яєць
    double eggs = eggsPerDay_ * calculateProductionBonus();
    
    // Бонус якщо курка щаслива
    if (happiness_ > 80.0) {
        eggs *= 1.2;
    }
    
    // Кулдаун 24 години
    productionCooldown_ = 24;
    eggsCollected_++;
    
    // Оновити статистику
    stats_.totalProduced++;
    stats_.totalEarnings += eggs * getProductPrice();
    
    return eggs;
}

double Chicken::getProductPrice() const {
    double basePrice = 5.0;  // Ціна за яйце
    double qualityMultiplier = 0.5 + (eggQuality_ / 100.0);
    return basePrice * qualityMultiplier;
}

double Chicken::getBasePrice() const {
    double basePrice = 150.0;
    
    switch (breed_) {
        case ChickenBreed::LEGHORN:
            basePrice = 120.0;
            break;
        case ChickenBreed::RHODE_ISLAND:
            basePrice = 180.0;
            break;
        case ChickenBreed::PLYMOUTH:
            basePrice = 160.0;
            break;
        case ChickenBreed::SUSSEX:
            basePrice = 200.0;
            break;
        case ChickenBreed::ORPINGTON:
            basePrice = 250.0;
            break;
    }
    
    return basePrice;
}

std::unique_ptr<Animal> Chicken::clone() const {
    auto chicken = std::make_unique<Chicken>(name_, age_, breed_);
    chicken->health_ = health_;
    chicken->hunger_ = hunger_;
    chicken->happiness_ = happiness_;
    chicken->eggQuality_ = eggQuality_;
    chicken->eggsPerDay_ = eggsPerDay_;
    return chicken;
}

void Chicken::update(double deltaTime) {
    Animal::update(deltaTime);
    
    if (!isAlive_) return;
    
    // Оновити насиджування
    if (isBroody_) {
        incubationDays_++;
        
        // Курча вилупляється через 21 день
        if (incubationDays_ >= 21) {
            chicks_++;
            incubationDays_ = 0;
            isBroody_ = false;
        }
    }
}

bool Chicken::feed(double feedQuality, double amount) {
    if (!Animal::feed(feedQuality, amount)) return false;
    
    // Якісне зерно покращує якість яєць
    if (feedQuality > 0.8) {
        eggQuality_ = std::min(100.0, eggQuality_ + 0.3);
    }
    
    return true;
}

void Chicken::onFed(double quality, double amount) {
    // Зерно особливо добре для курей
    if (quality > 0.7) {
        happiness_ = std::min(100.0, happiness_ + 3.0);
    }
}

double Chicken::calculateProductionBonus() const {
    double bonus = Animal::calculateProductionBonus();
    
    // Леггорни найкращі несучки
    if (breed_ == ChickenBreed::LEGHORN) {
        bonus *= 1.15;
    }
    
    return bonus;
}

void Chicken::hatchEggs() {
    if (!isBroody_ && health_ > 50.0 && age_ >= 180) {
        isBroody_ = true;
        incubationDays_ = 0;
    }
}

void Chicken::collectChicks() {
    chicks_ = 0;  // Курчат забрано
}

} // namespace FarmGame
