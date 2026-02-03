/**
 * @file Pig.hpp
 * @brief Клас свині
 */

#ifndef PIG_HPP
#define PIG_HPP

#include "Animal.hpp"

namespace FarmGame {

enum class PigBreed {
    LANDRACE,       // Ландрас - м'ясна
    YORKSHIRE,      // Йоркшир - універсальна
    DUROC,          // Дюрок - швидкий ріст
    HAMPSHIRE,      // Гемпшир - якісне м'ясо
    BERKSHIRE       // Беркшир - преміум м'ясо
};

/**
 * @class Pig
 * @brief Свиня - виробляє м'ясо, також може знаходити трюфелі
 */
class Pig : public Animal {
public:
    Pig(const std::string& name, int age = 0, PigBreed breed = PigBreed::YORKSHIRE);
    ~Pig() override = default;
    
    AnimalType getType() const override { return AnimalType::PIG; }
    std::string getTypeName() const override { return "Свиня"; }
    std::string makeSound() const override { return "Хрю-хрю!"; }
    double produce() override;
    std::string getProductName() const override { return "Сало"; }
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 2.5; }
    std::string getFavoriteFeed() const override { return "Комбікорм"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи
    PigBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    double getWeight() const { return weight_; }
    double getMeatQuality() const { return meatQuality_; }
    bool canFindTruffles() const { return truffleSkill_ > 50; }
    
    bool searchTruffles();  // Шукати трюфелі
    double slaughter();     // Забій (видаляє тварину, повертає м'ясо)
    
    void update(double deltaTime) override;
    bool feed(double feedQuality, double amount) override;
    
protected:
    void onFed(double quality, double amount) override;
    double calculateProductionBonus() const override;
    
private:
    PigBreed breed_;
    double weight_;
    double meatQuality_;
    double truffleSkill_;   // Навичка пошуку трюфелів
    int trufflesFound_;
    
    void initializeBreedStats();
    void gainWeight(double amount);
};

} // namespace FarmGame

#endif // PIG_HPP
