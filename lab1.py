import sys


from qu_s import QuerySystem
from ui import ui_main

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow




from PyQt5.QtCore import QObject


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
