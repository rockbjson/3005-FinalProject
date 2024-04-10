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
        ('Lucy', 'Wang', '2025-01-01'), 
        ('Qing', 'Gan', '2025-04-08'),
        ('Niket', 'Rathod', '2024-07-20'),
        ('Erwin', 'Huang', '2025-05-30'),
        ('Edward', 'Kan', '2025-06-02'),
        ('Nicole', 'Maxey', '2025-03-17'),
        ('Clair', 'Alexander', '2024-07-20'),
        ('Alex', 'Bon', '2024-06-12');

INSERT INTO trainers (first_name, last_name, class_type, available) 
VALUES ('Bob', 'Smith', 'Yoga', (ARRAY[FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE])), 
        ('Ana', 'Lee', 'Spinning', (ARRAY[TRUE,TRUE,FALSE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE])),
        ('Allan', 'Cao', 'Weight Lifting', (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE])),
        ('Taylor', 'Swift', 'HIIT', (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,FALSE])),
        ('Justin', 'Bieber', 'Aerobics', (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,FALSE,TRUE,TRUE])),
        ('Miley', 'Cyrus', 'Pilates', (ARRAY[TRUE,TRUE,TRUE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE])),
        ('Dwayne', 'Johnson', 'Boxing', (ARRAY[TRUE,TRUE,FALSE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE])),
        ('Usain','Bolt','Running',(ARRAY[FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE,FALSE]));

INSERT INTO admin_staff (first_name, last_name) 
VALUES ('John', 'Smith'), 
        ('Lisa', 'Lee'),
        ('Vivian', 'Ngan');

INSERT INTO rooms (times) 
VALUES (ARRAY[FALSE,TRUE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE]), 
        (ARRAY[TRUE,TRUE,FALSE,TRUE,TRUE,TRUE,FALSE,TRUE,TRUE]),
        (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,FALSE]),
        (ARRAY[TRUE,TRUE,FALSE,FALSE,TRUE,TRUE,TRUE,TRUE,TRUE]),
        (ARRAY[TRUE,TRUE,TRUE,TRUE,TRUE,FALSE,FALSE,TRUE,TRUE]);

INSERT INTO schedule (room_number, class_type, start_time, end_time, trainer, members) 
VALUES (1, 'Yoga', '08:00:00', '09:00:00', 1, '{1,2}'),
        (2, 'Spinning', '10:00:00', '11:00:00', 2, '{9}'),
        (3, 'HIIT', '15:00:00', '17:00:00', 4, '{1,2,3,4,5,6,7,8,9,10}'),
        (1, 'Boxing', '10:00:00', '11:00:00', 7, '{2,4,6,7}'),
        (4, 'Pilates', '11:00:00', '12:00:00', 6, '{1,8}');

INSERT INTO equipment (type, quantity, class_type)
VALUES ('Yoga mat', 10, 'Yoga'),
        ('Cycling shoes', 10, 'Spinning'),
        ('Weight rack', 5, 'Weight lifting'),
        ('Dumbbells', 20, 'HIIT'),
        ('Yoga ball', 15, 'Pilates'),
        ('Boxing gloves', 12, 'Boxing');

INSERT INTO payment_history (first_name, last_name, payment_amount, payment_date)
VALUES ('Ashley', 'Fong', 800, '2023-09-01'),
        ('Tanisi', 'Das', 800, '2023-07-01'),
        ('Lucy', 'Wang', 800, '2024-01-01'),
        ('Qing', 'Gan', 800, '2024-04-08'),
        ('Niket', 'Rathod', 800, '2023-07-20'),
        ('Erwin', 'Huang', 800, '2024-05-30'),
        ('Erwin', 'Huang', 800, '2023-05-30'),
        ('Edward', 'Kan', 800, '2024-06-02'),
        ('Edward', 'Kan', 800, '2023-06-02'),
        ('Nicole', 'Maxey', 800, '2024-03-17'),
        ('Clair', 'Alexander', 800, '2023-07-20'),
        ('Alex', 'Bon', 800, '2023-06-12'),
        ('Alex', 'Bon', 80, '2024-04-06'),
        ('Lucy', 'Wang', 80, '2023-04-07'),
        ('Nicole', 'Maxey', 80, '2023-04-05');

INSERT INTO priv_sessions (room_number, class_type, start_time, end_time, trainer, member)
VALUES (5,'Aerobics','13:00:00', '15:00:00', 5, 10),
        (4,'Weight Lifting','10:00:00', '11:00:00', 3, 3),
        (2,'Boxing','14:00:00', '15:00:00', 7, 8);