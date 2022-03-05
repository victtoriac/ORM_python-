
from xmlrpc.client import DateTime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
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

    def __str__(self):
        return self.username

#session para establecer una relacion entre la conexion (engine) y los modelos
#podemos generar la cant de sesiones q quiero

Session=sessionmaker(engine)
session=Session()


if __name__=='__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    #genero instancia de mi clase user
    user1=User(username='User1',email='user1@example.com')
    user2=User(username='User2',email='user2@example.com')
    user3=User(username='User3',email='user3@example.com')

    session.add(user1)
    session.add(user2)
    session.add(user3)

    #ahora hacemos q se ejecuten y queden los cambios
    session.commit()

    #quiero el primero 
    # 1)METODO FIRST

    user=session.query(User).filter(
        User.id==1 
    ).first() #pq si dejo solo User.id==1 me da algo iterable y yo solo quiero el primer registro
    #si no existe el metodo first me retorna None

    if user:
        print(user)
    else:
        print('no existe el usuario en la db')

    
    # 2)METODO ONE , ESTE A DIF DEL FIRST SI NO EXISTE EN VEZ DE NONE LARGA EXCEPCION
    #osea q si lo uso tengo q implementar un try 

    try:
        user=session.query(User).filter(
            User.id==100
        ).one()

        print(user)
    
    except NoResultFound as err:
        print('el usuario no existe en la bd')

    
