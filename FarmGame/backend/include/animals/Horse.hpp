/**
 * @file Horse.hpp
 * @brief Клас коня - транспорт та перегони
 */

#ifndef HORSE_HPP
#define HORSE_HPP

#include "Animal.hpp"

namespace FarmGame {

enum class HorseBreed {
    ARABIAN,        // Арабська - швидка
    THOROUGHBRED,   // Чистокровна - перегони
    QUARTER,        // Квотерхорс - робоча
    CLYDESDALE,     // Клайдсдейл - важковоз
    APPALOOSA       // Аппалуза - витривала
};

/**
 * @class Horse
 * @brief Кінь - транспорт, робота на полі, перегони
 */
class Horse : public Animal {
public:
    Horse(const std::string& name, int age = 0, HorseBreed breed = HorseBreed::QUARTER);
    ~Horse() override = default;
    
    AnimalType getType() const override { return AnimalType::HORSE; }
    std::string getTypeName() const override { return "Кінь"; }
    std::string makeSound() const override { return "І-го-го!"; }
    double produce() override;
    std::string getProductName() const override { return "Робота"; }
    double getProductPrice() const override;
    double getBasePrice() const override;
    double getFeedConsumption() const override { return 4.0; }
    std::string getFavoriteFeed() const override { return "Овес"; }
    std::unique_ptr<Animal> clone() const override;
    
    // Специфічні методи
    HorseBreed getBreed() const { return breed_; }
    std::string getBreedName() const;
    double getSpeed() const { return speed_; }
    double getStamina() const { return stamina_; }
    double getStrength() const { return strength_; }
    bool isTrained() const { return trainingLevel_ >= 50; }
    double getTrainingLevel() const { return trainingLevel_; }
    
    void train();               // Тренувати
    void race();                // Брати участь у перегонах
    double work(double hours);  // Робота на полі
    void ride();                // Катання
    void rest();                // Відпочинок
    
    void update(double deltaTime) override;
    bool feed(double feedQuality, double amount) override;
    
private:
    HorseBreed breed_;
    double speed_;
    double stamina_;
    double strength_;
    double trainingLevel_;
    double fatigue_;
    int racesWon_;
    int totalRaces_;
    
    void initializeBreedStats();
    void recoverStamina(double amount);
};

} // namespace FarmGame

#endif // HORSE_HPP
