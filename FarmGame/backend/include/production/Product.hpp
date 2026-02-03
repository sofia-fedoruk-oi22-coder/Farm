/**
 * @file Product.hpp
 * @brief Система продукції ферми
 */

#ifndef PRODUCT_HPP
#define PRODUCT_HPP

#include <string>
#include <memory>
#include <ctime>
#include <vector>

namespace FarmGame {

/**
 * @enum ProductType
 * @brief Типи продукції
 */
enum class ProductType {
    // Молочні продукти
    MILK,
    GOAT_MILK,
    CHEESE,
    BUTTER,
    CREAM,
    YOGURT,
    
    // Яйця
    CHICKEN_EGG,
    DUCK_EGG,
    QUAIL_EGG,
    
    // М'ясо
    BEEF,
    PORK,
    LAMB,
    CHICKEN_MEAT,
    DUCK_MEAT,
    RABBIT_MEAT,
    
    // Текстиль
    WOOL,
    MOHAIR,
    RABBIT_FUR,
    FEATHERS,
    LEATHER,
    
    // Спеціальні
    TRUFFLE,
    HONEY,
    MANURE,         // Добриво
    
    // Перероблені
    PROCESSED_MEAT,
    SMOKED_MEAT,
    WOOL_FABRIC
};

/**
 * @enum ProductQuality
 * @brief Якість продукції
 */
enum class ProductQuality {
    POOR,           // Погана
    NORMAL,         // Звичайна
    GOOD,           // Хороша
    EXCELLENT,      // Відмінна
    PREMIUM,        // Преміум
    ARTISAN         // Ремісник (найвища)
};

/**
 * @struct ProductInfo
 * @brief Інформація про тип продукту
 */
struct ProductInfo {
    std::string name;
    std::string description;
    double basePrice;
    int shelfLife;          // Термін придатності в днях
    bool isPerishable;      // Чи псується
    double weight;          // Вага в кг
};

/**
 * @class Product
 * @brief Базовий клас продукту
 */
class Product {
public:
    Product(ProductType type, double amount, ProductQuality quality = ProductQuality::NORMAL);
    virtual ~Product() = default;
    
    // Геттери
    ProductType getType() const { return type_; }
    std::string getName() const;
    std::string getDescription() const;
    double getAmount() const { return amount_; }
    ProductQuality getQuality() const { return quality_; }
    std::string getQualityString() const;
    double getQualityMultiplier() const;
    double getBasePrice() const;
    double getPrice() const;            // Ціна з урахуванням якості
    double getTotalValue() const;
    int getDaysRemaining() const { return daysRemaining_; }
    bool isExpired() const { return isPerishable() && daysRemaining_ <= 0; }
    bool isPerishable() const;
    int getProductId() const { return productId_; }
    std::time_t getProducedTime() const { return producedTime_; }
    
    // Операції
    void ageOneDay();
    double takeAmount(double amount);
    void addAmount(double amount);
    void setQuality(ProductQuality quality) { quality_ = quality; }
    
    // Статичні методи
    static ProductInfo getProductInfo(ProductType type);
    static std::string productTypeToString(ProductType type);
    static ProductType stringToProductType(const std::string& name);
    static ProductQuality calculateQuality(double qualityScore);
    
    // Фабричний метод
    static std::unique_ptr<Product> create(ProductType type, double amount, 
                                           ProductQuality quality = ProductQuality::NORMAL);
    
    // Комбінування продуктів одного типу
    bool canCombineWith(const Product& other) const;
    void combineWith(Product& other);
    
protected:
    ProductType type_;
    double amount_;
    ProductQuality quality_;
    int daysRemaining_;
    int productId_;
    std::time_t producedTime_;
    
    static int nextProductId_;
    
private:
    static std::map<ProductType, ProductInfo> productDatabase_;
    static void initializeProductDatabase();
    static bool isDatabaseInitialized_;
};

/**
 * @class DairyProduct
 * @brief Молочні продукти
 */
class DairyProduct : public Product {
public:
    DairyProduct(ProductType type, double amount, ProductQuality quality, 
                 double fatContent = 3.5);
    
    double getFatContent() const { return fatContent_; }
    bool isPasteurized() const { return isPasteurized_; }
    void pasteurize();
    
private:
    double fatContent_;
    bool isPasteurized_;
};

/**
 * @class MeatProduct
 * @brief М'ясні продукти
 */
class MeatProduct : public Product {
public:
    MeatProduct(ProductType type, double amount, ProductQuality quality);
    
    bool isProcessed() const { return isProcessed_; }
    bool isSmoked() const { return isSmoked_; }
    double getFreshness() const { return freshness_; }
    
    void process();
    void smoke();
    
private:
    bool isProcessed_;
    bool isSmoked_;
    double freshness_;
};

/**
 * @class TextileProduct
 * @brief Текстильні продукти (вовна, хутро)
 */
class TextileProduct : public Product {
public:
    TextileProduct(ProductType type, double amount, ProductQuality quality);
    
    double getSoftness() const { return softness_; }
    std::string getColor() const { return color_; }
    bool isProcessed() const { return isProcessed_; }
    
    void dye(const std::string& color);
    void process();
    
private:
    double softness_;
    std::string color_;
    bool isProcessed_;
};

} // namespace FarmGame

#endif // PRODUCT_HPP
