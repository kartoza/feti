--Run the script by psql -d gis -U docker -p 6543 -h localhost -f feti.sql

---creating csv files

create table nqf (nqf_level integer ,nqf_desc character varying (255),nqf_cert character varying (255) ,nqf_link character varying (255));
COPY nqf FROM '/home/setup/nqf.csv' WITH (
   FORMAT csv,
   HEADER true
   );

   alter table nqf add Primary Key (nqf_level);

create table nated (nated_level character varying (255),nated_descrip character varying (255));
COPY nated FROM '/home/setup/nated.csv' WITH (
   FORMAT csv,
   HEADER true
   );
ALTER TABLE nated ADD COLUMN "id" SERIAL PRIMARY KEY;

create table ncv (ncv_level integer ,ncv_descrip  character varying (255));
COPY ncv FROM '/home/setup/ncv.csv' WITH (
   FORMAT csv,
   HEADER true
   );
 alter table ncv add Primary Key (ncv_level);

create table fos (fos_class integer ,fos_descrip character varying (255));
COPY fos FROM '/home/setup/fos.csv' WITH (
   FORMAT csv,
   HEADER true
   );

    alter table fos add Primary Key (fos_class);


create table etqa (etqa_acro character varying (255),etqa_full character varying (255),etqa_url character varying (255));
COPY etqa FROM '/home/setup/etqa.csv' WITH (
   FORMAT csv,
   HEADER true
   );

 ALTER TABLE etqa ADD COLUMN "id" SERIAL PRIMARY KEY;
alter table fet_sample_data add column nated_id serial;
alter table fet_sample_data add column nqf_id integer;

alter table fet_sample_data add column etqa_id integer;

UPDATE fet_sample_data SET etqa_id = s.id
FROM etqa AS s 
WHERE upper(fet_sample_data.etqa) = s.etqa_acro;

alter table fet_sample_data add column nqf_level_temp character varying (255);
update fet_sample_data set nqf_level_temp = nqf_level;

--preparing for inserts
update fet_sample_data set nqf_level_temp = substring(nqf_level_temp,5) where length(nqf_level_temp) = 5;
update fet_sample_data set nqf_level_temp =   replace (nqf_level_temp,'NQF Level', '');
update fet_sample_data set nqf_level_temp =   replace (nqf_level_temp,'Level', '');
update fet_sample_data set nqf_level_temp =   replace (nqf_level_temp,' ','');
UPDATE fet_sample_data set nqf_level_temp = replace( nqf_level_temp, ' 0', '' ) WHERE nqf_level_temp LIKE ' 0%';


--Inserting values into database - use the sql to create the lookup tables
INSERT INTO feti_fieldofstudy(field_of_study_class, field_of_study_description) SELECT fos_class, fos_descrip FROM fos;

drop table fos;


INSERT INTO feti_educationtrainingqualityassurance( acronym, body_name, url)  SELECT etqa_acro, etqa_full, etqa_url FROM etqa;
Drop table etqa;

INSERT INTO feti_nationalgraduateschoolineducation( level, description) SELECT nated_level, nated_descrip FROM nated;
drop table nated;

INSERT INTO feti_nationalcertificatevocational( national_certificate_vocational_level, national_certificate_vocational_description) SELECT ncv_level, ncv_descrip  FROM ncv; 
drop table ncv;

INSERT INTO feti_nationalqualificationsframework(level, description, certification, link) SELECT nqf_level, nqf_desc, nqf_cert, nqf_link FROM nqf;
drop table nqf;


























