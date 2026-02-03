/**
 * @file Farm.hpp
 * @brief Головний клас ферми - об'єднує всі компоненти
 */

#ifndef FARM_HPP
#define FARM_HPP

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <functional>

#include "../animals/Animal.hpp"
#include "../animals/Cow.hpp"
#include "../animals/Chicken.hpp"
#include "../animals/Pig.hpp"
#include "../animals/Sheep.hpp"
#include "../animals/Goat.hpp"
#include "../animals/Duck.hpp"
#include "../animals/Rabbit.hpp"
#include "../animals/Horse.hpp"
#include "../production/Feed.hpp"
#include "../production/Product.hpp"
#include "../production/Storage.hpp"
#include "Farmer.hpp"

namespace FarmGame {

/**
 * @enum Season
 * @brief Пора року
 */
enum class Season {
    SPRING,     // Весна
    SUMMER,     // Літо
    AUTUMN,     // Осінь
    WINTER      // Зима
};

/**
 * @enum Weather
 * @brief Погода
 */
enum class Weather {
    SUNNY,      // Сонячно
    CLOUDY,     // Хмарно
    RAINY,      // Дощ
    STORMY,     // Шторм
    SNOWY,      // Сніг
    FOGGY       // Туман
};

/**
 * @struct FarmStats
 * @brief Загальна статистика ферми
 */
struct FarmStats {
    int totalAnimals = 0;
    int totalProducts = 0;
    double totalValue = 0.0;
    int daysPassed = 0;
    double dailyIncome = 0.0;
    double dailyExpenses = 0.0;
    int reputation = 0;
};

/**
 * @struct Building
 * @brief Будівля на фермі
 */
struct Building {
    std::string name;
    std::string type;
    int level;
    int capacity;
    double maintenanceCost;
    bool isUpgradable;
};

/**
 * @class Farm
 * @brief Головний клас ферми
 * 
 * Реалізує патерн Facade для об'єднання всіх підсистем
 */
class Farm {
public:
    /**
     * @brief Конструктор
     * @param name Назва ферми
     * @param farmerName Ім'я фермера
     */
    Farm(const std::string& name, const std::string& farmerName);
    ~Farm() = default;
    
    // ==================== Управління тваринами ====================
    
    /**
     * @brief Додати тварину на ферму
     * @param animal Вказівник на тварину
     * @return true якщо успішно
     */
    bool addAnimal(std::unique_ptr<Animal> animal);
    
    /**
     * @brief Видалити тварину з ферми
     * @param animalId ID тварини
     * @return true якщо успішно
     */
    bool removeAnimal(int animalId);
    
    /**
     * @brief Отримати тварину за ID
     * @param animalId ID тварини
     * @return Вказівник на тварину або nullptr
     */
    Animal* getAnimal(int animalId);
    
    /**
     * @brief Отримати всіх тварин
     * @return Вектор вказівників на тварин
     */
    std::vector<Animal*> getAllAnimals();
    
    /**
     * @brief Отримати тварин певного типу
     * @param type Тип тварини
     * @return Вектор вказівників
     */
    std::vector<Animal*> getAnimalsByType(AnimalType type);
    
    /**
     * @brief Отримати кількість тварин
     * @return Загальна кількість
     */
    int getAnimalCount() const { return static_cast<int>(animals_.size()); }
    
    /**
     * @brief Отримати кількість тварин певного типу
     * @param type Тип тварини
     * @return Кількість
     */
    int getAnimalCountByType(AnimalType type) const;
    
    // ==================== Управління кормами ====================
    
    /**
     * @brief Додати корм на склад
     * @param type Тип корму
     * @param amount Кількість
     * @return true якщо успішно
     */
    bool addFeed(FeedType type, double amount);
    
    /**
     * @brief Взяти корм зі складу
     * @param type Тип корму
     * @param amount Кількість
     * @return Взята кількість
     */
    double takeFeed(FeedType type, double amount);
    
    /**
     * @brief Перевірити наявність корму
     * @param type Тип корму
     * @param amount Кількість
     * @return true якщо є достатньо
     */
    bool hasFeed(FeedType type, double amount) const;
    
    /**
     * @brief Отримати кількість корму
     * @param type Тип корму
     * @return Кількість на складі
     */
    double getFeedAmount(FeedType type) const;
    
    // ==================== Управління продукцією ====================
    
    /**
     * @brief Додати продукт на склад
     * @param product Вказівник на продукт
     * @return true якщо успішно
     */
    bool addProduct(std::shared_ptr<Product> product);
    
    /**
     * @brief Взяти продукт зі складу
     * @param type Тип продукту
     * @param amount Кількість
     * @return Взята кількість
     */
    double takeProduct(ProductType type, double amount);
    
    /**
     * @brief Отримати кількість продукту
     * @param type Тип продукту
     * @return Кількість на складі
     */
    double getProductAmount(ProductType type) const;
    
    // ==================== Основні операції ====================
    
    /**
     * @brief Годувати всіх тварин
     * @return Кількість погодованих
     */
    int feedAllAnimals();
    
    /**
     * @brief Зібрати всю продукцію
     * @return Кількість зібраної продукції
     */
    int collectAllProducts();
    
    /**
     * @brief Продати всю продукцію
     * @return Отримані гроші
     */
    double sellAllProducts();
    
