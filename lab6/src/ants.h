#pragma once

#include <vector>
#include <cstddef>
#include <cstdint>
#include <unordered_set>
struct Road {
  size_t to;
  double weight;
  double pheromones;
  bool visited;
  bool elite_visited;
};

struct Path {
  size_t start;
  std::vector<Road*> roads;
  double sum_weight;
  bool is_complete;
};

class City {
  std::vector<std::vector<Road>> roads_;

 public:
  City(size_t size);
  void AddRoad(size_t from, size_t to, double weight);
  std::vector<Road>& GetRoads(size_t from);
  const std::vector<Road>& GetRoads(size_t from) const;
  size_t GetSize() const;
  Path Crowl(size_t iterations, size_t ants_count, size_t elite_count, double evaporation_rate,
             double common_pheromones, double elite_pheromones, double ph_pow, double weight_pow);
  Path BruteForce();

 private:
  void BruteForceRecursive(size_t true_start, std::vector<bool>& visited, size_t current, double current_weight,
                           std::vector<Road*>& current_path, Path& best_path, bool& found_path);
};

class Ant {
 public:
  size_t ChooseRoad(const std::vector<Road>& roads, double ph_pow, double weight_pow,
                    std::unordered_set<size_t>& visited);
  Path BuildPath(City& city, size_t start, double ph_pow, double weight_pow);
};
