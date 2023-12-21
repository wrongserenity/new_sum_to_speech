CREATE TABLE IF NOT EXISTS parsed_url(
    url_id serial primary key,
    url varchar(300) unique not null,
    text text,
    path_to_audio varchar(300),
    article_date date,
    path_to_img varchar(300)
);