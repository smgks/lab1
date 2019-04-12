import sys



from ui import ui_main

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QErrorMessage



from PyQt5 import QtSql
from PyQt5.QtCore import QObject

class QuerySystem(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.db = QtSql.QSqlDatabase

        self.db = self.db.addDatabase('QPSQL')
        self.db.setHostName('127.0.0.1')
        self.db.setPort(5432)
        self.db.setDatabaseName('postgres')
        self.db.setUserName('postgres')
        self.db.setPassword('postgres')
        self.query = QtSql.QSqlQuery()
        self.db.open()
        self.error = QErrorMessage()
    def __execute(self,qu):
        tmp_sq = QtSql.QSqlQuery(self.db)
        if tmp_sq.exec(qu):
            tmp_sq.finish()
        else:
            er_text = tmp_sq.lastError().text()
            self.error.showMessage(er_text.__str__())
            tmp_sq.finish()
    # was dismissed

    def t13_workers_of_patient(self, date_from, date_to, id_worker):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('''select distinct visits.idpatient, idworker from patients
    inner join visits on (patients.idpatients = visits.idpatient)
where ((date >= '%s') and (date <= '%s') and (visits.idpatient = %s));''' % (date_from, date_to, id_worker)))
        return model

    def t14_patients_of_worker(self, date_from, date_to, id_worker):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('''select distinct visits.idworker,idpatient from workers
    inner join visits on (workers.idworker = visits.idworker)
where ((date >= '%s') and (date <= '%s') and (visits.idworker = %s));''' % (date_from, date_to, id_worker)))
        return model

    def t15_visits_popularity(self, date_from, date_to):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('''select distinct services.idservices, count(services.idservices) over (PARTITION BY services.idservices) from visits
    inner join visitsboundserveses on (visits.idvisit = visitsboundserveses.idvisit)
    inner join services on (visitsboundserveses.idservices = services.idservices)
where ((date >= '%s') and (date <= '%s'));''' % (date_from, date_to)))
        return model

    def t17_workers_salary(self, date_from, date_to):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('''select distinct idworker, sum(price) OVER (PARTITION BY visits.idworker) from visits
    inner join visitsboundserveses on (visits.idvisit = visitsboundserveses.idvisit)
    inner join services on (visitsboundserveses.idservices = services.idservices)
where ((date >= '%s') and (date <= '%s'));''' % (date_from, date_to)))
        return model

    def t18_patient_expenses(self, date_from, date_to):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('''select distinct idpatient, sum(price) OVER (PARTITION BY visits.idpatient) from visits
    inner join visitsboundserveses on (visits.idvisit = visitsboundserveses.idvisit)
    inner join services on (visitsboundserveses.idservices = services.idservices)
where ((date >= '%s') and (date <= '%s'));''' % (date_from, date_to)))
        return model

    def t12_reg_visit(self, id_patient, id_worker, id_service, date, time):
        query_0 = '''with rowse as (
                            insert into visits(idpatient, date, time, idworker) 
        values (%s , '%s', '%s', %s) returning idvisit
                        ) insert into visitsboundserveses(idvisit, idservices) VALUES'''  % (id_patient, date, time ,id_worker)
        temp = id_service.split()
        for i in range(temp.__len__()):
            query_0 += ('''((select idvisit from rowse), %s)''' % (temp[i]))
            if i != (temp.__len__() - 1):
                query_0 += ','
        query_0 += ';'
        self.__execute(query_0)
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from visits'))
        return model

    def t11_find_worker(self, from_dafe, to_date, spec):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('''with temp_row as(
                  select * from visits where ((date > '%s') and (date < '%s'))
        ) select idvisit,idpatient,workers.idworker,date,time,idspecialization from temp_row inner join workers on (workers.idspecialization = %s);
''' % (from_dafe, to_date, spec)))
        return model

    def t10_activity_active(self, id, date):
        self.__execute('''insert into activity(activitytype, activitydate, idworker) 
                        values ('active', '%s', %s)''' % (date, id))
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from activity'))
        return model

    def t10_activity_inactive(self, id, date):
        self.__execute('''insert into activity(activitytype, activitydate, idworker) 
                values ('inactive', '%s', %s)''' % (date, id))
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from activity'))
        return model

    def t10_activity_dissmis(self, id, date):
        self.__execute('''insert into activity(activitytype, activitydate, idworker) 
        values ('was dismissed', '%s', %s)''' % (date, id))
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from activity'))
        return model

    def t09_workers_add(self, name, sex, specid, birthdate):
        self.__execute('''insert
        into
        workers(name, sex, idspecialization, birthdate)
        VALUES('%s', %s, %s, '%s');''' % (name, sex, specid, birthdate))
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from workers'))
        return model

    def t09_patients(self):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from patients'))
        return model

    def t09_patient_remove(self, id):
        self.__execute('''delete from patients where patients.idpatients = ''' + id)
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from patients'))
        return model

    def t09_patient_add(self,sex , name, birthdate, medicalid):
        self.__execute('''insert into patients(sex, name, birthdate, medicalid) values (%s,'%s','%s','%s')''' % (sex,name,birthdate,medicalid))
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from patients'))
        return model

    def t09_services(self):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from services'))
        return model

    def t09_services_remove(self,id):
        self.__execute('''delete from services where services.idservices = ''' + id)
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from services'))
        return model

    def t09_services_add(self, desc, price, linked_id_spec):
        query_0 = '''
        with rowse as (
            insert into services (description, price) VALUES ('%s', %s) returning idservices
        ) insert into specializationboundserveses(idservises, idspecialization) 
            VALUES ''' % (desc, price)
        temp = linked_id_spec.split()
        for i in range(temp.__len__()):
            query_0 += ('''((select idservices from rowse), %s)''' % (temp[i]))
            if i != (temp.__len__()-1):
                query_0 += ','
        query_0 += ';'
        self.__execute(query_0)
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from services'))
        return model

    def t09_spec_add(self, desc, linked_id_serv):
        query_0 = '''
                with rowse as (
                    insert into specializations(specializations) VALUES ('%s') returning idspecializations
                ) insert into specializationboundserveses(idservises, idspecialization) 
                    VALUES ''' % (desc)
        temp = linked_id_serv.split()
        for i in range(temp.__len__()):
            query_0 += ('''(%s, (select idspecializations from rowse))''' % (temp[i]))
            if i != (temp.__len__() - 1):
                query_0 += ','
        query_0 += ';'
        self.__execute(query_0)
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from specializations'))
        return model

    def t09_spec(self):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from specializations'))
        return model

    def t09_spec_remove(self, id):
        self.__execute('''delete from specializations where specializations.idspecializations = ''' + id)
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from specializations'))
        return model

    def t09_workers(self):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from workers'))
        return model

    def t09_workers_remove(self,id):
        self.__execute('''delete from  workers where  workers.idworker = ''' + id)
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from  workers'))
        return model

    def t10_activity(self):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('select * from activity'))
        return model
    def t16_visit_coast(self):
        model = QtSql.QSqlQueryModel()
        model.setQuery(QtSql.QSqlQuery('''select distinct visits.idvisit,idpatient,patients.name,date,time,sum(price) 
        OVER (PARTITION BY visits.idvisit) from visits
    inner join visitsboundserveses on (visits.idvisit = visitsboundserveses.idvisit)
    inner join services on (visitsboundserveses.idservices = services.idservices)
    inner join patients on (patients.idpatients = visits.idpatient);'''))
        return model


