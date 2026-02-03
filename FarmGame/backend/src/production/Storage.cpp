/**
 * @file Storage.cpp
 * @brief Реалізація системи зберігання
 */

#include "production/Storage.hpp"
#include <algorithm>

namespace FarmGame {

// ==================== Storage ====================

Storage::Storage(StorageType type, double capacity)
    : type_(type)
    , capacity_(capacity)
    , usedSpace_(0.0)
    , level_(1)
    , upgradeMultiplier_(1.5)
{
}

std::string Storage::getTypeName() const {
    switch (type_) {
        case StorageType::BARN: return "Амбар";
        case StorageType::WAREHOUSE: return "Склад";
        case StorageType::REFRIGERATOR: return "Холодильник";
        case StorageType::CELLAR: return "Погреб";
        case StorageType::SILO: return "Силос";
        default: return "Невідоме сховище";
    }
}

StorageStats Storage::getStats() const {
    return {
        usedSpace_,
        capacity_,
        0,  // Буде перевизначено в похідних класах
        0,
        0.0
    };
}

bool Storage::canStore(double amount) const {
    return (usedSpace_ + amount) <= capacity_;
}

void Storage::upgrade() {
    level_++;
    capacity_ *= upgradeMultiplier_;
}

void Storage::ageContents() {
    // Базова реалізація - нічого
}

void Storage::removeExpired() {
    // Базова реалізація - нічого
}

// ==================== FeedStorage ====================

FeedStorage::FeedStorage(double capacity)
    : Storage(StorageType::BARN, capacity)
{
}

bool FeedStorage::addFeed(std::shared_ptr<Feed> feed) {
    if (!feed || !canStore(feed->getAmount())) return false;
    
    // Якщо такий тип вже є - об'єднати
    auto it = feeds_.find(feed->getType());
    if (it != feeds_.end()) {
        it->second->addAmount(feed->getAmount());
    } else {
        feeds_[feed->getType()] = feed;
    }
    
    updateUsedSpace();
    return true;
}

bool FeedStorage::addFeed(FeedType type, double amount) {
    if (!canStore(amount)) return false;
    
    auto it = feeds_.find(type);
    if (it != feeds_.end()) {
        it->second->addAmount(amount);
    } else {
        feeds_[type] = std::make_shared<Feed>(type, amount);
    }
    
    updateUsedSpace();
    return true;
}

std::shared_ptr<Feed> FeedStorage::getFeed(FeedType type) {
    auto it = feeds_.find(type);
    if (it != feeds_.end()) {
        return it->second;
    }
    return nullptr;
}

double FeedStorage::takeFeed(FeedType type, double amount) {
    auto it = feeds_.find(type);
    if (it == feeds_.end()) return 0.0;
    
    double taken = it->second->takeAmount(amount);
    
    // Видалити якщо порожньо
    if (it->second->getAmount() <= 0) {
        feeds_.erase(it);
    }
    
    updateUsedSpace();
    return taken;
}

bool FeedStorage::hasFeed(FeedType type, double amount) const {
    auto it = feeds_.find(type);
    if (it != feeds_.end()) {
        return it->second->getAmount() >= amount;
    }
    return false;
}

double FeedStorage::getFeedAmount(FeedType type) const {
    auto it = feeds_.find(type);
    if (it != feeds_.end()) {
        return it->second->getAmount();
    }
    return 0.0;
}

std::vector<FeedType> FeedStorage::getAvailableFeedTypes() const {
    std::vector<FeedType> types;
    for (const auto& pair : feeds_) {
        if (pair.second->getAmount() > 0) {
            types.push_back(pair.first);
        }
    }
    return types;
}

double FeedStorage::getTotalFeedValue() const {
    double total = 0.0;
    for (const auto& pair : feeds_) {
        total += pair.second->getTotalValue();
    }
    return total;
}

void FeedStorage::ageContents() {
    for (auto& pair : feeds_) {
        pair.second->ageOneDay();
    }
}

void FeedStorage::removeExpired() {
    for (auto it = feeds_.begin(); it != feeds_.end();) {
        if (it->second->isExpired()) {
            it = feeds_.erase(it);
        } else {
            ++it;
        }
    }
    updateUsedSpace();
}

void FeedStorage::updateUsedSpace() {
    usedSpace_ = 0.0;
    for (const auto& pair : feeds_) {
        usedSpace_ += pair.second->getAmount();
    }
}

// ==================== ProductStorage ====================

ProductStorage::ProductStorage(StorageType type, double capacity)
    : Storage(type, capacity)
    , preservesFood_(type == StorageType::REFRIGERATOR)
{
}

bool ProductStorage::addProduct(std::shared_ptr<Product> product) {
    if (!product || !canStore(product->getAmount())) return false;
    
    // Спробувати об'єднати з існуючим
    for (auto& existing : products_) {
        if (existing->canCombineWith(*product)) {
            existing->combineWith(*product);
            updateUsedSpace();
            return true;
        }
    }
    
    products_.push_back(product);
    updateUsedSpace();
    return true;
}

bool ProductStorage::addProduct(ProductType type, double amount, ProductQuality quality) {
    auto product = Product::create(type, amount, quality);
    return addProduct(std::move(product));
}

std::shared_ptr<Product> ProductStorage::getProduct(ProductType type) {
    for (auto& product : products_) {
        if (product->getType() == type && product->getAmount() > 0) {
            return product;
        }
    }
    return nullptr;
}

double ProductStorage::takeProduct(ProductType type, double amount) {
    double totalTaken = 0.0;
    
    for (auto it = products_.begin(); it != products_.end() && totalTaken < amount;) {
        if ((*it)->getType() == type) {
            double taken = (*it)->takeAmount(amount - totalTaken);
            totalTaken += taken;
            
            if ((*it)->getAmount() <= 0) {
                it = products_.erase(it);
            } else {
                ++it;
            }
        } else {
            ++it;
        }
    }
    
    updateUsedSpace();
    return totalTaken;
}

bool ProductStorage::hasProduct(ProductType type, double amount) const {
    double total = 0.0;
    for (const auto& product : products_) {
        if (product->getType() == type) {
            total += product->getAmount();
        }
    }
    return total >= amount;
}

double ProductStorage::getProductAmount(ProductType type) const {
    double total = 0.0;
    for (const auto& product : products_) {
        if (product->getType() == type) {
            total += product->getAmount();
        }
    }
    return total;
}

std::vector<ProductType> ProductStorage::getAvailableProductTypes() const {
    std::vector<ProductType> types;
    for (const auto& product : products_) {
        if (product->getAmount() > 0) {
            ProductType type = product->getType();
            if (std::find(types.begin(), types.end(), type) == types.end()) {
                types.push_back(type);
            }
        }
    }
    return types;
}

double ProductStorage::getTotalProductValue() const {
    double total = 0.0;
    for (const auto& product : products_) {
        total += product->getTotalValue();
    }
    return total;
}

std::vector<std::shared_ptr<Product>> ProductStorage::findProducts(
    std::function<bool(const Product&)> predicate) const {
    std::vector<std::shared_ptr<Product>> result;
    for (const auto& product : products_) {
        if (predicate(*product)) {
            result.push_back(product);
        }
    }
    return result;
}

std::vector<std::shared_ptr<Product>> ProductStorage::getExpiringProducts(int daysThreshold) const {
    return findProducts([daysThreshold](const Product& p) {
        return p.isPerishable() && p.getDaysRemaining() <= daysThreshold;
    });
}

void ProductStorage::ageContents() {
    for (auto& product : products_) {
        if (!preservesFood_) {
            product->ageOneDay();
        }
    }
}

void ProductStorage::removeExpired() {
    products_.erase(
        std::remove_if(products_.begin(), products_.end(),
            [](const std::shared_ptr<Product>& p) {
                return p->isExpired() || p->getAmount() <= 0;
            }),
        products_.end()
    );
    updateUsedSpace();
}

void ProductStorage::updateUsedSpace() {
    usedSpace_ = 0.0;
    for (const auto& product : products_) {
        usedSpace_ += product->getAmount();
    }
}

// ==================== Refrigerator ====================

Refrigerator::Refrigerator(double capacity)
    : ProductStorage(StorageType::REFRIGERATOR, capacity)
    , temperature_(4.0)
    , preservationBonus_(3)  // +3 дні до терміну зберігання
{
}

void Refrigerator::setTemperature(double temp) {
    temperature_ = std::max(-20.0, std::min(10.0, temp));
    
    // Низька температура краще зберігає
    if (temperature_ <= 0) {
        preservationBonus_ = 7;
    } else if (temperature_ <= 4) {
        preservationBonus_ = 3;
    } else {
        preservationBonus_ = 1;
    }
}

void Refrigerator::ageContents() {
    // Холодильник сповільнює псування
    for (auto& product : products_) {
        // Псується повільніше
        if (product->getDaysRemaining() > preservationBonus_) {
            // Не старіємо сьогодні
        } else {
            product->ageOneDay();
        }
    }
}

} // namespace FarmGame
