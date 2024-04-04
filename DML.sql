-- COMP3005 
-- Final Project 
-- Version 2
-- Team 19
-- Tanisi Das 101216265
-- Ashley Fong 101226835
-- 10 April 2024 

-- DML file

INSERT INTO members (first_name, last_name, payment_date) 
VALUES ('Ashley', 'Fong', '2024-09-01'),
        ('Tanisi', 'Das', '2024-07-01'),
        ('Lucy', 'Wang', '2025-01-01');

INSERT INTO trainers (first_name, last_name, class_type, available) 
VALUES ('Bob', 'Smith', 'Yoga', (ARRAY[FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE])), 
        ('Ana', 'Lee', 'Spinning', (ARRAY[TRUE,TRUE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE])),
        ('Allan', 'Cao', 'Weight Lifting', (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]));

INSERT INTO admin_staff (first_name, last_name) 
VALUES ('John', 'Smith'), 
        ('Lisa', 'Lee'),
        ('Vivian', 'Ngan');

INSERT INTO rooms (times) 
VALUES (ARRAY[FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]), 
        (ARRAY[TRUE,TRUE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]),
        (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]),
        (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]),
        (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]);

INSERT INTO schedule (room_number, class_type, start_time, end_time, trainer, members) 
VALUES (1, 'Yoga', '08:00:00', '09:00:00', 1, '{1,2}'),
        (2, 'Spinning', '010:00:00', '11:00:00', 2, '{2}');

INSERT INTO equipment (type, quantity, class_type)
VALUES ('Yoga mat', 10, 'Yoga'),
        ('Cycling shoes', 10, 'Spinning'),
        ('Weight rack', 5, 'Weight lifting');

INSERT INTO payment_history (first_name, last_name, payment_amount, payment_date)
VALUES ('Ashley', 'Fong', 800, '2023-09-01'),
        ('Tanisi', 'Das', 800, '2023-07-01'),
        ('Lucy', 'Wang', 800, '2024-01-01');