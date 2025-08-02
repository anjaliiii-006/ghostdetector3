DROP TABLE IF EXISTS ghosts;

CREATE TABLE ghosts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  era TEXT NOT NULL,
  backstory TEXT NOT NULL,
  message TEXT NOT NULL,
  remedy TEXT, -- Added the remedy column
  discovered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
