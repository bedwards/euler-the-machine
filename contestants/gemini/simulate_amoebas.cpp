#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>

// Pack x, y, z into a single integer.
using Config = std::vector<uint16_t>;

uint16_t pack(int x, int y, int z) {
    return (uint16_t)((x << 10) | (y << 5) | z);
}

std::tuple<int, int, int> unpack(uint16_t p) {
    return {(p >> 10) & 0x1F, (p >> 5) & 0x1F, p & 0x1F};
}

int main() {
    // Current layer of configurations
    // Use vector of vectors.
    std::vector<Config> current_layer;
    current_layer.push_back({pack(0, 0, 0)});

    std::cout << "D(0) = 1" << std::endl;

    int max_n = 16; 

    for (int n = 1; n <= max_n; ++n) {
        std::vector<Config> next_layer;
        // Reserve memory? Hard to predict exact size, but maybe 3.4 * prev
        next_layer.reserve(current_layer.size() * 4);
        
        for (const auto& config : current_layer) {
            // For each amoeba in the config, try to divide it
            for (size_t i = 0; i < config.size(); ++i) {
                uint16_t p = config[i];
                auto [x, y, z] = unpack(p);
                
                uint16_t c1 = pack(x + 1, y, z);
                uint16_t c2 = pack(x, y + 1, z);
                uint16_t c3 = pack(x, y, z + 1);
                
                // Check if target cells are occupied in the CURRENT config
                bool occupied = false;
                for (uint16_t other : config) {
                    if (other == c1 || other == c2 || other == c3) {
                        occupied = true;
                        break;
                    }
                }
                
                if (!occupied) {
                    // Create new config
                    Config new_config = config;
                    // Remove current amoeba (swap with last and pop? No, order matters for canonical representation)
                    // The config must remain sorted for uniqueness check later?
                    // Actually, for next_layer unique check, we need canonical configs (sorted).
                    // So we remove 'p' and insert c1, c2, c3, then sort.
                    
                    new_config.erase(new_config.begin() + i);
                    new_config.push_back(c1);
                    new_config.push_back(c2);
                    new_config.push_back(c3);
                    
                    // Optimization: Use insertion sort or similar?
                    // Since mostly sorted, std::sort is fast.
                    std::sort(new_config.begin(), new_config.end());
                    
                    next_layer.push_back(std::move(new_config));
                }
            }
        }
        
        // Sort and unique the next_layer
        std::sort(next_layer.begin(), next_layer.end());
        next_layer.erase(std::unique(next_layer.begin(), next_layer.end()), next_layer.end());
        
        current_layer = std::move(next_layer);
        std::cout << "D(" << n << ") = " << current_layer.size() << std::endl;
    }

    return 0;
}