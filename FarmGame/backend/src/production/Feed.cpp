/**
 * @file Feed.cpp
 * @brief Реалізація системи кормів
 */

#include "production/Feed.hpp"
#include <algorithm>

namespace FarmGame {

std::map<FeedType, FeedInfo> Feed::feedDatabase_;
bool Feed::isDatabaseInitialized_ = false;

Feed::Feed(FeedType type, double amount)
    : type_(type)
    , amount_(amount)
    , quality_(100.0)
{
    if (!isDatabaseInitialized_) {
        initializeFeedDatabase();
    }
    
    FeedInfo info = getFeedInfo(type);
    daysRemaining_ = info.shelfLife;
}

void Feed::initializeFeedDatabase() {
    feedDatabase_[FeedType::HAY] = {
        "Сіно", "Висушена трава, основний корм для жуйних",
        10.0, 70.0, 75.0, false, 365
    };
    feedDatabase_[FeedType::GRAIN] = {
        "Зерно", "Пшениця, ячмінь та інші злаки",
        15.0, 85.0, 80.0, false, 180
    };
    feedDatabase_[FeedType::CORN] = {
        "Кукурудза", "Енергетичний корм для тварин",
        12.0, 90.0, 75.0, false, 150
    };
    feedDatabase_[FeedType::MIXED_FEED] = {
        "Комбікорм", "Збалансований корм для всіх тварин",
        25.0, 95.0, 90.0, false, 90
    };
    feedDatabase_[FeedType::GRASS] = {
        "Трава", "Свіжа трава з пасовища",
        5.0, 60.0, 85.0, true, 3
    };
    feedDatabase_[FeedType::VEGETABLES] = {
        "Овочі", "Морква, буряк, капуста",
        20.0, 75.0, 90.0, true, 14
    };
    feedDatabase_[FeedType::OATS] = {
        "Овес", "Улюблений корм коней",
        18.0, 88.0, 85.0, false, 180
    };
    feedDatabase_[FeedType::BRANCHES] = {
        "Гілки", "Гілки дерев для кіз",
        3.0, 40.0, 60.0, false, 30
    };
    feedDatabase_[FeedType::CARROTS] = {
        "Морква", "Улюблені ласощі для кроликів",
        8.0, 65.0, 95.0, true, 21
    };
    feedDatabase_[FeedType::PREMIUM_FEED] = {
        "Преміум корм", "Найкращий корм з добавками",
        50.0, 100.0, 100.0, false, 60
    };
    
    isDatabaseInitialized_ = true;
}

std::string Feed::getName() const {
    return getFeedInfo(type_).name;
}

std::string Feed::getDescription() const {
    return getFeedInfo(type_).description;
}

double Feed::getNutrition() const {
    return getFeedInfo(type_).nutritionValue * (quality_ / 100.0);
}

double Feed::getPricePerUnit() const {
    return getFeedInfo(type_).pricePerUnit;
}

bool Feed::isOrganic() const {
    return getFeedInfo(type_).isOrganic;
}

void Feed::addAmount(double amount) {
    amount_ += amount;
}

double Feed::takeAmount(double amount) {
    double taken = std::min(amount_, amount);
    amount_ -= taken;
    return taken;
}

void Feed::ageOneDay() {
    if (daysRemaining_ > 0) {
        daysRemaining_--;
        
        // Якість зменшується з часом
        if (daysRemaining_ < 30) {
            quality_ = std::max(0.0, quality_ - 1.0);
        }
    }
}

void Feed::setQuality(double quality) {
    quality_ = std::max(0.0, std::min(100.0, quality));
}

FeedInfo Feed::getFeedInfo(FeedType type) {
    if (!isDatabaseInitialized_) {
        initializeFeedDatabase();
    }
    
    auto it = feedDatabase_.find(type);
    if (it != feedDatabase_.end()) {
        return it->second;
    }
    
    return {"Невідомий", "Невідомий корм", 0.0, 0.0, 0.0, false, 0};
}

std::string Feed::feedTypeToString(FeedType type) {
    return getFeedInfo(type).name;
}

FeedType Feed::stringToFeedType(const std::string& name) {
    if (!isDatabaseInitialized_) {
        initializeFeedDatabase();
    }
    
    for (const auto& pair : feedDatabase_) {
        if (pair.second.name == name) {
            return pair.first;
        }
    }
    
    return FeedType::MIXED_FEED;  // За замовчуванням
}

std::unique_ptr<Feed> Feed::create(FeedType type, double amount) {
    return std::make_unique<Feed>(type, amount);
}

// ==================== OrganicFeed ====================

OrganicFeed::OrganicFeed(FeedType type, double amount)
    : Feed(type, amount)
    , organicBonus_(1.2)
    , healthBoost_(5.0)
{
    // Органічний корм завжди вищої якості
    setQuality(100.0);
}

// ==================== FeedMix ====================

FeedMix::FeedMix(const std::string& name, double amount)
    : Feed(FeedType::MIXED_FEED, amount)
    , customName_(name)
{
}

void FeedMix::addIngredient(FeedType type, double ratio) {
    ingredients_[type] = ratio;
}

double FeedMix::getIngredientRatio(FeedType type) const {
    auto it = ingredients_.find(type);
    if (it != ingredients_.end()) {
        return it->second;
    }
    return 0.0;
}

double FeedMix::calculateNutrition() const {
    double totalNutrition = 0.0;
    double totalRatio = 0.0;
    
    for (const auto& pair : ingredients_) {
        FeedInfo info = getFeedInfo(pair.first);
        totalNutrition += info.nutritionValue * pair.second;
        totalRatio += pair.second;
    }
    
    if (totalRatio > 0) {
        return totalNutrition / totalRatio;
    }
    return 0.0;
}

double FeedMix::calculateQuality() const {
    double totalQuality = 0.0;
    double totalRatio = 0.0;
    
    for (const auto& pair : ingredients_) {
        FeedInfo info = getFeedInfo(pair.first);
        totalQuality += info.quality * pair.second;
        totalRatio += pair.second;
    }
    
    if (totalRatio > 0) {
        return totalQuality / totalRatio;
    }
    return 0.0;
}

} // namespace FarmGame
