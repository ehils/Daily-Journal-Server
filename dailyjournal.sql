CREATE TABLE `Entry` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    `date` DATE NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`    TEXT NOT NULL
);
DROP TABLE `Customer`

INSERT INTO `Mood` VALUES (null, 'happy');
INSERT INTO `Mood` VALUES (null, 'Sad');
INSERT INTO `Mood` VALUES (null, 'Angry');
INSERT INTO `Mood` VALUES (null, 'Ok');

INSERT INTO `Entry` VALUES (null, "Javascript", "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.", 1, "Wed Sep 15 2021 10:10:47 ");
INSERT INTO `Entry` VALUES (null, "Python", "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", 4, "Wed Sep 15 2021 10:11:33 ");
INSERT INTO `Entry` VALUES (null, "Python", "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", 3, "Wed Sep 15 2021 10:13:11 ");
INSERT INTO `Entry` VALUES (null, "Javascript", "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 3, "Wed Sep 15 2021 10:14:05 ");

CREATE TABLE `Tag` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `tag` TEXT NOT NULL
);
CREATE TABLE `entrytag` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `tag_id` INTEGER NOT NULL,
    `entry_id` INTEGER NOT NULL,
    FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`),
    FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`)
);

INSERT INTO `Tag` VALUES (null, 'Python');
INSERT INTO `Tag` VALUES (null, 'React.js');
INSERT INTO `Tag` VALUES (null, 'Javascript');

INSERT INTO `entrytag` VALUES (null, 3, 1);
INSERT INTO `entrytag` VALUES (null, 1, 2);
INSERT INTO `entrytag` VALUES (null, 1, 3);
INSERT INTO `entrytag` VALUES (null, 2, 4);
INSERT INTO `entrytag` VALUES (null, 2, 1);
INSERT INTO `entrytag` VALUES (null, 2, 2);
INSERT INTO `entrytag` VALUES (null, 2, 3);
INSERT INTO `entrytag` VALUES (null, 3, 4);

SELECT
    *
FROM Entry e  
JOIN Mood as m
    On m.id = e.mood_id 
JOIN entrytag as et
    On et.entry_id = e.id   
JOIN Tag as t
    On t.id = et.tag_id  
WHERE e.id = 12
ORDER BY e.id 