SET FOREIGN_KEY_CHECKS=0; DROP TABLE Post; SET FOREIGN_KEY_CHECKS=1;
SET FOREIGN_KEY_CHECKS=0; DROP TABLE Usuarios; SET FOREIGN_KEY_CHECKS=1;
SET FOREIGN_KEY_CHECKS=0; DROP TABLE Passaros; SET FOREIGN_KEY_CHECKS=1;
drop table if exists Usuarios_Passaros;
drop table if exists Tag;
drop table if exists Mencionar;
drop table if exists Visualizado;
drop database if exists mydb;