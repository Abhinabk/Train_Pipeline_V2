SELECT train_no,file_path
FROM bronze.train_metadata
WHERE success = True and run_date::date = ?