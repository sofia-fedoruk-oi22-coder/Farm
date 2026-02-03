/**
 * @file Chicken.hpp
 * @brief Клас курки - виробляє яйця
 */

#ifndef CHICKEN_HPP
#define CHICKEN_HPP

#include "Animal.hpp"

namespace FarmGame {

/**
 * @enum ChickenBreed
 * @brief Порода курки
 */
enum class ChickenBreed {
    LEGHORN,        // Леггорн - багато яєць
    RHODE_ISLAND,   // Род-Айленд - універсальна
    PLYMOUTH,       // Плімутрок - м'ясо-яєчна
    SUSSEX,         // Сассекс - якісні яйця
    ORPINGTON       // Орпінгтон - великі яйця
};

/**
 * @class Chicken
 * @brief Курка - виробляє яйця
 */
class Chicken : public Animal {
public:
    Chicken(const std::string& name, int age = 0, ChickenBreed breed = ChickenBreed::LEGHORN);
    ~Chicken() override = default;
    
    // Реалізація абстрактних методів
    AnimalType getType() const override { return AnimalType::CHICKEN; }
    std::string getTypeName() const override { return "Курка"; }
    std::string makeSound() const override { return "Ко-ко-ко!"; }
    double produce() override;
    std::string getProductName() const override { return "Яйця"; }
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 0.5; }
    std::string getFavoriteFeed() const override { return "Зерно"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи
    ChickenBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    double getEggQuality() const { return eggQuality_; }
    int getEggsPerDay() const { return eggsPerDay_; }
    bool isBroody() const { return isBroody_; }
    int getChicks() const { return chicks_; }
    
    void hatchEggs();
    void collectChicks();
    
    void update(double deltaTime) override;
    bool feed(double feedQuality, double amount) override;
    
protected:
    void onFed(double quality, double amount) override;
    double calculateProductionBonus() const override;
    
private:
    ChickenBreed breed_;
    double eggQuality_;
    int eggsPerDay_;
    bool isBroody_;         // Чи насиджує яйця
    int incubationDays_;
    int chicks_;            // Кількість курчат
    int eggsCollected_;     // Зібраних яєць сьогодні
    
    void initializeBreedStats();
};

} // namespace FarmGame

#endif // CHICKEN_HPP
