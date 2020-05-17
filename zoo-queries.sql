 use zooAtl;
#search exhibit by name
select exhibitName from exhibit;
select * from exhibit where exhibitName = "Birds";
#search exhibit by size
select * from exhibit where size between 500 and 900;
#search exhibit by number of animals
select * from exhibit join animal on animal.exhibitName = exhibit.exhibitName;
select animal.exhibitName, count(*) from exhibit join animal
    on animal.exhibitName = exhibit.exhibitName group by animal.exhibitName;
#search for exhibit by number of animals
select animal.exhibitName, count(*) from exhibit join animal
    on animal.exhibitName = exhibit.exhibitName group by animal.exhibitName;
#search fro exhibit by taking into account whether the exhibit has water feature
select exhibitName from exhibit where waterFeature = '1';
#search for animals by name
select animalName from animal;
select * from animal where animalName = "Brad";
#search for animals by speacies
select animalSpecies from animal;
select * from animal where animalSpecies = "Goat";
#search for animals by age
select * from animal where age between 1 and 2;
#search for animal by type
select type_ from animal;
select * from animal where type_ = "Fish";
#search by exhibit
select animal.exhibitName, waterFeature, size, count(*) from exhibit
    join animal on animal.exhibitName = exhibit.exhibitName
        group by animal.exhibitName;
#search visitors by email address
select * from user join visitor on user.username = visitor.username;
select * from user join visitor on user.username = visitor.username
    where user.email = 'isabellarodriguez@mail.com';
#view visitors by username
select username from visitor;
select * from visitor where username = "isabella_rodriguez";
#view staff by email
select * from user;
select * from user where role = 'staff' and email = 'benjaminrao@gmail.com';
#view staff by username
select username from staff;
select * from staff where username = "ethan_roswell";
#view shows by name
select showName from show_;
select * from show_ where showName = "Climbing";
#view shows by exhibit
select exhibitName from show_;
select * from show_ where exhibitName = "Birds";
#view shows by date
select dateAndTime from show_;
select * from show_ where dateAndTime = "10/15/2018 02:00 PM";
#view animals by name
select animalName from animal;
select * from animal where animalName = "Brad";
#view animals by species
select animalSpecies from animal;
select * from animal where animalSpecies = "Goat";
#view animals by age
select age from animal;
select * from animal where age = 4;
#view animals by type
select type_ from animal;
select * from animal where type_ = "mammal";
#view animals by exhibit
select exhibitName from animal;
select * from animal where exhibitName = "Pacific";
#insert to animal care
insert into animalcare(animalName, animalSpecies, username, dateAndTime,
    notetext) values ("Brad", "Bald Eagle", "benjamin_rao",
    "10/10/2018 04:00 PM", "insert note here");
select * from animalcare;
#insert name, exhibit, staff, date, time into show_
insert into show_(showName, dateAndTime, username, exhibitName) values
    ("AnimalKingdom", "10/10/2108 06:00 PM", "ethan_roswell", "Jungle");
#insert name, type, exhibit, species, age into animal
insert into animal(animalName, animalSpecies, type_, age, exhibitName) values
    ("KingCobra", "snake", "reptile", "3","Sahara");

#To get Num of Animals on  Exhibit
select a.exhibitName as "Exhibit Name", a.waterFeature as "Water Feature",
    a.size as "Size", b.Num_Animals as "Num Animals" from exhibit as a
        right join (select exhibitName, count(*) as Num_Animals from animal
            group by exhibitName) as B on a.exhibitName = b.exhibitName;

#To get Num of Animals on  Exhibit = "Pacific"
select a.exhibitName as "Exhibit Name", a.waterFeature as "Water Feature",
    a.size as "Size", b.Num_Animals as "Num Animals" from exhibit as a right
        join (select exhibitName, count(*) as Num_Animals from animal
            group by exhibitName)as B on a.exhibitName = b.exhibitName
                where a.exhibitName = 'Pacific';

#Gets the Number of Visits of a visitor to Exhibits
select a.exhibitNameas as "Exhibit Name", a.dateandtime as "Date", b.num
    as "Number of Visits" from exhibitvisitor as a right join
        (select exhibitName, count(*) as num from exhibitvisitor
            group by exhibitName) as b on a.exhibitName = b.exhibitName;

select a.exhibitNameas as "Exhibit Name", a.dateandtime as "Date", b.num
    as "Number of Visits" from exhibitvisitor as a right join
        (select exhibitName, count(*) as num from exhibitvisitor
            group by exhibitName) as b on a.exhibitName = b.exhibitName
                where a.username = 'visitor1';

#To get Show History Table
select a.username, a.showName,a.dateandtime, b.exhibitName from showvisitor
    as a left join  (select showName,exhibitName from show_) as b
        on a.showName = b.showName;
#To get Show History Table with matching username
select a.username, a.showName,a.dateandtime, b.exhibitName from showvisitor
    as a left join  (select showName,exhibitName from show_) as b
        on a.showName = b.showName where username = 'visitor1';
