/**
 * @file Farm.cpp
 * @brief Реалізація головного класу Farm
 */

#include "farm/Farm.hpp"
#include <algorithm>
#include <sstream>
#include <fstream>
#include <random>
#include <ctime>

namespace FarmGame {

Farm::Farm(const std::string& name, const std::string& farmerName)
    : name_(name)
    , farmer_(std::make_unique<Farmer>(farmerName))
    , feedStorage_(std::make_unique<FeedStorage>(1000.0))
    , productStorage_(std::make_unique<ProductStorage>(StorageType::WAREHOUSE, 500.0))
    , refrigerator_(std::make_unique<Refrigerator>(100.0))
    , currentDay_(1)
    , currentHour_(6)  // Починаємо о 6 ранку
    , currentSeason_(Season::SPRING)
    , currentWeather_(Weather::SUNNY)
    , daysInSeason_(0)
    , dailyIncome_(0.0)
    , dailyExpenses_(0.0)
    , reputation_(0)
{
    initializeDefaultBuildings();
    
    // Початкові корми
    addFeed(FeedType::HAY, 50.0);
    addFeed(FeedType::GRAIN, 30.0);
    addFeed(FeedType::MIXED_FEED, 20.0);
}

void Farm::initializeDefaultBuildings() {
    buildings_.push_back({
        "Сарай", "barn", 1, 10, 50.0, true
    });
    buildings_.push_back({
        "Курник", "coop", 1, 20, 30.0, true
    });
    buildings_.push_back({
        "Хлів", "stable", 1, 5, 40.0, true
    });
    buildings_.push_back({
        "Склад", "warehouse", 1, 100, 20.0, true
    });
}

// ==================== Управління тваринами ====================

bool Farm::addAnimal(std::unique_ptr<Animal> animal) {
    if (!animal) return false;
    
    // Перевірка місткості
    int capacity = getTotalCapacity();
    if (static_cast<int>(animals_.size()) >= capacity) {
        triggerEvent("Недостатньо місця для нових тварин!");
        return false;
    }
    
    animals_.push_back(std::move(animal));
    triggerEvent("Нова тварина додана на ферму!");
    return true;
}

bool Farm::removeAnimal(int animalId) {
    auto it = std::find_if(animals_.begin(), animals_.end(),
        [animalId](const std::unique_ptr<Animal>& a) {
            return a->getId() == animalId;
        });
    
    if (it != animals_.end()) {
        animals_.erase(it);
        return true;
    }
    return false;
}

Animal* Farm::getAnimal(int animalId) {
    for (auto& animal : animals_) {
        if (animal->getId() == animalId) {
            return animal.get();
        }
    }
    return nullptr;
}

std::vector<Animal*> Farm::getAllAnimals() {
    std::vector<Animal*> result;
    result.reserve(animals_.size());
    for (auto& animal : animals_) {
        result.push_back(animal.get());
    }
    return result;
}

std::vector<Animal*> Farm::getAnimalsByType(AnimalType type) {
    std::vector<Animal*> result;
    for (auto& animal : animals_) {
        if (animal->getType() == type) {
            result.push_back(animal.get());
        }
    }
    return result;
}

int Farm::getAnimalCountByType(AnimalType type) const {
    return static_cast<int>(std::count_if(animals_.begin(), animals_.end(),
        [type](const std::unique_ptr<Animal>& a) {
            return a->getType() == type;
        }));
}

// ==================== Управління кормами ====================

bool Farm::addFeed(FeedType type, double amount) {
    return feedStorage_->addFeed(type, amount);
}

double Farm::takeFeed(FeedType type, double amount) {
    return feedStorage_->takeFeed(type, amount);
}

bool Farm::hasFeed(FeedType type, double amount) const {
    return feedStorage_->hasFeed(type, amount);
}

double Farm::getFeedAmount(FeedType type) const {
    return feedStorage_->getFeedAmount(type);
}

// ==================== Управління продукцією ====================

bool Farm::addProduct(std::shared_ptr<Product> product) {
    if (!product) return false;
    
    // Швидкопсувні продукти - в холодильник
    if (product->isPerishable()) {
        return refrigerator_->addProduct(product);
    }
    
    return productStorage_->addProduct(product);
}

double Farm::takeProduct(ProductType type, double amount) {
    double taken = productStorage_->takeProduct(type, amount);
    if (taken < amount) {
        taken += refrigerator_->takeProduct(type, amount - taken);
    }
    return taken;
}

double Farm::getProductAmount(ProductType type) const {
    return productStorage_->getProductAmount(type) + 
           refrigerator_->getProductAmount(type);
}

// ==================== Основні операції ====================

int Farm::feedAllAnimals() {
    int fed = 0;
    
    for (auto& animal : animals_) {
        if (!animal->isAlive() || !animal->needsFeeding()) continue;
        
        // Визначити улюблений корм
        FeedType preferredFeed = Feed::stringToFeedType(animal->getFavoriteFeed());
        double needed = animal->getFeedConsumption();
        
        // Спробувати погодувати улюбленим кормом
        if (hasFeed(preferredFeed, needed)) {
            takeFeed(preferredFeed, needed);
            farmer_->feedAnimal(animal.get(), preferredFeed, needed);
            fed++;
        }
        // Інакше - комбікормом
        else if (hasFeed(FeedType::MIXED_FEED, needed)) {
            takeFeed(FeedType::MIXED_FEED, needed);
            farmer_->feedAnimal(animal.get(), FeedType::MIXED_FEED, needed);
            fed++;
        }
    }
    
    if (fed > 0) {
        triggerEvent("Погодовано " + std::to_string(fed) + " тварин");
    }
    
    return fed;
}

int Farm::collectAllProducts() {
    int collected = 0;
    
    for (auto& animal : animals_) {
        if (!animal->isAlive() || !animal->canProduce()) continue;
        
        auto product = farmer_->collectProduct(animal.get());
        if (product) {
            addProduct(product);
            collected++;
        }
    }
    
    if (collected > 0) {
        triggerEvent("Зібрано продукцію від " + std::to_string(collected) + " тварин");
    }
    
    return collected;
}

double Farm::sellAllProducts() {
    double total = 0.0;
    
    // Продати з основного складу
    for (auto& product : productStorage_->getAllProducts()) {
        total += farmer_->sellProduct(product);
    }
    productStorage_->getAllProducts().clear();
    
    // Продати з холодильника
    for (auto& product : refrigerator_->getAllProducts()) {
        total += farmer_->sellProduct(product);
    }
    refrigerator_->getAllProducts().clear();
    
    if (total > 0) {
        dailyIncome_ += total;
        triggerEvent("Продано продукції на " + std::to_string(static_cast<int>(total)) + " грн");
    }
    
    return total;
}

int Farm::healSickAnimals() {
    int healed = 0;
    
    for (auto& animal : animals_) {
        if (animal->getState() == AnimalState::SICK) {
            double cost = farmer_->healAnimal(animal.get());
            if (cost > 0) {
                dailyExpenses_ += cost;
                healed++;
            }
        }
    }
    
    if (healed > 0) {
        triggerEvent("Вилікувано " + std::to_string(healed) + " тварин");
    }
    
    return healed;
}

// ==================== Час та погода ====================

std::string Farm::getTimeString() const {
    std::ostringstream oss;
    oss << "День " << currentDay_ << ", " << currentHour_ << ":00";
    return oss.str();
}

std::string Farm::getSeasonString() const {
    switch (currentSeason_) {
        case Season::SPRING: return "Весна";
        case Season::SUMMER: return "Літо";
        case Season::AUTUMN: return "Осінь";
        case Season::WINTER: return "Зима";
        default: return "Невідомо";
    }
}

std::string Farm::getWeatherString() const {
    switch (currentWeather_) {
        case Weather::SUNNY: return "Сонячно";
        case Weather::CLOUDY: return "Хмарно";
        case Weather::RAINY: return "Дощ";
        case Weather::STORMY: return "Шторм";
        case Weather::SNOWY: return "Сніг";
        case Weather::FOGGY: return "Туман";
        default: return "Невідомо";
    }
}

void Farm::advanceTime(int hours) {
    for (int i = 0; i < hours; ++i) {
        currentHour_++;
        
        if (currentHour_ >= 24) {
            advanceDay();
            currentHour_ = 0;
        }
        
        // Оновити всі сутності
        update(1.0);
    }
}

void Farm::advanceDay() {
    onDayEnd();
    currentDay_++;
    daysInSeason_++;
    onDayStart();
    
    // Зміна сезону кожні 30 днів
    if (daysInSeason_ >= 30) {
        processSeasonChange();
    }
    
    // Зміна погоди
    updateWeather();
}

// ==================== Будівлі ====================

bool Farm::addBuilding(const Building& building) {
    buildings_.push_back(building);
    return true;
}

bool Farm::upgradeBuilding(const std::string& name) {
    for (auto& building : buildings_) {
        if (building.name == name && building.isUpgradable) {
            double cost = building.level * 1000.0;
            if (farmer_->spendMoney(cost)) {
                building.level++;
                building.capacity *= 1.5;
                dailyExpenses_ += cost;
                triggerEvent(name + " покращено до рівня " + std::to_string(building.level));
                return true;
            }
        }
    }
    return false;
}

Building* Farm::getBuilding(const std::string& name) {
    for (auto& building : buildings_) {
        if (building.name == name) {
            return &building;
        }
    }
    return nullptr;
}

int Farm::getTotalCapacity() const {
    int total = 0;
    for (const auto& building : buildings_) {
        if (building.type == "barn" || building.type == "coop" || building.type == "stable") {
            total += building.capacity;
        }
    }
    return total;
}

// ==================== Економіка ====================

double Farm::getNetWorth() const {
    double worth = farmer_->getMoney();
    
    // Вартість тварин
    for (const auto& animal : animals_) {
        worth += animal->getCurrentValue();
    }
    
    // Вартість продукції
    worth += feedStorage_->getTotalFeedValue();
    worth += productStorage_->getTotalProductValue();
    worth += refrigerator_->getTotalProductValue();
    
    // Вартість будівель
    for (const auto& building : buildings_) {
        worth += building.level * 500.0;
    }
    
    return worth;
}

void Farm::calculateDailyFinances() {
    dailyExpenses_ = calculateMaintenanceCost();
    
    // Витрати на корми
    double feedCost = 0.0;
    for (const auto& animal : animals_) {
        feedCost += animal->getFeedConsumption() * 5.0;
    }
    dailyExpenses_ += feedCost;
}

double Farm::calculateMaintenanceCost() const {
    double cost = 0.0;
    for (const auto& building : buildings_) {
        cost += building.maintenanceCost;
    }
    return cost;
}

// ==================== Статистика ====================

FarmStats Farm::getStats() const {
    FarmStats stats;
    stats.totalAnimals = static_cast<int>(animals_.size());
    stats.totalProducts = productStorage_->getAllProducts().size() + 
                         refrigerator_->getAllProducts().size();
    stats.totalValue = getNetWorth();
    stats.daysPassed = currentDay_;
    stats.dailyIncome = dailyIncome_;
    stats.dailyExpenses = dailyExpenses_;
    stats.reputation = reputation_;
    return stats;
}

void Farm::addReputation(int amount) {
    reputation_ += amount;
    if (reputation_ < 0) reputation_ = 0;
}

// ==================== Оновлення гри ====================

void Farm::update(double deltaTime) {
    // Оновити фермера
    farmer_->update(deltaTime);
    
    // Оновити всіх тварин
    for (auto& animal : animals_) {
        animal->update(deltaTime);
    }
    
    // Застосувати ефекти погоди
    applyWeatherEffects();
    
    // Видалити мертвих тварин
    removeDeadAnimals();
    
    // Перевірити здоров'я тварин
    checkAnimalHealth();
}

void Farm::onDayStart() {
    farmer_->onDayStart();
    
    // Скинути денну статистику
    dailyIncome_ = 0.0;
    dailyExpenses_ = 0.0;
    
    // Оновити вік тварин
    for (auto& animal : animals_) {
        animal->ageOneDay();
    }
    
    // Старіння продукції
    feedStorage_->ageContents();
    productStorage_->ageContents();
    refrigerator_->ageContents();
    
    // Видалити прострочене
    feedStorage_->removeExpired();
    productStorage_->removeExpired();
    refrigerator_->removeExpired();
    
    triggerEvent("Новий день " + std::to_string(currentDay_) + "! " + getSeasonString() + ", " + getWeatherString());
}

void Farm::onDayEnd() {
    farmer_->onDayEnd();
    
    // Оплата утримання
    payMaintenanceCosts();
    
    calculateDailyFinances();
}

void Farm::processSeasonChange() {
    daysInSeason_ = 0;
    
    switch (currentSeason_) {
        case Season::SPRING:
            currentSeason_ = Season::SUMMER;
            break;
        case Season::SUMMER:
            currentSeason_ = Season::AUTUMN;
            break;
        case Season::AUTUMN:
            currentSeason_ = Season::WINTER;
            break;
        case Season::WINTER:
            currentSeason_ = Season::SPRING;
            break;
    }
    
    applySeasonEffects();
    triggerEvent("Настала нова пора року: " + getSeasonString());
}

void Farm::updateSeason() {
    // Реалізовано в processSeasonChange
}

void Farm::updateWeather() {
    currentWeather_ = generateRandomWeather();
}

Weather Farm::generateRandomWeather() const {
    std::random_device rd;
    std::mt19937 gen(rd());
    
    // Погода залежить від сезону
    std::vector<std::pair<Weather, int>> weights;
    
    switch (currentSeason_) {
        case Season::SPRING:
            weights = {{Weather::SUNNY, 30}, {Weather::CLOUDY, 30}, 
                      {Weather::RAINY, 30}, {Weather::FOGGY, 10}};
            break;
        case Season::SUMMER:
            weights = {{Weather::SUNNY, 60}, {Weather::CLOUDY, 20}, 
                      {Weather::STORMY, 15}, {Weather::FOGGY, 5}};
            break;
        case Season::AUTUMN:
            weights = {{Weather::SUNNY, 20}, {Weather::CLOUDY, 30}, 
                      {Weather::RAINY, 35}, {Weather::FOGGY, 15}};
            break;
        case Season::WINTER:
            weights = {{Weather::SUNNY, 15}, {Weather::CLOUDY, 25}, 
                      {Weather::SNOWY, 50}, {Weather::FOGGY, 10}};
            break;
    }
    
    int total = 0;
    for (const auto& w : weights) total += w.second;
    
    std::uniform_int_distribution<> dis(0, total - 1);
    int roll = dis(gen);
    
    int cumulative = 0;
    for (const auto& w : weights) {
        cumulative += w.second;
        if (roll < cumulative) {
            return w.first;
        }
    }
    
    return Weather::SUNNY;
}

void Farm::applySeasonEffects() {
    // Сезонні ефекти на тварин
    for (auto& animal : animals_) {
        switch (currentSeason_) {
            case Season::SPRING:
                // Весна - бонус до розмноження
                animal->setName(animal->getName()); // Placeholder
                break;
            case Season::SUMMER:
                // Літо - більше продукції
                break;
            case Season::AUTUMN:
                // Осінь - готування до зими
                break;
            case Season::WINTER:
                // Зима - потрібно більше корму
                break;
        }
    }
}

void Farm::applyWeatherEffects() {
    // Погодні ефекти
    switch (currentWeather_) {
        case Weather::STORMY:
            // Шторм - стрес для тварин
            for (auto& animal : animals_) {
                if (animal->isAlive()) {
                    // Зменшення щастя під час шторму
                }
            }
            break;
        case Weather::SNOWY:
            // Сніг - потрібно більше корму
            break;
        default:
            break;
    }
}

void Farm::payMaintenanceCosts() {
    double cost = calculateMaintenanceCost();
    if (farmer_->spendMoney(cost)) {
        dailyExpenses_ += cost;
    }
}

void Farm::checkAnimalHealth() {
    int sick = 0;
    for (const auto& animal : animals_) {
        if (animal->getState() == AnimalState::SICK) {
            sick++;
        }
    }
    
    if (sick > 0) {
        triggerEvent("Увага! " + std::to_string(sick) + " тварин хворіють!");
    }
}

void Farm::removeDeadAnimals() {
    auto it = std::remove_if(animals_.begin(), animals_.end(),
        [](const std::unique_ptr<Animal>& a) {
            return !a->isAlive();
        });
    
    if (it != animals_.end()) {
        int dead = std::distance(it, animals_.end());
        animals_.erase(it, animals_.end());
        triggerEvent("Помер" + std::string(dead > 1 ? "о" : "а") + " " + 
                    std::to_string(dead) + " тварин" + (dead > 1 ? "" : "а"));
    }
}

void Farm::triggerEvent(const std::string& eventMessage) {
    if (eventCallback_) {
        eventCallback_(eventMessage);
    }
}

// ==================== Серіалізація ====================

bool Farm::saveToFile(const std::string& filename) const {
    std::ofstream file(filename);
    if (!file.is_open()) return false;
    
    file << serialize();
    return true;
}

std::unique_ptr<Farm> Farm::loadFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) return nullptr;
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    
    return deserialize(buffer.str());
}

