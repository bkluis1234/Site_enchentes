create database if not exists site_enchentes;

USE site_enchentes;

DROP TABLE IF EXISTS ocorrencia;

CREATE TABLE ocorrencia (
    id int auto_increment primary key,
    tipo varchar(50) not null,
    descricao text not null,
    bairro varchar(100) not null,
    latitude decimal(10, 8) not null,
    longitude decimal(11, 8) not null,
    status enum('Em Verificação', 'Confirmado') default 'Em Verificação',
    data_criacao timestamp default current_timestamp,
    index idx_coordenadas (latitude, longitude)
);

INSERT INTO ocorrencia (tipo, descricao, bairro, latitude, longitude) 
VALUES ('Alagamento', 'Água acumulada na via principal', 'Centro', -23.550520, -46.633308);

SELECT * FROM ocorrencia;

DROP DATABASE tcc_enchente;