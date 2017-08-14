CREATE TABLE `wujun` (
  `id` int(11) NOT NULL,
  `code` varchar(32) NOT NULL,
  `title` varchar(256) DEFAULT NULL,
  `titleImage` varchar(256) DEFAULT NULL,
  `date` varchar(32) DEFAULT NULL,
  `likesCount` int(11) DEFAULT '0',
  `commentsCount` int(11) DEFAULT '0',
  `url` varchar(128) DEFAULT '',
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime,
  PRIMARY KEY (`id`)
);

create trigger wujun_update
before update on wujun
for each row
begin
     update A set time = datetime('now','localtime') where id = old.id;
end;
