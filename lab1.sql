DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS specializations CASCADE;
DROP TABLE IF EXISTS workers CASCADE;
DROP TABLE IF EXISTS specializationboundserveses CASCADE;
DROP TABLE IF EXISTS activity CASCADE;
DROP TABLE IF EXISTS visits CASCADE;
DROP TABLE IF EXISTS visitsboundserveses CASCADE;

create table patients
(
	idpatients serial not null
		constraint patients_pk
			primary key,
	sex integer not null,
	birthdate date not null,
	medicalid varchar(45) not null
);

alter table patients owner to veto;

create unique index patients_idpatients_uindex
	on patients (idpatients);

create table services
(
	idservices serial not null
		constraint services_pk
			primary key,
	description varchar not null,
    price INTEGER DEFAULT 0
);

alter table services owner to veto;

create unique index services_idservices_uindex
	on services (idservices);

create table specializations
(
	idspecializations serial not null
		constraint specializations_pk
			primary key,
	specializations varchar(45) not null
);

alter table specializations owner to veto;

create unique index specializations_specializations_uindex
	on specializations (specializations);

create unique index specializations_idspecializations_uindex
	on specializations (idspecializations);

create table workers
(
	idworker serial not null
		constraint workers_pk
			primary key,
	name varchar(45) not null,
	sex integer not null,
	birthdate date not null,
	idspecialization integer not null
		constraint workers_specialization_fkey
			references specializations
);

alter table workers owner to veto;

create unique index workers_idworker_uindex
	on workers (idworker);

create table specializationboundserveses
(
	idservises integer not null
		constraint specializationboundserveses_idserveses_fkey
			references services,
	idspecialization integer not null
		constraint specializationboundserveses_idspecialization_fkey
			references specializations
);

alter table specializationboundserveses owner to veto;

create table activity
(
	activitytype varchar(45) not null,
	activitydate date not null,
	idworker integer
		constraint activity_idworker_fkey
			references workers
				on delete cascade
);

alter table activity owner to veto;

create table visits
(
	idvisit serial not null
		constraint visits_pk
			primary key,
	idpatient integer not null
		constraint visits_idpatient_fkey
			references patients,
	date date not null,
	time time not null,
	idworker integer not null
		constraint visits_idworker_fkey
			references workers
);

alter table visits owner to veto;

create table visitsboundserveses
(
	idvisit integer not null
		constraint visitsboundserveses_idvisit_fkey
			references visits,
	idservices integer
		constraint visitsboundserveses_idservices_fkey
			references services
);

alter table visitsboundserveses owner to veto;

create OR REPLACE view existingservises_on_visit(idworker, idspecialization, idservises) as
SELECT workers.idworker,
       workers.idspecialization,
       specializationboundserveses.idservises
FROM (workers
         JOIN specializationboundserveses
              ON ((specializationboundserveses.idspecialization = workers.idspecialization)));

alter table existingservises_on_visit owner to veto;


begin;
    CREATE OR REPLACE FUNCTION recruit_worker_t()
      RETURNS TRIGGER
      AS $$
      BEGIN
        INSERT INTO activity(idworker, activitytype, activitydate)
            VALUES (NEW.idworker,'recruiting',current_date);
        RETURN NEW;
      END;
      $$
    LANGUAGE 'plpgsql';

    DROP TRIGGER IF EXISTS recruiting ON workers;
    CREATE TRIGGER recruiting
    AFTER INSERT ON workers
    FOR EACH ROW
    EXECUTE PROCEDURE recruit_worker_t();
commit;

begin; -- 19,20
INSERT INTO specializations(idspecializations, specializations) VALUES (0,'test');
    INSERT INTO workers(name, idspecialization, sex, birthdate)
        VALUES ('test', 0, 0, current_date);
    SELECT * FROM activity;
    DELETE FROM workers WHERE (name = 'test');
DELETE FROM specializations WHERE(TRUE);
commit;

