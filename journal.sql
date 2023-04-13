CREATE TABLE `Journal_Entries`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    FOREIGN KEY (`mood_id`) REFERENCES `moods`(`id`)
);
CREATE TABLE `Moods`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);
CREATE TABLE `Tags`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `subject` TEXT NOT NULL
);
CREATE TABLE `Entry_Tags`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
FOREIGN KEY(`entry_id`) REFERENCES `Journal__Entries`(`id`),
FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)

);

INSERT INTO `Journal_Entries` VALUES (null, 'Javascript', "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.", 1);
INSERT INTO `Journal_Entries` VALUES (null, 'Python', "This is a python entry", 3);
INSERT INTO `Journal_Entries` VALUES (null, 'Tailwind', "hello my name is poppy.", 2);
INSERT INTO `Journal_Entries` VALUES (null, 'Javascript', "this is another entry", 2);
INSERT INTO `Journal_Entries` VALUES (null, 'Python', "his is a python entry", 4);

INSERT INTO `Moods` VALUES (null, "Happy");
INSERT INTO `Moods` VALUES (null, "Sad");
INSERT INTO `Moods` VALUES (null, "Angry");
INSERT INTO `Moods` VALUES (null, "Meh");

INSERT INTO `Tags` VALUES (null, "components");
INSERT INTO `Tags` VALUES (null, "modals");
INSERT INTO `Tags` VALUES (null, "parent-child");
INSERT INTO `Tags` VALUES (null, "enumerating");

INSERT INTO `Entry_Tags` VALUES (null, 1, 1);
INSERT INTO `Entry_Tags` VALUES (null, 2, 2);
INSERT INTO `Entry_Tags` VALUES (null, 3, 2);
INSERT INTO `Entry_Tags` VALUES (null, 4, 1);
INSERT INTO `Entry_Tags` VALUES (null, 5, 4);

   SELECT DISTINCT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            m.label,
           (SELECT GROUP_CONCAT(t.id) 
           FROM Entry_Tags e JOIN Tags t ON e.tag_id = t.id WHERE e.entry_id = a.id ) AS Tags
        
        FROM Journal_Entries a
        JOIN Moods m ON m.id = a.mood_id
        LEFT JOIN Entry_Tags e ON a.id = e.entry_id
        JOIN Tags t ON e.tag_id = t.id