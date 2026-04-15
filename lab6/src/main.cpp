#include <chrono>
#include <fstream>
#include <iostream>

#include "ants.h"
int main() {
    std::cout << "Please choose the input mode:" << std::endl;
    std::cout << "1. File" << std::endl;
    std::cout << "2. Console" << std::endl;
    int mode;
    std::cin >> mode;
    std::istream* in_stream;
    std::ifstream in_file;
    if (mode == 1) {
        std::string file_name;
        std::cout << "Please enter the file name: ";
        std::cin >> file_name;
        in_file.open(file_name);
        in_stream = &in_file;
    } else {
        in_stream = &std::cin;
    }
    size_t cities_count;
    *in_stream >> cities_count;
    City city(cities_count);
    size_t roads_count;
    *in_stream >> roads_count;
    for (size_t i = 0; i < roads_count; ++i) {
        if (mode == 2) {
            std::cout << "Please enter the start and end of road " << i + 1
                      << ": ";
        }
        size_t start, end;
        *in_stream >> start >> end;
        if (mode == 2) {
            std::cout << "Please enter the weight of road " << i + 1 << ": ";
        }
        double weight;
        *in_stream >> weight;
        city.AddRoad(start, end, weight);
    }
    std::cout << "Please choose the algorithm to use:" << std::endl;
    std::cout << "1. Ant Colony Optimization" << std::endl;
    std::cout << "2. Brute Force" << std::endl;
    int algorithm_mode;
    std::cin >> algorithm_mode;
    Path path;
    if (algorithm_mode == 1) {
        if (mode == 2) {
            std::cout << "Please enter the number of iterations: ";
        }
        size_t iterations;
        *in_stream >> iterations;
        if (mode == 2) {
            std::cout << "Please enter the number of ants in each city: ";
        }
        size_t ants_count;
        *in_stream >> ants_count;
        if (mode == 2) {
            std::cout << "Please enter the number of elite ants: ";
        }
        size_t elite_count;
        *in_stream >> elite_count;
        if (mode == 2) {
            std::cout << "Please enter the evaporation rate: ";
        }
        double evaporation_rate;
        *in_stream >> evaporation_rate;
        if (mode == 2) {
            std::cout << "Please enter the common pheromones: ";
        }
        double common_pheromones;
        *in_stream >> common_pheromones;
        if (mode == 2) {
            std::cout << "Please enter the elite pheromones: ";
        }
        double elite_pheromones;
        *in_stream >> elite_pheromones;
        if (mode == 2) {
            std::cout << "Please enter the ph power: ";
        }
        double ph_pow;
        *in_stream >> ph_pow;
        if (mode == 2) {
            std::cout << "Please enter the weight power: ";
        }
        double weight_pow;
        *in_stream >> weight_pow;
        auto start_time = std::chrono::high_resolution_clock::now();

        path =
            city.Crowl(iterations, ants_count, elite_count, evaporation_rate,
                       common_pheromones, elite_pheromones, ph_pow, weight_pow);
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
                            end_time - start_time)
                            .count();

        std::cout << "The best path found has a total weight of: "
                  << path.sum_weight << std::endl;
        std::cout << "Starting city: " << path.start << std::endl;
        for (const auto& road : path.roads) {
            std::cout << road->to << " ";
        }
        std::cout << "Time taken: " << duration << " milliseconds"
                  << std::endl;  // Display time taken
    } else if (algorithm_mode == 2) {
        auto start_time = std::chrono::high_resolution_clock::now();

        path = city.BruteForce();

        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
                            end_time - start_time)
                            .count();

        if (path.is_complete) {
            std::cout << "The best path found has a total weight of: "
                      << path.sum_weight << std::endl;
            std::cout << "Starting city: " << path.start << std::endl;
            std::cout << "Path: " << path.start << " ";
            for (const auto& road : path.roads) {
                std::cout << road->to << " ";
            }
            std::cout << std::endl;
        } else {
            std::cout << "No valid path found!" << std::endl;
        }
        std::cout << "Time taken: " << duration << " milliseconds" << std::endl;
    } else {
        std::cerr << "Invalid algorithm mode chosen." << std::endl;
        return 1;
    }

    if (in_file.is_open()) {
        in_file.close();
    }
    return 0;
}
