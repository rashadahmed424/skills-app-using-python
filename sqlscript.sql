create database progress ;
use progress ;

CREATE USER 'test' IDENTIFIED BY 'test123';


create table user(
User_Name text ,
User_ID int(11)  primary key ,
email varchar(255) ,
Pass varchar(255) ,
Job_Profile text) ;



CREATE TABLE skills (
    Skill_Name TEXT,
    Progress INT(11),
    Start_Date DATE,
    End_Date DATE,
    Skill_Field TEXT,
    User_ID INT(11),
    FOREIGN KEY (User_ID) REFERENCES `user`(User_ID)
);


DELIMITER //
CREATE PROCEDURE InsertSkill(
    IN p_skill_name VARCHAR(255),
    IN p_progress INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_skill_field VARCHAR(255),
    IN p_user_id INT
)
BEGIN
    INSERT INTO skills (Skill_Name, Progress, Start_Date, End_Date, Skill_Field, User_ID)
    VALUES (p_skill_name, p_progress, p_start_date, p_end_date, p_skill_field, p_user_id);
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE UpdateSkill(
    IN p_old_skill_name VARCHAR(255),
    IN p_new_skill_name VARCHAR(255),
    IN p_progress INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_skill_field VARCHAR(255),
    IN p_user_id INT
)
BEGIN
    UPDATE skills
    SET Skill_Name = p_new_skill_name,
        Progress = p_progress,
        Start_Date = p_start_date,
        End_Date = p_end_date,
        Skill_Field = p_skill_field,
        User_ID = p_user_id
    WHERE Skill_Name = p_old_skill_name;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE DeleteSkill(
    IN p_skill_name VARCHAR(255)
)
BEGIN
    DELETE FROM skills
    WHERE Skill_Name = p_skill_name;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE InsertUser (
    IN p_username VARCHAR(255),
    IN p_user_id VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_job_profile VARCHAR(255)
)
BEGIN
    INSERT INTO user (User_Name, User_ID, email, Pass, Job_Profile)
    VALUES (p_username, p_user_id, p_email, p_password, p_job_profile);
END //

DELIMITER ;