begin;
    CREATE OR REPLACE FUNCTION remove_worker_t()
    RETURNS TRIGGER
    AS $$
    BEGIN
        IF EXISTS(
            SELECT * FROM visits WHERE (
                (visits.idworker = old.idworker) AND
                    (visits.date >= current_date) AND
                    (visits.time >= current_time)
                )
            ) THEN
                RAISE EXCEPTION 'error: there are active visits';
        END IF;
        IF EXISTS(
            SELECT * FROM visits WHERE (
                (visits.idworker = old.idworker) AND
                    (visits.date <= current_date) AND
                    (visits.time <= current_time)
                )
            ) THEN
                INSERT INTO activity(activitytype, activitydate, idworker)
                    VALUES ('was dismissed', current_date, OLD.idworker);
                RAISE NOTICE 'was dismissed';
                RETURN NULL;
        END IF;
        RETURN OLD;
    END;
    $$
    LANGUAGE 'plpgsql';


    DROP TRIGGER IF EXISTS remove_worker ON workers;
    CREATE TRIGGER remove_worker
    BEFORE DELETE ON workers
    FOR EACH ROW
    EXECUTE PROCEDURE remove_worker_t();
commit;

--CLEAN
    DELETE FROM specializationboundserveses WHERE (TRUE);
    DELETE FROM visitsboundserveses WHERE (TRUE);
    DELETE FROM services WHERE(TRUE);
    DELETE FROM specializationboundserveses WHERE (TRUE);
    DELETE FROM visits WHERE (TRUE);
    DELETE FROM patients WHERE (TRUE);
    DELETE FROM workers WHERE (TRUE);
    DELETE FROM specializations WHERE (TRUE);

begin; -- 21,22
    INSERT INTO specializations(idspecializations, specializations) VALUES (0,'test0');
    INSERT INTO workers(idworker, name, idspecialization, sex, birthdate)
        VALUES (0,'test0', 0, 0, current_date);
    INSERT INTO services(idservices, description) VALUES(0, 'test0');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (0, 0);
    INSERT INTO services(idservices, description) VALUES(10, 'test10');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (10, 0);
    -- ÏÅÐÂÛÉ ÐÀÁÎ×ÈÉ ÑÏÅÖÈÀÀËÈÇÀÀÖÈÈ 0 ÑÅÐÂÈÑÀ 0,10


    INSERT INTO specializations(idspecializations, specializations) VALUES (1,'test1');
    INSERT INTO workers(idworker, name, idspecialization, sex, birthdate)VALUES (1, 'test1', 1, 0, current_date);
    INSERT INTO services(idservices, description) VALUES(1, 'test1');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (1, 1);
    -- ÂÒÎÐÎÉ ÐÀÁÎ×ÈÉ ÑÏÅÖÈÀËÈÇÀÖÈÈ 1 CÅÐÂÈÑÀ 1

    INSERT INTO patients(idpatients, sex, birthdate, medicalid) VALUES(0, 0,current_date,0);
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                0,
                0,
                0,
                current_date + interval'1 day',
                current_time
                );
    -- ÏÀÖÈÅÍÒ 0 ÍÀ ÂÈÇÈÒ Ê ÐÀÁÎ×ÅÌÓ 0  Ñ ÑÅÐÂÈÑÎÌ 0,10


-- 0

    DO $$BEGIN
    DELETE FROM patients WHERE(TRUE);
    EXCEPTION
        WHEN OTHERS THEN
        DELETE FROM visits WHERE(TRUE);
        RAISE NOTICE 'it works';
    END $$;
    DELETE FROM patients WHERE(TRUE);
--1
    INSERT INTO patients(idpatients, sex, birthdate, medicalid) VALUES(0, 0,current_date,0);
    INSERT INTO workers(name, idspecialization, sex, birthdate)
        VALUES ('test', 0, 0, current_date);
    INSERT INTO visits(idworker, idpatient, date, time)
        VALUES (
                (SELECT idworker FROM workers WHERE (name = 'test') LIMIT 1),
                0,
                current_date - interval'1 day',
                current_time
                );
    DELETE FROM workers WHERE (name = 'test');
    DELETE FROM visits WHERE(TRUE);
    DELETE FROM workers WHERE(TRUE);
    DELETE FROM patients WHERE(TRUE);
--2
    INSERT INTO patients(idpatients, sex, birthdate, medicalid) VALUES(0, 0,current_date,0);
    INSERT INTO workers(name, idspecialization, sex, birthdate)
        VALUES ('test', 0, 0, current_date);
    INSERT INTO visits(idworker, idpatient, date, time)
        VALUES (
                (SELECT idworker FROM workers WHERE (name = 'test') LIMIT 1),
                0,
                current_date + interval'1 day',
                current_time
                );
    DO $$BEGIN
        DELETE FROM workers WHERE (name = 'test');
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'its works';
            DELETE FROM visits WHERE(TRUE);
    END $$;
