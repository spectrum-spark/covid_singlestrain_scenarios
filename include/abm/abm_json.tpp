#ifndef IBM_ABM_JSON_TPP
#define IBM_ABM_JSON_TPP
#include "nlohmann/json.hpp"
template <class T>
T getJsonValue(nlohmann::json& json, const std::string& key) {
  try {
    return static_cast<T>(json[key]);
  } catch (nlohmann::json::type_error& e) {
    throw std::runtime_error("Problem in json with key " + key + ":\n" + e.what());
  }
}
#endif