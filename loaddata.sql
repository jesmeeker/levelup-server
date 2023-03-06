SELECT *
FROM levelupapi_gametype;
SELECT *
FROM auth_user;
SELECT *
FROM authtoken_token;
SELECT *
FROM levelupapi_gamer;
UPDATE levelupapi_event
SET date_of_event = "2023-03-01"
WHERE id = 2;

SELECT e.id,
    e.date_of_event,
    e.start_time,
    g.name as game_name,
    u.first_name || ' ' || u.last_name as full_name
FROM levelupapi_event e
    JOIN levelupapi_game g ON e.game_id = g.id
    JOIN auth_user u ON gamer.user_id = u.id
    JOIN levelupapi_eventgamer eg ON e.id = eg.event_id
    JOIN levelupapi_gamer gamer ON eg.gamer_id = gamer.id

    SELECT 
                e.id as event_id,
                e.date_of_event,
                e.start_time,
                g.gamer_id,
                g.name as game_name,
                u.first_name || ' ' || u.last_name as full_name
            FROM levelupapi_event e
                JOIN levelupapi_game g ON e.game_id = g.id
                JOIN auth_user u ON gamer.user_id = u.id
                JOIN levelupapi_eventgamer eg ON e.id = eg.event_id
                JOIN levelupapi_gamer gamer ON eg.gamer_id = gamer.id