# coding: utf-8
from sqlalchemy import (
    ARRAY,
    Boolean,
    CHAR,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    Numeric,
    SmallInteger,
    Table,
    Text,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Actor(Base):
    __tablename__ = "actor"

    actor_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('actor_actor_id_seq'::regclass)"),
    )
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False, index=True)
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    def __repr__(self):
        return f"Actor - {self.actor_id} - {self.first_name}"


t_actor_info = Table(
    "actor_info",
    metadata,
    Column("actor_id", Integer),
    Column("first_name", Text),
    Column("last_name", Text),
    Column("film_info", Text),
)


class Category(Base):
    __tablename__ = "category"

    category_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('category_category_id_seq'::regclass)"),
    )
    name = Column(Text, nullable=False)
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))


class Country(Base):
    __tablename__ = "country"

    country_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('country_country_id_seq'::regclass)"),
    )
    country = Column(Text, nullable=False)
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))


t_customer_list = Table(
    "customer_list",
    metadata,
    Column("id", Integer),
    Column("name", Text),
    Column("address", Text),
    Column("zip code", Text),
    Column("phone", Text),
    Column("city", Text),
    Column("country", Text),
    Column("notes", Text),
    Column("sid", Integer),
)


t_film_list = Table(
    "film_list",
    metadata,
    Column("fid", Integer),
    Column("title", Text),
    Column("description", Text),
    Column("category", Text),
    Column("price", Numeric(4, 2)),
    Column("length", SmallInteger),
    Column("rating", Enum("G", "PG", "PG-13", "R", "NC-17", name="mpaa_rating")),
    Column("actors", Text),
)


class Language(Base):
    __tablename__ = "language"

    language_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('language_language_id_seq'::regclass)"),
    )
    name = Column(CHAR(20), nullable=False)
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))


t_nicer_but_slower_film_list = Table(
    "nicer_but_slower_film_list",
    metadata,
    Column("fid", Integer),
    Column("title", Text),
    Column("description", Text),
    Column("category", Text),
    Column("price", Numeric(4, 2)),
    Column("length", SmallInteger),
    Column("rating", Enum("G", "PG", "PG-13", "R", "NC-17", name="mpaa_rating")),
    Column("actors", Text),
)


t_payment = Table(
    "payment",
    metadata,
    Column(
        "payment_id",
        Integer,
        nullable=False,
        server_default=text("nextval('payment_payment_id_seq'::regclass)"),
    ),
    Column("customer_id", Integer, nullable=False, index=True),
    Column("staff_id", Integer, nullable=False, index=True),
    Column("rental_id", Integer, nullable=False),
    Column("amount", Numeric(5, 2), nullable=False),
    Column("payment_date", DateTime(True), nullable=False),
)


t_sales_by_film_category = Table(
    "sales_by_film_category",
    metadata,
    Column("category", Text),
    Column("total_sales", Numeric),
)


t_sales_by_store = Table(
    "sales_by_store",
    metadata,
    Column("store", Text),
    Column("manager", Text),
    Column("total_sales", Numeric),
)


t_staff_list = Table(
    "staff_list",
    metadata,
    Column("id", Integer),
    Column("name", Text),
    Column("address", Text),
    Column("zip code", Text),
    Column("phone", Text),
    Column("city", Text),
    Column("country", Text),
    Column("sid", Integer),
)


