/**
 * @file Farmer.hpp
 * @brief Клас фермера - головний персонаж
 */

#ifndef FARMER_HPP
#define FARMER_HPP

#include <string>
#include <memory>
#include <vector>
#include <map>
#include "../animals/Animal.hpp"
#include "../production/Feed.hpp"
#include "../production/Product.hpp"

namespace FarmGame {

/**
 * @enum FarmerSkill
 * @brief Навички фермера
 */
enum class FarmerSkill {
    ANIMAL_CARE,        // Догляд за тваринами
    FEEDING,            // Годування
    MILKING,            // Доїння
    SHEARING,           // Стрижка
    VETERINARY,         // Ветеринарія
    TRADING,            // Торгівля
    BREEDING,           // Розведення
    CRAFTING            // Ремесло (переробка)
};

/**
 * @struct FarmerStats
 * @brief Статистика фермера
 */
struct FarmerStats {
    int animalsFed = 0;
    int productionsCollected = 0;
    int animalsBought = 0;
    int animalsSold = 0;
    double totalEarnings = 0.0;
    double totalSpending = 0.0;
    int daysPlayed = 0;
    int achievementsUnlocked = 0;
};

/**
 * @class Farmer
 * @brief Фермер - головний персонаж гри
 * 
 * Керує всіма операціями на фермі
 */
class Farmer {
public:
    /**
     * @brief Конструктор
     * @param name Ім'я фермера
     */
    explicit Farmer(const std::string& name);
    ~Farmer() = default;
    
    // ==================== Основні дії з тваринами ====================
    
    /**
     * @brief Погодувати тварину
     * @param animal Вказівник на тварину
     * @param feed Тип корму
     * @param amount Кількість
     * @return true якщо успішно
     */
    bool feedAnimal(Animal* animal, FeedType feed, double amount);
    
    /**
     * @brief Погодувати всіх тварин певного типу
     * @param type Тип тварин
     * @param feed Тип корму
     * @return Кількість погодованих
     */
    int feedAllAnimals(AnimalType type, FeedType feed);
    
    /**
     * @brief Зібрати продукцію від тварини
     * @param animal Вказівник на тварину
     * @return Вказівник на зібрану продукцію
     */
    std::shared_ptr<Product> collectProduct(Animal* animal);
    
    /**
     * @brief Зібрати всю продукцію
     * @return Список зібраної продукції
     */
    std::vector<std::shared_ptr<Product>> collectAllProducts();
    
    /**
     * @brief Лікувати тварину
     * @param animal Вказівник на тварину
     * @return Вартість лікування
     */
    double healAnimal(Animal* animal);
    
    /**
     * @brief Погладити тварину
     * @param animal Вказівник на тварину
     */
    void petAnimal(Animal* animal);
    
    // ==================== Торгівля ====================
    
    /**
     * @brief Продати продукт
     * @param product Вказівник на продукт
     * @return Отримані гроші
     */
    double sellProduct(std::shared_ptr<Product> product);
    
    /**
     * @brief Продати всю продукцію певного типу
     * @param type Тип продукту
     * @return Отримані гроші
     */
    double sellAllProducts(ProductType type);
    
    /**
     * @brief Купити корм
     * @param type Тип корму
     * @param amount Кількість
     * @return true якщо успішно
     */
    bool buyFeed(FeedType type, double amount);
    
    /**
     * @brief Купити тварину
     * @param type Тип тварини
     * @return Вказівник на куплену тварину
     */
    std::unique_ptr<Animal> buyAnimal(AnimalType type, const std::string& name);
    
    /**
     * @brief Продати тварину
     * @param animal Вказівник на тварину
     * @return Отримані гроші
     */
    double sellAnimal(Animal* animal);
    
    // ==================== Економіка ====================
    
    double getMoney() const { return money_; }
    void addMoney(double amount);
    bool spendMoney(double amount);
    bool canAfford(double amount) const { return money_ >= amount; }
    double getNetWorth() const;
    
    // ==================== Навички ====================
    
    double getSkillLevel(FarmerSkill skill) const;
    void improveSkill(FarmerSkill skill, double amount);
    double getSkillBonus(FarmerSkill skill) const;
    bool isSkillMaxed(FarmerSkill skill) const;
    int getTotalSkillPoints() const;
    
    // ==================== Енергія та час ====================
    
    double getEnergy() const { return energy_; }
    double getMaxEnergy() const { return maxEnergy_; }
    void useEnergy(double amount);
    void restoreEnergy(double amount);
    bool hasEnergy(double amount) const { return energy_ >= amount; }
    void sleep();       // Відновити енергію повністю
    
    // ==================== Статистика ====================
    
    FarmerStats getStats() const { return stats_; }
    std::string getName() const { return name_; }
    void setName(const std::string& name) { name_ = name; }
    int getLevel() const { return level_; }
    double getExperience() const { return experience_; }
    double getExperienceToNextLevel() const;
    void addExperience(double xp);
    
    // ==================== Оновлення ====================
    
    void update(double deltaTime);
    void onDayEnd();
    void onDayStart();
    
    // Серіалізація
    std::string serialize() const;
    static std::unique_ptr<Farmer> deserialize(const std::string& data);
    
private:
    std::string name_;
    double money_;
    double energy_;
    double maxEnergy_;
    int level_;
    double experience_;
    std::map<FarmerSkill, double> skills_;
    FarmerStats stats_;
    
    // Внутрішні методи
    void initializeSkills();
    void checkLevelUp();
    double calculateSellingBonus() const;
    double calculateFeedingEfficiency() const;
};

} // namespace FarmGame

#endif // FARMER_HPP