commit;

--CLEAN
    DELETE FROM specializationboundserveses WHERE (TRUE);
    DELETE FROM visitsboundserveses WHERE (TRUE);
    DELETE FROM services WHERE(TRUE);
    DELETE FROM specializationboundserveses WHERE (TRUE);
    DELETE FROM visits WHERE (TRUE);
    DELETE FROM patients WHERE (TRUE);
    DELETE FROM workers WHERE (TRUE);
    DELETE FROM specializations WHERE (TRUE);


begin; -- 23
INSERT INTO specializations(idspecializations, specializations) VALUES (0,'test');
INSERT INTO workers(name, idspecialization, sex, birthdate)
        VALUES ('test', 0, 0, current_date);
DO $$BEGIN
        DELETE FROM specializations WHERE(TRUE);
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'its works';
            DELETE FROM workers WHERE(TRUE);
END $$;
    DELETE FROM specializations WHERE(TRUE);
commit;

DROP VIEW IF EXISTS existingservises_on_visit;
CREATE VIEW existingservises_on_visit AS
    SELECT workers.idworker,
           workers.idspecialization,
           specializationboundserveses.idservises
    FROM workers
         INNER JOIN specializationboundserveses
            ON (specializationboundserveses.idspecialization = workers.idspecialization)

;

begin;
    CREATE OR REPLACE FUNCTION add_service_tovisit_t()
      RETURNS TRIGGER
      AS $$
      BEGIN
        IF NOT EXISTS(
            SELECT * FROM existingservises_on_visit
            INNER JOIN visits USING (idworker)
            WHERE ((new.idvisit = idvisit) AND (new.idservices = idservises))
            ) THEN
            RAISE EXCEPTION 'error: worker cant do this work';
        END IF;
        RETURN new;
      END;
      $$
    LANGUAGE 'plpgsql';


    DROP TRIGGER IF EXISTS add_service_tovisit ON visitsboundserveses;
    CREATE TRIGGER add_service_tovisit
    BEFORE INSERT ON visitsboundserveses
    FOR EACH ROW
    EXECUTE PROCEDURE add_service_tovisit_t();
commit;

begin;--24
    INSERT INTO specializations(idspecializations, specializations) VALUES (0,'test0');
    INSERT INTO workers(idworker, name, idspecialization, sex, birthdate)
        VALUES (0,'test0', 0, 0, current_date);
    INSERT INTO services(idservices, description) VALUES(0, 'test0');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (0, 0);
    INSERT INTO services(idservices, description) VALUES(10, 'test10');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (10, 0);
    -- ÏÅÐÂÛÉ ÐÀÁÎ×ÈÉ ÑÏÅÖÈÀÀËÈÇÀÀÖÈÈ 0 ÑÅÐÂÈÑÀ 0,10


    INSERT INTO specializations(idspecializations, specializations) VALUES (1,'test1');
    INSERT INTO workers(idworker, name, idspecialization, sex, birthdate)VALUES (1, 'test1', 1, 0, current_date);
    INSERT INTO services(idservices, description) VALUES(1, 'test1');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (1, 1);
    -- ÂÒÎÐÎÉ ÐÀÁÎ×ÈÉ ÑÏÅÖÈÀËÈÇÀÖÈÈ 1 CÅÐÂÈÑÀ 1

    INSERT INTO patients(idpatients, sex, birthdate, medicalid) VALUES(0, 0,current_date,0);
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                0,
                0,
                0,
                current_date + interval'1 day',
                current_time
                );
    INSERT INTO visitsboundserveses(idvisit, idservices) VALUES (0,0);
    INSERT INTO visitsboundserveses(idvisit, idservices) VALUES (0,10);
    -- ÏÀÖÈÅÍÒ 0 ÍÀ ÂÈÇÈÒ Ê ÐÀÁÎ×ÅÌÓ 0  Ñ ÑÅÐÂÈÑÎÌ 0,10
    DO $$BEGIN
    INSERT INTO visitsboundserveses(idvisit, idservices) VALUES (0,1);
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'its works';

    END $$;
    -- ÎØÈÁÎ×ÍÀß ÇÀÏÈÑÜ
    INSERT INTO patients(idpatients, sex, birthdate, medicalid) VALUES(1, 0,current_date,1);
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                1,
                1,
                1,
                current_date + interval'1 day',
                current_time
                );
    INSERT INTO visitsboundserveses(idvisit, idservices) VALUES (1,1);
    -- ÏÀÖÈÅÍÒ 1 ÍÀ ÂÈÇÈÒ 1 Ê ÐÀÁÎ×ÅÌÓ 1  Ñ ÑÅÐÂÈÑÎÌ 1