class City(Base):
    __tablename__ = "city"

    city_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('city_city_id_seq'::regclass)"),
    )
    city = Column(Text, nullable=False)
    country_id = Column(
        ForeignKey("country.country_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    country = relationship("Country")


class Film(Base):
    __tablename__ = "film"

    film_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('film_film_id_seq'::regclass)"),
    )
    title = Column(Text, nullable=False, index=True)
    description = Column(Text)
    release_year = Column(Integer)
    language_id = Column(
        ForeignKey("language.language_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    original_language_id = Column(
        ForeignKey("language.language_id", ondelete="RESTRICT", onupdate="CASCADE"),
        index=True,
    )
    rental_duration = Column(SmallInteger, nullable=False, server_default=text("3"))
    rental_rate = Column(Numeric(4, 2), nullable=False, server_default=text("4.99"))
    length = Column(SmallInteger)
    replacement_cost = Column(
        Numeric(5, 2), nullable=False, server_default=text("19.99")
    )
    rating = Column(
        Enum("G", "PG", "PG-13", "R", "NC-17", name="mpaa_rating"),
        server_default=text("'G'::mpaa_rating"),
    )
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))
    special_features = Column(ARRAY(Text()))
    fulltext = Column(TSVECTOR, nullable=False, index=True)

    language = relationship(
        "Language", primaryjoin="Film.language_id == Language.language_id"
    )
    original_language = relationship(
        "Language", primaryjoin="Film.original_language_id == Language.language_id"
    )

    def __repr__(self):
        return f"Film - {self.film_id} - {self.title}"


