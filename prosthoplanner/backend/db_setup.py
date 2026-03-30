import pymysql

def create_database():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS prosthoplanner")
        print("Database 'prosthoplanner' verified/created.")
        
        conn.select_db("prosthoplanner")
        
        # Define tables
        tables = {}
        
        tables['users'] = (
            "CREATE TABLE IF NOT EXISTS `users` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `full_name` varchar(100) NOT NULL,"
            "  `email` varchar(100) NOT NULL,"
            "  `mobile_number` varchar(20) NOT NULL,"
            "  `password_hash` varchar(255) NOT NULL,"
            "  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,"
            "  PRIMARY KEY (`id`),"
            "  UNIQUE KEY (`email`)"
            ") ENGINE=InnoDB"
        )

        tables['patients'] = (
            "CREATE TABLE IF NOT EXISTS `patients` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `patient_external_id` varchar(50) DEFAULT NULL,"
            "  `full_name` varchar(100) NOT NULL,"
            "  `age` int(11) NOT NULL,"
            "  `gender` varchar(20) NOT NULL,"
            "  `mobile_number` varchar(20) DEFAULT NULL,"
            "  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,"
            "  PRIMARY KEY (`id`),"
            "  UNIQUE KEY (`patient_external_id`)"
            ") ENGINE=InnoDB"
        )
        
        tables['medical_history'] = (
            "CREATE TABLE IF NOT EXISTS `medical_history` ("
            "  `patient_id` int(11) NOT NULL,"
            "  `is_diabetic` boolean DEFAULT 0,"
            "  `has_hypertension` boolean DEFAULT 0,"
            "  `has_thyroid` boolean DEFAULT 0,"
            "  `has_asthma` boolean DEFAULT 0,"
            "  `is_smoker` boolean DEFAULT 0,"
            "  `drinks_alcohol` boolean DEFAULT 0,"
            "  `allergies` text,"
            "  `medications` text,"
            "  FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE"
            ") ENGINE=InnoDB"
        )
        
        tables['clinical_examinations'] = (
            "CREATE TABLE IF NOT EXISTS `clinical_examinations` ("
            "  `patient_id` int(11) NOT NULL,"
            "  `edentulous_area` varchar(100),"
            "  `kennedy_classification` varchar(50),"
            "  `tissue_condition` varchar(50),"
            "  `occlusion_type` varchar(50),"
            "  `clinical_notes` text,"
            "  FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE"
            ") ENGINE=InnoDB"
        )
        
        tables['treatment_suggestions'] = (
            "CREATE TABLE IF NOT EXISTS `treatment_suggestions` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `patient_id` int(11) NOT NULL,"
            "  `plan_a_treatment` varchar(255) NOT NULL,"
            "  `plan_a_cost` decimal(10,2),"
            "  `plan_a_time` varchar(100),"
            "  `plan_b_treatment` varchar(255) NOT NULL,"
            "  `plan_b_cost` decimal(10,2),"
            "  `plan_b_time` varchar(100),"
            "  `plan_c_treatment` varchar(255) NOT NULL,"
            "  `plan_c_cost` decimal(10,2),"
            "  `plan_c_time` varchar(100),"
            "  `selected_plan` enum('A', 'B', 'C') DEFAULT NULL,"
            "  `generated_at` timestamp DEFAULT CURRENT_TIMESTAMP,"
            "  PRIMARY KEY (`id`),"
            "  FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE"
            ") ENGINE=InnoDB"
        )

        tables['patient_imaging'] = (
            "CREATE TABLE IF NOT EXISTS `patient_imaging` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `patient_id` int(11) NOT NULL,"
            "  `image_type` enum('OPG', 'CBCT', 'INTRAORAL') NOT NULL,"
            "  `file_path` varchar(255) NOT NULL,"
            "  `vision_analysis_json` text,"
            "  `uploaded_at` timestamp DEFAULT CURRENT_TIMESTAMP,"
            "  PRIMARY KEY (`id`),"
            "  FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE"
            ") ENGINE=InnoDB"
        )
        
        for name, ddl in tables.items():
            print(f"Creating table {name}: ", end='')
            try:
                cursor.execute(ddl)
                print("OK")
            except Exception as err:
                print(str(err))
            
        cursor.close()
        conn.close()
        
    except Exception as err:
        print(f"Error initializing database: {err}")

if __name__ == "__main__":
    create_database()