std::string Farm::serialize() const {
    std::ostringstream oss;
    oss << "FARM|" << name_ << "|" << currentDay_ << "|" 
        << static_cast<int>(currentSeason_) << "|"
        << reputation_ << "|";
    oss << farmer_->serialize() << "|";
    oss << "ANIMALS:" << animals_.size();
    // TODO: Повна серіалізація тварин
    return oss.str();
}

std::unique_ptr<Farm> Farm::deserialize(const std::string& data) {
    // TODO: Повна десеріалізація
    return std::make_unique<Farm>("Farm", "Farmer");
}

// ==================== Фабрика тварин ====================

std::unique_ptr<Animal> AnimalFactory::createAnimal(AnimalType type, 
                                                     const std::string& name,
                                                     int age) {
    switch (type) {
        case AnimalType::COW:
            return createCow(name, CowBreed::HOLSTEIN, age);
        case AnimalType::CHICKEN:
            return createChicken(name, ChickenBreed::LEGHORN, age);
        case AnimalType::PIG:
            return createPig(name, PigBreed::YORKSHIRE, age);
        case AnimalType::SHEEP:
            return createSheep(name, SheepBreed::MERINO, age);
        case AnimalType::GOAT:
            return createGoat(name, GoatBreed::SAANEN, age);
        case AnimalType::DUCK:
            return createDuck(name, DuckBreed::PEKIN, age);
        case AnimalType::RABBIT:
            return createRabbit(name, RabbitBreed::NEW_ZEALAND, age);
        case AnimalType::HORSE:
            return createHorse(name, HorseBreed::QUARTER, age);
        default:
            return nullptr;
    }
}

