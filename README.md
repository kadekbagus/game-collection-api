# ps4-games-api
PS4 games collection API made using Python Flask, this API is just small part of a bigger application.
This API just demonstrate CRUD funtionality.

### List APIs

API for Create/Add game data

`ps4-games/api/v1/create` METHOD: POST, Input: JSON

sample JSON input:
```
{
  "title":"Drive Club",
  "genre":"Racing",
  "developer":"Evolution Studios",
  "publisher":"Sony Computer Entertainment",
  "release_date":"2014-10-07",
  "image_link":"https://upload.wikimedia.org/wikipedia/en/thumb/6/6f/Driveclub_box_art.jpg/250px-Driveclub_box_art.jpg"
}
```

API for showing list games

`ps4-games/api/v1/list' METHOD: GET


API for showing single game data

`ps4-games/api/v1/detail/<integer:Id>` METHOD: POST


API for delete game data

`ps4-games/api/v1/delete/<integer:Id>` METHOD: DELETE


API for Update game data

`ps4-games/api/v1/update/<integer:Id>` METHOD: PUT, Input: JSON (format same as API create)




### Database table
this API is using MySQL database with one table called ps4_games for storing game data
such as title, genre, game developer, publisher, etc.
```
CREATE TABLE `ps4_games` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
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
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_title` (`id`,`title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

### How to setup
```
pip install Flask
pip install flask-mysqldb

for ubuntu:
sudo apt-get install python-dev
sudo apt-get install libmysqlclient-dev
```

### How to run
```
python app.py
```
