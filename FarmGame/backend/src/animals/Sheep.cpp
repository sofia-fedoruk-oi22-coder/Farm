/**
 * @file Sheep.cpp
 * @brief Реалізація класу Sheep
 */

#include "animals/Sheep.hpp"
#include <algorithm>
#include <random>

namespace FarmGame {

Sheep::Sheep(const std::string& name, int age, SheepBreed breed)
    : Animal(name, age)
    , breed_(breed)
    , woolQuality_(70.0)
    , woolLength_(0.0)
    , woolGrowthRate_(0.05)
    , lambs_(0)
    , isPregnant_(false)
    , pregnancyDays_(0)
{
    initializeBreedStats();
}

void Sheep::initializeBreedStats() {
    switch (breed_) {
        case SheepBreed::MERINO:
            woolQuality_ = 95.0;   // Найкраща вовна
            woolGrowthRate_ = 0.08;
            break;
        case SheepBreed::SUFFOLK:
            woolQuality_ = 60.0;   // М'ясна порода
            woolGrowthRate_ = 0.04;
            break;
        case SheepBreed::DORSET:
            woolQuality_ = 75.0;
            woolGrowthRate_ = 0.06;
            break;
        case SheepBreed::ROMANOV:
            woolQuality_ = 70.0;
            woolGrowthRate_ = 0.05;
            break;
        case SheepBreed::LINCOLN:
            woolQuality_ = 85.0;   // Довга вовна
            woolGrowthRate_ = 0.1;
            break;
    }
}

std::string Sheep::getBreedName() const {
    switch (breed_) {
        case SheepBreed::MERINO: return "Меріно";
        case SheepBreed::SUFFOLK: return "Суффолк";
        case SheepBreed::DORSET: return "Дорсет";
        case SheepBreed::ROMANOV: return "Романівська";
        case SheepBreed::LINCOLN: return "Лінкольн";
        default: return "Невідома";
    }
}

double Sheep::produce() {
    // Вівці виробляють вовну тільки при стрижці
    // Цей метод повертає 0 якщо вовна ще не виросла
    if (!canProduce() || !canBeSheared()) return 0.0;
    
    return shear();
}

double Sheep::shear() {
    if (!canBeSheared()) return 0.0;
    
    // Кількість вовни залежить від довжини
    double wool = woolLength_ * 0.5 * calculateProductionBonus();
    
    // Бонус від породи
    if (breed_ == SheepBreed::MERINO) {
        wool *= 1.3;
    } else if (breed_ == SheepBreed::LINCOLN) {
        wool *= 1.2;
    }
    
    // Скинути довжину вовни
    woolLength_ = 0.0;
    
    // Кулдаун (вовна має відрости)
    productionCooldown_ = 24 * 30;  // ~30 днів
    
    // Оновити статистику
    stats_.totalProduced++;
    stats_.totalEarnings += wool * getProductPrice();
    
    // Вівці не люблять коли їх стрижуть, але потім легше
    happiness_ = std::max(50.0, happiness_ - 10.0);
    
    return wool;
}

double Sheep::getProductPrice() const {
    double basePrice = 50.0;  // Ціна за кг вовни
    double qualityMultiplier = 0.5 + (woolQuality_ / 100.0);
    
    // Меріно коштує дорожче
    if (breed_ == SheepBreed::MERINO) {
        basePrice = 80.0;
    }
    
    return basePrice * qualityMultiplier;
}

double Sheep::getBasePrice() const {
    double basePrice = 2000.0;
    
    switch (breed_) {
        case SheepBreed::MERINO:
            basePrice = 4000.0;
            break;
        case SheepBreed::SUFFOLK:
            basePrice = 2500.0;
            break;
        case SheepBreed::DORSET:
            basePrice = 2800.0;
            break;
        case SheepBreed::ROMANOV:
            basePrice = 2200.0;
            break;
        case SheepBreed::LINCOLN:
            basePrice = 3500.0;
            break;
    }
    
    return basePrice;
}

std::unique_ptr<Animal> Sheep::clone() const {
    auto sheep = std::make_unique<Sheep>(name_, age_, breed_);
    sheep->health_ = health_;
    sheep->hunger_ = hunger_;
    sheep->happiness_ = happiness_;
    sheep->woolQuality_ = woolQuality_;
    sheep->woolLength_ = woolLength_;
    sheep->woolGrowthRate_ = woolGrowthRate_;
    return sheep;
}

void Sheep::breedLambs() {
    if (!isPregnant_ && age_ >= 365 && health_ > 70.0) {
        isPregnant_ = true;
        pregnancyDays_ = 0;
    }
}

void Sheep::update(double deltaTime) {
    Animal::update(deltaTime);
    
    if (!isAlive_) return;
    
    // Ріст вовни
    growWool(deltaTime);
    
    // Оновити вагітність
    if (isPregnant_) {
        pregnancyDays_++;
        
        // Вагітність вівці ~150 днів
        if (pregnancyDays_ >= 150) {
            // Народження ягнят
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> dis(1, 3);
            
            lambs_ = dis(gen);
            if (breed_ == SheepBreed::ROMANOV) {
                lambs_ += 1;  // Романівські більш плодовиті
            }
            
            isPregnant_ = false;
            pregnancyDays_ = 0;
        }
    }
}

bool Sheep::feed(double feedQuality, double amount) {
    if (!Animal::feed(feedQuality, amount)) return false;
    
    // Якісний корм покращує якість вовни
    if (feedQuality > 0.8) {
        woolQuality_ = std::min(100.0, woolQuality_ + 0.2);
        woolGrowthRate_ = std::min(0.15, woolGrowthRate_ + 0.001);
    }
    
    return true;
}

void Sheep::onFed(double quality, double amount) {
    // Вівці люблять траву
    if (quality > 0.7) {
        happiness_ = std::min(100.0, happiness_ + 4.0);
    }
}

double Sheep::calculateProductionBonus() const {
    double bonus = Animal::calculateProductionBonus();
    
    // Меріно мають найкращу вовну
    if (breed_ == SheepBreed::MERINO) {
        bonus *= 1.2;
    }
    
    return bonus;
}

void Sheep::growWool(double deltaTime) {
    // Вовна росте залежно від здоров'я та ситості
    double growthFactor = (health_ / 100.0) * (hunger_ / 100.0);
    woolLength_ += woolGrowthRate_ * growthFactor * deltaTime;
    
    // Максимальна довжина
    double maxLength = 15.0;
    if (breed_ == SheepBreed::LINCOLN) {
        maxLength = 20.0;
    }
    
    woolLength_ = std::min(maxLength, woolLength_);
}

} // namespace FarmGame
