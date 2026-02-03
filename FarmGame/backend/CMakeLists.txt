cmake_minimum_required(VERSION 3.15)
project(FarmGame VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Пошук Python та pybind11
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG QUIET)

if(NOT pybind11_FOUND)
    # Якщо pybind11 не знайдено, завантажити через FetchContent
    include(FetchContent)
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.11.1
    )
    FetchContent_MakeAvailable(pybind11)
endif()

# Директорії з заголовними файлами
include_directories(${CMAKE_SOURCE_DIR}/include)

# Збір всіх .cpp файлів
file(GLOB_RECURSE ANIMAL_SOURCES "src/animals/*.cpp")
file(GLOB_RECURSE FARM_SOURCES "src/farm/*.cpp")
file(GLOB_RECURSE PRODUCTION_SOURCES "src/production/*.cpp")

set(ALL_SOURCES
    ${ANIMAL_SOURCES}
    ${FARM_SOURCES}
    ${PRODUCTION_SOURCES}
)

# Створення статичної бібліотеки
add_library(farm_core STATIC ${ALL_SOURCES})
target_include_directories(farm_core PUBLIC ${CMAKE_SOURCE_DIR}/include)

# Створення Python модуля
pybind11_add_module(farm_backend bindings/bindings.cpp)
target_link_libraries(farm_backend PRIVATE farm_core)
target_include_directories(farm_backend PRIVATE ${CMAKE_SOURCE_DIR}/include)

# Копіювання модуля до frontend директорії
add_custom_command(TARGET farm_backend POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    $<TARGET_FILE:farm_backend>
    ${CMAKE_SOURCE_DIR}/../frontend/game/
)

# Тести (опціонально)
option(BUILD_TESTS "Build tests" OFF)
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Інформація про збірку
message(STATUS "FarmGame Backend Configuration:")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Python Version: ${Python3_VERSION}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
