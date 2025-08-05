import streamlit as st
from abc import ABC, abstractmethod
from datetime import datetime

# ----------------------------
# Abstract Base Class: Person
# ----------------------------
class Person(ABC):
    def _init_(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    @abstractmethod
    def show_details(self):
        pass

# ----------------------------
# Patient Class
# ----------------------------
class Patient(Person):
    def _init_(self, patient_id, name, age, gender, disease):
        super()._init_(name, age, gender)
        self.patient_id = patient_id
        self.disease = disease
        self.admitted_date = datetime.now().strftime("%Y-%m-%d")
        self.doctor_assigned = None

    def show_details(self):
        return f"[{self.patient_id}] {self.name} | Age: {self.age} | Disease: {self.disease} | Admitted: {self.admitted_date} | Doctor: {self.doctor_assigned or 'Not Assigned'}"

# ----------------------------
# Doctor Class
# ----------------------------
class Doctor(Person):
    def _init_(self, doctor_id, name, age, gender, specialization):
        super()._init_(name, age, gender)
        self.doctor_id = doctor_id
        self.specialization = specialization

    def show_details(self):
        return f"[{self.doctor_id}] Dr. {self.name} | {self.specialization} | Age: {self.age}"

# ----------------------------
# Appointment Class
# ----------------------------
class Appointment:
    def _init_(self, patient, doctor, date, time):
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time

    def show_details(self):
        return f"📅 {self.date} {self.time} | Patient: {self.patient.name} | Doctor: Dr. {self.doctor.name}"

# ----------------------------
# Billing Class
# ----------------------------
class Billing:
    def _init_(self, patient_id, treatment, cost):
        self.patient_id = patient_id
        self.treatment = treatment
        self.cost = cost
        self.date = datetime.now().strftime("%Y-%m-%d")

    def show_bill(self):
        return f"🧾 Bill - Patient ID: {self.patient_id} | Treatment: {self.treatment} | Cost: ₹{self.cost} | Date: {self.date}"

# ----------------------------
# Hospital System Class
# ----------------------------
class Hospital:
    def _init_(self):
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.bills = []

    def add_patient(self, patient):
        self.patients.append(patient)

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def assign_doctor(self, patient_id, doctor_id):
        patient = next((p for p in self.patients if p.patient_id == patient_id), None)
        doctor = next((d for d in self.doctors if d.doctor_id == doctor_id), None)
        if patient and doctor:
            patient.doctor_assigned = doctor.name
            return f"✅ Doctor {doctor.name} assigned to {patient.name}"
        return "❌ Invalid Patient ID or Doctor ID"

    def book_appointment(self, patient_id, doctor_id, date, time):
        patient = next((p for p in self.patients if p.patient_id == patient_id), None)
        doctor = next((d for d in self.doctors if d.doctor_id == doctor_id), None)
        if patient and doctor:
            appt = Appointment(patient, doctor, date, time)
            self.appointments.append(appt)
            return "📅 Appointment booked"
        return "❌ Invalid IDs"

    def generate_bill(self, patient_id, treatment, cost):
        bill = Billing(patient_id, treatment, cost)
        self.bills.append(bill)
        return bill.show_bill()


# ----------------------------
# Streamlit App
# ----------------------------
st.set_page_config(page_title="🏥 Hospital Management", layout="centered")
st.title("🏥 Hospital Management System")

# Create hospital object
if 'hospital' not in st.session_state:
    st.session_state.hospital = Hospital()

menu = st.sidebar.selectbox("Menu", ["Add Patient", "Add Doctor", "Assign Doctor", "Book Appointment", "View Patients", "View Doctors", "View Appointments", "Generate Bill", "View Bills"])
h = st.session_state.hospital

# ----------------------------
# MENU OPTIONS
# ----------------------------
if menu == "Add Patient":
    st.header("➕ Add Patient")
    pid = st.text_input("Patient ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    disease = st.text_input("Disease")
    if st.button("Add Patient"):
        h.add_patient(Patient(pid, name, age, gender, disease))
        st.success(f"Patient {name} added.")

elif menu == "Add Doctor":
    st.header("🩺 Add Doctor")
    did = st.text_input("Doctor ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    spec = st.text_input("Specialization")
    if st.button("Add Doctor"):
        h.add_doctor(Doctor(did, name, age, gender, spec))
        st.success(f"Doctor {name} added.")

elif menu == "Assign Doctor":
    st.header("🔄 Assign Doctor to Patient")
    pid = st.text_input("Patient ID")
    did = st.text_input("Doctor ID")
    if st.button("Assign"):
        result = h.assign_doctor(pid, did)
        st.info(result)

elif menu == "Book Appointment":
    st.header("📅 Book Appointment")
    pid = st.text_input("Patient ID")
    did = st.text_input("Doctor ID")
    date = st.date_input("Date").strftime("%Y-%m-%d")
    time = st.time_input("Time").strftime("%H:%M")
    if st.button("Book"):
        result = h.book_appointment(pid, did, date, time)
        st.info(result)

elif menu == "View Patients":
    st.header("🧑‍⚕ Patients List")
    if not h.patients:
        st.warning("No patients.")
    else:
        for p in h.patients:
            st.write(p.show_details())

elif menu == "View Doctors":
    st.header("👨‍⚕ Doctors List")
    if not h.doctors:
        st.warning("No doctors.")
    else:
        for d in h.doctors:
            st.write(d.show_details())

elif menu == "View Appointments":
    st.header("📅 All Appointments")
    if not h.appointments:
        st.warning("No appointments.")
    else:
        for a in h.appointments:
            st.write(a.show_details())

elif menu == "Generate Bill":
    st.header("💸 Generate Bill")
    pid = st.text_input("Patient ID")
    treatment = st.text_input("Treatment")
    cost = st.number_input("Cost", min_value=0.0)
    if st.button("Generate"):
        st.success(h.generate_bill(pid, treatment, cost))

elif menu == "View Bills":
    st.header("🧾 Billing Records")
    if not h.bills:
        st.warning("No bills.")
    else:
        for b in h.bills:
            st.write(b.show_bill())
