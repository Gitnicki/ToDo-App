USE todo;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    taskname VARCHAR(255) NOT NULL,
    taskstatus VARCHAR(255) DEFAULT 'open',
    taskcategory VARCHAR(255) NOT NULL
);
