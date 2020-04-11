
CREATE TABLE IF NOT EXISTS vkuser
(
    id          SERIAL PRIMARY KEY,
    uid      	INTEGER,
    name     	VARCHAR(30),
    city        VARCHAR(50),
    timer       INTEGER
);

CREATE INDEX ON vkuser (uid);

