#include <chrono>
#include <condition_variable>
#include <fstream>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <unordered_map>
#include <variant>
#include <vector>

struct IngredientInfo {
    std::string name;
    std::string quantity;
};

struct Recipe {
    std::string id;
    std::string issue_id;
    std::string url;
    std::string title;
    std::vector<IngredientInfo> ingredients;
    std::vector<std::string> steps;
    std::string image_url;
};

bool gumbo = false;
std::vector<Recipe> parse_recipes(const std::string& file_path) {
    gumbo = true;
    std::vector<Recipe> recipes;
    // pugi::xml_document doc;

    // // Load the XML file
    // if (!doc.load_file(file_path.c_str())) {
    //   std::cerr << "Error loading file: " << file_path << std::endl;
    //   return recipes;
    // }

    // // Iterate over recipe sections
    // auto nodes = doc.select_nodes("//text:p");
    // for (size_t i = 0; i < nodes.size(); ++i) {
    //   auto recipe_node = nodes[i].node();
    //   Recipe recipe;

    // Extract URL and ID
    //   if (auto link_node = recipe_node.child("text:a")) {
    //     recipe.url = link_node.attribute("xlink:href").value();
    //     size_t last_slash = recipe.url.find_last_of('/');
    //     if (last_slash != std::string::npos) {
    //       recipe.id = recipe.url.substr(last_slash + 1);
    //     }
    //   }

    //   if (auto span_node = recipe_node.child("text:span")) {
    //     recipe.title = span_node.text().get();
    //   }

    //   format. for (const auto& ingredient_node_path :
    //   recipe_node.select_nodes("//ingredient")) {
    //     auto ingredient_node = ingredient_node_path.node();
    //     IngredientInfo ingredient;
    //     ingredient.name = ingredient_node.child_value("name");
    //     ingredient.quantity = ingredient_node.child_value("quantity");
    //     recipe.ingredients.push_back(ingredient);
    //   }

    //   for (const auto& step_node_path : recipe_node.select_nodes("//step")) {
    //     auto step_node = step_node_path.node();
    //     recipe.steps.push_back(step_node.text().get());
    //   }

    //   if (auto image_node =
    //   recipe_node.child("draw:frame").child("draw:image")) {
    //     recipe.image_url = image_node.attribute("xlink:href").value();
    //   }

    //   if (!recipe.title.empty()) {
    //     recipes.push_back(recipe);
    //   }
    // }

    return recipes;
}

enum class TaskType {
    READ,
    EXTRACT,
    STORE,
};

struct Task {
    TaskType type;
    std::variant<std::string, Recipe> data;
    std::chrono::steady_clock::time_point created_time;
};

std::queue<Task> read_queue;
std::queue<Task> extract_queue;
std::queue<Task> store_queue;
std::mutex mtx;
std::condition_variable read_cv, extract_cv, store_cv;

bool reading_done = false;
bool extracting_done = false;
bool storing_done = false;
size_t id = 0;

void read_stage() {
    while (true) {
        Task task;

        {
            std::unique_lock<std::mutex> lock(mtx);
            while (!reading_done && read_queue.empty()) {
                read_cv.wait(lock);
            }

            if (read_queue.empty()) {
                break;
            }

            task = read_queue.front();
            read_queue.pop();
        }

        std::ifstream input_stream(std::get<std::string>(task.data));
        if (!input_stream.is_open()) {
            std::cerr << "Ошибка чтения файла: "
                      << std::get<std::string>(task.data) << std::endl;
            continue;
        }

        std::string html((std::istreambuf_iterator<char>(input_stream)),
                         std::istreambuf_iterator<char>());
        if (html.empty()) {
            std::cerr << "Ошибка: Файл пустой или не содержит данных: "
                      << std::get<std::string>(task.data) << std::endl;
            continue;
        }
        extract_queue.push(
            {TaskType::EXTRACT, html, std::chrono::steady_clock::now()});
        reading_done = true;
        extract_cv.notify_all();
    }
}

void extract_stage() {
    while (true) {
        Task task;

        {
            std::unique_lock<std::mutex> lock(mtx);
            while (!extracting_done && extract_queue.empty()) {
                extract_cv.wait(lock);
            }

            if (extracting_done && extract_queue.empty()) {
                break;
            }

            task = extract_queue.front();
            extract_queue.pop();
            if (reading_done && extract_queue.empty()) {
                extracting_done = true;
                extract_cv.notify_all();
            }
        }

        if (auto html_data = std::get_if<std::string>(&task.data)) {
            auto recipes = parse_recipes(*html_data);
            {
                std::lock_guard<std::mutex> lock(mtx);
                for (auto& recipe : recipes) {
                    recipe.issue_id = id++;
                    store_queue.push({TaskType::STORE, recipe,
                                      std::chrono::steady_clock::now()});
                }
                store_cv.notify_all();
            }
        }
    }
}

void store_stage() {
    const std::string connection_string =
        "dbname=test user=postgres password=secret host=localhost port=5432";
    // pqxx::connection conn(connection_string);
    // if (!conn.is_open()) {
    //   throw std::runtime_error("Не удалось подключиться к базе данных
    //   PostgreSQL");
    // }
    // pqxx::work txn(conn);

    // while (true) {
    //   Task task;
    //   {
    //     std::unique_lock<std::mutex> lock(mtx);
    //     while (!storing_done && store_queue.empty()) {
    //       store_cv.wait(lock);
    //     }

    //     task = store_queue.front();
    //     store_queue.pop();
    //     if (extracting_done && store_queue.empty()) {
    //       storing_done = true;
    //       store_cv.notify_all();
    //     }
    //   }

    //   if (auto recipe = std::get_if<Recipe>(&task.data)) {
    //     std::string query = R"(
    //           INSERT INTO recipes (issue_id, url, title, steps, image_url)
    //           VALUES ($1, $2, $3, $4, $5);
    //       )";
    //     txn.exec_params(query, recipe->issue_id != "" ? recipe->issue_id :
    //     "0", recipe->url,
    //                     recipe->title != "" ? recipe->title : "error", "",
    //                     recipe->image_url);

    //     txn.commit();
    //     std::cout << "Рецепт сохранен в PostgreSQL: " << recipe->title <<
    //     std::endl;
    //   }
    // }
}

int main() {
    std::cout << "Запуск программы..." << std::endl;
    if (!gumbo) {
        std::cout << "No such file or directory: \"gumbo.h\"" << std::endl;
    }
    // Создание потоков
    std::thread reader(read_stage);
    std::thread extractor(extract_stage);
    std::thread storer(store_stage);

    read_queue.push({TaskType::READ, "page_" + std::to_string(1) + ".html",
                     std::chrono::steady_clock::now()});
    read_cv.notify_one();
    {
        std::lock_guard<std::mutex> lock(mtx);
        reading_done = true;
        extract_cv.notify_all();
    }

    reader.join();
    extractor.join();
    storer.join();

    std::cout << "Программа завершена." << std::endl;
    return 0;
}
