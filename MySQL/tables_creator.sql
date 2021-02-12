drop tables Posts, Users;


create table Users (
    username varchar(30) primary key,
    followers int unsigned not null
);

create table Posts (
	insta_url varchar(11) not null unique primary key,
    date date not null,
	time time not null,
    likes int unsigned not null,
	popularity float not null,
    text varchar(2200),
    username varchar(30),
    
    constraint FK_username foreign key (username)
    references Users (username)
    on delete cascade
    on update cascade
);
