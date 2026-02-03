/**
 * @file Goat.hpp
 * @brief Клас кози - виробляє молоко та сир
 */

#ifndef GOAT_HPP
#define GOAT_HPP

#include "Animal.hpp"

namespace FarmGame {

enum class GoatBreed {
    ALPINE,         // Альпійська - багато молока
    NUBIAN,         // Нубійська - жирне молоко
    SAANEN,         // Зааненська - продуктивна
    BOER,           // Бурська - м'ясна
    ANGORA          // Ангорська - шерсть (мохер)
};

/**
 * @class Goat
 * @brief Коза - виробляє молоко, може робити сир
 */
class Goat : public Animal {
public:
    Goat(const std::string& name, int age = 0, GoatBreed breed = GoatBreed::SAANEN);
    ~Goat() override = default;
    
    AnimalType getType() const override { return AnimalType::GOAT; }
    std::string getTypeName() const override { return "Коза"; }
    std::string makeSound() const override { return "Ме-е-е!"; }
    double produce() override;
    std::string getProductName() const override;
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 1.2; }
    std::string getFavoriteFeed() const override { return "Гілки"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи
    GoatBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    double getMilkProduction() const { return milkProduction_; }
    bool isAngoraType() const { return breed_ == GoatBreed::ANGORA; }
    
    double makeCheese(double milkAmount);   // Зробити сир з молока
    double collectMohair();                  // Зібрати мохер (для ангорської)
    
    void update(double deltaTime) override;
    
private:
    GoatBreed breed_;
    double milkProduction_;
    double mohairLength_;
    double cheeseSkill_;    // Навичка виробництва сиру
    
    void initializeBreedStats();
};

} // namespace FarmGame

#endif // GOAT_HPP
