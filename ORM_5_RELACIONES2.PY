
from xmlrpc.client import DateTime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import ForeignKey
#declaro mi clase base asi la clase user puede ser tomada como modelo pq hereda de la base. 

engine=create_engine('postgresql://postgres:postgres@127.0.0.1/python_orm')
Base=declarative_base()

#cuando trabajo con objetos lo primero q hago es definir una clase q sera mi modelo.
# #para q una clase pueda considerarse un modelo debe heredarse de una clase base.  
class User(Base): 
    __tablename__='users'
    #ahora toca definir los atributos (columnas) de nuestra clase y definir su tipo de dato
    id=Column(Integer(),primary_key=True)
    username=Column(String(50),nullable=False,unique=True)
    email=Column(String(50),nullable=False,unique=True)
    created_at=Column(DateTime(),default=datetime.now())
    #mediante el atributo courses un usuario podra acceder a la relacion, es decir podra acceder a sus cursos
    
    #AHORA QUIERO ACCEDER AL USUARIO A PARTIR DE UN OBJETO DE TIPO CURSO 
    courses=relationship('Course',backref='user') #funcion para acceder a la relacion q recibe como argumento el nombre del modelo
                                                  #q poseer la llave foranea.
    #CON BACKREF= USER ESTOY INDICANDO QUE TODOS LOS OBJS DE TIPO CURSO POSEAN UN NUEVO ATRIBUTO (USER)
    #Y A PARTIR DE ESTE ATRIB PODRAN ACCEDER AL USUARIO

    def __str__(self):
        return self.username

#session para establecer una relacion entre la conexion (engine) y los modelos
#podemos generar la cant de sesiones q quiero

Session=sessionmaker(engine)
session=Session()

class Course(Base):
    __tablename__= 'courses'

    id=Column(Integer(),primary_key=True)
    title=Column(String(50),nullable=False)
    user_id=Column(ForeignKey('users.id'))
    created_at=Column(DateTime(),default=datetime.now())

    def __str__(self):
        return self.title


if __name__=='__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    #establezco relacion 1 a muchos entre mi modelo User y mi modelo Cursos
    #un usuario puede poseer multiples cursos y un curso le pertenece a un usuario

    user1=User(username='user1', email='user1@example.com')
    user2=User(username='user2', email='user2@example.com')

    

    session.add(user1)
    session.add(user2)
    

    session.commit()

    #creo el objeto de tipo curso
    course1=Course(title='Curso profesional de bd',user_id=user1.id)
    course2=Course(title='Curso profesional de bd 2',user_id=user1.id)
    course3=Course(title='Curso profesional de bd 3',user_id=user1.id)
    session.add(course1)
    session.add(course2)
    session.add(course3)
    session.commit()


    #itero sobre todos los cursos del usuario numero 1 
    #for course in user1.courses: #accedi al atributo q declare arriba courses con relationship
    #    print(course)

    print(course1.user)
    #tmb podria acceder a los atributos por ej print(course1.user.created_at)