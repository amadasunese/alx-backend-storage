-- A SQL script that creates a trigger that resets the attribute
--- valid_email only when the email has been changed.

DELIMITER //

CREATE TRIGGER reset_valid_email
AFTER UPDATE ON your_table
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        -- Reset the valid_email attribute to its default value
        SET NEW.valid_email = DEFAULT;
    END IF;
END;
//

DELIMITER ;
