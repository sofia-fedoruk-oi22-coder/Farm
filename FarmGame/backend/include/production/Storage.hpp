/**
 * @file Storage.hpp
 * @brief Система зберігання продукції та кормів
 */

#ifndef STORAGE_HPP
#define STORAGE_HPP

#include <vector>
#include <memory>
#include <map>
#include <functional>
#include "Feed.hpp"
#include "Product.hpp"

namespace FarmGame {

/**
 * @enum StorageType
 * @brief Типи сховищ
 */
enum class StorageType {
    BARN,           // Амбар (корми)
    WAREHOUSE,      // Склад (продукція)
    REFRIGERATOR,   // Холодильник (швидкопсувні)
    CELLAR,         // Погреб
    SILO            // Силос (зерно)
};

/**
 * @struct StorageStats
 * @brief Статистика сховища
 */
struct StorageStats {
    double currentCapacity;
    double maxCapacity;
    int totalItems;
    int expiredItems;
    double totalValue;
};

/**
 * @class Storage
 * @brief Базовий клас сховища
 */
class Storage {
public:
    Storage(StorageType type, double capacity);
    virtual ~Storage() = default;
    
    // Геттери
    StorageType getType() const { return type_; }
    std::string getTypeName() const;
    double getCapacity() const { return capacity_; }
    double getUsedSpace() const { return usedSpace_; }
    double getFreeSpace() const { return capacity_ - usedSpace_; }
    double getUsagePercent() const { return (usedSpace_ / capacity_) * 100.0; }
    bool isFull() const { return usedSpace_ >= capacity_; }
    bool isEmpty() const { return usedSpace_ <= 0; }
    StorageStats getStats() const;
    int getLevel() const { return level_; }
    
    // Операції
    virtual bool canStore(double amount) const;
    virtual void upgrade();
    virtual void ageContents();      // Старіння вмісту на 1 день
    virtual void removeExpired();     // Видалити прострочене
    
    // Сеттери
    void setCapacity(double capacity) { capacity_ = capacity; }
    
protected:
    StorageType type_;
    double capacity_;
    double usedSpace_;
    int level_;
    double upgradeMultiplier_;
};

/**
 * @class FeedStorage
 * @brief Сховище для кормів
 */
class FeedStorage : public Storage {
public:
    FeedStorage(double capacity = 1000.0);
    
    // Операції з кормами
    bool addFeed(std::shared_ptr<Feed> feed);
    bool addFeed(FeedType type, double amount);
    std::shared_ptr<Feed> getFeed(FeedType type);
    double takeFeed(FeedType type, double amount);
    bool hasFeed(FeedType type, double amount = 1.0) const;
    double getFeedAmount(FeedType type) const;
    std::vector<FeedType> getAvailableFeedTypes() const;
    double getTotalFeedValue() const;
    
    // Перевизначення
    void ageContents() override;
    void removeExpired() override;
    
    // Отримати всі корми
    std::map<FeedType, std::shared_ptr<Feed>>& getAllFeeds() { return feeds_; }
    const std::map<FeedType, std::shared_ptr<Feed>>& getAllFeeds() const { return feeds_; }
    
private:
    std::map<FeedType, std::shared_ptr<Feed>> feeds_;
    void updateUsedSpace();
};

/**
 * @class ProductStorage
 * @brief Сховище для продукції
 */
class ProductStorage : public Storage {
public:
    ProductStorage(StorageType type = StorageType::WAREHOUSE, double capacity = 500.0);
    
    // Операції з продукцією
    bool addProduct(std::shared_ptr<Product> product);
    bool addProduct(ProductType type, double amount, ProductQuality quality = ProductQuality::NORMAL);
    std::shared_ptr<Product> getProduct(ProductType type);
    double takeProduct(ProductType type, double amount);
    bool hasProduct(ProductType type, double amount = 1.0) const;
    double getProductAmount(ProductType type) const;
    std::vector<ProductType> getAvailableProductTypes() const;
    double getTotalProductValue() const;
    
    // Пошук за критеріями
    std::vector<std::shared_ptr<Product>> findProducts(
        std::function<bool(const Product&)> predicate) const;
    std::vector<std::shared_ptr<Product>> getExpiringProducts(int daysThreshold) const;
    
    // Перевизначення
    void ageContents() override;
    void removeExpired() override;
    
    // Отримати всі продукти
    std::vector<std::shared_ptr<Product>>& getAllProducts() { return products_; }
    const std::vector<std::shared_ptr<Product>>& getAllProducts() const { return products_; }
    
private:
    std::vector<std::shared_ptr<Product>> products_;
    bool preservesFood_;    // Чи зберігає свіжість (холодильник)
    void updateUsedSpace();
};

/**
 * @class Refrigerator
 * @brief Холодильник - подовжує термін зберігання
 */
class Refrigerator : public ProductStorage {
public:
    Refrigerator(double capacity = 100.0);
    
    double getTemperature() const { return temperature_; }
    void setTemperature(double temp);
    int getPreservationBonus() const { return preservationBonus_; }
    
    void ageContents() override;
    
private:
    double temperature_;
    int preservationBonus_;
};

} // namespace FarmGame

#endif // STORAGE_HPP
