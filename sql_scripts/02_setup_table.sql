USE todo;

CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    todoitem VARCHAR(255) NOT NULL,
    itemstatus VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);