/**
 * @file Cow.hpp
 * @brief Клас корови - виробляє молоко
 * 
 * Демонструє наслідування та поліморфізм
 */

#ifndef COW_HPP
#define COW_HPP

#include "Animal.hpp"

namespace FarmGame {

/**
 * @enum CowBreed
 * @brief Порода корови
 */
enum class CowBreed {
    HOLSTEIN,       // Голштинська - багато молока
    JERSEY,         // Джерсі - жирне молоко
    ANGUS,          // Ангус - м'ясна порода
    HEREFORD,       // Херефорд - універсальна
    SIMMENTAL       // Симентальська - молоко + м'ясо
};

/**
 * @class Cow
 * @brief Корова - виробляє молоко
 */
class Cow : public Animal {
public:
    /**
     * @brief Конструктор
     * @param name Ім'я корови
     * @param age Вік у днях
     * @param breed Порода
     */
    Cow(const std::string& name, int age = 0, CowBreed breed = CowBreed::HOLSTEIN);
    
    ~Cow() override = default;
    
    // Реалізація абстрактних методів
    AnimalType getType() const override { return AnimalType::COW; }
    std::string getTypeName() const override { return "Корова"; }
    std::string makeSound() const override { return "Муууу!"; }
    double produce() override;
    std::string getProductName() const override { return "Молоко"; }
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 3.0; }
    std::string getFavoriteFeed() const override { return "Сіно"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи корови
    CowBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    double getMilkQuality() const { return milkQuality_; }
    double getMilkProduction() const { return milkProduction_; }
    bool isPregnant() const { return isPregnant_; }
    int getPregnancyDays() const { return pregnancyDays_; }
    
    void breed();
    void updatePregnancy();
    bool canBreed() const;
    
    // Перевизначення методів
    void update(double deltaTime) override;
    bool feed(double feedQuality, double amount) override;
    
protected:
    void onFed(double quality, double amount) override;
    double calculateProductionBonus() const override;
    
private:
    CowBreed breed_;
    double milkQuality_;        // Якість молока (0-100)
    double milkProduction_;     // Базова продуктивність молока
    bool isPregnant_;
    int pregnancyDays_;
    int lactationPeriod_;       // Період лактації в днях
    
    void initializeBreedStats();
};

} // namespace FarmGame

#endif // COW_HPP
