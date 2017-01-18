drop table vacancy;
drop sequence vacancy_id_seq;

drop table city;
drop sequence city_id_seq;

drop table company;
drop sequence company_id_seq;

drop table site;
drop sequence site_id_seq;

CREATE SEQUENCE site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


CREATE TABLE site (
    id bigint default nextval('site_id_seq') PRIMARY KEY,
    name text
);
CREATE UNIQUE INDEX city_idx ON site (name);

INSERT INTO public.site(id, name) VALUES ('1','http://www.cv.lt/');
INSERT INTO public.site(id, name) VALUES ('2','http://www.cvbankas.lt/');
INSERT INTO public.site(id, name) VALUES ('2','http://www.cvmarket.lt/');

CREATE SEQUENCE city_id_seq
    START WITH 62
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


CREATE TABLE city (
    id bigint default nextval('city_id_seq') PRIMARY KEY,
    name text
);
CREATE UNIQUE INDEX site_idx ON city (name);

CREATE SEQUENCE company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.company_id_seq OWNER TO postgres;

CREATE TABLE company (
    id bigint default nextval('company_id_seq') PRIMARY KEY,
    name text
);
CREATE UNIQUE INDEX company_idx ON city (name);


CREATE SEQUENCE vacancy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.vacancy_id_seq OWNER TO postgres;


CREATE TABLE vacancy (
    id bigint default nextval('vacancy_id_seq') PRIMARY KEY,
    city_id bigint,
    site bigint,
    "time" timestamp without time zone,
    "date" date,
    jobtitle text,
    salary text,
    url text,
    company_id bigint,
    FOREIGN KEY (city_id) REFERENCES city (id),
    FOREIGN KEY (company_id) REFERENCES company (id)
);

ALTER TABLE public.vacancy OWNER TO postgres;


INSERT INTO public.city(id, name) VALUES ('1','Kitas');
INSERT INTO public.city(id, name) VALUES ('2','Vilnius');
INSERT INTO public.city(id, name) VALUES ('3','Telšiai');
INSERT INTO public.city(id, name) VALUES ('4','Pagėgiai');
INSERT INTO public.city(id, name) VALUES ('5','Kaunas');
INSERT INTO public.city(id, name) VALUES ('6','Kėdainiai');
INSERT INTO public.city(id, name) VALUES ('7','Plungė');
INSERT INTO public.city(id, name) VALUES ('8','Mažeikiai');
INSERT INTO public.city(id, name) VALUES ('9','Šiauliai');
INSERT INTO public.city(id, name) VALUES ('10','Radviliškis');
INSERT INTO public.city(id, name) VALUES ('11','Tauragė');
INSERT INTO public.city(id, name) VALUES ('12','Palanga');
INSERT INTO public.city(id, name) VALUES ('13','Klaipėda');
INSERT INTO public.city(id, name) VALUES ('14','Panevėžys');
INSERT INTO public.city(id, name) VALUES ('15','Vievis');
INSERT INTO public.city(id, name) VALUES ('16','Prienai');
INSERT INTO public.city(id, name) VALUES ('17','Vilkaviškis');
INSERT INTO public.city(id, name) VALUES ('18','Visaginas');
INSERT INTO public.city(id, name) VALUES ('19','Birštonas');
INSERT INTO public.city(id, name) VALUES ('20','Molėtai');
INSERT INTO public.city(id, name) VALUES ('21','Raseiniai');
INSERT INTO public.city(id, name) VALUES ('22','Naujoji Akmenė');
INSERT INTO public.city(id, name) VALUES ('23','Šilutė');
INSERT INTO public.city(id, name) VALUES ('24','Marijampolė');
INSERT INTO public.city(id, name) VALUES ('25','Varėna');
INSERT INTO public.city(id, name) VALUES ('26','Lazdijai');
INSERT INTO public.city(id, name) VALUES ('27','Utena');
INSERT INTO public.city(id, name) VALUES ('28','Kuršėnai');
INSERT INTO public.city(id, name) VALUES ('29','Druskininkai');
INSERT INTO public.city(id, name) VALUES ('30','Kalvarija');
INSERT INTO public.city(id, name) VALUES ('31','Jurbarkas');
INSERT INTO public.city(id, name) VALUES ('32','Šakiai');
INSERT INTO public.city(id, name) VALUES ('33','Šilalė');
INSERT INTO public.city(id, name) VALUES ('34','Ukmergė');
INSERT INTO public.city(id, name) VALUES ('35','Jonava');
INSERT INTO public.city(id, name) VALUES ('36','Ignalina');
INSERT INTO public.city(id, name) VALUES ('37','Gargždai');
INSERT INTO public.city(id, name) VALUES ('38','Anykščiai');
INSERT INTO public.city(id, name) VALUES ('39','Kaišiadorys');
INSERT INTO public.city(id, name) VALUES ('40','Alytus');
INSERT INTO public.city(id, name) VALUES ('41','Pakruojis');
INSERT INTO public.city(id, name) VALUES ('42','Elektrėnai');
INSERT INTO public.city(id, name) VALUES ('43','Skuodas');
INSERT INTO public.city(id, name) VALUES ('44','Kupiškis');
INSERT INTO public.city(id, name) VALUES ('45','Kretinga');
INSERT INTO public.city(id, name) VALUES ('46','Joniškis');
INSERT INTO public.city(id, name) VALUES ('47','Biržai');
INSERT INTO public.city(id, name) VALUES ('48','Šalčininkai');
INSERT INTO public.city(id, name) VALUES ('49','Lentvaris');
INSERT INTO public.city(id, name) VALUES ('50','Trakai');
INSERT INTO public.city(id, name) VALUES ('51','Švenčionys');
INSERT INTO public.city(id, name) VALUES ('52','Širvintos');
INSERT INTO public.city(id, name) VALUES ('53','Pasvalys');
INSERT INTO public.city(id, name) VALUES ('54','Zarasai');
INSERT INTO public.city(id, name) VALUES ('55','Bet kuris miestas');
INSERT INTO public.city(id, name) VALUES ('56','Užsienyje');
INSERT INTO public.city(id, name) VALUES ('57','Rokiškis');
INSERT INTO public.city(id, name) VALUES ('58','Kazlų Rūda');
INSERT INTO public.city(id, name) VALUES ('59','Kelmė');
INSERT INTO public.city(id, name) VALUES ('60','Rietavas');
INSERT INTO public.city(id, name) VALUES ('61','Neringa');