class mainWin(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)








class UiSystem(QObject):
    def __init__(self):
        super().__init__()
        self.qu_s = QuerySystem()
        self.win = mainWin()
        self.win.show()
        self.win.verticalLayout.addWidget(QWidget())

        # show section
        self.win.t09_patients.clicked.connect(self.ont09_patients)
        self.win.t09_services.clicked.connect(self.ont09_services)
        self.win.t09_spec.clicked.connect(self.ont09_spec)
        self.win.t09_workers.clicked.connect(self.ont09_workers)
        self.win.t10_activity.clicked.connect(self.ont10_activity)
        self.win.t16_visit_coast.clicked.connect(self.ont16_visit_coast)
        self.win.t18_patient_expenses.clicked.connect(self.ont18_patient_expenses)
        self.win.t17_workers_salary.clicked.connect(self.ont17_workers_salary)
        self.win.t15_visits_popularity.clicked.connect(self.ont15_visits_popularity)
        self.win.t11_find_worker.clicked.connect(self.ont11_find_worker)
        self.win.t14_patients_of_worker.clicked.connect(self.ont14_patients_of_worker)
        self.win.t13_workers_of_patient.clicked.connect(self.ont13_workers_of_patient)

        # remove
        self.win.t09_patient_remove.clicked.connect(self.ont09_patient_remove)
        self.win.t09_services_remove.clicked.connect(self.ont09_services_remove)
        self.win.t09_spec_remove.clicked.connect(self.ont09_spec_remove)
        self.win.t09_workers_remove.clicked.connect(self.ont09_workers_remove)

        # add
        self.win.t09_patient_add.clicked.connect(self.ont09_patient_add)
        self.win.t09_services_add.clicked.connect(self.ont09_services_add)
        self.win.t09_spec_add.clicked.connect(self.ont09_spec_add)
        self.win.t09_workers_add.clicked.connect(self.ont09_workers_add)
        self.win.t12_reg_visit.clicked.connect(self.ont12_reg_visit)

        # state
        self.win.t10_activity_dissmis.clicked.connect(self.ont10_activity_dissmis)
        self.win.t10_activity_inactive.clicked.connect(self.ont10_activity_inactive)
        self.win.t10_activity_active.clicked.connect(self.ont10_activity_active)

    def ont13_workers_of_patient(self):
        self.win.table.setModel(
            self.qu_s.t13_workers_of_patient(
                self.win.t13_workers_of_patient_from.date().toString('yyyy-MM-dd'),
                self.win.t13_workers_of_patient_to.date().toString('yyyy-MM-dd'),
                self.win.t13_workers_of_patient_patient_id.text()
            )
        )

    def ont14_patients_of_worker(self):
        self.win.table.setModel(
            self.qu_s.t14_patients_of_worker(
                self.win.t14_patients_of_worker_from.date().toString('yyyy-MM-dd'),
                self.win.t14_patients_of_worker_to.date().toString('yyyy-MM-dd'),
                self.win.t14_patients_of_worker_worker_id.text()
            )
        )

    def ont15_visits_popularity(self):
        self.win.table.setModel(
            self.qu_s.t15_visits_popularity(
                self.win.t15_visits_popularity_from.date().toString('yyyy-MM-dd'),
                self.win.t15_visits_popularity_to.date().toString('yyyy-MM-dd')
            )
        )

    def ont17_workers_salary(self):
        self.win.table.setModel(
            self.qu_s.t18_patient_expenses(
                self.win.t17_workers_salary_from.date().toString('yyyy-MM-dd'),
                self.win.t17_workers_salary_to.date().toString('yyyy-MM-dd')
            )
        )

    def ont18_patient_expenses(self):
        self.win.table.setModel(
            self.qu_s.t18_patient_expenses(
                self.win.t18_patient_expenses_from.date().toString('yyyy-MM-dd'),
                self.win.t18_patient_expenses_to.date().toString('yyyy-MM-dd')
            )
        )

    def ont12_reg_visit(self, pressed):
        self.win.table.setModel(
            self.qu_s.t12_reg_visit(
                self.win.t12_reg_visit_patient_id.text(),
                self.win.t12_reg_visit_worker_id.text(),
                self.win.t12_reg_visit_services_id.text(),
                self.win.dateTimeEdit.date().toString('yyyy-MM-dd'),
                self.win.dateTimeEdit.time().toString('HH:mm')
            )
        )

    def ont11_find_worker(self, pressed):
        self.win.table.setModel(
            self.qu_s.t11_find_worker(
                self.win.t11_find_worker_from.dateTime().toString('yyyy-MM-dd'),
                self.win.t11_find_worker_to.dateTime().toString('yyyy-MM-dd'),
                self.win.t11_find_worker_spec_id.text()
            )
        )

    def ont10_activity_active(self, pressed):
        self.win.table.setModel(
            self.qu_s.t10_activity_active(
                self.win.t10_activity_active_worker_id.text(),
                self.win.t10_activity_date.dateTime().toString('yyyy-MM-dd')
            )
        )

    def ont10_activity_inactive(self, pressed):
        self.win.table.setModel(
            self.qu_s.t10_activity_inactive(
                self.win.t10_activity_active_worker_id.text(),
                self.win.t10_activity_date.dateTime().toString('yyyy-MM-dd')
            )
        )

    def ont10_activity_dissmis(self, pressed):
        self.win.table.setModel(
            self.qu_s.t10_activity_dissmis(
                self.win.t10_activity_active_worker_id.text(),
                self.win.t10_activity_date.dateTime().toString('yyyy-MM-dd')
            )
        )

    def ont09_workers_add(self, pressed):
        self.win.table.setModel(
            self.qu_s.t09_workers_add(
                self.win.t09_workers_name.text(),
                self.win.t09_workers_sex.text(),
                self.win.t09_workers_spec.text(),
                self.win.t09_workers_birthdate.dateTime().toString('yyyy-MM-dd')
            )
        )

    def ont09_spec_add(self, pressed):
        self.win.table.setModel(
            self.qu_s.t09_spec_add(
                self.win.t09_spec_description.text(),
                self.win.t09_spec_linked_serv.text())
        )

    def ont09_workers_remove(self, pressed):
        self.win.table.setModel(self.qu_s.t09_workers_remove(self.win.t09_workers_id.text()))

    def ont09_services_remove(self, pressed):
        self.win.table.setModel(self.qu_s.t09_services_remove(self.win.t09_services_id.text()))

    def ont09_spec_remove(self, pressed):
        self.win.table.setModel(self.qu_s.t09_spec_remove(self.win.t09_spec_id.text()))

    def ont16_visit_coast(self, pressed):
        self.win.table.setModel(self.qu_s.t16_visit_coast())

    def ont09_services_add(self, pressed):
        self.win.table.setModel(
            self.qu_s.t09_services_add(self.win.t09_services_description.text(),
                                       self.win.t09_services_price.text(),
                                       self.win.t09_services_linked_spec.text()))

    def ont09_patients(self, pressed):
        self.win.table.setModel(self.qu_s.t09_patients())

    def ont09_patient_remove(self, pressed):
        self.win.table.setModel(
            self.qu_s.t09_patient_remove(self.win.t09_patient_id.text()))

    def ont09_patient_add(self, pressed):
        self.win.table.setModel(
            self.qu_s.t09_patient_add(str(self.win.t09_patient_sex.value()),
                                      self.win.t09_patient_name.text(),
                                      self.win.t09_patient_birthdate.dateTime().toString('yyyy-MM-dd'),
                                      self.win.t09_patient_medicalid.text()))

    def ont09_services(self, pressed):
        self.win.table.setModel(self.qu_s.t09_services())

    def ont09_spec(self, pressed):
        self.win.table.setModel(self.qu_s.t09_spec())

    def ont09_workers(self, pressed):
        self.win.table.setModel(self.qu_s.t09_workers())

    def ont10_activity(self, pressed):
        self.win.table.setModel(self.qu_s.t10_activity())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = UiSystem()

    app.exec_()
    sys.exit()