    /**
     * @brief Лікувати хворих тварин
     * @return Кількість вилікуваних
     */
    int healSickAnimals();
    
    // ==================== Час та погода ====================
    
    Season getCurrentSeason() const { return currentSeason_; }
    Weather getCurrentWeather() const { return currentWeather_; }
    int getCurrentDay() const { return currentDay_; }
    int getCurrentHour() const { return currentHour_; }
    std::string getTimeString() const;
    std::string getSeasonString() const;
    std::string getWeatherString() const;
    
    void advanceTime(int hours = 1);
    void advanceDay();
    void setWeather(Weather weather) { currentWeather_ = weather; }
    
    // ==================== Будівлі ====================
    
    bool addBuilding(const Building& building);
    bool upgradeBuilding(const std::string& name);
    std::vector<Building> getBuildings() const { return buildings_; }
    Building* getBuilding(const std::string& name);
    int getTotalCapacity() const;
    
    // ==================== Економіка ====================
    
    double getMoney() const { return farmer_->getMoney(); }
    double getDailyIncome() const { return dailyIncome_; }
    double getDailyExpenses() const { return dailyExpenses_; }
    double getNetWorth() const;
    void calculateDailyFinances();
    
    // ==================== Статистика ====================
    
    FarmStats getStats() const;
    std::string getName() const { return name_; }
    void setName(const std::string& name) { name_ = name; }
    Farmer* getFarmer() { return farmer_.get(); }
    int getReputation() const { return reputation_; }
    void addReputation(int amount);
    
    // ==================== Сховища ====================
    
    FeedStorage* getFeedStorage() { return feedStorage_.get(); }
    ProductStorage* getProductStorage() { return productStorage_.get(); }
    Refrigerator* getRefrigerator() { return refrigerator_.get(); }
    
    // ==================== Оновлення гри ====================
    
    void update(double deltaTime);
    void onDayStart();
    void onDayEnd();
    void processSeasonChange();
    
    // ==================== Серіалізація ====================
    
    std::string serialize() const;
    static std::unique_ptr<Farm> deserialize(const std::string& data);
    bool saveToFile(const std::string& filename) const;
    static std::unique_ptr<Farm> loadFromFile(const std::string& filename);
    
    // ==================== События ====================
    
    using EventCallback = std::function<void(const std::string&)>;
    void setEventCallback(EventCallback callback) { eventCallback_ = callback; }
    void triggerEvent(const std::string& eventMessage);
    
private:
    std::string name_;
    std::unique_ptr<Farmer> farmer_;
    std::vector<std::unique_ptr<Animal>> animals_;
    std::unique_ptr<FeedStorage> feedStorage_;
    std::unique_ptr<ProductStorage> productStorage_;
    std::unique_ptr<Refrigerator> refrigerator_;
    std::vector<Building> buildings_;
    
    // Час та погода
    int currentDay_;
    int currentHour_;
    Season currentSeason_;
    Weather currentWeather_;
    int daysInSeason_;
    
    // Економіка
    double dailyIncome_;
    double dailyExpenses_;
    int reputation_;
    
    // Обробники подій
    EventCallback eventCallback_;
    
    // Внутрішні методи
    void initializeDefaultBuildings();
    void updateSeason();
    void updateWeather();
    void applySeasonEffects();
    void applyWeatherEffects();
    void payMaintenanceCosts();
    void checkAnimalHealth();
    void removeDeadAnimals();
    double calculateMaintenanceCost() const;
    Weather generateRandomWeather() const;
};

// ==================== Фабрика тварин ====================

/**
 * @class AnimalFactory
 * @brief Фабрика для створення тварин (патерн Factory)
 */
class AnimalFactory {
public:
    static std::unique_ptr<Animal> createAnimal(AnimalType type, 
                                                 const std::string& name,
                                                 int age = 0);
    
    static std::unique_ptr<Cow> createCow(const std::string& name, 
                                           CowBreed breed = CowBreed::HOLSTEIN,
                                           int age = 0);
    
    static std::unique_ptr<Chicken> createChicken(const std::string& name,
                                                   ChickenBreed breed = ChickenBreed::LEGHORN,
                                                   int age = 0);
    
    static std::unique_ptr<Pig> createPig(const std::string& name,
                                           PigBreed breed = PigBreed::YORKSHIRE,
                                           int age = 0);
    
    static std::unique_ptr<Sheep> createSheep(const std::string& name,
                                               SheepBreed breed = SheepBreed::MERINO,
                                               int age = 0);
    
    static std::unique_ptr<Goat> createGoat(const std::string& name,
                                             GoatBreed breed = GoatBreed::SAANEN,
                                             int age = 0);
    
    static std::unique_ptr<Duck> createDuck(const std::string& name,
                                             DuckBreed breed = DuckBreed::PEKIN,
                                             int age = 0);
    
    static std::unique_ptr<Rabbit> createRabbit(const std::string& name,
                                                 RabbitBreed breed = RabbitBreed::NEW_ZEALAND,
                                                 int age = 0);
    
    static std::unique_ptr<Horse> createHorse(const std::string& name,
                                               HorseBreed breed = HorseBreed::QUARTER,
                                               int age = 0);
    
    static double getAnimalPrice(AnimalType type);
    static std::string getAnimalTypeName(AnimalType type);
};

} // namespace FarmGame

#endif // FARM_HPP
