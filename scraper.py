import urllib.request
import urllib.parse
import json
def fetch_article(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles={title}&explaintext=1&format=json"
    req = urllib.request.Request(url, headers={"User-Agent" : "mini-rag",})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    #fichier_test = open("temp.json","w")
    #fichier_test.write(json.dumps(data, indent=2))
    #fichier_test.close()
    page = list(data["query"]["pages"].values())[0]
    extrait = page["extract"]
    return extrait 

if __name__ == "__main__":
    titles = [
      "Solar_panel", "Solar_energy", "Photovoltaics", "Solar_cell",
      "Renewable_energy", "Wind_power", "Nuclear_power", "Hydroelectricity",
      "Electricity", "Electric_battery", "Lithium-ion_battery",
      "Power_station", "Electrical_grid", "Energy_storage",
      "Photovoltaic_system", "Solar_inverter", "Net_metering",
      "Concentrated_solar_power", "Solar_thermal_energy",
      "Semiconductor", "Silicon", "Thin-film_solar_cell",
      "Perovskite_solar_cell", "Solar_tracker", "Maximum_power_point_tracking",
      "Greenhouse_gas", "Climate_change", "Carbon_footprint",
      "Energy_transition", "Fossil_fuel", "Natural_gas", "Coal",
      "Petroleum", "Geothermal_energy", "Biomass", "Tidal_power",
      "Wave_power", "Fuel_cell", "Hydrogen_economy",
      "Electric_vehicle", "Heat_pump", "Insulation",
      "Energy_efficiency", "Smart_grid", "Microgrid",
      "Transformer", "Alternating_current", "Direct_current",
      "Superconductivity", "Photon"
  ]
    for title in titles:
        article = open(f"data/{title}.txt", "w")
        article.write(fetch_article(title))
        article.close()

