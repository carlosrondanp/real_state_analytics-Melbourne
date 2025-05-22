#Inicializar Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

docker ps                # contenedores corriendo
docker volume ls         # volúmenes creados

## Creamos los volumenes fijos
docker volume create bd_introds


## Creamos los contenedores (1 vez o cuando lo eliminamos)
# PostgreSQL
# version: https://hub.docker.com/_/postgres
docker run -d \
  --name postgres_db_introds \
  --restart=always \
  -e POSTGRES_USER=intro \
  -e POSTGRES_PASSWORD=data123 \
  -e POSTGRES_DB=bdintrods \
  -v bd_introds:/var/lib/postgresql/data \
  -p 5433:5432 \
  postgres:15


# | Parámetro          | Explicación                                                            |
# | ------------------ | ---------------------------------------------------------------------- |
# | `--name`           | Nombre único del contenedor                                            |
# | `--restart=always` | Hace que el contenedor se levante automáticamente al reiniciar Docker  |
# | `-e`               | Define variables de entorno (usuario, contraseña, nombre de BD, etc.)  |
# | `-v`               | Crea/monta un volumen Docker (datos persistentes en el disco del host) |
# | `-p`               | Mapea un puerto del contenedor al puerto del sistema anfitrión         |
# | `postgres:15`      | Imagen usada de Docker Hub (puedes cambiar la versión si lo necesitas) |

#docker stop postgres_db_introds      # Detiene el contenedor
#docker rm postgres_db_introds        # Elimina el contenedor (sin borrar datos)
#docker volume rm bd_introds      # Elimina los volumenes

# Eliminar todo
#docker rm -f postgres_db_introds && docker volume rm bd_introds

# Verificar eliminación
#docker ps -a

#Dbeaver
# | Campo         | Valor                                     |
# | ------------- | ----------------------------------------- |
# | Host          | `localhost`                               |
# | Puerto        | `5433`                                    |
# | Base de datos | `bdintrods`                                  |
# | Usuario       | `intro`                                   |
# | Contraseña    | `data123`                                |
# | Driver        | PostgreSQL (viene por defecto en DBeaver) |

### CARGAR DATOS Y PROBAR:
CREATE TABLE clientes (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  email VARCHAR(100),
  edad INTEGER,
  fecha_reg DATE
);
INSERT INTO clientes (nombre, email, edad, fecha_reg) VALUES
('Ana Pérez', 'ana@gmail.com', 28, '2024-06-12'),
('Luis Soto', 'luis@example.com', 35, '2024-05-30'),
('María León', 'maria@correo.com', 42, '2023-12-01'),
('Jorge Díaz', NULL, 30, '2025-01-15'),
('Lucía Torres', 'lucia.torres@gmail.com', NULL, CURRENT_DATE);
select *
  from clientes 


# Eliminar imagen: docker rmi <<IMAGE ID>>

# --restart=always hace que se levanten automáticamente si Docker arranca al encender tu PC.

# | Motor      | Host        | Puerto | Usuario | Contraseña  | DB Inicial |
# | ---------- | ----------- | ------ | ------- | ----------- | ---------- |
# | PostgreSQL | `localhost` | 5432   | `admin` | `admin123`  | `testdb`   |


##### REUSARL BD

# En caso reinicie la computadora, encendemos Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
docker info
docker ps
docker start postgres_db_introds
