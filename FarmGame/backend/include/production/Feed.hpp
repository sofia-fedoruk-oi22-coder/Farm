/**
 * @file Feed.hpp
 * @brief Система кормів для тварин
 */

#ifndef FEED_HPP
#define FEED_HPP

#include <string>
#include <memory>
#include <map>

namespace FarmGame {

/**
 * @enum FeedType
 * @brief Типи кормів
 */
enum class FeedType {
    HAY,            // Сіно
    GRAIN,          // Зерно
    CORN,           // Кукурудза
    MIXED_FEED,     // Комбікорм
    GRASS,          // Трава
    VEGETABLES,     // Овочі
    OATS,           // Овес
    BRANCHES,       // Гілки
    CARROTS,        // Морква
    PREMIUM_FEED    // Преміум корм
};

/**
 * @struct FeedInfo
 * @brief Інформація про корм
 */
struct FeedInfo {
    std::string name;
    std::string description;
    double pricePerUnit;
    double nutritionValue;      // Поживність (0-100)
    double quality;             // Якість (0-100)
    bool isOrganic;            // Органічний
    int shelfLife;             // Термін придатності в днях
};

/**
 * @class Feed
 * @brief Базовий клас корму
 */
class Feed {
public:
    Feed(FeedType type, double amount = 0.0);
    virtual ~Feed() = default;
    
    // Геттери
    FeedType getType() const { return type_; }
    std::string getName() const;
    std::string getDescription() const;
    double getAmount() const { return amount_; }
    double getQuality() const { return quality_; }
    double getNutrition() const;
    double getPricePerUnit() const;
    double getTotalValue() const { return amount_ * getPricePerUnit(); }
    int getDaysRemaining() const { return daysRemaining_; }
    bool isExpired() const { return daysRemaining_ <= 0; }
    bool isOrganic() const;
    
    // Сеттери та операції
    void addAmount(double amount);
    double takeAmount(double amount);
    void ageOneDay();
    void setQuality(double quality);
    
    // Статичні методи для отримання інформації про типи кормів
    static FeedInfo getFeedInfo(FeedType type);
    static std::string feedTypeToString(FeedType type);
    static FeedType stringToFeedType(const std::string& name);
    
    // Фабричний метод
    static std::unique_ptr<Feed> create(FeedType type, double amount);
    
protected:
    FeedType type_;
    double amount_;
    double quality_;
    int daysRemaining_;
    
private:
    static std::map<FeedType, FeedInfo> feedDatabase_;
    static void initializeFeedDatabase();
    static bool isDatabaseInitialized_;
};

/**
 * @class OrganicFeed
 * @brief Органічний корм (преміум)
 */
class OrganicFeed : public Feed {
public:
    OrganicFeed(FeedType type, double amount = 0.0);
    
    double getOrganicBonus() const { return organicBonus_; }
    double getHealthBoost() const { return healthBoost_; }
    
private:
    double organicBonus_;
    double healthBoost_;
};

/**
 * @class FeedMix
 * @brief Змішаний корм (кілька типів)
 */
class FeedMix : public Feed {
public:
    FeedMix(const std::string& name, double amount = 0.0);
    
    void addIngredient(FeedType type, double ratio);
    double getIngredientRatio(FeedType type) const;
    std::string getCustomName() const { return customName_; }
    double calculateNutrition() const;
    double calculateQuality() const;
    
private:
    std::string customName_;
    std::map<FeedType, double> ingredients_;
};

} // namespace FarmGame

#endif // FEED_HPP
