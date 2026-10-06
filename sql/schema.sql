PRAGMA foreign_keys = ON;
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE incidents (
 id INTEGER PRIMARY KEY,
 product_id INTEGER NOT NULL REFERENCES products(id),
 status TEXT NOT NULL CHECK(status IN ('OPEN','IN_PROGRESS','CLOSED')),
 priority TEXT NOT NULL CHECK(priority IN ('P1','P2','P3')),
 assignee TEXT,
 error_code INTEGER NOT NULL,
 created_at TEXT NOT NULL
);
INSERT INTO products VALUES (1,'FileQueue'),(2,'MailGateway'),(3,'AdminConsole');
INSERT INTO incidents VALUES
 (1,1,'OPEN','P1',NULL,500,'2026-10-01'),
 (2,1,'IN_PROGRESS','P2','engineer-a',422,'2026-10-02'),
 (3,2,'CLOSED','P2','engineer-b',401,'2026-10-01'),
 (4,2,'OPEN','P1','engineer-b',503,'2026-10-03'),
 (5,3,'OPEN','P3',NULL,404,'2026-10-04'),
 (6,1,'CLOSED','P3','engineer-a',400,'2026-09-29'),
 (7,3,'IN_PROGRESS','P2','engineer-c',500,'2026-10-04'),
 (8,2,'CLOSED','P1','engineer-b',503,'2026-09-28');
CREATE INDEX idx_incidents_status ON incidents(status);
