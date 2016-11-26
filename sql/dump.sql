drop table vacancy;
drop sequence vacancy_id_seq;

drop table city;
drop sequence city_id_seq;

CREATE SEQUENCE city_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.city_id_seq OWNER TO postgres;

CREATE TABLE city (
    id bigint default nextval('city_id_seq') PRIMARY KEY,
    name text
);
CREATE UNIQUE INDEX city_idx ON city (name);


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
    site text,
    "time" timestamp without time zone,
    "date" date,
    jobtitle text,
    hiring_organisation text,
    job_location text,
    url text,
    FOREIGN KEY (city_id) REFERENCES city (id)
);

ALTER TABLE public.vacancy OWNER TO postgres;




select * from vacancy;


select job_location, count(job_location) from vacancy group by job_location order by count(job_location) desc;

select jobtitle, count(jobtitle) from vacancy group by jobtitle order by count(jobtitle) desc;