class Addres(Base):
    __tablename__ = "address"

    address_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('address_address_id_seq'::regclass)"),
    )
    address = Column(Text, nullable=False)
    address2 = Column(Text)
    district = Column(Text, nullable=False)
    city_id = Column(
        ForeignKey("city.city_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    postal_code = Column(Text)
    phone = Column(Text, nullable=False)
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    city = relationship("City")


class FilmActor(Base):
    __tablename__ = "film_actor"

    actor_id = Column(
        ForeignKey("actor.actor_id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    film_id = Column(
        ForeignKey("film.film_id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    actor = relationship("Actor")
    film = relationship("Film")


class FilmCategory(Base):
    __tablename__ = "film_category"

    film_id = Column(
        ForeignKey("film.film_id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    category_id = Column(
        ForeignKey("category.category_id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    category = relationship("Category")
    film = relationship("Film")


class Store(Base):
    __tablename__ = "store"

    store_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('store_store_id_seq'::regclass)"),
    )
    manager_staff_id = Column(Integer, nullable=False, unique=True)
    address_id = Column(
        ForeignKey("address.address_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    address = relationship("Addres")


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('customer_customer_id_seq'::regclass)"),
    )
    store_id = Column(
        ForeignKey("store.store_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False, index=True)
    email = Column(Text)
    address_id = Column(
        ForeignKey("address.address_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    activebool = Column(Boolean, nullable=False, server_default=text("true"))
    create_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    last_update = Column(DateTime(True), server_default=text("now()"))
    active = Column(Integer)

    address = relationship("Addres")
    store = relationship("Store")


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (Index("idx_store_id_film_id", "store_id", "film_id"),)

    inventory_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('inventory_inventory_id_seq'::regclass)"),
    )
    film_id = Column(
        ForeignKey("film.film_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    store_id = Column(
        ForeignKey("store.store_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    film = relationship("Film")
    store = relationship("Store")


class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('staff_staff_id_seq'::regclass)"),
    )
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    address_id = Column(
        ForeignKey("address.address_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    email = Column(Text)
    store_id = Column(ForeignKey("store.store_id"), nullable=False)
    active = Column(Boolean, nullable=False, server_default=text("true"))
    username = Column(Text, nullable=False)
    password = Column(Text)
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))
    picture = Column(LargeBinary)

    address = relationship("Addres")
    store = relationship("Store")


class Rental(Base):
    __tablename__ = "rental"
    __table_args__ = (
        Index(
            "idx_unq_rental_rental_date_inventory_id_customer_id",
            "rental_date",
            "inventory_id",
            "customer_id",
            unique=True,
        ),
    )

    rental_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('rental_rental_id_seq'::regclass)"),
    )
    rental_date = Column(DateTime(True), nullable=False)
    inventory_id = Column(
        ForeignKey("inventory.inventory_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    customer_id = Column(
        ForeignKey("customer.customer_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    return_date = Column(DateTime(True))
    staff_id = Column(
        ForeignKey("staff.staff_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    last_update = Column(DateTime(True), nullable=False, server_default=text("now()"))

    customer = relationship("Customer")
    inventory = relationship("Inventory")
    staff = relationship("Staff")


t_payment_p2020_01 = Table(
    "payment_p2020_01",
    metadata,
    Column(
        "payment_id",
        Integer,
        nullable=False,
        server_default=text("nextval('payment_payment_id_seq'::regclass)"),
    ),
    Column(
        "customer_id", ForeignKey("customer.customer_id"), nullable=False, index=True
    ),
    Column("staff_id", ForeignKey("staff.staff_id"), nullable=False, index=True),
    Column("rental_id", ForeignKey("rental.rental_id"), nullable=False),
    Column("amount", Numeric(5, 2), nullable=False),
    Column("payment_date", DateTime(True), nullable=False),
)


t_payment_p2020_02 = Table(
    "payment_p2020_02",
    metadata,
    Column(
        "payment_id",
        Integer,
        nullable=False,
        server_default=text("nextval('payment_payment_id_seq'::regclass)"),
    ),
    Column(
        "customer_id", ForeignKey("customer.customer_id"), nullable=False, index=True
    ),
    Column("staff_id", ForeignKey("staff.staff_id"), nullable=False, index=True),
    Column("rental_id", ForeignKey("rental.rental_id"), nullable=False),
    Column("amount", Numeric(5, 2), nullable=False),
    Column("payment_date", DateTime(True), nullable=False),
)


t_payment_p2020_03 = Table(
    "payment_p2020_03",
    metadata,
    Column(
        "payment_id",
        Integer,
        nullable=False,
        server_default=text("nextval('payment_payment_id_seq'::regclass)"),
    ),
    Column(
        "customer_id", ForeignKey("customer.customer_id"), nullable=False, index=True
    ),
    Column("staff_id", ForeignKey("staff.staff_id"), nullable=False, index=True),
    Column("rental_id", ForeignKey("rental.rental_id"), nullable=False),
    Column("amount", Numeric(5, 2), nullable=False),
    Column("payment_date", DateTime(True), nullable=False),
)


t_payment_p2020_04 = Table(
    "payment_p2020_04",
    metadata,
    Column(
        "payment_id",
        Integer,
        nullable=False,
        server_default=text("nextval('payment_payment_id_seq'::regclass)"),
    ),
    Column(
        "customer_id", ForeignKey("customer.customer_id"), nullable=False, index=True
    ),
    Column("staff_id", ForeignKey("staff.staff_id"), nullable=False, index=True),
    Column("rental_id", ForeignKey("rental.rental_id"), nullable=False),
    Column("amount", Numeric(5, 2), nullable=False),
    Column("payment_date", DateTime(True), nullable=False),
)


t_payment_p2020_05 = Table(
    "payment_p2020_05",
    metadata,
    Column(
        "payment_id",
        Integer,
        nullable=False,
        server_default=text("nextval('payment_payment_id_seq'::regclass)"),
    ),
    Column(
        "customer_id", ForeignKey("customer.customer_id"), nullable=False, index=True
    ),
    Column("staff_id", ForeignKey("staff.staff_id"), nullable=False, index=True),
    Column("rental_id", ForeignKey("rental.rental_id"), nullable=False),
    Column("amount", Numeric(5, 2), nullable=False),
    Column("payment_date", DateTime(True), nullable=False),
)


t_payment_p2020_06 = Table(
    "payment_p2020_06",
    metadata,
    Column(
        "payment_id",
        Integer,
        nullable=False,
        server_default=text("nextval('payment_payment_id_seq'::regclass)"),
    ),
    Column(
        "customer_id", ForeignKey("customer.customer_id"), nullable=False, index=True
    ),
    Column("staff_id", ForeignKey("staff.staff_id"), nullable=False, index=True),
    Column("rental_id", ForeignKey("rental.rental_id"), nullable=False),
    Column("amount", Numeric(5, 2), nullable=False),
    Column("payment_date", DateTime(True), nullable=False),
)
