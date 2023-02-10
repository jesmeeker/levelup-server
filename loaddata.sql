SELECT * FROM levelupapi_gametype;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;

UPDATE levelupapi_event
SET date_of_event = "2023-03-01"
WHERE id = 2;