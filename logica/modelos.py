# logica/modelos.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuramos SQLite creará un archivo físico llamado 'tickets.db
URL_BASE_DATOS = "sqlite:///tickets.db"
engine = create_engine(URL_BASE_DATOS, echo=False)

# Clase base de la que heredarán nuestros modelos
Base = declarative_base()

# Definimos nuestra tabla como una clase de Python 
class TicketORM(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String, unique=True, nullable=False) # Para guardar el "Tik-01"
    problema = Column(String, nullable=False)
    prioridad = Column(String, nullable=False)
    comentarios = Column(String, nullable=True)
    fecha = Column(String, nullable=False)
    estado = Column(String, default="Pendiente")


Base.metadata.create_all(engine)

#'fábrica' de conexiones para poder guardar y leer datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)