commit;

--CLEAN
DELETE FROM specializationboundserveses WHERE (TRUE);
DELETE FROM visitsboundserveses WHERE (TRUE);
DELETE FROM services WHERE(TRUE);
DELETE FROM specializationboundserveses WHERE (TRUE);
DELETE FROM visits WHERE (TRUE);
DELETE FROM patients WHERE (TRUE);
DELETE FROM workers WHERE (TRUE);
DELETE FROM specializations WHERE (TRUE);


begin;  --25,26,27
    CREATE OR REPLACE FUNCTION add_visit_t()
      RETURNS TRIGGER
      AS $$
      BEGIN
        IF (
            ((
                    SELECT activitytype FROM activity WHERE (
                    (new.idworker = activity.idworker)
                    ) ORDER BY activitydate DESC LIMIT 1
                ) = 'inactive') OR
                (
                    SELECT activitytype FROM activity WHERE (
                    (new.idworker = activity.idworker)
                    ) ORDER BY activitydate LIMIT 1
                ) = 'was dismissed'
            ) THEN
            RAISE EXCEPTION 'error: worker  inactive';
        END IF;
        IF EXISTS(
            SELECT idpatient,idworker,date,time FROM visits
            WHERE (
                    (
                        (date = new.date) AND (time = new.time) AND (idworker = new.idworker)
                    )
                OR  (
                        (idpatient = new.idpatient)  AND (date = new.date) AND (time = new.time)
                    )
                )
            ) THEN
            RAISE EXCEPTION 'error: this vist already exist or ';
        END IF;
        IF (
                (new.date < current_date) and (new.time < current_time)
            ) THEN
            RAISE EXCEPTION 'error: ti 3.14***, tak nelza';
        END IF;
        RETURN new;
      END;
      $$
    LANGUAGE 'plpgsql';


    DROP TRIGGER IF EXISTS add_visit ON visits;
    CREATE TRIGGER add_visit
    BEFORE INSERT ON visits
    FOR EACH ROW
    EXECUTE PROCEDURE add_visit_t();
commit;

