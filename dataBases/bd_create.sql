-- Criar basedados
CREATE DATABASE [noname]

-- Criar tabela estufas
CREATE TABLE Stoves (
    id INT PRIMARY KEY IDENTITY,
    stove_number INT NOT NULL,
    active BIT NOT NULL,
);
