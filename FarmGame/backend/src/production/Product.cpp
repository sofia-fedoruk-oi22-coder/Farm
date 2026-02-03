/**
 * @file Product.cpp
 * @brief Реалізація системи продукції
 */

#include "production/Product.hpp"
#include <algorithm>

namespace FarmGame {

std::map<ProductType, ProductInfo> Product::productDatabase_;
bool Product::isDatabaseInitialized_ = false;
int Product::nextProductId_ = 1;

Product::Product(ProductType type, double amount, ProductQuality quality)
    : type_(type)
    , amount_(amount)
    , quality_(quality)
    , productId_(nextProductId_++)
    , producedTime_(std::time(nullptr))
{
    if (!isDatabaseInitialized_) {
        initializeProductDatabase();
    }
    
    ProductInfo info = getProductInfo(type);
    daysRemaining_ = info.shelfLife;
}

void Product::initializeProductDatabase() {
    // Молочні продукти
    productDatabase_[ProductType::MILK] = {
        "Молоко", "Свіже коров'яче молоко", 15.0, 7, true, 1.0
    };
    productDatabase_[ProductType::GOAT_MILK] = {
        "Козине молоко", "Свіже козине молоко", 25.0, 5, true, 0.8
    };
    productDatabase_[ProductType::CHEESE] = {
        "Сир", "Домашній сир", 80.0, 30, true, 0.5
    };
    productDatabase_[ProductType::BUTTER] = {
        "Масло", "Вершкове масло", 60.0, 21, true, 0.25
    };
    productDatabase_[ProductType::CREAM] = {
        "Вершки", "Свіжі вершки", 40.0, 5, true, 0.5
    };
    productDatabase_[ProductType::YOGURT] = {
        "Йогурт", "Натуральний йогурт", 35.0, 14, true, 0.5
    };
    
    // Яйця
    productDatabase_[ProductType::CHICKEN_EGG] = {
        "Курячі яйця", "Свіжі курячі яйця", 5.0, 30, true, 0.06
    };
    productDatabase_[ProductType::DUCK_EGG] = {
        "Качині яйця", "Великі качині яйця", 8.0, 28, true, 0.08
    };
    productDatabase_[ProductType::QUAIL_EGG] = {
        "Перепелині яйця", "Дієтичні перепелині яйця", 3.0, 35, true, 0.01
    };
    
    // М'ясо
    productDatabase_[ProductType::BEEF] = {
        "Яловичина", "М'ясо великої рогатої худоби", 120.0, 5, true, 1.0
    };
    productDatabase_[ProductType::PORK] = {
        "Свинина", "Свиняче м'ясо", 80.0, 5, true, 1.0
    };
    productDatabase_[ProductType::LAMB] = {
        "Баранина", "Баряче м'ясо", 150.0, 5, true, 1.0
    };
    productDatabase_[ProductType::CHICKEN_MEAT] = {
        "Курятина", "Куряче м'ясо", 60.0, 3, true, 1.0
    };
    productDatabase_[ProductType::DUCK_MEAT] = {
        "Качатина", "Качине м'ясо", 90.0, 3, true, 1.0
    };
    productDatabase_[ProductType::RABBIT_MEAT] = {
        "Крольчатина", "Дієтичне кроляче м'ясо", 100.0, 3, true, 1.0
    };
    
    // Текстиль
    productDatabase_[ProductType::WOOL] = {
        "Вовна", "Овеча вовна", 50.0, 365, false, 1.0
    };
    productDatabase_[ProductType::MOHAIR] = {
        "Мохер", "Ангорська шерсть", 150.0, 365, false, 1.0
    };
    productDatabase_[ProductType::RABBIT_FUR] = {
        "Хутро кролика", "М'яке кроляче хутро", 80.0, 365, false, 0.5
    };
    productDatabase_[ProductType::FEATHERS] = {
        "Пір'я", "Пташине пір'я", 20.0, 365, false, 0.1
    };
    productDatabase_[ProductType::LEATHER] = {
        "Шкіра", "Натуральна шкіра", 200.0, 365, false, 2.0
    };
    
    // Спеціальні
    productDatabase_[ProductType::TRUFFLE] = {
        "Трюфель", "Рідкісний гриб", 500.0, 7, true, 0.1
    };
    productDatabase_[ProductType::HONEY] = {
        "Мед", "Натуральний мед", 100.0, 730, false, 1.0
    };
    productDatabase_[ProductType::MANURE] = {
        "Добриво", "Органічне добриво", 2.0, 180, false, 10.0
    };
    
    // Перероблені
    productDatabase_[ProductType::PROCESSED_MEAT] = {
        "Ковбаса", "Домашня ковбаса", 150.0, 14, true, 1.0
    };
    productDatabase_[ProductType::SMOKED_MEAT] = {
        "Копченості", "Копчене м'ясо", 180.0, 30, true, 1.0
    };
    productDatabase_[ProductType::WOOL_FABRIC] = {
        "Вовняна тканина", "Тканина з вовни", 200.0, 365, false, 1.0
    };
    
    isDatabaseInitialized_ = true;
}

std::string Product::getName() const {
    return getProductInfo(type_).name;
}

std::string Product::getDescription() const {
    return getProductInfo(type_).description;
}

std::string Product::getQualityString() const {
    switch (quality_) {
        case ProductQuality::POOR: return "Погана";
        case ProductQuality::NORMAL: return "Звичайна";
        case ProductQuality::GOOD: return "Хороша";
        case ProductQuality::EXCELLENT: return "Відмінна";
        case ProductQuality::PREMIUM: return "Преміум";
        case ProductQuality::ARTISAN: return "Ремісницька";
        default: return "Невідома";
    }
}

double Product::getQualityMultiplier() const {
    switch (quality_) {
        case ProductQuality::POOR: return 0.5;
        case ProductQuality::NORMAL: return 1.0;
        case ProductQuality::GOOD: return 1.25;
        case ProductQuality::EXCELLENT: return 1.5;
        case ProductQuality::PREMIUM: return 2.0;
        case ProductQuality::ARTISAN: return 2.5;
        default: return 1.0;
    }
}

double Product::getBasePrice() const {
    return getProductInfo(type_).basePrice;
}

double Product::getPrice() const {
    return getBasePrice() * getQualityMultiplier();
}

double Product::getTotalValue() const {
    return getPrice() * amount_;
}

bool Product::isPerishable() const {
    return getProductInfo(type_).isPerishable;
}

void Product::ageOneDay() {
    if (daysRemaining_ > 0) {
        daysRemaining_--;
    }
    
    // Якщо продукт псується, знижуємо якість
    if (isPerishable() && daysRemaining_ < 3) {
        if (quality_ != ProductQuality::POOR) {
            quality_ = static_cast<ProductQuality>(
                static_cast<int>(quality_) - 1
            );
        }
    }
}

double Product::takeAmount(double amount) {
    double taken = std::min(amount_, amount);
    amount_ -= taken;
    return taken;
}

void Product::addAmount(double amount) {
    amount_ += amount;
}

ProductInfo Product::getProductInfo(ProductType type) {
    if (!isDatabaseInitialized_) {
        initializeProductDatabase();
    }
    
    auto it = productDatabase_.find(type);
    if (it != productDatabase_.end()) {
        return it->second;
    }
    
    return {"Невідомий", "Невідомий продукт", 0.0, 0, false, 0.0};
}

std::string Product::productTypeToString(ProductType type) {
    return getProductInfo(type).name;
}

ProductType Product::stringToProductType(const std::string& name) {
    if (!isDatabaseInitialized_) {
        initializeProductDatabase();
    }
    
    for (const auto& pair : productDatabase_) {
        if (pair.second.name == name) {
            return pair.first;
        }
    }
    
    return ProductType::MANURE;
}

ProductQuality Product::calculateQuality(double qualityScore) {
    if (qualityScore >= 95) return ProductQuality::ARTISAN;
    if (qualityScore >= 85) return ProductQuality::PREMIUM;
    if (qualityScore >= 70) return ProductQuality::EXCELLENT;
    if (qualityScore >= 50) return ProductQuality::GOOD;
    if (qualityScore >= 30) return ProductQuality::NORMAL;
    return ProductQuality::POOR;
}

std::unique_ptr<Product> Product::create(ProductType type, double amount, 
                                          ProductQuality quality) {
    return std::make_unique<Product>(type, amount, quality);
}

bool Product::canCombineWith(const Product& other) const {
    return type_ == other.type_ && quality_ == other.quality_;
}

void Product::combineWith(Product& other) {
    if (canCombineWith(other)) {
        amount_ += other.amount_;
        other.amount_ = 0;
        
        // Взяти менший термін придатності
        daysRemaining_ = std::min(daysRemaining_, other.daysRemaining_);
    }
}

// ==================== DairyProduct ====================

DairyProduct::DairyProduct(ProductType type, double amount, ProductQuality quality,
                           double fatContent)
    : Product(type, amount, quality)
    , fatContent_(fatContent)
    , isPasteurized_(false)
{
}

void DairyProduct::pasteurize() {
    isPasteurized_ = true;
    // Пастеризація подовжує термін зберігання
    daysRemaining_ += 7;
}

// ==================== MeatProduct ====================

MeatProduct::MeatProduct(ProductType type, double amount, ProductQuality quality)
    : Product(type, amount, quality)
    , isProcessed_(false)
    , isSmoked_(false)
    , freshness_(100.0)
{
}

void MeatProduct::process() {
    isProcessed_ = true;
    type_ = ProductType::PROCESSED_MEAT;
    daysRemaining_ += 7;
}

void MeatProduct::smoke() {
    isSmoked_ = true;
    type_ = ProductType::SMOKED_MEAT;
    daysRemaining_ += 21;
}

// ==================== TextileProduct ====================

TextileProduct::TextileProduct(ProductType type, double amount, ProductQuality quality)
    : Product(type, amount, quality)
    , softness_(70.0)
    , color_("натуральний")
    , isProcessed_(false)
{
}

void TextileProduct::dye(const std::string& color) {
    color_ = color;
}

void TextileProduct::process() {
    isProcessed_ = true;
    if (type_ == ProductType::WOOL) {
        type_ = ProductType::WOOL_FABRIC;
    }
}

} // namespace FarmGame
