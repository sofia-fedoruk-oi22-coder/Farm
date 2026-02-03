/**
 * @file Farmer.cpp
 * @brief Реалізація класу Farmer
 */

#include "farm/Farmer.hpp"
#include <algorithm>
#include <sstream>
#include <cmath>

namespace FarmGame {

Farmer::Farmer(const std::string& name)
    : name_(name)
    , money_(10000.0)    // Початковий капітал
    , energy_(100.0)
    , maxEnergy_(100.0)
    , level_(1)
    , experience_(0.0)
{
    initializeSkills();
    stats_ = FarmerStats();
}

void Farmer::initializeSkills() {
    skills_[FarmerSkill::ANIMAL_CARE] = 10.0;
    skills_[FarmerSkill::FEEDING] = 10.0;
    skills_[FarmerSkill::MILKING] = 5.0;
    skills_[FarmerSkill::SHEARING] = 5.0;
    skills_[FarmerSkill::VETERINARY] = 5.0;
    skills_[FarmerSkill::TRADING] = 10.0;
    skills_[FarmerSkill::BREEDING] = 5.0;
    skills_[FarmerSkill::CRAFTING] = 5.0;
}

bool Farmer::feedAnimal(Animal* animal, FeedType feed, double amount) {
    if (!animal || !hasEnergy(5.0)) return false;
    
    // Витрата енергії
    useEnergy(5.0);
    
    // Ефективність залежить від навички
    double efficiency = calculateFeedingEfficiency();
    double quality = Feed::getFeedInfo(feed).quality / 100.0 * efficiency;
    
    bool success = animal->feed(quality, amount);
    
    if (success) {
        stats_.animalsFed++;
        addExperience(2.0);
        improveSkill(FarmerSkill::FEEDING, 0.1);
        improveSkill(FarmerSkill::ANIMAL_CARE, 0.05);
    }
    
    return success;
}

int Farmer::feedAllAnimals(AnimalType type, FeedType feed) {
    // Цей метод буде використовуватись через Farm
    // Тут просто повертаємо 0, бо не маємо прямого доступу до тварин
    return 0;
}

std::shared_ptr<Product> Farmer::collectProduct(Animal* animal) {
    if (!animal || !hasEnergy(10.0)) return nullptr;
    
    if (!animal->canProduce()) return nullptr;
    
    useEnergy(10.0);
    
    double amount = animal->produce();
    if (amount <= 0) return nullptr;
    
    // Визначити якість на основі навичок
    double skillBonus = getSkillBonus(FarmerSkill::ANIMAL_CARE);
    ProductQuality quality = Product::calculateQuality(
        animal->getHappiness() * skillBonus
    );
    
    // Створити продукт на основі типу тварини
    ProductType productType;
    switch (animal->getType()) {
        case AnimalType::COW:
            productType = ProductType::MILK;
            improveSkill(FarmerSkill::MILKING, 0.1);
            break;
        case AnimalType::CHICKEN:
            productType = ProductType::CHICKEN_EGG;
            break;
        case AnimalType::SHEEP:
            productType = ProductType::WOOL;
            improveSkill(FarmerSkill::SHEARING, 0.1);
            break;
        case AnimalType::GOAT:
            productType = ProductType::GOAT_MILK;
            break;
        case AnimalType::DUCK:
            productType = ProductType::DUCK_EGG;
            break;
        case AnimalType::PIG:
            productType = ProductType::MANURE;
            break;
        default:
            productType = ProductType::MANURE;
    }
    
    auto product = Product::create(productType, amount, quality);
    
    stats_.productionsCollected++;
    addExperience(5.0);
    
    return product;
}

std::vector<std::shared_ptr<Product>> Farmer::collectAllProducts() {
    // Буде реалізовано через Farm
    return {};
}

double Farmer::healAnimal(Animal* animal) {
    if (!animal || !hasEnergy(20.0)) return 0.0;
    
    useEnergy(20.0);
    
    double cost = animal->heal();
    
    // Знижка залежить від навички ветеринарії
    double discount = getSkillBonus(FarmerSkill::VETERINARY) - 1.0;
    cost *= (1.0 - discount * 0.5);
    
    if (spendMoney(cost)) {
        improveSkill(FarmerSkill::VETERINARY, 0.2);
        addExperience(10.0);
        return cost;
    }
    
    return 0.0;
}

void Farmer::petAnimal(Animal* animal) {
    if (!animal || !hasEnergy(2.0)) return;
    
    useEnergy(2.0);
    animal->pet();
    
    improveSkill(FarmerSkill::ANIMAL_CARE, 0.05);
    addExperience(1.0);
}

double Farmer::sellProduct(std::shared_ptr<Product> product) {
    if (!product) return 0.0;
    
    double price = product->getTotalValue();
    
    // Бонус від торгівлі
    price *= calculateSellingBonus();
    
    addMoney(price);
    stats_.totalEarnings += price;
    
    improveSkill(FarmerSkill::TRADING, 0.1);
    addExperience(3.0);
    
    return price;
}

double Farmer::sellAllProducts(ProductType type) {
    // Буде реалізовано через Farm
    return 0.0;
}

bool Farmer::buyFeed(FeedType type, double amount) {
    FeedInfo info = Feed::getFeedInfo(type);
    double cost = info.pricePerUnit * amount;
    
    // Знижка від торгівлі
    double discount = (getSkillBonus(FarmerSkill::TRADING) - 1.0) * 0.3;
    cost *= (1.0 - discount);
    
    if (spendMoney(cost)) {
        stats_.totalSpending += cost;
        return true;
    }
    
    return false;
}

std::unique_ptr<Animal> Farmer::buyAnimal(AnimalType type, const std::string& name) {
    // Ціна тварини буде визначена у Farm через AnimalFactory
    return nullptr;
}

double Farmer::sellAnimal(Animal* animal) {
    if (!animal) return 0.0;
    
    double price = animal->getCurrentValue();
    price *= calculateSellingBonus();
    
    addMoney(price);
    stats_.animalsSold++;
    stats_.totalEarnings += price;
    
    improveSkill(FarmerSkill::TRADING, 0.2);
    addExperience(15.0);
    
    return price;
}

void Farmer::addMoney(double amount) {
    money_ += amount;
}

bool Farmer::spendMoney(double amount) {
    if (money_ >= amount) {
        money_ -= amount;
        return true;
    }
    return false;
}

double Farmer::getNetWorth() const {
    // Тільки гроші, активи рахуються у Farm
    return money_;
}

double Farmer::getSkillLevel(FarmerSkill skill) const {
    auto it = skills_.find(skill);
    if (it != skills_.end()) {
        return it->second;
    }
    return 0.0;
}

void Farmer::improveSkill(FarmerSkill skill, double amount) {
    if (skills_.find(skill) != skills_.end()) {
        skills_[skill] = std::min(100.0, skills_[skill] + amount);
    }
}

double Farmer::getSkillBonus(FarmerSkill skill) const {
    double level = getSkillLevel(skill);
    return 1.0 + (level / 100.0) * 0.5;  // Максимум +50% бонус
}

bool Farmer::isSkillMaxed(FarmerSkill skill) const {
    return getSkillLevel(skill) >= 100.0;
}

int Farmer::getTotalSkillPoints() const {
    int total = 0;
    for (const auto& pair : skills_) {
        total += static_cast<int>(pair.second);
    }
    return total;
}

void Farmer::useEnergy(double amount) {
    energy_ = std::max(0.0, energy_ - amount);
}

void Farmer::restoreEnergy(double amount) {
    energy_ = std::min(maxEnergy_, energy_ + amount);
}

void Farmer::sleep() {
    energy_ = maxEnergy_;
}

double Farmer::getExperienceToNextLevel() const {
    return level_ * 100.0;  // Простий рівневий прогрес
}

void Farmer::addExperience(double xp) {
    experience_ += xp;
    checkLevelUp();
}

void Farmer::checkLevelUp() {
    while (experience_ >= getExperienceToNextLevel()) {
        experience_ -= getExperienceToNextLevel();
        level_++;
        
        // Бонуси при підвищенні рівня
        maxEnergy_ += 5.0;
        energy_ = maxEnergy_;
        
        // Невеликий бонус до всіх навичок
        for (auto& pair : skills_) {
            pair.second = std::min(100.0, pair.second + 1.0);
        }
    }
}

void Farmer::update(double deltaTime) {
    // Природне відновлення енергії
    if (energy_ < maxEnergy_) {
        restoreEnergy(0.1 * deltaTime);
    }
}

void Farmer::onDayEnd() {
    stats_.daysPlayed++;
}

void Farmer::onDayStart() {
    // Відновлення енергії вранці
    restoreEnergy(30.0);
}

double Farmer::calculateSellingBonus() const {
    return getSkillBonus(FarmerSkill::TRADING);
}

double Farmer::calculateFeedingEfficiency() const {
    return getSkillBonus(FarmerSkill::FEEDING);
}

std::string Farmer::serialize() const {
    std::ostringstream oss;
    oss << name_ << "|"
        << money_ << "|"
        << energy_ << "|"
        << maxEnergy_ << "|"
        << level_ << "|"
        << experience_ << "|";
    
    // Серіалізація навичок
    for (const auto& pair : skills_) {
        oss << static_cast<int>(pair.first) << ":" << pair.second << ",";
    }
    oss << "|";
    
    // Серіалізація статистики
    oss << stats_.animalsFed << ","
        << stats_.productionsCollected << ","
        << stats_.animalsBought << ","
        << stats_.animalsSold << ","
        << stats_.totalEarnings << ","
        << stats_.totalSpending << ","
        << stats_.daysPlayed << ","
        << stats_.achievementsUnlocked;
    
    return oss.str();
}

std::unique_ptr<Farmer> Farmer::deserialize(const std::string& data) {
    // Реалізація десеріалізації
    // Спрощена версія - потрібен повний парсинг
    auto farmer = std::make_unique<Farmer>("Farmer");
    // TODO: Повний парсинг даних
    return farmer;
}

} // namespace FarmGame
