create table category(
    name varchar(255),
    codename varchar(255) primary key,
    is_regular_expense boolean
);

create table expense(
    id integer primary key,
    amount double,
    created datetime,
    category_codename integer,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (name, codename, is_regular_expense)
values
    ("Подписки", "subscriptions", true),
    ("Работа", "work", true),
    ("Мобильный счет", "telephone", true),
	("Интернет", "internet", true),
    ("Стрижка", "haircut", true),
	("Благотворительность", "charity", true),
	("Коммунальные услуги", "public service", true),
	("Стрельба", "shooting range", true),
    ("Развлечения", "entertainment", false),
	("Косметолог", "cosmetologist", false),
    ("Здоровье", "health", false),
	("Цветы", "flowers", false),
	("Одежда", "clothes", false),
	("Покупки", "purchases", false),
    ("Квартира", "flat", false),	
    ("Бассейн", "swimming", false),	
    ("Продукты", "products", false),
	("Топливо", "fuel", false),
    ("Питание", "food", false),
    ("Транспорт", "transport", false),
	("Авто", "auto", false),
	("Аптека", "pharm", false),
	("Подарки", "gifts", false),
    ("Прочее", "other", false);