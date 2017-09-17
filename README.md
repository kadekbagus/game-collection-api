# ps4-games-api
PS4 games collection API made using Python Flask, this API is just small part of a bigger application.
This API just demonstrate CRUD funtionality.


### Database table
this API is using MySQL database with one table called ps4_games for storing game data
such as title, genre, game developer, publisher, etc.
```
CREATE TABLE `ps4_games` (
  `id` bigint(20) NOT NULL,
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

### How to Setup
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
