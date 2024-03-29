-- COMP3005 
-- Final Project 
-- Version 2
-- Team 19
-- Tanisi Das 101216265
-- Ashley Fong 101226835
-- 10 April 2024 

-- DML file

INSERT INTO members (first_name, last_name, payment_date) 
VALUES ('Ashley', 'Fong', '2023-09-01'), 
        ('Tanisi', 'Das', '2023-07-01');

INSERT INTO trainers (first_name, last_name, class_type, start_time, end_time) 
VALUES ('Bob', 'Smith', 'Yoga', '09:00:00', '13:00:00'), 
        ('Ana', 'Lee', 'Spinning','11:00:00', '17:00:00');

INSERT INTO admin_staff (first_name, last_name) 
VALUES ('John', 'Smith'), 
        ('Lisa', 'Lee');

INSERT INTO rooms (start_time, end_time, available) 
VALUES ('09:00:00', '17:00:00', TRUE), 
        ('08:00:00', '17:00:00', TRUE),
        ('08:00:00', '17:00:00', TRUE),
        ('08:00:00', '17:00:00', TRUE),
        ('08:00:00', '17:00:00', TRUE);

INSERT INTO schedule (room_number, class_type, start_time, end_time, trainer, members) 
VALUES (1, 'Yoga', '08:00:00', '09:00:00', 1, '{1,2}'),
        (2, 'Spinning', '08:00:00', '09:30:00', 2, '{2}');

INSERT INTO equipment (type, quantity, class_id) 
VALUES ('Yoga mat', 10, 1),
        ('Cycling shoes', 10, 1)
