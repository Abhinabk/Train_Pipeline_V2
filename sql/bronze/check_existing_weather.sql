SELECT * from  bronze.open_meteo_metadata
WHERE station_code = ?
and success = True
and run_date::DATE = ?
