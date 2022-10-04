create schema sania ;

use sania ;

create table fonctions(
	id_fonction TINYINT AUTO_INCREMENT ,
	libelle_fonction varchar(25),
	constraint pk_fonction primary key(id_fonction)
);

-- add fonctionnalite 

INSERT INTO fonctions(libelle_fonction)VALUES('admin'),('receptionniste'),('secretariat'),('dircab'),('dircaba'),('ministre'),('conseiller');

-- create table agents 

create table agents(
id_agent mediumint AUTO_INCREMENT primary key ,
nom_agent varchar(40),
email_agent varchar(50),
phone_agent varchar(15),
fonction tinyint ,
date_Enregistrement date default current_date(),
constraint fk_fonction foreign key(fonction) references fonctions(id_fonction) 
);

alter table agents add login_agent varchar(40) default 'sania' , add sexe_agent varchar(15);


-- default agent 

INSERT INTO agents(nom_agent,email_agent,phone_agent,fonction,login_agent,sexe_agent)VALUES('admin','admin@gmail.com','0995540211',1,'admin','masculin');

-- ajout de la fonction aider_

insert into fonctions(libelle_fonction)values('aider');

-- create table messages 

create table messages(
id_messages int auto_increment primary key ,
sujet varchar(100) , 
expediteurs int ,
destinataire int ,
descriptions longtext ,
pdf longtext ,
heures time default current_time(),
jours date default current_date(),
fonction_personne tinyint ,
agent_personne mediumint ,
constraint fk_fct foreign key(fonction_personne) references fonctions(id_fonction) on delete set null on update cascade ,
constraint fk_agt foreign key(agent_personne) references agents(id_agent) on delete set null on update cascade);