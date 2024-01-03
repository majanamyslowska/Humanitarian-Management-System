from connectdb import *
def pop_db():
    with setup_conn() as conn:
        cursor = conn.cursor()
        
        insert_humanitarianplan = '''
            INSERT INTO humanitarianplan (planID, type, description, location, campNo, start_date, end_date)
            VALUES 
            (1, 'flood', 'Flood Relief Plan', 'Europe', 3, '2023-01-01', NULL),
            (2, 'fire', 'Fire Aid Plan', 'Asia', 3, '2023-12-11', NULL),
            (3, 'tsunami', 'Tsunami Response Plan', 'Africa', 3, '2023-02-01', NULL),
            (4, 'tsunami', 'Tsunami Response Plan', 'Africa', 3, '2023-02-01', NULL);
        '''

        insert_camps = '''
            INSERT INTO camps (campID, planID, country, city, capacity, totalRefugees, totalVolunteers, status, resourcesState, totalGF, totalDF, totalNN, totalVgn, totalVgt, totalOmn, totalSP, temperature, humidity, windSpeed, weatherDescription, weather)
            VALUES
            (1, 1, 'Spain', 'Madrid', 10, 3, 3, 'Active', 'Sufficient', 1, 0, 0, 0, 1, 1, 2, 12, 50, 7, 'Overcast', 'Sunny'),
            (2, 1, 'Spain', 'Madrid', 20, 3, 3, 'Active', 'Sufficient', 1, 0, 0, 1, 1, 0, 1 ,12, 67, 7, 'Overcast', 'Sunny'),
            (3, 1, 'Spain', 'Madrid', 5, 3, 3, 'Active', 'Sufficient', 1, 2, 0, 0, 0, 0, 2, 12, 80, 7, 'Overcast', 'Sunny'),
            (4, 2, 'Japan', 'Kyoto', 3, 3, 3, 'Active', 'Sufficient', 0, 0, 1, 1, 1, 0, 0, 18, 50, 3, 'Sunny', 'Sunny'),
            (5, 2, 'Japan', 'Kyoto', 10, 3, 3, 'Active', 'Sufficient', 0, 0, 0, 2, 1, 0, 2, 18, 90, 3, 'Sunny', 'Sunny'),
            (6, 2, 'Japan', 'Kyoto', 10, 3, 3, 'Active', 'Sufficient', 0, 0, 0, 2, 0, 1, 2, 18, 20, 3, 'Sunny', 'Sunny'),
            (7, 3, 'Nigeria', 'Lagos', 10, 3, 3, 'Active', 'Sufficient', 1, 0, 1, 0, 1, 0, 2, 32, 40, 4, 'Sunny', 'Sunny'),
            (8, 3, 'Nigeria', 'Lagos', 10, 3, 3, 'Active', 'Sufficient', 1, 1, 1, 0, 0, 0, 2, 32, 50, 4, 'Sunny', 'Sunny'),
            (9, 3, 'Nigeria', 'Lagos', 10, 3, 3, 'Active', 'Sufficient', 1, 0, 0, 0, 2, 0, 2, 32, 50, 4, 'Clouds', 'Cloudy'),
            (10, 4, 'Nigeria', 'Lagos', 10, 3, 3, 'Active', 'Sufficient', 1, 0, 0, 0, 2, 0, 2, 32, 50, 4, 'Clouds', 'Cloudy');
        '''

        insert_users = '''
            INSERT INTO users (userID, username, password, name, surname, phone, campID, availability, user_type, status)
            VALUES 
            (1, 'volunteer1', '111', 'Oliver', 'Smith', '+441234567890', 1, 'full-time', 'volunteer', 'active'),
            (2, 'volunteer2', '111', 'Emily', 'Johnson', '+441234567891', 1, 'part-time', 'volunteer', 'inactive'),
            (3, 'volunteer3', '111', 'Harry', 'Williams', '+441234567892', 1, 'full-time', 'volunteer', 'active'),
            (4, 'volunteer4', '111', 'Amelia', 'Brown', '+441234567893', 2, 'part-time', 'volunteer', 'active'),
            (5, 'volunteer5', '111', 'Jack', 'Jones', '+441234567894', 2, 'full-time', 'volunteer', 'active'),
            (6, 'volunteer6', '111', 'Isabella', 'Garcia', '+441234567895', 2, 'part-time', 'volunteer', 'active'),
            (7, 'volunteer7', '111', 'Jacob', 'Miller', '+441234567896', 3, 'full-time', 'volunteer', 'active'),
            (8, 'volunteer8', '111', 'Sophia', 'Davis', '+441234567897', 3, 'part-time', 'volunteer', 'active'),
            (9, 'volunteer9', '111', 'Charlie', 'Rodriguez', '+441234567898', 3, 'full-time', 'volunteer', 'active'),
            (10, 'volunteer10', '111', 'Mia', 'Martinez', '+441234567899', 4, 'part-time', 'volunteer', 'active'),
            (11, 'volunteer11', '111', 'Thomas', 'Hernandez', '+441234567800', 4, 'full-time', 'volunteer', 'active'),
            (12, 'volunteer12', '111', 'Ella', 'Lopez', '+441234567801', 4, 'part-time', 'volunteer', 'active'),
            (13, 'volunteer13', '111', 'George', 'Gonzalez', '+441234567802', 5, 'full-time', 'volunteer', 'active'),
            (14, 'volunteer14', '111', 'Grace', 'Wilson', '+441234567803', 5, 'part-time', 'volunteer', 'active'),
            (15, 'volunteer15', '111', 'Alfie', 'Anderson', '+441234567804', 5, 'full-time', 'volunteer', 'active'),
            (16, 'volunteer16', '111', 'Lily', 'Thomas', '+441234567805', 6, 'part-time', 'volunteer', 'active'),
            (17, 'volunteer17', '111', 'James', 'Taylor', '+441234567806', 6, 'full-time', 'volunteer', 'active'),
            (18, 'volunteer18', '111', 'Freya', 'Moore', '+441234567807', 6, 'part-time', 'volunteer', 'active'),
            (19, 'volunteer19', '111', 'Oscar', 'Jackson', '+441234567808', 7, 'full-time', 'volunteer', 'inactive'),
            (20, 'volunteer20', '111', 'Evie', 'Martin', '+441234567809', 7, 'part-time', 'volunteer', 'inactive'),
            (21, 'volunteer21', '111', 'William', 'Lee', '+441234567810', 7, 'full-time', 'volunteer', 'active'),
            (22, 'volunteer22', '111', 'Isabelle', 'Perez', '+441234567811', 8, 'part-time', 'volunteer', 'active'),
            (23, 'volunteer23', '111', 'Joshua', 'Thompson', '+441234567812', 8, 'full-time', 'volunteer', 'active'),
            (24, 'volunteer24', '111', 'Poppy', 'White', '+441234567813', 8, 'part-time', 'volunteer', 'active'),
            (25, 'volunteer25', '111', 'Ethan', 'Harris', '+441234567814', 9, 'full-time', 'volunteer', 'active'),
            (26, 'volunteer26', '111', 'Ava', 'Sanchez', '+441234567815', 9, 'part-time', 'volunteer', 'active'),
            (27, 'volunteer27', '111', 'Noah', 'Clark', '+441234567816', 9, 'full-time', 'volunteer', 'active');
        '''
        
        insert_refugee = '''
            INSERT INTO refugee (refugeeID, name, surname, age, campID, languages, gender, bloodType, psyHealth, physHealth, familyID, glutenFree, dairyFree, noNuts, vegan, vegetarian, omnivore, epipen, painRelief, bandages, sanitaryProducts)
            VALUES 
            (1, 'James', 'Brown', 28, 1, 'English', 'Male', 'O+', 'Good', 'Good', 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0),
            (2, 'Sophia', 'Wilson', 34, 1, 'German', 'Female', 'A-', 'Moderate', 'Good', 2, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1),
            (3, 'Oliver', 'Taylor', 22, 1, 'Italian', 'Male', 'B+', 'Good', 'Good', 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1),
            (4, 'Isabella', 'Evans', 29, 2, 'Portuguese', 'Female', 'AB-', 'Poor', 'Moderate', 2, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0),
            (5, 'Ethan', 'Davies', 26, 2, 'Swedish', 'Male', 'A+', 'Good', 'Good', 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1),
            (6, 'Amelia', 'Jones', 32, 2, 'Norwegian', 'Female', 'O-', 'Good', 'Good', 2, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1),
            (7, 'Harry', 'Johnson', 25, 3, 'Polish', 'Male', 'B-', 'Moderate', 'Moderate', 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0),
            (8, 'Lily', 'Walker', 30, 3, 'Hungarian', 'Female', 'AB+', 'Poor', 'Poor', 2, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1),
            (9, 'William', 'White', 27, 3, 'Latvian', 'Male', 'A-', 'Good', 'Good', 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0),
            (10, 'Ella', 'Roberts', 31, 4, 'Estonian', 'Female', 'O+', 'Moderate', 'Good', 2, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1),
            (11, 'Noah', 'Hall', 29, 4, 'Bulgarian', 'Male', 'B+', 'Good', 'Good', 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0),
            (12, 'Charlotte', 'Green', 23, 4, 'Slovenian', 'Female', 'A-', 'Moderate', 'Moderate', 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1),
            (13, 'Thomas', 'Edwards', 33, 5, 'Greek', 'Male', 'AB-', 'Poor', 'Poor', 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0),
            (14, 'Mia', 'Clark', 28, 5, 'Serbian', 'Female', 'O+', 'Good', 'Good', 2, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0),
            (15, 'Olivia', 'Harris', 24, 5, 'English', 'Female', 'A+', 'Good', 'Good', 5, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0),
            (16, 'Noah', 'Wilson', 26, 6, 'German', 'Male', 'O-', 'Moderate', 'Good', 6, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1),
            (17, 'Ella', 'Jones', 32, 6, 'Italian', 'Female', 'B+', 'Good', 'Good', 6, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1),
            (18, 'Jacob', 'Brown', 27, 6, 'Portuguese', 'Male', 'AB-', 'Poor', 'Moderate', 6, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0),
            (19, 'Lily', 'Davis', 29, 7, 'Swedish', 'Female', 'A+', 'Good', 'Good', 7, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1),
            (20, 'William', 'Evans', 30, 7, 'Finnish', 'Male', 'O+', 'Good', 'Good', 7, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1),
            (21, 'Sophia', 'Wilson', 28, 7, 'Polish', 'Female', 'AB+', 'Moderate', 'Moderate', 7, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0),
            (22, 'George', 'Taylor', 25, 8, 'Hungarian', 'Male', 'B-', 'Poor', 'Poor', 8, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1),
            (23, 'Charlotte', 'Thomas', 31, 8, 'Latvian', 'Female', 'A-', 'Good', 'Good', 8, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0),
            (24, 'Harry', 'Johnson', 27, 8, 'Bulgarian', 'Male', 'O+', 'Moderate', 'Good', 8, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1),
            (25, 'Mia', 'Roberts', 22, 9, 'English', 'Female', 'A+', 'Good', 'Good', 9, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0),
            (26, 'Ethan', 'Lewis', 28, 9, 'German', 'Male', 'O-', 'Moderate', 'Good', 9, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1),
            (27, 'Amelia', 'Walker', 22, 9, 'Italian', 'Female', 'B+', 'Good', 'Good', 9, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1);
            '''

        insert_ressourcesNew = '''
            INSERT INTO ressourcesNew (planID, newGF, newDairyFree, newNoNuts, newVegan, newVegetarian, newOmnivore, newEpipen, newPainRelief, newBandages, newSanitaryProducts, newCoughsyrup, newAllergyMedication, newIndigestion, newSkincream)
            VALUES 
            (1, 5, 5, 0, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5),
            (2, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100),
            (3, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100),
            (4, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100);
        '''
        
        insert_ressourcesOld = '''
            INSERT INTO ressourcesOld (campID, volunteerID, entryDate, glutenFree, dairyFree, noNuts, vegan, vegetarian, omnivore, epipen, painRelief, bandages, sanitaryProducts, coughsyrup, allergyMedication, indigestion, skincream)
            VALUES 
            (1, 1, '2023-11-01', 10, 0, 0, 0, 8, 9, 1, 2, 3, 4, 2, 2, 2, 2),
            (2, 4, '2023-11-02', 8, 4, 6, 5, 7, 10, 2, 3, 4, 5, 2, 2, 2, 2),
            (3, 7, '2023-11-03', 6, 3, 5, 4, 6, 11, 1, 2, 3, 4, 2, 2, 2, 2),
            (4, 10, '2023-11-04', 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21),
            (5, 13, '2023-11-05', 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70),
            (6, 16, '2023-11-06', 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70),
            (7, 19, '2023-11-07', 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70),
            (8, 22, '2023-11-08', 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70),
            (9, 25, '2023-11-09', 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70),
            (10, 25, '2023-11-09', 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70);
        '''

        insert_bookings = '''
            INSERT INTO bookings (bookingID, userID, bookingDate)
            VALUES 
            (NULL, 1, '2023-01-01'),
            (NULL, 2, '2023-01-02'),
            (NULL, 1, '2023-01-03'),
            (NULL, 3, '2023-01-04'),
            (NULL, 2, '2023-01-05');
        '''

        cursor.execute(f"SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        if count == 0:
            
            cursor.execute(insert_humanitarianplan)
            cursor.execute(insert_camps)
            cursor.execute(insert_users)
            cursor.execute(insert_refugee)
            cursor.execute(insert_ressourcesNew)
            cursor.execute(insert_ressourcesOld)
            cursor.execute(insert_bookings)
        else: 
            pass
        
# pop_db()
