
--personal schedule 
SELECT class_id, room_number, class_type, start_time, end_time, trainer
FROM schedule 
WHERE 2 = ANY(members);

--trainer schedule
SELECT class_id, room_number, class_type, start_time, end_time, members
FROM schedule 
WHERE trainer=1;

-- register for class / insert member into schedule
INSERT INTO schedule (members) VALUES (ARRAY[2]);

ARRAY[false,false,false,false,false,false,false,false,false]
