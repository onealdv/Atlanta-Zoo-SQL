use ZooAtl;

insert into user values ('martha_johnson',MD5('password1'),'marthajohnson@hotmail.com','staff');
insert into user values ('benjamin_rao',MD5('password2'),'benjaminrao@gmail.com','staff');
insert into user values ('ethan_roswell',MD5('password3'),'ethanroswell@yahoo.com','staff');
insert into user values ('xavier_swenson',MD5('password4'),'xavierswenson@outlook.com','visitor');
insert into user values ('isabella_rodriguez',MD5('password5'),'isabellarodriguez@mail.com','visitor');
insert into user values ('nadias_tevens',MD5('password6'),'nadiastevens@gmail.com','visitor');
insert into user values ('robert_bernheardt',MD5('password7'),'robertbernheardt@yahoo.com','visitor');
insert into user values ('admin1', MD5('password8'), 'administrator@mail.com', 'admin');

insert into adminUser values ('admin1');

insert into staff values ('martha_johnson');
insert into staff values ('benjamin_rao');
insert into staff values ('ethan_roswell');

insert into visitor values ('xavier_swenson');
insert into visitor values ('isabella_rodriguez');
insert into visitor values ('nadias_tevens');
insert into visitor values ('robert_bernheardt');


insert into exhibit values('Pacific',true,'850');
insert into exhibit values('Jungle',false,'600');
insert into exhibit values('Sahara',false,'1000');
insert into exhibit values('Mountainous',false,'1200');
insert into exhibit values('Birds',true,'1000');


insert into animal values('Goldy','Goldfish','Fish',1,'Pacific');
insert into animal values('Nemo','Clownfish','Fish',2,'Pacific');
insert into animal values('Pedro','Poison Dart frog','Amphibian',3,'Jungle');
insert into animal values('Lincoln','Lion','Mammal',8,'Sahara');
insert into animal values('Greg','Goat','Mammal',6,'Mountainous');
insert into animal values('Brad','Bald Eagle','Bird',4,'Birds');




insert into show_ values('Jungle Cruise','10/07/2018 09:00 AM','martha_johnson','Jungle');
insert into show_ values('Feed the Fish','12/12/2018 12:00 PM','martha_johnson','Pacific');
insert into show_ values('Fun Facts','10/09/2018 03:00 PM','martha_johnson','Sahara');
insert into show_ values('Climbing','10/10/2018 04:00 AM','benjamin_rao','Mountainous');
insert into show_ values('Flight of the Birds','10/05/2018 03:00 AM','ethan_roswell','Birds');
insert into show_ values('Jungle Cruise','10/12/2018 02:00 PM','martha_johnson','Jungle');
insert into show_ values('Feed the Fish','10/11/2018 02:00 PM','ethan_roswell','Pacific');
insert into show_ values('Fun Facts','10/13/2018 01:00 AM','benjamin_rao','Sahara');
insert into show_ values('Climbing','10/13/2018 05:00 PM','benjamin_rao','Mountainous');
insert into show_ values('Flight of the Birds','10/14/2018 02:00 AM','ethan_roswell','Birds');
insert into show_ values('Bald Eagle Show','10/15/2018 02:00 PM','ethan_roswell','Birds');
