CREATE OR REPLACE PROCEDURE upsert_contact(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_username) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE username = p_value OR phone = p_value;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_names TEXT[],
    IN p_phones TEXT[],
    INOUT invalid_data TEXT DEFAULT ''
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays p_names and p_phones must have the same length';
    END IF;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]{11}$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_names[i]) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE username = p_names[i];
            ELSE
                INSERT INTO phonebook(username, phone)
                VALUES (p_names[i], p_phones[i]);
            END IF;
        ELSE
            invalid_data := invalid_data || '(' || p_names[i] || ', ' || p_phones[i] || ') ';
        END IF;
    END LOOP;
END;
$$;