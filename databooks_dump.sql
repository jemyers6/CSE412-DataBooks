--
-- PostgreSQL database dump
--

\restrict 3VC337aWwbNj6lKOMKhTYlugkLh4TIfo2IIqra7v3AWS3he31njLxcBeDGtBgmW

-- Dumped from database version 15.14 (Homebrew)
-- Dumped by pg_dump version 15.14 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: addedtoshelf; Type: TABLE; Schema: public; Owner: josephinemyers
--

CREATE TABLE public.addedtoshelf (
    shelf_id integer NOT NULL,
    isbn character(13) NOT NULL
);


ALTER TABLE public.addedtoshelf OWNER TO josephinemyers;

--
-- Name: author; Type: TABLE; Schema: public; Owner: josephinemyers
--

CREATE TABLE public.author (
    author_id integer NOT NULL,
    name character varying(100),
    avg_rating numeric(3,2)
);


ALTER TABLE public.author OWNER TO josephinemyers;

--
-- Name: book; Type: TABLE; Schema: public; Owner: josephinemyers
--

CREATE TABLE public.book (
    isbn character(13) NOT NULL,
    title character varying(200) NOT NULL,
    edition character varying(20),
    list_price numeric(8,2),
    publicationyear integer,
    editor character varying(100),
    avg_rating numeric(3,2),
    num_pages integer,
    lang character varying(50),
    citation text
);


ALTER TABLE public.book OWNER TO josephinemyers;

--
-- Name: bookstatus; Type: TABLE; Schema: public; Owner: josephinemyers
--

CREATE TABLE public.bookstatus (
    isbn character(13) NOT NULL,
    progress_page integer,
    read_status character varying(20),
    updated_at character varying(50),
    start_date character varying(50),
    finish_date character varying(50),
    CONSTRAINT bookstatus_progress_page_check CHECK ((progress_page >= 0)),
    CONSTRAINT bookstatus_read_status_check CHECK (((read_status)::text = ANY ((ARRAY['WANT_TO_READ'::character varying, 'CURRENTLY_READING'::character varying, 'READ'::character varying])::text[])))
);


ALTER TABLE public.bookstatus OWNER TO josephinemyers;

--
-- Name: digitalshelf; Type: TABLE; Schema: public; Owner: josephinemyers
--

CREATE TABLE public.digitalshelf (
    shelf_id integer NOT NULL,
    shelf_type character varying(50),
    name character varying(100)
);


ALTER TABLE public.digitalshelf OWNER TO josephinemyers;

--
-- Name: personalrating; Type: TABLE; Schema: public; Owner: josephinemyers
--

