--
-- PostgreSQL database dump
--

\restrict I8BOF5fDidnX36fDk81CByEJIva3wjGde2gcGtyPggJI9gRqG2vIGpWDa541VpF

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-19 17:44:55

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 228 (class 1259 OID 16452)
-- Name: alumno; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alumno (
    no_control integer NOT NULL,
    correo character varying(100) NOT NULL,
    id_usuario integer NOT NULL
);


ALTER TABLE public.alumno OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16451)
-- Name: alumno_no_control_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.alumno_no_control_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.alumno_no_control_seq OWNER TO postgres;

--
-- TOC entry 5083 (class 0 OID 0)
-- Dependencies: 227
-- Name: alumno_no_control_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.alumno_no_control_seq OWNED BY public.alumno.no_control;


--
-- TOC entry 230 (class 1259 OID 16469)
-- Name: externo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.externo (
    id_externo integer NOT NULL,
    id_usuario integer NOT NULL
);


ALTER TABLE public.externo OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16468)
-- Name: externo_id_externo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.externo_id_externo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.externo_id_externo_seq OWNER TO postgres;

--
-- TOC entry 5084 (class 0 OID 0)
-- Dependencies: 229
-- Name: externo_id_externo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.externo_id_externo_seq OWNED BY public.externo.id_externo;


--
-- TOC entry 222 (class 1259 OID 16404)
-- Name: ingresos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingresos (
    id_ingreso integer NOT NULL,
    fecha_entrada timestamp without time zone NOT NULL,
    fecha_salida timestamp without time zone,
    id_usuario integer NOT NULL
);


ALTER TABLE public.ingresos OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16403)
-- Name: ingresos_id_ingreso_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingresos_id_ingreso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingresos_id_ingreso_seq OWNER TO postgres;

--
-- TOC entry 5085 (class 0 OID 0)
-- Dependencies: 221
-- Name: ingresos_id_ingreso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingresos_id_ingreso_seq OWNED BY public.ingresos.id_ingreso;


--
-- TOC entry 224 (class 1259 OID 16419)
-- Name: membresias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.membresias (
    no_membresia integer NOT NULL,
    fecha_inicial date NOT NULL,
    fecha_final date NOT NULL,
    id_usuario integer NOT NULL
);


ALTER TABLE public.membresias OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16418)
-- Name: membresias_no_membresia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.membresias_no_membresia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.membresias_no_membresia_seq OWNER TO postgres;

--
-- TOC entry 5086 (class 0 OID 0)
-- Dependencies: 223
-- Name: membresias_no_membresia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.membresias_no_membresia_seq OWNED BY public.membresias.no_membresia;


--
-- TOC entry 226 (class 1259 OID 16435)
-- Name: observaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.observaciones (
    id_observacion integer NOT NULL,
    fecha_observacion date NOT NULL,
    descripcion text,
    id_usuario integer NOT NULL
);


ALTER TABLE public.observaciones OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16434)
-- Name: observaciones_id_observacion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.observaciones_id_observacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.observaciones_id_observacion_seq OWNER TO postgres;

--
-- TOC entry 5087 (class 0 OID 0)
-- Dependencies: 225
-- Name: observaciones_id_observacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.observaciones_id_observacion_seq OWNED BY public.observaciones.id_observacion;


--
-- TOC entry 232 (class 1259 OID 16483)
-- Name: representativos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.representativos (
    id_representativo integer NOT NULL,
    no_control integer NOT NULL,
    equipo character varying(100) NOT NULL
);


ALTER TABLE public.representativos OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16482)
-- Name: representativos_id_representativo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.representativos_id_representativo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.representativos_id_representativo_seq OWNER TO postgres;

--
-- TOC entry 5088 (class 0 OID 0)
-- Dependencies: 231
-- Name: representativos_id_representativo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.representativos_id_representativo_seq OWNED BY public.representativos.id_representativo;


--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    usuario character varying(50) NOT NULL,
    contrasena character varying(100) NOT NULL,
    nombres character varying(100) NOT NULL,
    apellido_paterno character varying(100) NOT NULL,
    apellido_materno character varying(100)
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO postgres;

--
-- TOC entry 5089 (class 0 OID 0)
-- Dependencies: 219
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;


--
-- TOC entry 4890 (class 2604 OID 16455)
-- Name: alumno no_control; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alumno ALTER COLUMN no_control SET DEFAULT nextval('public.alumno_no_control_seq'::regclass);


--
-- TOC entry 4891 (class 2604 OID 16472)
-- Name: externo id_externo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.externo ALTER COLUMN id_externo SET DEFAULT nextval('public.externo_id_externo_seq'::regclass);


--
-- TOC entry 4887 (class 2604 OID 16407)
-- Name: ingresos id_ingreso; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos ALTER COLUMN id_ingreso SET DEFAULT nextval('public.ingresos_id_ingreso_seq'::regclass);


--
-- TOC entry 4888 (class 2604 OID 16422)
-- Name: membresias no_membresia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membresias ALTER COLUMN no_membresia SET DEFAULT nextval('public.membresias_no_membresia_seq'::regclass);


--
-- TOC entry 4889 (class 2604 OID 16438)
-- Name: observaciones id_observacion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.observaciones ALTER COLUMN id_observacion SET DEFAULT nextval('public.observaciones_id_observacion_seq'::regclass);


