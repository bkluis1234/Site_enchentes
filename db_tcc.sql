create database tcc_enchente;

use tcc_enchente;

create table ocorrencia(
	id int auto_increment primary key,
    tipo varchar(50) not null, /*Exemplo: Alagamento, bairro, cidade, e etc*/
    latitude decimal(10, 8) not null,
    longitude decimal(11, 8) not null,
    status enum('Em Verificação', 'Confirmado') default 'Em verificação',/*tajo de verificação*/
    data_criacao timestamp default current_timestamp,
    index idx_coordenadas (latitude, longitude)
);

select * from ocorrencia;