std::unique_ptr<Cow> AnimalFactory::createCow(const std::string& name, 
                                               CowBreed breed, int age) {
    return std::make_unique<Cow>(name, age, breed);
}

std::unique_ptr<Chicken> AnimalFactory::createChicken(const std::string& name,
                                                       ChickenBreed breed, int age) {
    return std::make_unique<Chicken>(name, age, breed);
}

std::unique_ptr<Pig> AnimalFactory::createPig(const std::string& name,
                                               PigBreed breed, int age) {
    return std::make_unique<Pig>(name, age, breed);
}

std::unique_ptr<Sheep> AnimalFactory::createSheep(const std::string& name,
                                                   SheepBreed breed, int age) {
    return std::make_unique<Sheep>(name, age, breed);
}

std::unique_ptr<Goat> AnimalFactory::createGoat(const std::string& name,
                                                 GoatBreed breed, int age) {
    return std::make_unique<Goat>(name, age, breed);
}

std::unique_ptr<Duck> AnimalFactory::createDuck(const std::string& name,
                                                 DuckBreed breed, int age) {
    return std::make_unique<Duck>(name, age, breed);
}

std::unique_ptr<Rabbit> AnimalFactory::createRabbit(const std::string& name,
                                                     RabbitBreed breed, int age) {
    return std::make_unique<Rabbit>(name, age, breed);
}

