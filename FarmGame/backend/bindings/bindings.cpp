/**
 * @file bindings.cpp
 * @brief Python біндинги для C++ класів через pybind11
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include "animals/Animal.hpp"
#include "animals/Cow.hpp"
#include "animals/Chicken.hpp"
#include "animals/Pig.hpp"
#include "animals/Sheep.hpp"
#include "animals/Goat.hpp"
#include "animals/Duck.hpp"
#include "animals/Rabbit.hpp"
#include "animals/Horse.hpp"
#include "production/Feed.hpp"
#include "production/Product.hpp"
#include "production/Storage.hpp"
#include "farm/Farmer.hpp"
#include "farm/Farm.hpp"

namespace py = pybind11;
using namespace FarmGame;

PYBIND11_MODULE(farm_backend, m) {
    m.doc() = "Бекенд гри 'Ферма' - Python біндинги для C++ класів";
    
    // ==================== Перелічення ====================
    
    py::enum_<AnimalState>(m, "AnimalState")
        .value("HEALTHY", AnimalState::HEALTHY)
        .value("HUNGRY", AnimalState::HUNGRY)
        .value("SICK", AnimalState::SICK)
        .value("PRODUCING", AnimalState::PRODUCING)
        .value("SLEEPING", AnimalState::SLEEPING)
        .value("HAPPY", AnimalState::HAPPY);
    
    py::enum_<AnimalType>(m, "AnimalType")
        .value("COW", AnimalType::COW)
        .value("CHICKEN", AnimalType::CHICKEN)
        .value("PIG", AnimalType::PIG)
        .value("SHEEP", AnimalType::SHEEP)
        .value("GOAT", AnimalType::GOAT)
        .value("DUCK", AnimalType::DUCK)
        .value("RABBIT", AnimalType::RABBIT)
        .value("HORSE", AnimalType::HORSE);
    
    py::enum_<Season>(m, "Season")
        .value("SPRING", Season::SPRING)
        .value("SUMMER", Season::SUMMER)
        .value("AUTUMN", Season::AUTUMN)
        .value("WINTER", Season::WINTER);
    
    py::enum_<Weather>(m, "Weather")
        .value("SUNNY", Weather::SUNNY)
        .value("CLOUDY", Weather::CLOUDY)
        .value("RAINY", Weather::RAINY)
        .value("STORMY", Weather::STORMY)
        .value("SNOWY", Weather::SNOWY)
        .value("FOGGY", Weather::FOGGY);
    
    py::enum_<FeedType>(m, "FeedType")
        .value("HAY", FeedType::HAY)
        .value("GRAIN", FeedType::GRAIN)
        .value("CORN", FeedType::CORN)
        .value("MIXED_FEED", FeedType::MIXED_FEED)
        .value("GRASS", FeedType::GRASS)
        .value("VEGETABLES", FeedType::VEGETABLES)
        .value("OATS", FeedType::OATS)
        .value("BRANCHES", FeedType::BRANCHES)
        .value("CARROTS", FeedType::CARROTS)
        .value("PREMIUM_FEED", FeedType::PREMIUM_FEED);
    
    py::enum_<ProductType>(m, "ProductType")
        .value("MILK", ProductType::MILK)
        .value("GOAT_MILK", ProductType::GOAT_MILK)
        .value("CHEESE", ProductType::CHEESE)
        .value("BUTTER", ProductType::BUTTER)
        .value("CHICKEN_EGG", ProductType::CHICKEN_EGG)
        .value("DUCK_EGG", ProductType::DUCK_EGG)
        .value("BEEF", ProductType::BEEF)
        .value("PORK", ProductType::PORK)
        .value("LAMB", ProductType::LAMB)
        .value("WOOL", ProductType::WOOL)
        .value("TRUFFLE", ProductType::TRUFFLE)
        .value("MANURE", ProductType::MANURE);
    
    py::enum_<ProductQuality>(m, "ProductQuality")
        .value("POOR", ProductQuality::POOR)
        .value("NORMAL", ProductQuality::NORMAL)
        .value("GOOD", ProductQuality::GOOD)
        .value("EXCELLENT", ProductQuality::EXCELLENT)
        .value("PREMIUM", ProductQuality::PREMIUM)
        .value("ARTISAN", ProductQuality::ARTISAN);
    
    py::enum_<CowBreed>(m, "CowBreed")
        .value("HOLSTEIN", CowBreed::HOLSTEIN)
        .value("JERSEY", CowBreed::JERSEY)
        .value("ANGUS", CowBreed::ANGUS)
        .value("HEREFORD", CowBreed::HEREFORD)
        .value("SIMMENTAL", CowBreed::SIMMENTAL);
    
    py::enum_<ChickenBreed>(m, "ChickenBreed")
        .value("LEGHORN", ChickenBreed::LEGHORN)
        .value("RHODE_ISLAND", ChickenBreed::RHODE_ISLAND)
        .value("PLYMOUTH", ChickenBreed::PLYMOUTH)
        .value("SUSSEX", ChickenBreed::SUSSEX)
        .value("ORPINGTON", ChickenBreed::ORPINGTON);
    
    py::enum_<PigBreed>(m, "PigBreed")
        .value("LANDRACE", PigBreed::LANDRACE)
        .value("YORKSHIRE", PigBreed::YORKSHIRE)
        .value("DUROC", PigBreed::DUROC)
        .value("HAMPSHIRE", PigBreed::HAMPSHIRE)
        .value("BERKSHIRE", PigBreed::BERKSHIRE);
    
    py::enum_<SheepBreed>(m, "SheepBreed")
        .value("MERINO", SheepBreed::MERINO)
        .value("SUFFOLK", SheepBreed::SUFFOLK)
        .value("DORSET", SheepBreed::DORSET)
        .value("ROMANOV", SheepBreed::ROMANOV)
        .value("LINCOLN", SheepBreed::LINCOLN);
    
    // ==================== Структури ====================
    
    py::class_<AnimalStats>(m, "AnimalStats")
        .def(py::init<>())
        .def_readwrite("total_fed", &AnimalStats::totalFed)
        .def_readwrite("total_produced", &AnimalStats::totalProduced)
        .def_readwrite("days_on_farm", &AnimalStats::daysOnFarm)
        .def_readwrite("total_earnings", &AnimalStats::totalEarnings);
    
    py::class_<FarmStats>(m, "FarmStats")
        .def(py::init<>())
        .def_readwrite("total_animals", &FarmStats::totalAnimals)
        .def_readwrite("total_products", &FarmStats::totalProducts)
        .def_readwrite("total_value", &FarmStats::totalValue)
        .def_readwrite("days_passed", &FarmStats::daysPassed)
        .def_readwrite("daily_income", &FarmStats::dailyIncome)
        .def_readwrite("daily_expenses", &FarmStats::dailyExpenses)
        .def_readwrite("reputation", &FarmStats::reputation);
    
    py::class_<FarmerStats>(m, "FarmerStats")
        .def(py::init<>())
        .def_readwrite("animals_fed", &FarmerStats::animalsFed)
        .def_readwrite("productions_collected", &FarmerStats::productionsCollected)
        .def_readwrite("total_earnings", &FarmerStats::totalEarnings)
        .def_readwrite("days_played", &FarmerStats::daysPlayed);
    
    py::class_<Building>(m, "Building")
        .def(py::init<>())
        .def_readwrite("name", &Building::name)
        .def_readwrite("type", &Building::type)
        .def_readwrite("level", &Building::level)
        .def_readwrite("capacity", &Building::capacity)
        .def_readwrite("maintenance_cost", &Building::maintenanceCost)
        .def_readwrite("is_upgradable", &Building::isUpgradable);
    
    // ==================== Клас Animal (базовий) ====================
    
    py::class_<Animal>(m, "Animal")
        .def("get_type", &Animal::getType)
        .def("get_type_name", &Animal::getTypeName)
        .def("make_sound", &Animal::makeSound)
        .def("produce", &Animal::produce)
        .def("get_product_name", &Animal::getProductName)
        .def("get_product_price", &Animal::getProductPrice)
        .def("get_base_price", &Animal::getBasePrice)
        .def("get_feed_consumption", &Animal::getFeedConsumption)
        .def("get_favorite_feed", &Animal::getFavoriteFeed)
        .def("feed", &Animal::feed, py::arg("feed_quality") = 1.0, py::arg("amount") = 1.0)
        .def("update", &Animal::update)
        .def("heal", &Animal::heal)
        .def("pet", &Animal::pet)
        .def("get_name", &Animal::getName)
        .def("get_age", &Animal::getAge)
        .def("get_health", &Animal::getHealth)
        .def("get_hunger", &Animal::getHunger)
        .def("get_happiness", &Animal::getHappiness)
        .def("get_state", &Animal::getState)
        .def("get_id", &Animal::getId)
        .def("is_alive", &Animal::isAlive)
        .def("can_produce", &Animal::canProduce)
        .def("get_stats", &Animal::getStats)
        .def("get_current_value", &Animal::getCurrentValue)
        .def("get_state_string", &Animal::getStateString)
        .def("get_production_cooldown", &Animal::getProductionCooldown)
        .def("set_name", &Animal::setName)
        .def("age_one_day", &Animal::ageOneDay)
        .def("get_info", &Animal::getInfo)
        .def("needs_feeding", &Animal::needsFeeding)
        .def("needs_healing", &Animal::needsHealing);
    
    // ==================== Похідні класи тварин ====================
    
    py::class_<Cow, Animal>(m, "Cow")
        .def(py::init<const std::string&, int, CowBreed>(),
             py::arg("name"), py::arg("age") = 0, 
             py::arg("breed") = CowBreed::HOLSTEIN)
        .def("get_breed", &Cow::getBreed)
        .def("get_breed_name", &Cow::getBreedName)
        .def("get_milk_quality", &Cow::getMilkQuality)
        .def("get_milk_production", &Cow::getMilkProduction)
        .def("is_pregnant", &Cow::isPregnant)
        .def("breed", &Cow::breed)
        .def("can_breed", &Cow::canBreed);
    
    py::class_<Chicken, Animal>(m, "Chicken")
        .def(py::init<const std::string&, int, ChickenBreed>(),
             py::arg("name"), py::arg("age") = 0,
             py::arg("breed") = ChickenBreed::LEGHORN)
        .def("get_breed", &Chicken::getBreed)
        .def("get_breed_name", &Chicken::getBreedName)
        .def("get_egg_quality", &Chicken::getEggQuality)
        .def("get_eggs_per_day", &Chicken::getEggsPerDay)
        .def("is_broody", &Chicken::isBroody)
        .def("get_chicks", &Chicken::getChicks)
        .def("hatch_eggs", &Chicken::hatchEggs)
        .def("collect_chicks", &Chicken::collectChicks);
    
    py::class_<Pig, Animal>(m, "Pig")
        .def(py::init<const std::string&, int, PigBreed>(),
             py::arg("name"), py::arg("age") = 0,
             py::arg("breed") = PigBreed::YORKSHIRE)
        .def("get_breed", &Pig::getBreed)
        .def("get_breed_name", &Pig::getBreedName)
        .def("get_weight", &Pig::getWeight)
        .def("get_meat_quality", &Pig::getMeatQuality)
        .def("can_find_truffles", &Pig::canFindTruffles)
        .def("search_truffles", &Pig::searchTruffles)
        .def("slaughter", &Pig::slaughter);
    
    py::class_<Sheep, Animal>(m, "Sheep")
        .def(py::init<const std::string&, int, SheepBreed>(),
             py::arg("name"), py::arg("age") = 0,
             py::arg("breed") = SheepBreed::MERINO)
        .def("get_breed", &Sheep::getBreed)
        .def("get_breed_name", &Sheep::getBreedName)
        .def("get_wool_quality", &Sheep::getWoolQuality)
        .def("get_wool_length", &Sheep::getWoolLength)
        .def("can_be_sheared", &Sheep::canBeSheared)
        .def("get_lambs", &Sheep::getLambs)
        .def("shear", &Sheep::shear)
        .def("breed_lambs", &Sheep::breedLambs);
    
    // ==================== Feed ====================
    
    py::class_<Feed, std::shared_ptr<Feed>>(m, "Feed")
        .def(py::init<FeedType, double>(),
             py::arg("type"), py::arg("amount") = 0.0)
        .def("get_type", &Feed::getType)
        .def("get_name", &Feed::getName)
        .def("get_description", &Feed::getDescription)
        .def("get_amount", &Feed::getAmount)
        .def("get_quality", &Feed::getQuality)
        .def("get_nutrition", &Feed::getNutrition)
        .def("get_price_per_unit", &Feed::getPricePerUnit)
        .def("get_total_value", &Feed::getTotalValue)
        .def("is_expired", &Feed::isExpired)
        .def("add_amount", &Feed::addAmount)
        .def("take_amount", &Feed::takeAmount)
        .def("age_one_day", &Feed::ageOneDay)
        .def_static("feed_type_to_string", &Feed::feedTypeToString);
    
    // ==================== Product ====================
    
    py::class_<Product, std::shared_ptr<Product>>(m, "Product")
        .def(py::init<ProductType, double, ProductQuality>(),
             py::arg("type"), py::arg("amount"),
             py::arg("quality") = ProductQuality::NORMAL)
        .def("get_type", &Product::getType)
        .def("get_name", &Product::getName)
        .def("get_description", &Product::getDescription)
        .def("get_amount", &Product::getAmount)
        .def("get_quality", &Product::getQuality)
        .def("get_quality_string", &Product::getQualityString)
        .def("get_price", &Product::getPrice)
        .def("get_total_value", &Product::getTotalValue)
        .def("get_days_remaining", &Product::getDaysRemaining)
        .def("is_expired", &Product::isExpired)
        .def("is_perishable", &Product::isPerishable)
        .def("take_amount", &Product::takeAmount)
        .def("age_one_day", &Product::ageOneDay)
        .def_static("product_type_to_string", &Product::productTypeToString);
    
    // ==================== Farmer ====================
    
    py::class_<Farmer>(m, "Farmer")
        .def(py::init<const std::string&>())
        .def("feed_animal", &Farmer::feedAnimal)
        .def("collect_product", &Farmer::collectProduct)
        .def("heal_animal", &Farmer::healAnimal)
        .def("pet_animal", &Farmer::petAnimal)
        .def("sell_product", &Farmer::sellProduct)
        .def("buy_feed", &Farmer::buyFeed)
        .def("sell_animal", &Farmer::sellAnimal)
        .def("get_money", &Farmer::getMoney)
        .def("add_money", &Farmer::addMoney)
        .def("spend_money", &Farmer::spendMoney)
        .def("can_afford", &Farmer::canAfford)
        .def("get_energy", &Farmer::getEnergy)
        .def("get_max_energy", &Farmer::getMaxEnergy)
        .def("has_energy", &Farmer::hasEnergy)
        .def("sleep", &Farmer::sleep)
        .def("get_stats", &Farmer::getStats)
        .def("get_name", &Farmer::getName)
        .def("set_name", &Farmer::setName)
        .def("get_level", &Farmer::getLevel)
        .def("get_experience", &Farmer::getExperience)
        .def("update", &Farmer::update);
    
    // ==================== Farm ====================
    
    py::class_<Farm>(m, "Farm")
        .def(py::init<const std::string&, const std::string&>())
        .def("add_animal", [](Farm& f, py::object animal) {
            // Перетворення Python об'єкта на C++ unique_ptr
            if (py::isinstance<Cow>(animal)) {
                auto& cow = animal.cast<Cow&>();
                return f.addAnimal(cow.clone());
            }
            // Додати інші типи за потреби
            return false;
        })
        .def("remove_animal", &Farm::removeAnimal)
        .def("get_animal", &Farm::getAnimal, py::return_value_policy::reference)
        .def("get_all_animals", &Farm::getAllAnimals, py::return_value_policy::reference)
        .def("get_animals_by_type", &Farm::getAnimalsByType, py::return_value_policy::reference)
        .def("get_animal_count", &Farm::getAnimalCount)
        .def("get_animal_count_by_type", &Farm::getAnimalCountByType)
        .def("add_feed", &Farm::addFeed)
        .def("take_feed", &Farm::takeFeed)
        .def("has_feed", &Farm::hasFeed)
        .def("get_feed_amount", &Farm::getFeedAmount)
        .def("add_product", &Farm::addProduct)
        .def("take_product", &Farm::takeProduct)
        .def("get_product_amount", &Farm::getProductAmount)
        .def("feed_all_animals", &Farm::feedAllAnimals)
        .def("collect_all_products", &Farm::collectAllProducts)
        .def("sell_all_products", &Farm::sellAllProducts)
        .def("heal_sick_animals", &Farm::healSickAnimals)
        .def("get_current_season", &Farm::getCurrentSeason)
        .def("get_current_weather", &Farm::getCurrentWeather)
        .def("get_current_day", &Farm::getCurrentDay)
        .def("get_current_hour", &Farm::getCurrentHour)
        .def("get_time_string", &Farm::getTimeString)
        .def("get_season_string", &Farm::getSeasonString)
        .def("get_weather_string", &Farm::getWeatherString)
        .def("advance_time", &Farm::advanceTime, py::arg("hours") = 1)
        .def("advance_day", &Farm::advanceDay)
        .def("get_buildings", &Farm::getBuildings)
        .def("upgrade_building", &Farm::upgradeBuilding)
        .def("get_total_capacity", &Farm::getTotalCapacity)
        .def("get_money", &Farm::getMoney)
        .def("get_daily_income", &Farm::getDailyIncome)
        .def("get_daily_expenses", &Farm::getDailyExpenses)
        .def("get_net_worth", &Farm::getNetWorth)
        .def("get_stats", &Farm::getStats)
        .def("get_name", &Farm::getName)
        .def("set_name", &Farm::setName)
        .def("get_farmer", &Farm::getFarmer, py::return_value_policy::reference)
        .def("get_reputation", &Farm::getReputation)
        .def("update", &Farm::update)
        .def("save_to_file", &Farm::saveToFile)
        .def("set_event_callback", &Farm::setEventCallback);
    
    // ==================== AnimalFactory ====================
    
    py::class_<AnimalFactory>(m, "AnimalFactory")
        .def_static("create_animal", &AnimalFactory::createAnimal)
        .def_static("create_cow", &AnimalFactory::createCow,
                    py::arg("name"), py::arg("breed") = CowBreed::HOLSTEIN,
                    py::arg("age") = 0)
        .def_static("create_chicken", &AnimalFactory::createChicken,
                    py::arg("name"), py::arg("breed") = ChickenBreed::LEGHORN,
                    py::arg("age") = 0)
        .def_static("create_pig", &AnimalFactory::createPig,
                    py::arg("name"), py::arg("breed") = PigBreed::YORKSHIRE,
                    py::arg("age") = 0)
        .def_static("create_sheep", &AnimalFactory::createSheep,
                    py::arg("name"), py::arg("breed") = SheepBreed::MERINO,
                    py::arg("age") = 0)
        .def_static("get_animal_price", &AnimalFactory::getAnimalPrice)
        .def_static("get_animal_type_name", &AnimalFactory::getAnimalTypeName);
    
    // ==================== Допоміжні функції ====================
    
    m.def("get_version", []() { return "1.0.0"; });
    m.def("get_author", []() { return "Курсова робота з ООП"; });
}
