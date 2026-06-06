SELECT MAX(weather_end)
FROM bronze.open_meteo_metadata
WHERE station_code = ? AND success = TRUE