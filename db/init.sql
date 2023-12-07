CREATE TABLE IF NOT EXISTS parsed_url(
    url_id serial primary key,
    url varchar(300) unique not null,
    text text,
    path_to_audio varchar(300),
    article_date date
);

INSERT INTO parsed_url (url) VALUES ('test_url');