std::unique_ptr<Horse> AnimalFactory::createHorse(const std::string& name,
                                                   HorseBreed breed, int age) {
    return std::make_unique<Horse>(name, age, breed);
}

double AnimalFactory::getAnimalPrice(AnimalType type) {
    switch (type) {
        case AnimalType::COW: return 15000.0;
        case AnimalType::CHICKEN: return 150.0;
        case AnimalType::PIG: return 3000.0;
        case AnimalType::SHEEP: return 2000.0;
        case AnimalType::GOAT: return 1800.0;
        case AnimalType::DUCK: return 100.0;
        case AnimalType::RABBIT: return 200.0;
        case AnimalType::HORSE: return 25000.0;
        default: return 0.0;
    }
}

std::string AnimalFactory::getAnimalTypeName(AnimalType type) {
    switch (type) {
        case AnimalType::COW: return "Корова";
        case AnimalType::CHICKEN: return "Курка";
        case AnimalType::PIG: return "Свиня";
        case AnimalType::SHEEP: return "Вівця";
        case AnimalType::GOAT: return "Коза";
        case AnimalType::DUCK: return "Качка";
        case AnimalType::RABBIT: return "Кролик";
        case AnimalType::HORSE: return "Кінь";
        default: return "Невідомо";
    }
}

} // namespace FarmGame
