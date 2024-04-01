-- COMP3005 
-- Final Project 
-- Version 2
-- Team 19
-- Tanisi Das 101216265
-- Ashley Fong 101226835
-- 10 April 2024 

CREATE TABLE members (
    member_id SERIAL Primary Key, 
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL, 
    weight_goal INT, 
    time_goal INT, 
    weight INT,
    height INT,
    payment_date DATE
);

CREATE TABLE trainers (
    trainer_id SERIAL Primary Key,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL, 
    class_type VARCHAR(20) NOT NULL,
    available BOOLEAN[]
);

CREATE TABLE admin_staff (
    admin_id SERIAL Primary Key,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL
);

CREATE TABLE rooms (
    number SERIAL Primary Key,
    times BOOLEAN[]
    -- available BOOLEAN NOT NULL
);

CREATE TABLE schedule (
    class_id SERIAL Primary Key,
    room_number INT NOT NULL,
    class_type VARCHAR(20) NOT NULL, 
    start_time TIME,
    end_time TIME,
    trainer INT NOT NULL, 
    members INT[],
    Foreign Key (trainer) References trainers(trainer_id),
    Foreign Key (room_number) References rooms(number)
);

CREATE TABLE equipment (
    equipment_id SERIAL Primary Key,
    type VARCHAR(20),
    quantity INT,
    class_id INT,
    Foreign Key (class_id) References schedule(class_id)
);