CREATE TABLE public.personalrating (
    isbn character(13) NOT NULL,
    rating integer,
    text_review character varying(1000),
    CONSTRAINT personalrating_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.personalrating OWNER TO josephinemyers;

--
-- Name: writes; Type: TABLE; Schema: public; Owner: josephinemyers
--

CREATE TABLE public.writes (
    author_id integer NOT NULL,
    isbn character(13) NOT NULL
);


ALTER TABLE public.writes OWNER TO josephinemyers;

--
-- Data for Name: addedtoshelf; Type: TABLE DATA; Schema: public; Owner: josephinemyers
--

COPY public.addedtoshelf (shelf_id, isbn) FROM stdin;
5	9788416029747
4	9780670919536
8	9781781251492
\.


--
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: josephinemyers
--

COPY public.author (author_id, name, avg_rating) FROM stdin;
1	Brené Brown	3.50
2	Ryan Holliday	4.20
3	Harvard Business Review	3.90
4	Lars Schmidt	4.00
5	Robert Greene	4.80
6	Lawrence Freedman	3.40
7	Michael Bungay Stanier	4.30
8	Julie Zhuo	4.00
9	Josh Kaufman	4.10
10	Jorge Riechman	3.30
11	Erich Fromm	4.90
12	Daniel Goleman	3.20
13	Joe Navarro	3.40
14	Jeff Weiss	4.60
15	Amy Gallo	4.50
16	Karen Dillon	4.80
17	Max Tegmark	3.20
18	Caterina Kostoula	3.50
19	Chris Voss	3.80
\.


--
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: josephinemyers
--

COPY public.book (isbn, title, edition, list_price, publicationyear, editor, avg_rating, num_pages, lang, citation) FROM stdin;
9781984854032	Dare to Lead: Brave Work. Tough Conversations. Whole Hearts.	First	16.47	2018	Random House International	4.20	298	English	Brown, B. (2018). Dare to lead: brave work. tough conversations. whole hearts.. Random House International.
9781781251492	The Obstacle Is the Way: The Timeless Art of Turning Trials into Triumph	Second	11.62	2015	Profile Books	4.15	201	English	Holliday, R. (2015). The obstacle is the way:  the timeless art of turning trials into triumph. (Second ed.). Profile Books.
9781422187609	HBR Guide to Managing Up and Across (HBR Guide Series)	First	14.78	2013	Harvard Business Review Press	3.72	192	English	Review, HB. (2013). Hbr guide to managing up and across (hbr guide series). Harvard Business Review Press.
9781789667042	Redefining HR: Transforming People Teams to Drive Business Performance	First	26.31	2021	KoganPage	4.24	252	English	Schmidt, L. (2021). Redefining hr:  transforming people teams to drive business performance. KoganPage.
9781861979780	The 33 Strategies of War	First	20.59	2007	Profile Books	4.21	470	English	Greene, R. (2007). The 33 strategies of war. (First Paperback ed.). Profile Books.
9780190229238	Strategy: A History	First	24.95	2015	Oxford University Press	3.97	751	English	Freedman, L. (2015). Strategy:  a history. Oxford University Press.
9780978440749	The Coaching Habit: Say Less, Ask More & Change the Way You Lead Forever	First	16.95	2016	Page Two Books	4.02	227	English	Stanier, MB. (2016). The coaching habit:  say less, ask more & change the way you lead forever. Page Two Books.
9781788166331	Discipline is Destiny	First	14.99	2022	Profile Books	4.30	312	English	Holliday, R. (2022). Discipline is destiny. Profile Books.
9780753552896	The Making of a Manager: How to Crush Your Job as the New Boss	First	14.99	2019	Virgin Books	4.22	260	English	Zhuo, J. (2019). The making of a manager:  how to crush your job as the new boss. Virgin Books.
9780670919536	The Personal MBA	Second	12.99	2020	Penguin Random House UK	4.11	464	English	Kaufman, J. (2020). The personal mba. (Second ed.). Penguin Random House UK.
9788483194195	La habitación de Pascal: Ensayos para fundamentar éticas de suficiencia y políticas de autocontención	First	19.00	2009	Los Libros de la Catarata	4.50	317	Spanish	Riechman, J. (2009). La habitaci¢n de pascal:  ensayos para fundamentar éticas de suficiencia y políticas de autocontención. Los Libros de la Catarata.
9788498462050	Tenir o Ésser	Seventh	12.49	2011	Claret Editorial	4.19	273	Catalan	Fromm, E. (2011). Tenir o ésser. (Seventh Edition ed.). Claret Editorial.
9788499883052	Focus: Desarrollar la atención para alcanzar la excelencia	Fourth	18.00	2013	Editorial Kairós	3.56	357	Spanish	Goleman, D. (2013). Focus:  desarrollar la atención para alcanzar la excelencia. (Fourth edition ed.). Editorial Kairós.
9788492819577	La inteligencia no verbal	First	16.00	2011	Viceversa Editorial	3.85	248	Spanish	Navarro, J. (2011). La inteligencia no verbal. (First edition ed.). Viceversa Editorial.
9781633690769	HBR Guide to Negotiating (HBR guide series)	First	12.99	2016	Harvard Business Review Press	3.68	177	English	Weiss, J. (2016). Hbr guide to negotiating (hbr guide series). (First edition ed.). Harvard Business Review Press.
9781633692152	HBR Guide to Dealing with Conflict (HBR Guide Series)	First	14.19	2017	Harvard Business Review Press	3.82	193	English	Gallo, A. (2017). Hbr guide to dealing with conflict (hbr guide series). (First edition ed.). Harvard Business Review Press.
9781625275325	HBR Guide to Office Politics (HBR Guide Series)	First	14.78	2014	Harvard Business Review Press	3.77	175	English	Dillon, K. (2014). Hbr guide to office politics (hbr guide series). (First edition ed.). Harvard Business Review Press.
9780141981802	Life 3.0: Being Human in the Age of Artificial Intelligence	Second	10.99	2018	Penguin Random House	4.02	364	English	Tegmark, M. (2018). Life 3.0:  being human in the age of artificial intelligence. (Second ed.). Penguin Random House UK.
9780241481950	Hold Successful Meetings	First	9.99	2021	Penguin Random House	4.17	202	English	Kostoula, C. (2021). Hold successful meetings. Penguiin Rnadom House UK.
9788416029747	Rompe la barrera del NO	Third	18.90	2019	Penguin Random House	4.36	349	Spanish	Voss, C. (2019). Rompe la barrera del no. (Third ed.). Penguin Random House.
\.


--
-- Data for Name: bookstatus; Type: TABLE DATA; Schema: public; Owner: josephinemyers
--

COPY public.bookstatus (isbn, progress_page, read_status, updated_at, start_date, finish_date) FROM stdin;
9780670919536	100	READ	2025-12-5	2025-12-05	2025-12-5
9788416029747	349	READ	2025-12-05	2025-12-05	2025-12-05
9781781251492	201	READ	2025-12-05	2025-12-05	2025-12-05
\.


--
-- Data for Name: digitalshelf; Type: TABLE DATA; Schema: public; Owner: josephinemyers
--

COPY public.digitalshelf (shelf_id, shelf_type, name) FROM stdin;
4	OTHER	Classics
5	OTHER	Mystery
7	OTHER	Made me cry
8	OTHER	Hated
9	OTHER	romance
10	OTHER	Fantasy
6	OTHER	Bestsellers
\.


--
-- Data for Name: personalrating; Type: TABLE DATA; Schema: public; Owner: josephinemyers
--

COPY public.personalrating (isbn, rating, text_review) FROM stdin;
9780670919536	2	i didn't like it
9788416029747	4	this book was so awesome
9781781251492	1	this was the worst book ever
\.


--
-- Data for Name: writes; Type: TABLE DATA; Schema: public; Owner: josephinemyers
--

COPY public.writes (author_id, isbn) FROM stdin;
2	9781781251492
3	9781422187609
4	9781789667042
5	9781861979780
6	9780190229238
7	9780978440749
8	9781788166331
9	9780753552896
10	9780670919536
11	9788483194195
12	9788498462050
13	9788499883052
14	9788492819577
15	9781633690769
16	9781633692152
17	9781625275325
18	9780141981802
19	9780241481950
1	9781984854032
2	9781788166331
\.


--
-- Name: addedtoshelf addedtoshelf_pkey; Type: CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.addedtoshelf
    ADD CONSTRAINT addedtoshelf_pkey PRIMARY KEY (shelf_id, isbn);


--
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (author_id);


--
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (isbn);


--
-- Name: bookstatus bookstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.bookstatus
    ADD CONSTRAINT bookstatus_pkey PRIMARY KEY (isbn);


--
-- Name: digitalshelf digitalshelf_pkey; Type: CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.digitalshelf
    ADD CONSTRAINT digitalshelf_pkey PRIMARY KEY (shelf_id);


--
-- Name: personalrating personalrating_pkey; Type: CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.personalrating
    ADD CONSTRAINT personalrating_pkey PRIMARY KEY (isbn);


--
-- Name: writes writes_pkey; Type: CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.writes
    ADD CONSTRAINT writes_pkey PRIMARY KEY (author_id, isbn);


--
-- Name: addedtoshelf addedtoshelf_isbn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.addedtoshelf
    ADD CONSTRAINT addedtoshelf_isbn_fkey FOREIGN KEY (isbn) REFERENCES public.book(isbn) ON DELETE CASCADE;


--
-- Name: addedtoshelf addedtoshelf_shelf_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.addedtoshelf
    ADD CONSTRAINT addedtoshelf_shelf_id_fkey FOREIGN KEY (shelf_id) REFERENCES public.digitalshelf(shelf_id) ON DELETE CASCADE;


--
-- Name: bookstatus bookstatus_isbn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.bookstatus
    ADD CONSTRAINT bookstatus_isbn_fkey FOREIGN KEY (isbn) REFERENCES public.book(isbn) ON DELETE CASCADE;


--
-- Name: personalrating personalrating_isbn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.personalrating
    ADD CONSTRAINT personalrating_isbn_fkey FOREIGN KEY (isbn) REFERENCES public.book(isbn) ON DELETE CASCADE;


--
-- Name: writes writes_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.writes
    ADD CONSTRAINT writes_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.author(author_id) ON DELETE CASCADE;


--
-- Name: writes writes_isbn_fkey; Type: FK CONSTRAINT; Schema: public; Owner: josephinemyers
--

ALTER TABLE ONLY public.writes
    ADD CONSTRAINT writes_isbn_fkey FOREIGN KEY (isbn) REFERENCES public.book(isbn) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 3VC337aWwbNj6lKOMKhTYlugkLh4TIfo2IIqra7v3AWS3he31njLxcBeDGtBgmW

