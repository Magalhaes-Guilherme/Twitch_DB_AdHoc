# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Date, DateTime, ForeignKey, Integer, String,Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('categories_codigo_seq'::regclass)"))
    category_id = Column(String(13), nullable=False, unique=True)
    category_name = Column(String(80), nullable=False, unique=True)


class Usuario(Base):
    __tablename__ = 'usuarios'
    __table_args__ = (
        CheckConstraint("((broadcaster_type)::text = 'affiliate'::text) OR ((broadcaster_type)::text = 'partner'::text) OR ((broadcaster_type)::text = ''::text)"),
        CheckConstraint("((user_type)::text = 'admin'::text) OR ((user_type)::text = 'global mod'::text) OR ((user_type)::text = 'staff'::text) OR ((user_type)::text = ''::text)")
    )

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('usuarios_codigo_seq'::regclass)"))
    user_id = Column(String(13), nullable=False, unique=True)
    login = Column(String(30), nullable=False, unique=True)
    display_name = Column(String(30), nullable=False, unique=True)
    user_type = Column(String(10))
    broadcaster_type = Column(String(10))
    description = Column(Text)
    created_at = Column(Date)


class Canais(Base):
    __tablename__ = 'canais'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('canais_codigo_seq'::regclass)"))
    channel_id = Column(String(13), nullable=False, unique=True)
    broadcaster_name = Column(ForeignKey('usuarios.display_name'), nullable=False, unique=True)
    broadcaster_lang = Column(String(15))

    usuario = relationship('Usuario', uselist=False)


class Videos(Base):
    __tablename__ = 'videos'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('videos_codigo_seq'::regclass)"))
    video_id = Column(String(13), nullable=False, unique=True)
    user_id = Column(ForeignKey('usuarios.user_id'), nullable=False)
    title = Column(String(140), nullable=False)
    created_at = Column(DateTime)
    published_at = Column(DateTime)
    view_count = Column(Integer)
    video_language = Column(String(5))
    video_type = Column(String(15))
    duration = Column(String(10))

    user = relationship('Usuario')


class Streams(Base):
    __tablename__ = 'streams'

    codigo = Column(Integer, primary_key=True, server_default=text("nextval('streams_codigo_seq'::regclass)"))
    stream_id = Column(String(13), unique=True)
    broadcaster_name = Column(ForeignKey('canais.broadcaster_name'), nullable=False, unique=True)
    title = Column(String(140), nullable=False)
    started_at = Column(Date)
    viewer_count = Column(Integer)
    stream_lang = Column(String(15))
    category_name = Column(ForeignKey('categories.category_name'))

    canai = relationship('Canais', uselist=False)
    category = relationship('Category')


t_relatorio_videos = Table(
    'relatorio_videos', metadata,
    Column('codigo', Integer),
    Column('video_id', String(13)),
    Column('user_id', String(13), ForeignKey('usuarios.user_id')),
    Column('title', String(140)),
    Column('created_at', DateTime),
    Column('published_at', DateTime),
    Column('view_count', Integer),
    Column('video_language', String(5)),
    Column('video_type', String(15)),
    Column('duration', String(10)),
    schema='public'
)

v_relatorios_streams = Table(
    'v_relatorios_streams', metadata,
    Column('codigo', Integer),
    Column('stream_id', String(13), unique=True),
    Column('broadcaster_name', String(30), ForeignKey('canais.broadcaster_name'), nullable=False),
    Column('title', String(140), nullable=False),
    Column('started_at', Date),
    Column('viewer_count', Integer),
    Column('stream_lang', String(15)),
    Column('category_name', String(80), ForeignKey('categories.category_name')),
    schema='public'
)

t_relatorios_canais = Table(
    'relatorios_canais', metadata,
    Column('codigo', Integer, primary_key=True),
    Column('channel_id', String(13), nullable=False, unique=True),
    Column('broadcaster_name', String(30), ForeignKey('usuarios.display_name'), nullable=False, unique=True),
    Column('broadcaster_lang', String(15)),
    schema='public'
)

t_relatorios_usuarios = Table(
    't_relatorios_usuarios', metadata,
    Column('codigo', Integer, primary_key=True),
    Column('user_id', String(13), nullable=False, unique=True),
    Column('login', String(30), nullable=False, unique=True),
    Column('display_name', String(30), nullable=False, unique=True),
    Column('user_type', String(10)),
    Column('broadcaster_type', String(10)),
    Column('description', Text),
    Column('created_at', Date),
    schema='public'
)

t_relatorios_categories = Table(
    'relatorios_categories', metadata,
    Column('codigo', Integer, primary_key=True),
    Column('category_id', String(13), nullable=False, unique=True),
    Column('category_name', String(80), nullable=False, unique=True),
    schema='public'
)