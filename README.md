# ps4-games-api
PS4 games collection API made using Python Flask


## database table
```
CREATE TABLE `ps4_games` (
  `ps4_game_id` bigint(20) NOT NULL,
  `title` varchar(500) NOT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `exclusive` char(3) DEFAULT NULL,
  `developer` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `image_link` varchar(255) DEFAULT NULL,
  `release_date` date DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```