CREATE TABLE urls (
    "url" TEXT NOT NULL,
    "added" REAL NOT NULL,
    "status" TEXT
);

CREATE TABLE screenshots (
    "id" INTEGER PRIMARY KEY,
    "url" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "scheduled" REAL,
    "taken" REAL,
    "path" TEXT,
    "retries" INTEGER DEFAULT (0)
);