begin;
    INSERT INTO specializations(idspecializations, specializations) VALUES (0,'test0');
    INSERT INTO workers(idworker, name, idspecialization, sex, birthdate)
        VALUES (0,'test0', 0, 0, current_date);
    INSERT INTO services(idservices, description) VALUES(0, 'test0');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (0, 0);
    INSERT INTO services(idservices, description) VALUES(10, 'test10');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (10, 0);
    -- ÏÅÐÂÛÉ ÐÀÁÎ×ÈÉ ÑÏÅÖÈÀÀËÈÇÀÀÖÈÈ 0 ÑÅÐÂÈÑÀ 0,10


    INSERT INTO specializations(idspecializations, specializations) VALUES (1,'test1');
    INSERT INTO workers(idworker, name, idspecialization, sex, birthdate)VALUES (1, 'test1', 1, 0, current_date);
    INSERT INTO services(idservices, description) VALUES(1, 'test1');
    INSERT INTO specializationboundserveses(idservises, idspecialization)VALUES (1, 1);
    -- ÂÒÎÐÎÉ ÐÀÁÎ×ÈÉ ÑÏÅÖÈÀËÈÇÀÖÈÈ 1 CÅÐÂÈÑÀ 1

    INSERT INTO patients(idpatients, sex, birthdate, medicalid) VALUES(0, 0,current_date,0);
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                0,
                0,
                0,
                current_date + interval'1 day',
                time'10:10'
                );
    -- ÏÀÖÈÅÍÒ 0 ÍÀ ÂÈÇÈÒ 0 Ê ÐÀÁÎ×ÅÌÓ 0
    DO $$BEGIN
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                1,
                1,
                0,
                current_date + interval'1 day',
                time'10:10'
                );
    EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'its works';

    END $$;
    -- ÏÀÖÈÅÍÒ 0 ÍÀ ÂÈÇÈÒ 1 Ê ÐÀÁÎ×ÅÌÓ 1
    -- ÎØÈÁÊÀ 1 çàïèñü ê ðàçíîìó âðà÷ó â 1 âðåìÿ
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                1,
                1,
                0,
                current_date + interval'1 day',
                time'10:20'
                );
    -- ÏÐÀÂÈËÜÍÀß ÇÀÏÈÑÜ
    INSERT INTO patients(idpatients, sex, birthdate, medicalid) VALUES(1, 0,current_date,0);
    DO $$BEGIN
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                2,
                0,
                1,
                current_date + interval'1 day',
                time'10:10'
                );
    EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'its works';

    END $$;
    -- ÏÀÖÈÅÍÒ 1 ÍÀ ÂÈÇÈÒ 2 Ê ÐÀÁÎ×ÅÌÓ 0
    -- ÎØÈÁÊÀ
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                2,
                0,
                1,
                current_date + interval'1 day',
                time'10:20'
               );

    -- ÏÐÀÂÈËÜÍÀß ÇÀÏÈÑÜ
    DO $$BEGIN
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                3,
                0,
                1,
                current_date - interval'1 day',
                current_time - time'10:10'
                );
    EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'its works';

    END $$;
    -- îøèáêà  Çàäíåå ÷èñëî

    INSERT INTO activity(activitytype, activitydate, idworker) VALUES ('inactive',current_date+INTERVAL'2 day',0);
    DO $$BEGIN
        INSERT INTO visits(idvisit, idworker, idpatient, date, time)
            VALUES (
                    3,
                    0,
                    1,
                    current_date + INTERVAL '3 day',
                    current_time + time'10:10'
                    );
        EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'its works';

    END $$;
    INSERT INTO activity(activitytype, activitydate, idworker) VALUES ('active',current_date+INTERVAL'5 day',0);
    INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                3,
                0,
                1,
                current_date + INTERVAL '6 day',
                current_time + time'10:10'
                );
    commit;

begin; --28
    CREATE OR REPLACE FUNCTION activity_action_t()
      RETURNS TRIGGER
      AS $$
      BEGIN
        IF (
            (new.activitytype = 'inactive') OR
            (new.activitytype = 'was dismissed')
            )THEN
                IF EXISTS(
                    SELECT * FROM visits WHERE (
                        (visits.idworker >= NEW.idworker) AND
                        (visits.date >= NEW.activitydate)
                        )
                )THEN
                    RAISE EXCEPTION 'error: some vistits on this time';
                END IF ;
        END IF ;

        RETURN new;
      END;
      $$
    LANGUAGE 'plpgsql';


    DROP TRIGGER IF EXISTS activity_action ON activity;
    CREATE TRIGGER activity_action
    BEFORE INSERT ON activity
    FOR EACH ROW
    EXECUTE PROCEDURE activity_action_t();
commit;

begin;
INSERT INTO visits(idvisit, idworker, idpatient, date, time)
        VALUES (
                4,
                0,
                1,
                current_date + INTERVAL '20 day',
                current_time + time'10:10'
                );
    commit;
     DO $$BEGIN
        INSERT INTO activity(activitytype, activitydate, idworker) VALUES ('inactive',current_date+INTERVAL'7 day',0);
        EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'its works';

    END $$;
    commit;
    DO $$BEGIN
        INSERT INTO activity(activitytype, activitydate, idworker) VALUES ('was dismissed',current_date+INTERVAL'7 day',0);
        EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'its works';

    END $$;
    commit;
commit;

    --CLEAN
    DELETE FROM specializationboundserveses WHERE (TRUE);
    DELETE FROM visitsboundserveses WHERE (TRUE);
    DELETE FROM services WHERE(TRUE);
    DELETE FROM specializationboundserveses WHERE (TRUE);
    DELETE FROM visits WHERE (TRUE);
    DELETE FROM patients WHERE (TRUE);
    DELETE FROM workers WHERE (TRUE);
    DELETE FROM specializations WHERE (TRUE);