/**
 * @file Animal.hpp
 * @brief Абстрактний базовий клас для всіх тварин на фермі
 * 
 * Демонструє принципи ООП:
 * - Абстракція (чисто віртуальні методи)
 * - Інкапсуляція (private/protected члени)
 * - Поліморфізм (віртуальні методи)
 */

#ifndef ANIMAL_HPP
#define ANIMAL_HPP

#include <string>
#include <memory>
#include <ctime>

namespace FarmGame {

/**
 * @enum AnimalState
 * @brief Стан тварини
 */
enum class AnimalState {
    HEALTHY,        // Здорова
    HUNGRY,         // Голодна
    SICK,           // Хвора
    PRODUCING,      // Виробляє продукцію
    SLEEPING,       // Спить
    HAPPY           // Щаслива
};

/**
 * @enum AnimalType
 * @brief Тип тварини
 */
enum class AnimalType {
    COW,
    CHICKEN,
    PIG,
    SHEEP,
    GOAT,
    DUCK,
    RABBIT,
    HORSE
};

/**
 * @struct AnimalStats
 * @brief Статистика тварини
 */
struct AnimalStats {
    int totalFed = 0;           // Скільки разів годували
    int totalProduced = 0;      // Скільки продукції вироблено
    int daysOnFarm = 0;         // Днів на фермі
    double totalEarnings = 0.0; // Загальний прибуток від тварини
};

/**
 * @class Animal
 * @brief Абстрактний базовий клас для тварин
 * 
 * Реалізує патерн Template Method для загальної поведінки тварин
 */
class Animal {
public:
    /**
     * @brief Конструктор
     * @param name Ім'я тварини
     * @param age Вік у днях
     */
    Animal(const std::string& name, int age = 0);
    
    /**
     * @brief Віртуальний деструктор для правильного поліморфізму
     */
    virtual ~Animal() = default;
    
    // ==================== Чисто віртуальні методи (Абстракція) ====================
    
    /**
     * @brief Отримати тип тварини
     * @return Тип тварини
     */
    virtual AnimalType getType() const = 0;
    
    /**
     * @brief Отримати назву типу тварини
     * @return Рядок з назвою типу
     */
    virtual std::string getTypeName() const = 0;
    
    /**
     * @brief Отримати звук тварини
     * @return Рядок зі звуком
     */
    virtual std::string makeSound() const = 0;
    
    /**
     * @brief Виробити продукцію
     * @return Кількість виробленої продукції
     */
    virtual double produce() = 0;
    
    /**
     * @brief Отримати назву продукції
     * @return Назва продукції
     */
    virtual std::string getProductName() const = 0;
    
    /**
     * @brief Отримати ціну продукції за одиницю
     * @return Ціна
     */
    virtual double getProductPrice() const = 0;
    
    /**
     * @brief Отримати базову вартість тварини
     * @return Вартість
     */
    virtual double getBasePrice() const = 0;
    
    /**
     * @brief Отримати споживання корму за день
     * @return Кількість корму
     */
    virtual double getFeedConsumption() const = 0;
    
    /**
     * @brief Отримати улюблений тип корму
     * @return Назва корму
     */
    virtual std::string getFavoriteFeed() const = 0;
    
    /**
     * @brief Клонувати тварину (патерн Prototype)
     * @return Вказівник на нову тварину
     */
    virtual std::unique_ptr<Animal> clone() const = 0;
    
    // ==================== Віртуальні методи з реалізацією (Поліморфізм) ====================
    
    /**
     * @brief Погодувати тварину
     * @param feedQuality Якість корму (0.0 - 1.0)
     * @param amount Кількість корму
     * @return true якщо тварина поїла
     */
    virtual bool feed(double feedQuality = 1.0, double amount = 1.0);
    
    /**
     * @brief Оновити стан тварини (викликається кожен ігровий тік)
     * @param deltaTime Час з останнього оновлення
     */
    virtual void update(double deltaTime);
    
    /**
     * @brief Лікувати тварину
     * @return Вартість лікування
     */
    virtual double heal();
    
    /**
     * @brief Погладити тварину (збільшує щастя)
     */
    virtual void pet();
    
    // ==================== Звичайні методи (Інкапсуляція) ====================
    
    // Геттери
    std::string getName() const { return name_; }
    int getAge() const { return age_; }
    double getHealth() const { return health_; }
    double getHunger() const { return hunger_; }
    double getHappiness() const { return happiness_; }
    AnimalState getState() const { return state_; }
    int getId() const { return id_; }
    bool isAlive() const { return isAlive_; }
    bool canProduce() const;
    AnimalStats getStats() const { return stats_; }
    double getCurrentValue() const;
    std::string getStateString() const;
    int getProductionCooldown() const { return productionCooldown_; }
    
    // Сеттери
    void setName(const std::string& name) { name_ = name; }
    void setState(AnimalState state) { state_ = state; }
    
    // Утиліти
    void ageOneDay();
    std::string getInfo() const;
    bool needsFeeding() const { return hunger_ < 50.0; }
    bool needsHealing() const { return health_ < 30.0; }
    
protected:
    // Захищені члени для доступу з похідних класів
    std::string name_;
    int age_;                           // Вік у днях
    double health_;                     // Здоров'я (0-100)
    double hunger_;                     // Ситість (0-100)
    double happiness_;                  // Щастя (0-100)
    AnimalState state_;
    bool isAlive_;
    int productionCooldown_;            // Час до наступного виробництва
    AnimalStats stats_;
    
    // Захищені віртуальні методи для розширення в похідних класах
    virtual void onFed(double quality, double amount);
    virtual void onStateChanged(AnimalState oldState, AnimalState newState);
    virtual double calculateProductionBonus() const;
    
private:
    int id_;
    static int nextId_;
    std::time_t birthTime_;
    
    void updateState();
};

} // namespace FarmGame

#endif // ANIMAL_HPP