--
-- TOC entry 4892 (class 2604 OID 16486)
-- Name: representativos id_representativo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.representativos ALTER COLUMN id_representativo SET DEFAULT nextval('public.representativos_id_representativo_seq'::regclass);


--
-- TOC entry 4886 (class 2604 OID 16393)
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);


--
-- TOC entry 5073 (class 0 OID 16452)
-- Dependencies: 228
-- Data for Name: alumno; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alumno (no_control, correo, id_usuario) FROM stdin;
\.


--
-- TOC entry 5075 (class 0 OID 16469)
-- Dependencies: 230
-- Data for Name: externo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.externo (id_externo, id_usuario) FROM stdin;
\.


--
-- TOC entry 5067 (class 0 OID 16404)
-- Dependencies: 222
-- Data for Name: ingresos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingresos (id_ingreso, fecha_entrada, fecha_salida, id_usuario) FROM stdin;
\.


--
-- TOC entry 5069 (class 0 OID 16419)
-- Dependencies: 224
-- Data for Name: membresias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.membresias (no_membresia, fecha_inicial, fecha_final, id_usuario) FROM stdin;
\.


--
-- TOC entry 5071 (class 0 OID 16435)
-- Dependencies: 226
-- Data for Name: observaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.observaciones (id_observacion, fecha_observacion, descripcion, id_usuario) FROM stdin;
\.


--
-- TOC entry 5077 (class 0 OID 16483)
-- Dependencies: 232
-- Data for Name: representativos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.representativos (id_representativo, no_control, equipo) FROM stdin;
\.


--
-- TOC entry 5065 (class 0 OID 16390)
-- Dependencies: 220
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, usuario, contrasena, nombres, apellido_paterno, apellido_materno) FROM stdin;
\.


--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 227
-- Name: alumno_no_control_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.alumno_no_control_seq', 1, false);


--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 229
-- Name: externo_id_externo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.externo_id_externo_seq', 1, false);


--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 221
-- Name: ingresos_id_ingreso_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingresos_id_ingreso_seq', 1, false);


--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 223
-- Name: membresias_no_membresia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.membresias_no_membresia_seq', 1, false);


--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 225
-- Name: observaciones_id_observacion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.observaciones_id_observacion_seq', 1, false);


--
-- TOC entry 5095 (class 0 OID 0)
-- Dependencies: 231
-- Name: representativos_id_representativo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.representativos_id_representativo_seq', 1, false);


--
-- TOC entry 5096 (class 0 OID 0)
-- Dependencies: 219
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 1, false);


--
-- TOC entry 4904 (class 2606 OID 16462)
-- Name: alumno alumno_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alumno
    ADD CONSTRAINT alumno_correo_key UNIQUE (correo);


--
-- TOC entry 4906 (class 2606 OID 16460)
-- Name: alumno alumno_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alumno
    ADD CONSTRAINT alumno_pkey PRIMARY KEY (no_control);


--
-- TOC entry 4908 (class 2606 OID 16476)
-- Name: externo externo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.externo
    ADD CONSTRAINT externo_pkey PRIMARY KEY (id_externo);


--
-- TOC entry 4898 (class 2606 OID 16412)
-- Name: ingresos ingresos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos
    ADD CONSTRAINT ingresos_pkey PRIMARY KEY (id_ingreso);


--
-- TOC entry 4900 (class 2606 OID 16428)
-- Name: membresias membresias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membresias
    ADD CONSTRAINT membresias_pkey PRIMARY KEY (no_membresia);


--
-- TOC entry 4902 (class 2606 OID 16445)
-- Name: observaciones observaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.observaciones
    ADD CONSTRAINT observaciones_pkey PRIMARY KEY (id_observacion);


--
-- TOC entry 4910 (class 2606 OID 16491)
-- Name: representativos representativos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.representativos
    ADD CONSTRAINT representativos_pkey PRIMARY KEY (id_representativo);


--
-- TOC entry 4894 (class 2606 OID 16400)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4896 (class 2606 OID 16402)
-- Name: usuario usuario_usuario_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_usuario_key UNIQUE (usuario);


--
-- TOC entry 4914 (class 2606 OID 16463)
-- Name: alumno alumno_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alumno
    ADD CONSTRAINT alumno_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4915 (class 2606 OID 16477)
-- Name: externo externo_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.externo
    ADD CONSTRAINT externo_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4911 (class 2606 OID 16413)
-- Name: ingresos ingresos_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingresos
    ADD CONSTRAINT ingresos_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4912 (class 2606 OID 16429)
-- Name: membresias membresias_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membresias
    ADD CONSTRAINT membresias_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4913 (class 2606 OID 16446)
-- Name: observaciones observaciones_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.observaciones
    ADD CONSTRAINT observaciones_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4916 (class 2606 OID 16492)
-- Name: representativos representativos_no_control_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.representativos
    ADD CONSTRAINT representativos_no_control_fkey FOREIGN KEY (no_control) REFERENCES public.alumno(no_control) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2025-10-19 17:44:56

--
-- PostgreSQL database dump complete
--

\unrestrict I8BOF5fDidnX36fDk81CByEJIva3wjGde2gcGtyPggJI9gRqG2vIGpWDa541VpF

