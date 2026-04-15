#include <iostream>
#include <fstream>
#include <unordered_set>
#include <queue>
#include <string>
#include <thread>
#include <vector>
#include <chrono>
#include <mutex>
#include <curl/curl.h>

class Scraper {
public:
    Scraper(const std::string& initialUrl, int maxPages)
        : initialUrl(initialUrl), maxDownloadPages(maxPages) {}

    void singleThreadedCrawl() {
        std::unordered_set<std::string> visited;
        std::queue<std::string> q;
        q.push(initialUrl);
        int pagesSaved = 0;

        while (pagesSaved < maxDownloadPages && !q.empty()) {
            std::string currentUrl = q.front();
            q.pop();

            if (visited.find(currentUrl) != visited.end()) {
                continue; 
            }

            std::string content = fetchPageContent(currentUrl);
            visited.insert(currentUrl);

            std::unordered_set<std::string> foundLinks;
            bool hasIngredientSection = extractLinks(content, foundLinks);

            if (hasIngredientSection) {
                writeToDisk(content, "data/page_" + std::to_string(pagesSaved + 1) + ".html");
                ++pagesSaved; 
            }

            for (const auto &link : foundLinks) {
                if (!visited.count(link)) {
                    q.push(link);
                }
            }
        }

    }

    void multiThreadedCrawl(int threadCount) {
        std::unordered_set<std::string> visited;
        std::vector<std::thread> threads;
        std::queue<std::string> q;
        q.push(initialUrl);
        int pagesSaved = 0;

        auto threadFunction = [&visited, &q, &pagesSaved, this]() {
            while (true) {
                std::string currentUrl;

                {
                    std::lock_guard<std::mutex> lock(mtx);
                    if (q.empty() || pagesSaved >= maxDownloadPages) {
                        return; 
                    }
                    currentUrl = q.front();
                    q.pop();
                }

                if (visited.count(currentUrl)) {
                    continue; 
                }

                std::string content = fetchPageContent(currentUrl);

                {
                    std::lock_guard<std::mutex> lock(mtx);
                    visited.insert(currentUrl);

                    std::unordered_set<std::string> foundLinks;
                    bool hasIngredientSection = extractLinks(content, foundLinks);

                    if (hasIngredientSection) {
                        writeToDisk(content, "data/page_" + std::to_string(pagesSaved + 1) + ".html");
                        ++pagesSaved;
                    }

                    for (const auto &link : foundLinks) {
                        if (!visited.count(link)) {
                            q.push(link);
                        }
                    }
                }
            }
        };

        for (int i = 0; i < threadCount; ++i) {
            threads.emplace_back(threadFunction);
        }

        for (auto &thread : threads) {
            thread.join();
        }
    }

    class UrlInitializationError : public std::exception {};

private:
    std::string initialUrl;
    int maxDownloadPages;
    std::mutex mtx;
    static const size_t TEMPLATE_SIZE;

    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
        (reinterpret_cast<std::string *>(userp))->append((char*)contents, size * nmemb);
        return size * nmemb;
    }

    static std::string fetchPageContent(const std::string& url) {
        CURL* curl = curl_easy_init();
        std::string readBuffer;

        if (!curl) {
            std::cerr << "Ошибка инициализации cURL." << std::endl;
            throw UrlInitializationError();
        }

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L); 
        curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 5L); 
        CURLcode res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "Ошибка при выполнении запроса: " << curl_easy_strerror(res) << std::endl;
            curl_easy_cleanup(curl);
            throw UrlInitializationError();
        }

        curl_easy_cleanup(curl);
        return readBuffer;
    }

    bool extractLinks(const std::string& content, std::unordered_set<std::string>& foundLinks) {
        size_t pos = 0;
        while ((pos = content.find("<a href=\"", pos)) != std::string::npos) {
            pos += 9; 
            size_t end_pos = content.find("\"", pos);
            if (end_pos == std::string::npos) {
                break;
            }
            std::string link = content.substr(pos, end_pos - pos);

            if (link.empty() || link == "#" || link == "javascript:void(0);" || 
                (!link.starts_with("http://") && !link.starts_with("https://"))) {
                pos = end_pos + 1; 
                continue;
            }

            if (link.starts_with("/")) {
                link = "https://eda.menu" + link; 
            }

            foundLinks.insert(link);
            pos = end_pos + 1; 
        }
        return content.find("ingredient") != std::string::npos; 
    }

    void writeToDisk(const std::string& content, const std::string& filename) {
        std::ofstream outfout(filename);
        outfout << content;
        outfout.close();
    }
};

const size_t Scraper::TEMPLATE_SIZE = 9;

void performThreadTests(const std::string &initialUrl, int maxPages) {
    Scraper webScraper(initialUrl, maxPages);
    
    std::ofstream resultsFile("results.csv");
    if (!resultsFile.is_open()) {
        std::cerr << "Ошибка при открытии файла results.csv для записи!" << std::endl;
        return; 
    }
    resultsFile << "Threads,MaxPages,ElapsedTime\n";

    for (int threads = 1; threads <= 256; threads *= 2) {
        std::chrono::duration<double> elapsedTime = std::chrono::duration<double>::zero();
        for (int i = 0; i < 20; i++) {
            auto start = std::chrono::high_resolution_clock::now();
            if (threads == 1) {
                webScraper.singleThreadedCrawl();
            } else {
                webScraper.multiThreadedCrawl(threads);
            }
            auto end = std::chrono::high_resolution_clock::now();
            elapsedTime += end - start;
            system("rm data/*.html");
        }
        double averageTime = elapsedTime.count() / 20.0;
        
        resultsFile << threads << "," << maxPages << "," << averageTime << "\n";
    }

    resultsFile.close();
}

int main(int argc, char** argv) {
    std::string initialUrl = "https://eda.menu"; 
    int maxPages = 10; 

    performThreadTests(initialUrl, maxPages);

    return 0;
}