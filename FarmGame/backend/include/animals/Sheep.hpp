/**
 * @file Sheep.hpp
 * @brief Клас вівці - виробляє вовну
 */

#ifndef SHEEP_HPP
#define SHEEP_HPP

#include "Animal.hpp"

namespace FarmGame {

enum class SheepBreed {
    MERINO,         // Меріно - найкраща вовна
    SUFFOLK,        // Суффолк - м'ясна
    DORSET,         // Дорсет - універсальна
    ROMANOV,        // Романівська - плодовита
    LINCOLN         // Лінкольн - довга вовна
};

/**
 * @class Sheep
 * @brief Вівця - виробляє вовну
 */
class Sheep : public Animal {
public:
    Sheep(const std::string& name, int age = 0, SheepBreed breed = SheepBreed::MERINO);
    ~Sheep() override = default;
    
    AnimalType getType() const override { return AnimalType::SHEEP; }
    std::string getTypeName() const override { return "Вівця"; }
    std::string makeSound() const override { return "Бе-е-е!"; }
    double produce() override;
    std::string getProductName() const override { return "Вовна"; }
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 1.5; }
    std::string getFavoriteFeed() const override { return "Трава"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи
    SheepBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    double getWoolQuality() const { return woolQuality_; }
    double getWoolLength() const { return woolLength_; }
    bool canBeSheared() const { return woolLength_ >= 5.0; }
    int getLambs() const { return lambs_; }
    
    double shear();         // Стригти вовну
    void breedLambs();      // Народити ягнят
    
    void update(double deltaTime) override;
    bool feed(double feedQuality, double amount) override;
    
protected:
    void onFed(double quality, double amount) override;
    double calculateProductionBonus() const override;
    
private:
    SheepBreed breed_;
    double woolQuality_;
    double woolLength_;     // Довжина вовни в см
    double woolGrowthRate_; // Швидкість росту вовни
    int lambs_;
    bool isPregnant_;
    int pregnancyDays_;
    
    void initializeBreedStats();
    void growWool(double deltaTime);
};

} // namespace FarmGame

#endif // SHEEP_HPP
