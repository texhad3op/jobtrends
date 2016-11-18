CREATE SEQUENCE events_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO postgres;


CREATE TABLE events (
    id bigint default nextval('events_id_seq'),
    site test,
    "time" timestamp without time zone,
    "date" date,
    jobtitle text,
    hiring_organisation text,
    job_location text,
    url text
);

ALTER TABLE ONLY events
ADD CONSTRAINT events_pkey PRIMARY KEY (id);

ALTER TABLE public.events OWNER TO postgres;
