#include "ants.h"

#include <algorithm>
#include <random>
City::City(size_t size) : roads_(size) {}

void City::AddRoad(size_t from, size_t to, double weight) {
    roads_[from].push_back({to, weight, 1, false, false});
    roads_[to].push_back({from, weight, 1, false, false});
}

std::vector<Road>& City::GetRoads(size_t from) { return roads_[from]; }

const std::vector<Road>& City::GetRoads(size_t from) const {
    return roads_[from];
}

size_t City::GetSize() const { return roads_.size(); }

size_t BinarySearch(const std::vector<double>& roads, double value) {
    size_t left = 0;
    size_t right = roads.size() - 1;
    while (left + 1 < right) {
        size_t mid = (left + right) / 2;
        if (roads[mid] < value) {
            left = mid;
        } else {
            right = mid;
        }
    }
    return right;
}

double GetCoefficient(const Road& road, double ph_pow, double weight_pow) {
    return pow(road.pheromones, ph_pow) * pow(1 / road.weight, weight_pow);
}

double GetWholePheromones(const std::vector<size_t>& roads_indices,
                          const std::vector<Road>& roads, double ph_pow,
                          double weight_pow) {
    double whole_pheromones = 0;
    for (const auto& index : roads_indices) {
        whole_pheromones += GetCoefficient(roads[index], ph_pow, weight_pow);
    }
    return whole_pheromones;
}

size_t Ant::ChooseRoad(const std::vector<Road>& roads, double ph_pow,
                       double weight_pow, std::unordered_set<size_t>& visited) {
    std::vector<size_t> roads_indices;
    for (size_t i = 0; i < roads.size(); ++i) {
        if (visited.find(roads[i].to) == visited.end()) {
            roads_indices.push_back(i);
        }
    }
    if (roads_indices.empty()) {
        return roads.size();
    }
    double whole_pheromones =
        GetWholePheromones(roads_indices, roads, ph_pow, weight_pow);
    std::vector<double> buckets(roads_indices.size() + 1);
    buckets[0] = 0;
    for (size_t i = 1; i < buckets.size(); ++i) {
        buckets[i] =
            buckets[i - 1] +
            GetCoefficient(roads[roads_indices[i - 1]], ph_pow, weight_pow);
    }
    for (int i = 0; i < buckets.size(); ++i) {
        buckets[i] /= whole_pheromones;
    }
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0, buckets.back());
    double value = dis(gen);
    return roads_indices[BinarySearch(buckets, value) - 1];
}

Path Ant::BuildPath(City& city, size_t start, double ph_pow,
                    double weight_pow) {
    Path path;
    path.is_complete = false;
    size_t current = start;
    std::unordered_set<size_t> visited;
    visited.insert(current);
    path.sum_weight = 0;
    while (visited.size() < city.GetSize()) {
        size_t chosen_road_index =
            ChooseRoad(city.GetRoads(current), ph_pow, weight_pow, visited);
        if (chosen_road_index == city.GetRoads(current).size()) {
            return path;
        }
        path.roads.push_back(&city.GetRoads(current)[chosen_road_index]);
        path.sum_weight += city.GetRoads(current)[chosen_road_index].weight;
        current = city.GetRoads(current)[chosen_road_index].to;
        visited.insert(current);
    }
    path.is_complete = true;
    path.start = start;
    return path;
}

#include <iostream>

Path City::Crowl(size_t iterations, size_t ants_count, size_t elite_count,
                 double evaporation_rate, double common_pheromones,
                 double elite_pheromones, double ph_pow, double weight_pow) {
    Path best_path;
    bool found_path = false;
    for (size_t i = 0; i < iterations; ++i) {
        std::vector<Path> paths(ants_count * roads_.size());
        for (size_t j = 0; j < ants_count * roads_.size(); ++j) {
            size_t start = j % roads_.size();
            paths[j] = Ant().BuildPath(*this, start, ph_pow, weight_pow);
        }
        for (auto& path : paths) {
            for (auto& road : path.roads) {
                road->pheromones *= (1 - evaporation_rate);
            }
        }
        std::sort(paths.begin(), paths.end(), [](const Path& a, const Path& b) {
            if (a.is_complete && !b.is_complete) {
                return true;
            }
            if (!a.is_complete && b.is_complete) {
                return false;
            }
            return a.sum_weight < b.sum_weight;
        });
        for (size_t j = 0; j < elite_count; ++j) {
            if (!paths[j].is_complete) {
                continue;
            }
            for (auto& road : paths[j].roads) {
                road->elite_visited = true;
            }
        }
        for (size_t j = elite_count; j < paths.size(); ++j) {
            if (!paths[j].is_complete) {
                continue;
            }
            for (auto& road : paths[j].roads) {
                road->visited = true;
            }
        }
        for (auto& path : paths) {
            for (auto& road : path.roads) {
                if (road->elite_visited) {
                    road->pheromones += elite_pheromones;
                } else if (road->visited) {
                    road->pheromones += common_pheromones;
                }
                road->elite_visited = false;
                road->visited = false;
            }
        }
        if (paths[0].is_complete &&
            (!found_path || paths[0].sum_weight < best_path.sum_weight)) {
            best_path = paths[0];
            found_path = true;
        }
    }
    return best_path;
}

Path City::BruteForce() {
    Path best_path;
    best_path.sum_weight = std::numeric_limits<double>::infinity();
    best_path.is_complete = false;
    bool found_path = false;
    for (size_t start = 0; start < roads_.size(); ++start) {
        std::vector<bool> visited(roads_.size(), false);
        std::vector<Road*> current_path;

        visited[start] = true;
        BruteForceRecursive(start, visited, start, 0, current_path, best_path,
                            found_path);
    }

    return best_path;
}

void City::BruteForceRecursive(size_t true_start, std::vector<bool>& visited,
                               size_t current, double current_weight,
                               std::vector<Road*>& current_path,
                               Path& best_path, bool& found_path) {
    bool all_visited = true;
    for (size_t i = 0; i < roads_.size(); ++i) {
        if (!visited[i]) {
            all_visited = false;
            break;
        }
    }

    if (all_visited) {
        if (!found_path || current_weight < best_path.sum_weight) {
            best_path.roads = current_path;
            best_path.sum_weight = current_weight;
            best_path.start = true_start;
            best_path.is_complete = true;
            found_path = true;
        }
        return;
    }

    for (auto& road : roads_[current]) {
        if (!visited[road.to]) {
            visited[road.to] = true;
            current_path.push_back(&road);

            BruteForceRecursive(true_start, visited, road.to,
                                current_weight + road.weight, current_path,
                                best_path, found_path);
            current_path.pop_back();
            visited[road.to] = false;
        }
    }
}
