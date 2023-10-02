CREATE PROCEDURE `sp_add_artist` (
in_name varchar(100)
)
BEGIN
IF NOT EXISTS (select name from music_artists where name = in_name) THEN
	INSERT INTO music_artists(name) values (in_name);
END IF;
END

CREATE DEFINER=`pa_web`@`%` PROCEDURE `sp_add_title`(
in_name varchar(100)
)
BEGIN
IF NOT EXISTS (select name from music_titles where name = in_name) THEN
	INSERT INTO music_titles(name) values (in_name);
END IF;
END

CREATE DEFINER=`pa_web`@`%` PROCEDURE `sp_add_album`(
in_name varchar(100)
)
BEGIN
IF NOT EXISTS (select name from music_albums where name = in_name) THEN
	INSERT INTO music_albums(name) values (in_name);
END IF;
END

CREATE DEFINER=`pa_web`@`%` PROCEDURE `sp_add_path`(
in_name varchar(400)
)
BEGIN
IF NOT EXISTS (select name from music_paths where name = in_name) THEN
	INSERT INTO music_paths(name) values (in_name);
END IF;
END

CREATE DEFINER=`pa_web`@`%` PROCEDURE `sp_add_filename`(
in_name varchar(400)
)
BEGIN
IF NOT EXISTS (select name from music_filenames where name = in_name) THEN
	INSERT INTO music_filenames(name) values (in_name);
END IF;
END

