CREATE TABLE `wujun` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `code` varchar(32) NOT NULL,
    `title` varchar(256) DEFAULT NULL,
    `titleImage` varchar(256) DEFAULT NULL,
    `date` varchar(32) DEFAULT NULL,
    `likesCount` int(11) DEFAULT 0,
    `commentsCount` int(11) DEFAULT 0,
    `url` varchar(128) DEFAULT 0,
    `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
