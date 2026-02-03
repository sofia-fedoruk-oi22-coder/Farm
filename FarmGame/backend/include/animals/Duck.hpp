/**
 * @file Duck.hpp
 * @brief Клас качки - виробляє яйця та пір'я
 */

#ifndef DUCK_HPP
#define DUCK_HPP

#include "Animal.hpp"

namespace FarmGame {

enum class DuckBreed {
    PEKIN,          // Пекінська - м'ясна
    KHAKI_CAMPBELL, // Хакі-Кемпбел - яєчна
    RUNNER,         // Бігунок - активна
    MUSCOVY,        // Мускусна - тиха
    ROUEN           // Руанська - декоративна
};

/**
 * @class Duck
 * @brief Качка - виробляє яйця та пір'я
 */
class Duck : public Animal {
public:
    Duck(const std::string& name, int age = 0, DuckBreed breed = DuckBreed::PEKIN);
    ~Duck() override = default;
    
    AnimalType getType() const override { return AnimalType::DUCK; }
    std::string getTypeName() const override { return "Качка"; }
    std::string makeSound() const override { return "Кря-кря!"; }
    double produce() override;
    std::string getProductName() const override { return "Качині яйця"; }
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 0.8; }
    std::string getFavoriteFeed() const override { return "Зерно"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи
    DuckBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    double getFeatherQuality() const { return featherQuality_; }
    bool needsWater() const { return true; }  // Качки потребують води
    
    double collectFeathers();   // Зібрати пір'я
    void swim();                // Плавання (покращує здоров'я)
    
    void update(double deltaTime) override;
    
private:
    DuckBreed breed_;
    double featherQuality_;
    double featherAmount_;
    bool hasSwimmedToday_;
    int eggsLaid_;
    
    void initializeBreedStats();
};

} // namespace FarmGame

#endif // DUCK_HPP
