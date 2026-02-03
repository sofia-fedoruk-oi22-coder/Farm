/**
 * @file Rabbit.hpp
 * @brief Клас кролика
 */

#ifndef RABBIT_HPP
#define RABBIT_HPP

#include "Animal.hpp"

namespace FarmGame {

enum class RabbitBreed {
    NEW_ZEALAND,    // Новозеландський - м'ясний
    CALIFORNIAN,    // Каліфорнійський - універсальний
    ANGORA,         // Ангорський - вовна
    FLEMISH,        // Фландр - великий
    REX             // Рекс - хутро
};

/**
 * @class Rabbit
 * @brief Кролик - виробляє м'ясо, хутро, може розмножуватись
 */
class Rabbit : public Animal {
public:
    Rabbit(const std::string& name, int age = 0, RabbitBreed breed = RabbitBreed::NEW_ZEALAND);
    ~Rabbit() override = default;
    
    AnimalType getType() const override { return AnimalType::RABBIT; }
    std::string getTypeName() const override { return "Кролик"; }
    std::string makeSound() const override { return "*тиша*"; }
    double produce() override;
    std::string getProductName() const override;
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 0.3; }
    std::string getFavoriteFeed() const override { return "Морква"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи
    RabbitBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    int getOffspring() const { return offspring_; }
    bool isAngoraType() const { return breed_ == RabbitBreed::ANGORA; }
    double getFurQuality() const { return furQuality_; }
    
    void breed();               // Розмножитись
    double collectFur();        // Зібрати хутро
    double collectWool();       // Зібрати вовну (ангора)
    
    void update(double deltaTime) override;
    
private:
    RabbitBreed breed_;
    double furQuality_;
    double woolAmount_;
    int offspring_;
    bool isPregnant_;
    int pregnancyDays_;
    
    void initializeBreedStats();
};

} // namespace FarmGame

#endif // RABBIT_HPP
