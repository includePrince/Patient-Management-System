import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime
from num2words import num2words
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from tkinter import PhotoImage
from PIL import Image, ImageTk

#--------------------------
id = "admin"
password = "admin"
#--------------------------



# Functions

def focus_next_widget(event, next_widget):
    next_widget.focus_set()
    return "break"

def option_selected(var, next_widget):
    next_widget.focus_set()

def generate_bill_no():
    # Get the current date and time
    now = datetime.now()
    # Format the date and time as YYYYMMDDHHMM
    bill_no = now.strftime('%Y%m%d%H%M')
    return bill_no

def generate_registration_ids(prefix="VEH", start_sequence=1, count=1050):
    ids = []
    sequence = start_sequence
    letter = 'A'
    number = count

    while number > 9999:
        number = number - 10000
        letter = chr(ord(letter) + 1)
        if letter == 'Z' and number>9999:
            letter = 'A'
            sequence +=1
 

    reg_id = f"{prefix}{sequence:02d}{letter}{number:04d}"
    ids.append(reg_id)
    return ids

def generate_receipt_ids(prefix="VEHR", start_sequence='A', count=1050):
    ids = []
    sequence = start_sequence
    letter = 'A'
    number = count

    while number > 9999:
        number = number - 10000
        letter = chr(ord(letter) + 1)
        if letter == 'Z' and number>9999:
            letter = 'A'
            sequence = chr(ord(sequence) + 1)

 

    reg_id = f"{prefix}{sequence}{letter}{number:04d}"
    ids.append(reg_id)
    return ids

def get_current_date():
    return datetime.now().strftime("%d/%m/%Y")

def get_current_time():
    return datetime.now().strftime("%I:%M %p")

def convert_amount_to_words(amount):
    integer_part = int(amount)
    fractional_part = int(round((amount - integer_part) * 100))
    
    words = num2words(integer_part, to='cardinal', lang='en_IN')
    words += " Rupees"
    
    if fractional_part > 0:
        words += f" and {num2words(fractional_part, to='cardinal', lang='en_IN')} paise"
    
    words += " Only"

    return words.title()


# Function to merge generated bill with the template
def merge_with_template(bill_file_name, template_file_name):
    template = PdfReader(template_file_name)
    bill = PdfReader(bill_file_name)
    
    writer = PdfWriter()
    
    template_page = template.pages[0]
    for bill_page in bill.pages:
        merged_page = PageObject.create_blank_page(width=template_page.mediabox.width, height=template_page.mediabox.height)
        merged_page.merge_page(template_page)
        merged_page.merge_page(bill_page)
        writer.add_page(merged_page)
    
    with open(bill_file_name, "wb") as output_pdf:
        writer.write(output_pdf)

def exit():
    root.destroy()

# Login Frame Functions
# Function to check login credentials
def login():
    admin_id = login_admin_entry.get()
    passwrd = login_password_entry.get()
    if admin_id == id and passwrd == password:  
        show_main_page()
    else:
        messagebox.showerror("Error", "Invalid Admin Id or Password")

# Function to navigate to main page
def show_main_page():
    login_frame.pack_forget()
    main_menu_frame.pack()


# Main Menu Frame Functions
def main_menu_back():
    main_menu_frame.pack_forget()
    login_frame.pack()

def show_patient_registration_page():
    main_menu_frame.pack_forget()
    file_path = f"Data/registrations.txt"
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Step 2: Parse the content and update the values
    for line in lines:
        if line.startswith("registrations :"):
            registrations = int(line.split(': ')[1])
            registrations += 1
    patient_registration_registrationNo_entry.set(str(generate_registration_ids(count=registrations)[0]))
    patient_registration_admitDate_entry.set(get_current_date())
    patient_registration_frame.pack()

def show_add_services_page():
    main_menu_frame.pack_forget()
    add_services_frame.pack()


def show_updatePatient_page():
    main_menu_frame.pack_forget()
    updatePatient_frame.pack()


def show_money_receipt_page():
    main_menu_frame.pack_forget()
    money_receipt_frame.pack()

def show_discharge_bill_page():
    main_menu_frame.pack_forget()
    discharge_bill_frame.pack()


# Patient Registration Frame Functions
def patient_registration_back():
    patient_registration_page_reset()
    patient_registration_frame.pack_forget()
    main_menu_frame.pack()

def register_patient():
    patient_registration_registrationNo = patient_registration_registrationNo_entry.get()
    patient_registration_name = patient_registration_patientName_entry.get().strip().title()
    patient_registration_contact = patient_registration_contactNo_entry.get().strip()
    patient_registration_address = patient_registration_address_entry.get().strip().title()
    patient_registration_age = patient_registration_age_entry.get().strip()
    patient_registration_gender = patient_registration_gender_var.get().strip()
    patient_registration_co = patient_registration_co_entry.get().strip().title()
    patient_registration_so = patient_registration_so_entry.get().strip().title()
    patient_registration_admitDate = patient_registration_admitDate_entry.get().strip()
    patient_registration_consultant = patient_registration_consultant_entry.get().strip().title()
    patient_registration_ward = patient_registration_ward_var.get().strip()
    patient_registration_bedNo = patient_registration_bedNo_entry.get().strip()
    patient_registration_advanceAmount = patient_registration_advanceAmount_entry.get().strip()
    if patient_registration_advanceAmount == "":
        patient_registration_advanceAmount = "0"



    if patient_registration_registrationNo and patient_registration_name :
        if patient_registration_gender != "Select" and patient_registration_ward != "Select":
            try:            
                with open(f"Patients/{patient_registration_registrationNo}.txt", "w") as file:
                    file.write(f"Registration No. : {patient_registration_registrationNo}\nPatient Name : {patient_registration_name}\nContact No. : {patient_registration_contact}\nAddress : {patient_registration_address}\nAge : {patient_registration_age}\nGender : {patient_registration_gender}\nC/O : {patient_registration_co}\nS/O : {patient_registration_so}\nAdmit Date : {patient_registration_admitDate}\nConsultant : {patient_registration_consultant}\nWard : {patient_registration_ward}\nBed No. : {patient_registration_bedNo}\nPaid Amount : {float(patient_registration_advanceAmount)}\nServices : ")
                messagebox.showinfo("Success", "Patient registered successfully!")
                file_path = f"Data/registrations.txt"
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                # Step 2: Parse the content and update the values
                updated_lines = []
                for line in lines:
                    if line.startswith("registrations :"):
                        registrations = int(line.split(': ')[1])
                        registrations += 1
                        updated_lines.append(f"registrations : {registrations}\n")
                    else:
                        updated_lines.append(line)

                            # Step 3: Write the updated content back to the file
                with open(file_path, 'w') as file:
                    file.writelines(updated_lines)


                # Create a new PDF with customer details and products
                pdf_filename = f"Registration Slips/{patient_registration_registrationNo}_Registration_Slip.pdf"
                c = canvas.Canvas(pdf_filename, pagesize=(595.2, 421.68))
                c.setFont("Helvetica", 9)

                # Add customer details

                c.drawString(84, 230, patient_registration_registrationNo)  # Reg. No.
                c.drawString(247, 230, patient_registration_name)  # Patient Name
                c.drawString(468, 230, patient_registration_age)  # Age
                c.drawString(529, 230, patient_registration_gender)  # Gender

                c.drawString(84, 220, patient_registration_contact)  # Contact
                c.drawString(68, 210, patient_registration_co)  # C/O
                c.drawString(69, 200, patient_registration_so)  # S/O

                c.drawString(84, 188, patient_registration_address)  # Address


                c.drawString(468, 186, patient_registration_advanceAmount)  # Paid Amount

                c.save()

                # Merge with template
                template_filename = "Data/Templates/Hospital_Registration_Slip.pdf"  # The template file should be available in the same directory
                merge_with_template(pdf_filename, template_filename)
                messagebox.showinfo("Success", f"receipt generated: {pdf_filename}")

                directory = "Registration Slips"
                pdf_filename = os.path.join(directory, f"{patient_registration_registrationNo}_Registration_Slip.pdf")
                try:
                    if os.name == 'nt':  # For Windows
                        os.startfile(pdf_filename)
                    elif os.name == 'posix':  # For macOS and Linux
                        os.system(f'open "{pdf_filename}"')  # macOS
                        os.system(f'xdg-open "{pdf_filename}"')  # Linux
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to open PDF file: {e}")

                patient_registration_page_reset()
                patient_registration_frame.pack_forget()
                main_menu_frame.pack()
            except ValueError:
                messagebox.showerror("Input Error", "Advance Amount should be in real number")

        else:
            messagebox.showerror("Error", "Please Select in Gender and Ward.")
    else:
        messagebox.showerror("Error", "Patient Name are required.")
    
def patient_registration_page_reset():
    patient_registration_registrationNo_entry.set("")
    patient_registration_patientName_entry.delete(0, tk.END)
    patient_registration_contactNo_entry.delete(0, tk.END)
    patient_registration_address_entry.delete(0, tk.END)
    patient_registration_age_entry.delete(0, tk.END)
    patient_registration_gender_var.set("Select")
    patient_registration_co_entry.delete(0, tk.END)
    patient_registration_so_entry.delete(0, tk.END)
    patient_registration_admitDate_entry.set("")
    patient_registration_consultant_entry.delete(0, tk.END)
    patient_registration_ward_var.set("Select")
    patient_registration_bedNo_entry.delete(0, tk.END)
    patient_registration_advanceAmount_entry.delete(0, tk.END)




# Add Services Frame Functions
def add_services_back():
    add_services_page_reset()
    add_services_frame.pack_forget()
    main_menu_frame.pack()

def add_services_fetch_patient_details():
    add_services_entry_reset()
    patient_registrationNo = add_services_registrationNo_entry.get().strip()
    try:
        with open(f"Patients/{patient_registrationNo}.txt", "r") as file:
            patient_details = file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "Patient not found")
        return
    
    z = 1
    for line in patient_details.split("\n"):
        a = 0
        for i in range(len(line)):
            if line[i] == ':':
                a = i + 1
                
        line = line[a:]
        if z == 1:
            add_services_registrationNo_fetched.set(line.strip())
        elif z == 2:
            add_services_patientName_fetched.set(line)
        elif z == 3:
            add_services_contactNo_fetched.set(line)
       
        z = z+1


def add_service():
    unit = add_services_unit_var.get().strip()
    qty = add_services_qty_entry.get().strip()
    service = add_services_particulars_manual_var.get().strip()
    price = add_services_price_manual_var.get().strip()
    aDt = add_services_aDate_manual_var.get().strip()
    iDt = add_services_iDate_manual_var.get().strip()


    add_services_patientName = add_services_patientName_fetched.get().strip()
    if add_services_patientName:
        if qty and unit!="Select" and service and price:
            try:
                amount = float(qty) * float(price) 
                add_services_tree.insert("", "end", values=(service, aDt, iDt, unit, qty, price, amount))
                # Clear the entry fields
                add_services_particulars_var.set("Select a Service")
                add_services_aDate_manual_var.set(get_current_date())
                add_services_iDate_manual_var.set(get_current_date())
                add_services_price_manual_var.set("")
                add_services_particulars_manual_var.set("")
                add_services_unit_var.set("Select")
                add_services_qty_entry.set("")
                add_services_amount_entry.set("")
            except ValueError:
                messagebox.showerror("Input Error", "Unit, Qty and Rate should be numbers")
        else:
            messagebox.showerror("Input Error", "Please fill in all fields")
    else:
        messagebox.showerror("Input Error", "Please find a Patient First")



def add_services_submit():
# Step 1: Read the file content
    total = 0.0 
    due = 0.0
    add_services_registrationNo = add_services_registrationNo_fetched.get()
    try:
        file_path = f"Patients/{add_services_registrationNo}.txt"

        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Step 2: Parse the content and update the values
        updated_lines = []
        for line in lines:
            if line.startswith("Services :"):
                existing_services = line
                existing_services = existing_services.strip()
                for line in add_services_tree.get_children():
                    particulars, adate, idate, unit, qty, rate, amount = add_services_tree.item(line, "values")
                    new_services = f"\n{particulars}, {adate}, {idate}, {unit}, {qty}, {rate}, {amount}"
                    existing_services += new_services

                updated_lines.append(f"{existing_services}\n")
            else:
                updated_lines.append(line)
        # Step 3: Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)
        messagebox.showinfo("Success", f"Services Added")
        add_services_page_reset()
    except FileNotFoundError:
        messagebox.showerror("Error", "Patient not found")
        return

    
def add_services_page_reset():
    add_services_registrationNo_entry.delete(0, tk.END)
    add_services_registrationNo_fetched.set("")
    add_services_patientName_fetched.set("")
    add_services_contactNo_fetched.set("")
    add_services_particulars_var.set("Select a Service")
    add_services_particulars_manual_var.set("")
    add_services_price_manual_var.set("")
    add_services_unit_var.set("Select")
    add_services_qty_entry.set("")
    for item in add_services_tree.get_children():
        add_services_tree.delete(item)

def add_services_entry_reset():
    add_services_particulars_var.set("Select a Service")
    add_services_price_manual_var.set("")
    add_services_particulars_manual_var.set("")
    add_services_unit_var.set("Select")
    add_services_qty_entry.set("")
    for item in add_services_tree.get_children():
        add_services_tree.delete(item)

def add_services_read_services(file_path):
    services = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ',' in line:
                service, price = line.split(',')
                services[service.strip()] = int(price.strip())
    return services



# Money receipt Frame Functions
def money_receipt_back():
    money_receipt_page_reset()
    money_receipt_frame.pack_forget()
    main_menu_frame.pack()

def money_receipt_fetch_patient_details():
    money_receipt_entry_reset()
    
    patient_registrationNo = money_receipt_registrationNo_entry.get().strip()
    try:
        with open(f"Patients/{patient_registrationNo}.txt", "r") as file:
            patient_details = file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "Patient not found")
        return
    
    
    
    z = 1
    for line in patient_details.split("\n"):
        a = 0
        for i in range(len(line)):
            if line[i] == ':':
                a = i + 1
                
        line = line[a:]
        if z == 1:
            money_receipt_registrationNo_fetched.set(line)
        elif z == 2:
            money_receipt_patientName_fetched.set(line)
        elif z == 3:
            money_receipt_contactNo_fetched.set(line)
        elif z == 4:
            money_receipt_address_fetched.set(line)
        elif z == 5:
            money_receipt_age_fetched.set(line)
        elif z == 6:
            money_receipt_gender_fetched.set(line)
        elif z == 11:
            money_receipt_ward_fetched.set(line)
        elif z == 12:
            money_receipt_bedNo_fetched.set(line)            
       
        z = z+1
    date = get_current_date()
    time = get_current_time()
    money_receipt_date_entry.set(date)
    money_receipt_time_fetched.set(time)

    file_path1 = f"Data/registrations.txt"
    with open(file_path1, 'r') as file:
        lines = file.readlines()
    # Step 2: Parse the content and update the values
    for line in lines:
        if line.startswith("receipts :"):
            receipts = int(line.split(': ')[1])
            receipts += 1

    money_receipt_receiptNo_entry.set(str(generate_receipt_ids(count=receipts)[0]))

    # Auto receipt No. Generator ------------------

def money_receipt_generate_receipt():
    money_receipt_receiptNo = money_receipt_receiptNo_entry.get().strip()
    money_receipt_date = money_receipt_date_entry.get().strip()
    money_receipt_time = money_receipt_time_fetched.get().strip()
    money_receipt_age = money_receipt_age_fetched.get().strip()
    money_receipt_gender = money_receipt_gender_fetched.get().strip()
    money_receipt_contactNo = money_receipt_contactNo_fetched.get().strip()
    money_receipt_registrationNo = money_receipt_registrationNo_fetched.get().strip()
    money_receipt_patientName = money_receipt_patientName_fetched.get().strip()
    money_receipt_address = money_receipt_address_fetched.get().strip()
    money_receipt_ward = money_receipt_ward_fetched.get().strip()
    money_receipt_bedNo = money_receipt_bedNo_fetched.get().strip()
    money_receipt_modeOfPay = money_receipt_modeOfPay_var.get().strip()
    money_receipt_paid_amount = money_receipt_paidAmount_entry.get().strip()

    if money_receipt_patientName:
        if money_receipt_modeOfPay != "Select" and money_receipt_paid_amount:
            try:
                money_receipt_amount_words = convert_amount_to_words(float(money_receipt_paid_amount.strip()))
                 # Step 1: Read the file content
                file_path = f"Patients/{money_receipt_registrationNo}.txt"

                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Step 2: Parse the content and update the values
                updated_lines = []
                for line in lines:
                    if line.startswith("Paid Amount :"):
                        current_paid_amount = float(line.split(': ')[1])
                        new_paid_amount = current_paid_amount + float(money_receipt_paid_amount)
                        updated_lines.append(f"Paid Amount : {new_paid_amount}\n")
                    else:
                        updated_lines.append(line)

                # Step 3: Write the updated content back to the file
                with open(file_path, 'w') as file:
                    file.writelines(updated_lines)

                # Create a new PDF with customer details and products
                pdf_filename = f"Receipts/{money_receipt_registrationNo}_{money_receipt_receiptNo}_receipt.pdf"
                c = canvas.Canvas(pdf_filename, pagesize=(595.2, 421.68))
                c.setFont("Helvetica", 11)

                # Add customer details
                c.drawString(78, 274, money_receipt_receiptNo)  # Receipt No
                c.drawString(390, 274, money_receipt_date)  # Date
                c.drawString(530, 274, money_receipt_time)  # Time

                c.setFont("Helvetica", 10)
                c.drawString(58, 250, money_receipt_registrationNo)  # Reg. No.
                c.drawString(235, 250, money_receipt_patientName)  # Patient Name
                c.drawString(481, 250, money_receipt_age)  # Age
                c.drawString(550, 250, money_receipt_gender)  # Gender

                c.drawString(58, 232, money_receipt_contactNo)  # Contact

                c.drawString(58, 214, money_receipt_address)  # Address

                c.drawString(354, 232, money_receipt_ward)  # Ward
                c.drawString(481, 232, money_receipt_bedNo)  # Bed No.

                c.setFont("Helvetica", 12)
                c.drawString(116, 188, money_receipt_modeOfPay)  # Mode of Payment
                c.drawString(400, 188, money_receipt_paid_amount)  # Paid Amount

                c.setFont("Helvetica", 11)
                c.drawString(15, 147, money_receipt_amount_words)  # Amount In Words

                c.save()

                # Merge with template
                template_filename = "Data/Templates/Hospital_Money_Receipt.pdf"  # The template file should be available in the same directory
                merge_with_template(pdf_filename, template_filename)
                messagebox.showinfo("Success", f"receipt generated: {pdf_filename}")

                directory = "Receipts"
                pdf_filename = os.path.join(directory, f"{money_receipt_registrationNo}_{money_receipt_receiptNo}_receipt.pdf")
                try:
                    if os.name == 'nt':  # For Windows
                        os.startfile(pdf_filename)
                    elif os.name == 'posix':  # For macOS and Linux
                        os.system(f'open "{pdf_filename}"')  # macOS
                        os.system(f'xdg-open "{pdf_filename}"')  # Linux
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to open PDF file: {e}")

                file_path1 = f"Data/registrations.txt"
                with open(file_path1, 'r') as file:
                    lines = file.readlines()
                # Step 2: Parse the content and update the values
                updated_lines = []
                for line in lines:
                    if line.startswith("receipts :"):
                        receipts = int(line.split(': ')[1])
                        receipts += 1
                        updated_lines.append(f"receipts : {receipts}\n")
                    else:
                        updated_lines.append(line)

                            # Step 3: Write the updated content back to the file
                with open(file_path1, 'w') as file:
                    file.writelines(updated_lines)

                money_receipt_page_reset()
            except ValueError:
                messagebox.showerror("Input Error", "Paid Amount should be in real number")

        else:
            messagebox.showerror("Input Error", "Please fill Mode of Pay and Paid Amount")

    else:
        messagebox.showerror("Input Error", "Please find a Patient First")



   


def money_receipt_page_reset():
    money_receipt_registrationNo_entry.delete(0, tk.END)
    money_receipt_receiptNo_entry.set("")
    money_receipt_date_entry.set("")
    money_receipt_registrationNo_fetched.set("")
    money_receipt_patientName_fetched.set("")
    money_receipt_address_fetched.set("")
    money_receipt_ward_fetched.set("")
    money_receipt_bedNo_fetched.set("")
    money_receipt_modeOfPay_var.set("Select")
    money_receipt_paidAmount_entry.delete(0, tk.END)
    money_receipt_gender_fetched.set("")
    money_receipt_age_fetched.set("")
    money_receipt_contactNo_fetched.set("")

def money_receipt_entry_reset():
    money_receipt_modeOfPay_var.set("Select")
    money_receipt_paidAmount_entry.delete(0, tk.END)


# Update Patient Frame Functions
def updatePatient_back():
    updatePatient_page_reset()
    updatePatient_frame.pack_forget()
    main_menu_frame.pack()



def updatePatient_page_reset():
    updatePatient_registrationNo_entry.delete(0, tk.END)
    updatePatient_registrationNo_fetched.set("")
    updatePatient_patientName_fetched.set("")
    updatePatient_contactNo_fetched.set("")
    updatePatient_age_fetched.set("")
    updatePatient_gender_fetched.set("")
    updatePatient_address_fetched.set("")
    updatePatient_co_fetched.set("")
    updatePatient_so_fetched.set("")
    updatePatient_consultant_fetched.set("")
    updatePatient_ward_fetched.set("")
    updatePatient_bedNo_fetched.set("")
    updatePatient_admitDate_fetched.set("")
    for item in updatePatient_tree.get_children():
        updatePatient_tree.delete(item)


def updatePatient_fetch_patient_details():
    patient_registrationNo = updatePatient_registrationNo_entry.get().strip()
    try:
        with open(f"Patients/{patient_registrationNo}.txt", "r") as file:
            patient_details = file.read()
        updatePatient_entry_reset()
    except FileNotFoundError:
        messagebox.showerror("Error", "Patient not found")
        return
    total = 0.0
    z = 1
    for line in patient_details.split("\n"):
        a = 0
        for i in range(len(line)):
            if line[i] == ':':
                a = i + 1
                
        line = line[a:]
        if z == 1:
            updatePatient_registrationNo_fetched.set(line)
        elif z == 2:
            updatePatient_patientName_fetched.set(line)
        elif z == 3:
            updatePatient_contactNo_fetched.set(line)
        elif z == 4:
            updatePatient_address_fetched.set(line)
        elif z == 5:
            updatePatient_age_fetched.set(line)
        elif z == 6:
            updatePatient_gender_fetched.set(line)
        elif z == 7:
            updatePatient_co_fetched.set(line)
        elif z == 8:
            updatePatient_so_fetched.set(line)
        elif z == 9:
            updatePatient_admitDate_fetched.set(line)
        elif z == 10:
            updatePatient_consultant_fetched.set(line)
        elif z == 11:
            updatePatient_ward_fetched.set(line)          
        elif z == 12:
            updatePatient_bedNo_fetched.set(line)                     
        elif z > 14 and line.strip() != "":            
            parts = line.split(',')
            cost = float(parts[-1].strip())
            total = total + cost
        z = z+1


    with open(f"Patients/{patient_registrationNo}.txt", 'r') as file:
        content = file.read()
        
    # Extract the "Services" section
    services_section = content.split("Services :")[1].strip()
    services_lines = services_section.splitlines()
    
    # Process services data into a list of tuples
    services_data = [list(line.split(", ")) for line in services_lines]
    
    for row in services_data:
        updatePatient_tree.insert("", tk.END, values=row)
    

def updatePatient_entry_reset():
    for item in updatePatient_tree.get_children():
        updatePatient_tree.delete(item)


def updatePatient_update():
    updatePatient_registrationNo = updatePatient_registrationNo_fetched.get().strip()
    updatePatient_patientName = updatePatient_patientName_fetched.get().strip()
    updatePatient_contactNo = updatePatient_contactNo_fetched.get().strip()
    updatePatient_age = updatePatient_age_fetched.get().strip()
    updatePatient_gender = updatePatient_gender_fetched.get().strip()
    updatePatient_address = updatePatient_address_fetched.get().strip()
    updatePatient_co = updatePatient_co_fetched.get().strip()
    updatePatient_so = updatePatient_so_fetched.get().strip()
    updatePatient_consulant = updatePatient_consultant_fetched.get().strip()
    updatePatient_ward = updatePatient_ward_fetched.get().strip()
    updatePatient_bedNo = updatePatient_bedNo_fetched.get().strip()
    updatePatient_admitDate = updatePatient_admitDate_fetched.get().strip()

    file_path = f"Patients/{updatePatient_registrationNo}.txt"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Step 2: Parse the content and update the values
    updated_lines = []
    for line in lines:
        if line.startswith("Registration No. :"):
            updated_lines.append(line)
        elif line.startswith("Patient Name :"):            
            updated_lines.append(f"Patient Name : {updatePatient_patientName}\n")
        elif line.startswith("Contact No. :"):            
            updated_lines.append(f"Contact No. : {updatePatient_contactNo}\n")    
        elif line.startswith("Address :"):            
            updated_lines.append(f"Address : {updatePatient_address}\n") 
        elif line.startswith("Age :"):            
            updated_lines.append(f"Age : {updatePatient_age}\n") 
        elif line.startswith("Gender :"):            
            updated_lines.append(f"Gender : {updatePatient_gender}\n") 
        elif line.startswith("C/O :"):            
            updated_lines.append(f"C/O : {updatePatient_co}\n") 
        elif line.startswith("S/O :"):            
            updated_lines.append(f"S/O : {updatePatient_so}\n") 
        elif line.startswith("Admit Date :"):            
            updated_lines.append(f"Admit Date : {updatePatient_admitDate}\n") 
        elif line.startswith("Consultant :"):            
            updated_lines.append(f"Consultant : {updatePatient_consulant}\n") 
        elif line.startswith("Ward :"):            
            updated_lines.append(f"Ward : {updatePatient_ward}\n") 
        elif line.startswith("Bed No. :"):            
            updated_lines.append(f"Bed No. : {updatePatient_bedNo}\n") 
        elif line.startswith("Paid Amount :"):
            updated_lines.append(line)
        elif line.startswith("Services :"):
            updated_lines.append(line)
            for line in updatePatient_tree.get_children():
                particulars, adate, idate, unit, qty, rate, amount = updatePatient_tree.item(line, "values")
                updated_services = f"{particulars}, {adate}, {idate}, {unit}, {qty}, {rate}, {amount}\n"
                updated_lines.append(updated_services)
            
    # Step 3: Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)
    
    messagebox.showinfo("Success", f"Patient Updated")
    updatePatient_page_reset()




# Discharge Bill Frame Functions
def discharge_bill_back():
    discharge_bill_page_reset()
    discharge_bill_frame.pack_forget()
    main_menu_frame.pack()


def discharge_bill_fetch_patient_details():
    patient_registrationNo = discharge_bill_registrationNo_entry.get().strip()
    try:
        with open(f"Patients/{patient_registrationNo}.txt", "r") as file:
            patient_details = file.read()
        discharge_bill_entry_reset()
    except FileNotFoundError:
        messagebox.showerror("Error", "Patient not found")
        return
    total = 0.0
    z = 1
    for line in patient_details.split("\n"):
        a = 0
        for i in range(len(line)):
            if line[i] == ':':
                a = i + 1
                
        line = line[a:]
        if z == 1:
            discharge_bill_registrationNo_fetched.set(line)
        elif z == 2:
            discharge_bill_patientName_fetched.set(line)
        elif z == 3:
            discharge_bill_contactNo_fetched.set(line)
        elif z == 4:
            discharge_bill_address_fetched.set(line)
        elif z == 5:
            discharge_bill_age_fetched.set(line)
        elif z == 6:
            discharge_bill_gender_fetched.set(line)
        elif z == 7:
            discharge_bill_co_fetched.set(line)
        elif z == 8:
            discharge_bill_so_fetched.set(line)
        elif z == 9:
            discharge_bill_admitDate_fetched.set(line)
        elif z == 10:
            discharge_bill_consultant_fetched.set(line)
        elif z == 11:
            discharge_bill_ward_fetched.set(line)          
        elif z == 12:
            discharge_bill_bedNo_fetched.set(line)                     
        elif z == 13:
            line = round(float(line.strip()), 2)
            discharge_bill_totalPaidAmount_fetched.set(line)  
        elif z > 14 and line.strip() != "":            
            parts = line.split(',')
            cost = float(parts[-1].strip())
            total = total + cost
        z = z+1


    discharge_bill_billNo_entry.set(generate_bill_no())

    discharge_bill_subTotal_fetched.set(round(total, 2))
    date = get_current_date()
    time = get_current_time()
    discharge_bill_billDate_entry.set(date)
    discharge_bill_time_entry.set(time)
    discharge_bill_dischargeDate_entry.set(date)
    subTotal = float(discharge_bill_subTotal_fetched.get().strip())
    gst = 0.05 * subTotal
    discharge_bill_gst_fetched.set(round(gst,2))
    roundOff = subTotal + gst
    discharge_bill_roundOff_fetched.set(round(roundOff, 2))
    net = roundOff - float(discharge_bill_totalPaidAmount_fetched.get().strip())
    totalDueAmount = 0
    balanceAmount = 0
    if net > 0:
        totalDueAmount = net
    elif net < 0:
        balanceAmount = net * -1
    discharge_bill_totalDuesAmount_fetched.set(round(totalDueAmount,2))
    discharge_bill_balanceAmount_fetched.set(round(balanceAmount,2))


    with open(f"Patients/{patient_registrationNo}.txt", 'r') as file:
        content = file.read()
        
    # Extract the "Services" section
    services_section = content.split("Services :")[1].strip()
    services_lines = services_section.splitlines()
    
    # Process services data into a list of tuples
    services_data = [list(line.split(", ")) for line in services_lines]
    x = 1
    for lst in services_data:
        lst.insert(0, f"{x}.")
        x += 1
    for row in services_data:
        discharge_bill_tree.insert("", tk.END, values=row)
    
    
#------------------------------------------------------------------------------------------------------------





def discharge_bill_generate_bill():


    discharge_bill_billNo = discharge_bill_billNo_entry.get().strip()
    discharge_bill_date = discharge_bill_billDate_entry.get().strip()
    discharge_bill_time = discharge_bill_time_entry.get().strip()
    discharge_bill_registrationNo = discharge_bill_registrationNo_fetched.get().strip()
    discharge_bill_patientName = discharge_bill_patientName_fetched.get().strip() 
    discharge_bill_contactNo = discharge_bill_contactNo_fetched.get().strip()
    discharge_bill_age = discharge_bill_age_fetched.get().strip()
    discharge_bill_gender = discharge_bill_gender_fetched.get().strip()
    discharge_bill_address = discharge_bill_address_fetched.get().strip()
    discharge_bill_co = discharge_bill_co_fetched.get().strip()
    discharge_bill_so = discharge_bill_so_fetched.get().strip()
    discharge_bill_consulant = discharge_bill_consultant_fetched.get().strip()
    discharge_bill_ward = discharge_bill_ward_fetched.get().strip()
    discharge_bill_bedNo = discharge_bill_bedNo_fetched.get().strip()
    discharge_bill_admitDate = discharge_bill_admitDate_fetched.get().strip()
    discharge_bill_dischargeDate = discharge_bill_dischargeDate_entry.get().strip()
    discharge_bill_subTotal = discharge_bill_subTotal_fetched.get().strip()
    discharge_bill_gst = discharge_bill_gst_fetched.get().strip()
    discharge_bill_discount = discharge_bill_discount_entry.get().strip()
    if discharge_bill_discount == "":
        discharge_bill_discount = 0.0
    discharge_bill_discount = f"{round(float(discharge_bill_discount), 2)}"
    discharge_bill_roundOff = discharge_bill_roundOff_fetched.get().strip()
    discharge_bill_totalPaidAmount = discharge_bill_totalPaidAmount_fetched.get().strip()
    discharge_bill_totalDuesAmount = discharge_bill_totalDuesAmount_fetched.get().strip()
    discharge_bill_recievedAmount = discharge_bill_recievedAmount_fetched.get().strip()
    discharge_bill_balanceAmount = discharge_bill_balanceAmount_fetched.get().strip()
    discharge_bill_amount_words = convert_amount_to_words(float(discharge_bill_totalPaidAmount))

    if discharge_bill_discount != "":
        discharge_bill_roundOff = f"{round((float(discharge_bill_roundOff) - float(discharge_bill_discount)), 2)}"
        net = round((float(discharge_bill_roundOff) - float(discharge_bill_totalPaidAmount)) , 2)
        discharge_bill_balanceAmount = "0"
        discharge_bill_totalDuesAmount = "0"
        if net > 0:
            discharge_bill_totalDuesAmount = f"{net}"
        elif net < 0:
            discharge_bill_balanceAmount = f"{-1 * net}"


    if discharge_bill_patientName:
        

    # Create a new PDF with customer details and products
        pdf_filename = f"Discharge Bills/{discharge_bill_registrationNo}_{discharge_bill_billNo}.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica", 11)

        
        y = 555  # Starting y position for table entries


        # # Add customer details
        c.drawString(65, 681.7, discharge_bill_billNo)  # Bill No
        c.drawString(369, 681.7, discharge_bill_date)  # Date
        c.drawString(505, 681.7, discharge_bill_time)  # Time

        c.setFont("Helvetica", 10)

        c.drawString(64, 658, discharge_bill_registrationNo)  # Reg. No.
        c.drawString(240, 658, discharge_bill_patientName)  # Patient Name
        c.drawString(478, 658, discharge_bill_age)  # Age
        c.drawString(542, 658, discharge_bill_gender)  # Gender

        c.drawString(64, 647, discharge_bill_contactNo)  # Contact
        c.drawString(195, 647, discharge_bill_co)  # C/O
        c.drawString(360, 647, discharge_bill_so)  # S/O

        c.drawString(65, 634, discharge_bill_address)  # Address

        c.drawString(78, 611.5, discharge_bill_consulant)  # Consultant
        c.drawString(369, 611.5, discharge_bill_ward)  # Ward
        c.drawString(493, 611.5, discharge_bill_bedNo)  # Bed No.

        c.drawString(111, 598, discharge_bill_admitDate)  # Date Of Admission
        c.drawString(424, 598, discharge_bill_dischargeDate)  # Date Of Discharge



        for line in discharge_bill_tree.get_children():
            if y <= 130:
                c.showPage()
                c.setFont("Helvetica", 11)

                        # # Add customer details
                c.drawString(65, 681.7, discharge_bill_billNo)  # Bill No
                c.drawString(369, 681.7, discharge_bill_date)  # Date
                c.drawString(505, 681.7, discharge_bill_time)  # Time

                c.setFont("Helvetica", 10)

                c.drawString(64, 658, discharge_bill_registrationNo)  # Reg. No.
                c.drawString(240, 658, discharge_bill_patientName)  # Patient Name
                c.drawString(478, 658, discharge_bill_age)  # Age
                c.drawString(542, 658, discharge_bill_gender)  # Gender

                c.drawString(64, 647, discharge_bill_contactNo)  # Contact
                c.drawString(195, 647, discharge_bill_co)  # C/O
                c.drawString(360, 647, discharge_bill_so)  # S/O

                c.drawString(65, 634, discharge_bill_address)  # Address

                c.drawString(78, 611.5, discharge_bill_consulant)  # Consultant
                c.drawString(369, 611.5, discharge_bill_ward)  # Ward
                c.drawString(493, 611.5, discharge_bill_bedNo)  # Bed No.

                c.drawString(111, 598, discharge_bill_admitDate)  # Date Of Admission
                c.drawString(424, 598, discharge_bill_dischargeDate)  # Date Of Discharge


                y = 555

            c.setFont("Helvetica", 8)
            sno, particulars, aDate, iDate, unit, qty, rate, amount = discharge_bill_tree.item(line, "values")
            x = 21
            c.drawString(x, y, sno)
            x += 25
            y1 = y
            y2 = y
            i = 0
            while i < len(particulars):
                c.drawString(x, y1, particulars[i:i+28])
                if len(particulars) > 28:
                    y1 -= 13
                i += 28

            x += 177
            c.drawString(x, y, aDate)
            x += 92
            c.drawString(x, y, iDate)
            x += 75
            c.drawString(x, y, unit)
            x += 35
            c.drawString(x, y, qty)
            x += 34
            c.drawString(x, y, rate)
            x += 60
            c.drawString(x, y, amount)
            if y1 != y2:
                y -=50
            else:   
                y -= 25 
            


        c.drawString(525, 124, discharge_bill_subTotal) 
        c.drawString(527, 107, discharge_bill_gst) 
        c.drawString(527, 90, discharge_bill_discount) 
        c.drawString(527, 74, discharge_bill_roundOff) 

        c.drawString(295, 122, discharge_bill_totalPaidAmount) 
        c.drawString(295, 108, discharge_bill_totalDuesAmount) 
        c.drawString(295, 94, discharge_bill_recievedAmount) 
        c.drawString(286, 75, discharge_bill_balanceAmount) 

        c.drawString(16, 40, discharge_bill_amount_words) 

        c.save()

        # Merge with template
        template_filename = "Data/Templates/Hospital_Discharge_Bill.pdf"  # The template file should be available in the same directory
        merge_with_template(pdf_filename, template_filename)
        messagebox.showinfo("Success", f"receipt generated: {pdf_filename}")

        directory = "Discharge Bills"
        pdf_filename = os.path.join(directory, f"{discharge_bill_registrationNo}_{discharge_bill_billNo}.pdf")
        try:
            if os.name == 'nt':  # For Windows
                os.startfile(pdf_filename)
            elif os.name == 'posix':  # For macOS and Linux
                os.system(f'open "{pdf_filename}"')  # macOS
                os.system(f'xdg-open "{pdf_filename}"')  # Linux
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open PDF file: {e}")

        discharge_bill_page_reset()

    else:
        messagebox.showerror("Input Error", "Please find a Patient First")




def discharge_bill_page_reset():
    discharge_bill_billNo_entry.set("")
    discharge_bill_billDate_entry.set("")
    discharge_bill_time_entry.set("")
    discharge_bill_registrationNo_entry.delete(0, tk.END)
    discharge_bill_registrationNo_fetched.set("")
    discharge_bill_patientName_fetched.set("")
    discharge_bill_contactNo_fetched.set("")
    discharge_bill_age_fetched.set("")
    discharge_bill_gender_fetched.set("")
    discharge_bill_address_fetched.set("")
    discharge_bill_co_fetched.set("")
    discharge_bill_so_fetched.set("")
    discharge_bill_consultant_fetched.set("")
    discharge_bill_ward_fetched.set("")
    discharge_bill_bedNo_fetched.set("")
    discharge_bill_admitDate_fetched.set("")
    discharge_bill_dischargeDate_entry.set("")
    discharge_bill_subTotal_fetched.set("")
    discharge_bill_gst_fetched.set("")
    discharge_bill_discount_entry.set("")
    discharge_bill_roundOff_fetched.set("")
    discharge_bill_totalPaidAmount_fetched.set("")
    discharge_bill_totalDuesAmount_fetched.set("")
    discharge_bill_recievedAmount_fetched.set("")
    discharge_bill_balanceAmount_fetched.set("")
    for item in discharge_bill_tree.get_children():
        discharge_bill_tree.delete(item)


def discharge_bill_entry_reset():
    discharge_bill_billNo_entry.set("")
    for item in discharge_bill_tree.get_children():
        discharge_bill_tree.delete(item)




#-------------------------------------------------------------------------------------------------------------
# Funtion to check int data type
def validate_int_input(input_value):
    # Allow only digits (0-9) and empty input
    if input_value.isdigit() or input_value == "":
        return True
    return False

def validate_real_number(input):
    if input == "":
        return True  # Allow empty input
    try:
        float(input)
        return True
    except ValueError:
        return False





# Create necessary directories
os.makedirs("Patients", exist_ok=True)
os.makedirs("Registration Slips", exist_ok=True)
os.makedirs("Receipts", exist_ok=True)
os.makedirs("Discharge Bills", exist_ok=True)


# UI

root = tk.Tk()
root.title("PATIENT MANAGEMENT SYSTEM")
root.geometry("1200x800")
root.wm_minsize(width=1200, height=800)
icon = PhotoImage(file='Data/Templates/logo.png')
root.iconphoto(False, icon)

######
validate_real_cmd = (root.register(validate_real_number), '%P')
validate_int_cmd = (root.register(validate_int_input), '%P')
######
# Login Frame

login_frame = tk.Frame(root)
login_frame.pack()

login_outside_container = tk.Frame(login_frame, bg='#fff', bd=2, relief='solid')
login_outside_container.grid(row=0, column=0)

login_header = tk.Frame(login_outside_container,  bg='grey', borderwidth=5, relief="groove")
login_header.grid(row=0, column=0, pady=10, sticky='ew')

login_header_title = tk.Label(login_header, text="Login", font=('Arial', 18), bg='grey', fg='white')
login_header_title.pack()

login_container = tk.Frame(login_outside_container, bg='#fff', relief='solid', padx=208, pady=80)
login_container.grid(row=1, column=0)

# for row spacing design
# tk.Label(login_container, text="", bg='white').grid(row=1, column=0)
# tk.Label(login_container, text="", bg='white').grid(row=2, column=0)
# tk.Label(login_container, text="", bg='white').grid(row=3, column=0)
# tk.Label(login_container, text="", bg='white').grid(row=4, column=0)
# tk.Label(login_container, text="", bg='white').grid(row=5, column=0)
# tk.Label(login_container, text="", bg='white').grid(row=6, column=0)
# tk.Label(login_container, text="", bg='white').grid(row=7, column=0)
image = Image.open("Data/Templates/logo.png")
image = image.resize((145, 145), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)
label = tk.Label(login_container, image=photo)
label.grid(row=1, column=0)
# ------------------------
tk.Label(login_container, text="", bg='white').grid(row=2, column=0)


login_form = tk.Frame(login_container, bg='#fff', bd=2, relief='solid', padx=40, pady=60)
login_form.grid(row=9, column=0, pady=10, padx=200, sticky='')

login_admin_label = tk.Label(login_form, text="Admin Id ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
login_admin_label.grid(row=0, column=0, pady=5, sticky='w')

login_admin_entry = tk.Entry(login_form, font=('Arial', 12), border=2)
login_admin_entry.grid(row=0, column=1, pady=5)

login_password_label = tk.Label(login_form, text="Password ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
login_password_label.grid(row=1, column=0, pady=5, sticky='w')

login_password_entry = tk.Entry(login_form, font=('Arial', 12), border=2, show='*')
login_password_entry.grid(row=1, column=1, pady=5)

login_btn = tk.Button(login_form, text="Login", bg='lightblue', command=login, width=11)
login_btn.grid(row=2, column=1, pady=2, padx=5, sticky='w')

# for row spacing design
tk.Label(login_container, text="", bg='white').grid(row=10, column=0)
tk.Label(login_container, text="", bg='white').grid(row=11, column=0)
tk.Label(login_container, text="", bg='white').grid(row=12, column=0)
tk.Label(login_container, text="", bg='white').grid(row=13, column=0)
tk.Label(login_container, text="", bg='white').grid(row=14, column=0)
tk.Label(login_container, text="", bg='white').grid(row=15, column=0)
tk.Label(login_container, text="", bg='white').grid(row=16, column=0)
# ------------------------


# Main Menu Frame

main_menu_frame = tk.Frame(root)
    
main_menu_container = tk.Frame(main_menu_frame, bg='#fff', bd=2, relief='solid')
main_menu_container.pack()

main_menu_header = tk.Frame(main_menu_container,  bg='grey', borderwidth=5, relief="groove")
main_menu_header.grid(row=0, column=0, pady=10, sticky='ew')

main_menu_header_back_btn = tk.Button(main_menu_header, text="Back", bg="orange", fg="#fff", font=("Arial", 16), command=main_menu_back)
main_menu_header_back_btn.grid(row=0, column=0)

main_menu_header_title = tk.Label(main_menu_header, text="\t\t\t\t      Main Menu      \t\t\t\t\t", font=('Arial', 18), bg='grey', fg='white')
main_menu_header_title.grid(row=0, column=1)

main_menu_header_exit_btn = tk.Button(main_menu_header, text="Exit", bg="red", fg="#fff", font=("Arial", 16), command=exit)
main_menu_header_exit_btn.grid(row=0, column=3)

# for row spacing design
tk.Label(main_menu_container, text="", bg='white').grid(row=1, column=0)
tk.Label(main_menu_container, text="", bg='white').grid(row=2, column=0)
# ------------------------

main_menu_margin_between_container_containerInside = tk.Frame(main_menu_container,  bg='#fff',  relief='solid', padx=200)
main_menu_margin_between_container_containerInside.grid(row=3, column=0, padx=20, sticky='')

main_menu_inside_container = tk.Frame(main_menu_margin_between_container_containerInside, bg='#fff', bd=2, relief='solid', padx=20, pady=20)
main_menu_inside_container.grid(row=0, column=0, pady=10, padx=20, sticky='')

main_menu_registration_contianer = tk.Frame(main_menu_inside_container, bg='#fff', bd=2, relief='solid', padx=20, pady=20)
main_menu_registration_contianer.grid(row=0, column=0, pady=10, padx=20, sticky='')

main_menu_registrationPage_btn = tk.Button(main_menu_registration_contianer, text="Patient\nRegistration", bg='lightgrey', font=('Arial', 18, 'bold'), command=show_patient_registration_page, width=12,height=5)
main_menu_registrationPage_btn.grid(row=0, column=0, pady=2, padx=5, sticky='w')

main_menu_addServicesPage_contianer = tk.Frame(main_menu_inside_container, bg='#fff', bd=2, relief='solid', padx=20, pady=20)
main_menu_addServicesPage_contianer.grid(row=0, column=1, pady=10, padx=20, sticky='')

main_menu_addServicesPage_btn = tk.Button(main_menu_addServicesPage_contianer, text="Add\nServices", bg='lightgrey', font=('Arial', 18, 'bold'), command=show_add_services_page, width=12, height=5)
main_menu_addServicesPage_btn.grid(row=0, column=0, pady=2, padx=5, sticky='w')

main_menu_updatePatient_contianer = tk.Frame(main_menu_inside_container, bg='#fff', bd=2, relief='solid', padx=20, pady=20)
main_menu_updatePatient_contianer.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky='')

main_menu_updatePatient_btn = tk.Button(main_menu_updatePatient_contianer, text="Update Patient", bg='lightgrey',font=('Arial', 18, 'bold'),  command=show_updatePatient_page, width=15, height=2)
main_menu_updatePatient_btn.grid(row=0, column=0, pady=2, padx=5, sticky='w')

main_menu_moneyreceipt_contianer = tk.Frame(main_menu_inside_container, bg='#fff', bd=2, relief='solid', padx=20, pady=20)
main_menu_moneyreceipt_contianer.grid(row=2, column=0, pady=10, padx=20, sticky='')

main_menu_moneyreceipt_btn = tk.Button(main_menu_moneyreceipt_contianer, text="Money\nreceipt", bg='lightgrey', font=('Arial', 18, 'bold'), command=show_money_receipt_page, width=12, height=5)
main_menu_moneyreceipt_btn.grid(row=0, column=0, pady=2, padx=5, sticky='w')

main_menu_dischargeBill_contianer = tk.Frame(main_menu_inside_container, bg='#fff', bd=2, relief='solid', padx=20, pady=20)
main_menu_dischargeBill_contianer.grid(row=2, column=1, pady=10, padx=20, sticky='')

main_menu_dischargeBill_btn = tk.Button(main_menu_dischargeBill_contianer, text="Discharge\nBill", bg='lightgrey',font=('Arial', 18, 'bold'),  command=show_discharge_bill_page, width=12, height=5)
main_menu_dischargeBill_btn.grid(row=0, column=0, pady=2, padx=5, sticky='w')

# for row spacing design
tk.Label(main_menu_container, text="", bg='white').grid(row=4, column=0)
tk.Label(main_menu_container, text="", bg='white').grid(row=5, column=0)
# ------------------------


# Patient Registration Frame

patient_registration_frame = tk.Frame(root)

patient_registration_outer_container = tk.Frame(patient_registration_frame, bg='#fff', bd=2, relief='solid')
patient_registration_outer_container.grid(row=0, column=0)

patient_registration_header = tk.Frame(patient_registration_outer_container,  bg='grey', borderwidth=5, relief="groove")
patient_registration_header.grid(row=0, column=0, pady=10, sticky='ew')

patient_registration_header_back_btn = tk.Button(patient_registration_header, text="Back", bg="orange", fg="#fff", font=("Arial", 16), command=patient_registration_back)
patient_registration_header_back_btn.grid(row=0, column=0)

patient_registration_header_title = tk.Label(patient_registration_header, text="\t\t\t\tPatient Registration\t\t\t\t", font=('Arial', 18), bg='grey', fg='white')
patient_registration_header_title.grid(row=0, column=1)

patient_registration_header_exit_btn = tk.Button(patient_registration_header, text="Exit", bg="red", fg="#fff", font=("Arial", 16), command=exit)
patient_registration_header_exit_btn.grid(row=0, column=3)

patient_registration_innercontainer = tk.Frame(patient_registration_outer_container, bg='#fff', relief='solid', pady=80)
patient_registration_innercontainer.grid(row=1, column=0)

patient_registration_container = tk.Frame(patient_registration_innercontainer, bg='#fff', bd=2, relief='solid', pady=10)
patient_registration_container.grid(row=0, column=0)

patient_registration_form = tk.Frame(patient_registration_container, bg='#fff')
patient_registration_form.grid(row=1, column=0, pady=10, padx=200, sticky='ew')

patient_registration_registrationNo_label = tk.Label(patient_registration_form, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_registrationNo_label.grid(row=0, column=0, pady=5, sticky='w')

patient_registration_registrationNo_entry = tk.Variable()
patient_registration_registrationNo_entry.set("")
tk.Label(patient_registration_form,textvariable=patient_registration_registrationNo_entry, font=('Arial', 12), border=2).grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        
patient_registration_patientName_label = tk.Label(patient_registration_form, text="Patient Name :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_patientName_label.grid(row=1, column=0, pady=5, sticky='w')

patient_registration_patientName_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2)
patient_registration_patientName_entry.grid(row=1, column=1, pady=5, padx=10, sticky='ew')

patient_registration_contactNo_label = tk.Label(patient_registration_form, text="Contact No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_contactNo_label.grid(row=2, column=0, pady=5, sticky='w')

patient_registration_contactNo_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2, validate="key", validatecommand=(validate_int_cmd))
patient_registration_contactNo_entry.grid(row=2, column=1, pady=5, padx=10, sticky='ew')

patient_registration_address_label = tk.Label(patient_registration_form, text="Address :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_address_label.grid(row=3, column=0, pady=5, sticky='w')

patient_registration_address_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2)
patient_registration_address_entry.grid(row=3, column=1, pady=5, padx=10, sticky='ew')

patient_registration_age_label = tk.Label(patient_registration_form, text="Age :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_age_label.grid(row=4, column=0, pady=5, sticky='w')

patient_registration_age_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2, validate="key", validatecommand=(validate_int_cmd))
patient_registration_age_entry.grid(row=4, column=1, pady=5, padx=10, sticky='ew')

patient_registration_gender_label = tk.Label(patient_registration_form, text="Gender :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_gender_label.grid(row=5, column=0, pady=5, sticky='w')

patient_registration_gender_var = tk.StringVar()
patient_registration_gender_var.set("Select")
patient_registration_gender_entry = tk.OptionMenu(patient_registration_form,patient_registration_gender_var,"Male", "Female", "Other", command=lambda _: option_selected(patient_registration_gender_var, patient_registration_co_entry))
patient_registration_gender_entry.config(width=7)
patient_registration_gender_entry.grid(row=5, column=1, pady=5, padx=10, sticky='w')
            
patient_registration_co_label = tk.Label(patient_registration_form, text="C/O :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_co_label.grid(row=6, column=0, pady=5, sticky='w')

patient_registration_co_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2)
patient_registration_co_entry.grid(row=6, column=1, pady=5, padx=10, sticky='ew')

patient_registration_so_label = tk.Label(patient_registration_form, text="S/O :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_so_label.grid(row=7, column=0, pady=5, sticky='w')

patient_registration_so_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2)
patient_registration_so_entry.grid(row=7, column=1, pady=5, padx=10, sticky='ew')

patient_registration_admitDate_label = tk.Label(patient_registration_form, text="Admit Date :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_admitDate_label.grid(row=8, column=0, pady=5, sticky='w')

patient_registration_admitDate_entry = tk.StringVar()
patient_registration_admitDate_entry.set("")
tk.Entry(patient_registration_form,textvariable=patient_registration_admitDate_entry,  font=('Arial', 12), border=2).grid(row=8, column=1, pady=5, padx=10, sticky='ew')

patient_registration_consultant_label = tk.Label(patient_registration_form, text="Consultant :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_consultant_label.grid(row=9, column=0, pady=5, sticky='w')

patient_registration_consultant_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2)
patient_registration_consultant_entry.grid(row=9, column=1, pady=5, padx=10, sticky='ew')

patient_registration_ward_label = tk.Label(patient_registration_form, text="Ward :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_ward_label.grid(row=10, column=0, pady=5, sticky='w')

patient_registration_ward_var = tk.StringVar()
patient_registration_ward_var.set("Select")
patient_registration_ward_entry = tk.OptionMenu(patient_registration_form,patient_registration_ward_var,"ICU", "NICU", "BURN", "GENERAL WARD", "PRIVATE ROOM", command=lambda _: option_selected(patient_registration_ward_var, patient_registration_bedNo_entry))
patient_registration_ward_entry.config(width=7)
patient_registration_ward_entry.grid(row=10, column=1, pady=5, padx=10, sticky='w')

patient_registration_bedNo_label = tk.Label(patient_registration_form, text="Bed No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_bedNo_label.grid(row=11, column=0, pady=5, sticky='w')

patient_registration_bedNo_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2)
patient_registration_bedNo_entry.grid(row=11, column=1, pady=5, padx=10, sticky='ew')

patient_registration_advanceAmount_label = tk.Label(patient_registration_form, text="Advance Amount :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
patient_registration_advanceAmount_label.grid(row=12, column=0, pady=5, sticky='w')

patient_registration_advanceAmount_entry = tk.Entry(patient_registration_form, font=('Arial', 12), border=2, validate="key", validatecommand=(validate_real_cmd))
patient_registration_advanceAmount_entry.grid(row=12, column=1, pady=5, padx=10, sticky='ew')


patient_registration_register_button = tk.Button(patient_registration_form, text="Register", bg='#007bff', fg='white', cursor='hand2', border=5, font=('Arial', 15, "bold"), command=register_patient)
patient_registration_register_button.grid(row=13, column=0, columnspan=2, sticky='ew')

patient_registration_patientName_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_contactNo_entry))
patient_registration_contactNo_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_address_entry))
patient_registration_address_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_age_entry))
patient_registration_age_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_gender_entry))
patient_registration_co_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_so_entry))
patient_registration_so_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_consultant_entry))
patient_registration_consultant_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_ward_entry))
patient_registration_bedNo_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_advanceAmount_entry))
patient_registration_advanceAmount_entry.bind("<Return>", lambda event: focus_next_widget(event, patient_registration_register_button))


# Add Services Frame

add_services_frame = tk.Frame(root)

add_services_outer_container = tk.Frame(add_services_frame, bg='#fff', bd=2, relief='solid')
add_services_outer_container.grid(row=0, column=0)

add_services_header = tk.Frame(add_services_outer_container,  bg='grey', borderwidth=5, relief="groove")
add_services_header.grid(row=0, column=0, pady=10, sticky='ew')

add_services_header_back_btn = tk.Button(add_services_header, text="Back", bg="orange", fg="#fff", font=("Arial", 16), command=add_services_back)
add_services_header_back_btn.grid(row=0, column=0)

add_services_header_title = tk.Label(add_services_header, text="\t\t\t\t    Add Services      \t\t\t\t", font=('Arial', 18), bg='grey', fg='white')
add_services_header_title.grid(row=0, column=1)

add_services_header_exit_btn = tk.Button(add_services_header, text="Exit", bg="red", fg="#fff", font=("Arial", 16), command=exit)
add_services_header_exit_btn.grid(row=0, column=3)

add_services_container = tk.Frame(add_services_outer_container, bg='#fff', relief='solid', padx=192)
add_services_container.grid(row=1, column=0)

add_services_form = tk.Frame(add_services_container, bg='#fff', bd=2, relief='solid')
add_services_form.grid(row=1, column=0, sticky='')

add_services_registrationNo_label = tk.Label(add_services_form, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
add_services_registrationNo_label.grid(row=0, column=0, pady=5)

add_services_registrationNo_entry = tk.Entry(add_services_form, font=('Arial', 12), border=2)
add_services_registrationNo_entry.grid(row=0, column=1, pady=5)

add_services_find_btn = tk.Button(add_services_form, text="Find", bg='lightgrey', command=add_services_fetch_patient_details)
add_services_find_btn.grid(row=0, column=2, pady=2, padx=5)

add_services_fetched_deatils_frame = tk.Frame(add_services_container, bg='#fff', pady=25)
add_services_fetched_deatils_frame.grid(row=2, column=0)

add_services_patientName_label = tk.Label(add_services_fetched_deatils_frame, text="Patient Name :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
add_services_patientName_label.grid(row=0, column=0, sticky='w')

add_services_patientName_fetched = tk.StringVar()
add_services_patientName_fetched.set("")
tk.Label(add_services_fetched_deatils_frame, textvariable=add_services_patientName_fetched,font=('Arial', 12, "bold"), bg='#fff', width=38, anchor='w').grid(row=0, column=1, pady=5, sticky='w')

add_services_contactNo_label = tk.Label(add_services_fetched_deatils_frame, text="Contact No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
add_services_contactNo_label.grid(row=0, column=2, pady=5, sticky='w')

add_services_contactNo_fetched = tk.StringVar()
add_services_contactNo_fetched.set("")
tk.Label(add_services_fetched_deatils_frame, textvariable=add_services_contactNo_fetched,font=('Arial', 12, "bold"), bg='#fff', width=15, anchor='w').grid(row=0, column=3, pady=5, sticky='w')

frame1 = tk.Frame(add_services_container, bg='white', pady=10)
frame1.grid(row=3, column=0)

services = add_services_read_services('Data/services.txt')

def on_option_change(*args):
    selected_service = add_services_particulars_var.get()
    if selected_service in services:
        add_services_particulars_manual_var.set(selected_service)
        add_services_price_manual_var.set(services[selected_service])
    else:
        add_services_particulars_manual_var.set('')
        add_services_price_manual_var.set('')

add_services_particulars_var = tk.StringVar()
add_services_particulars_var.set("Select a Service")
option_menu = tk.OptionMenu(frame1, add_services_particulars_var, *services.keys())
option_menu.config(width=50)
option_menu.grid(row=0, column=0, sticky='ew')

add_services_addServices_frame = tk.Frame(add_services_container, bg='white', pady=10)
add_services_addServices_frame.grid(row=4, column=0)


add_services_particulars_label = tk.Label(add_services_addServices_frame, text="Service    ",font=('Arial', 12, "bold"), bg='white')
add_services_particulars_label.grid(row=0, column=0,sticky='w')

add_services_particulars_manual_var = tk.StringVar()
add_services_particulars_manual_var.set("")
add_services_particulars_entry = tk.Entry(add_services_addServices_frame, text = add_services_particulars_manual_var, border=2)
add_services_particulars_entry.config(width=35)
add_services_particulars_entry.grid(row=0, column=1, sticky='ew')

tk.Label(add_services_addServices_frame, bg="white").grid(row=0 , column=2)

add_services_price_label = tk.Label(add_services_addServices_frame, text="Rate",font=('Arial', 12, "bold"), bg='white')
add_services_price_label.grid(row=0, column=3,sticky='w')

add_services_price_manual_var = tk.StringVar()
add_services_price_manual_var.set("")
add_services_price_entry = tk.Entry(add_services_addServices_frame, text = add_services_price_manual_var, validate="key", validatecommand=(validate_real_cmd), border=2)
add_services_price_entry.grid(row=0, column=4, sticky='ew')

add_services_particulars_var.trace('w', on_option_change)

tk.Label(add_services_addServices_frame, bg="white").grid(row=1 , column=0)

add_services_unit_label = tk.Label(add_services_addServices_frame, text="Unit",font=('Arial', 12, "bold"), bg='white')
add_services_unit_label.grid(row=2, column=0, sticky='w')

add_services_unit_var = tk.StringVar()
add_services_unit_var.set("Select")
add_services_unit_entry = tk.OptionMenu(add_services_addServices_frame,add_services_unit_var,"P/D", "P/H", "P/T", "FIX")
add_services_unit_entry.config(width=5)
add_services_unit_entry.grid(row=2, column=1, sticky='w')

tk.Label(add_services_addServices_frame, bg="white").grid(row=2 , column=2)

add_services_qty_label = tk.Label(add_services_addServices_frame, text="Days/Qty",font=('Arial', 12, "bold"), bg='white')
add_services_qty_label.grid(row=2, column=3, sticky='w')

add_services_qty_entry = tk.StringVar()
add_services_qty_entry.set("")
tk.Entry(add_services_addServices_frame, text=add_services_qty_entry,font=('Arial', 12, "bold"), bg='#fff', width=5, validate="key", validatecommand=(validate_real_cmd), border=2).grid(row=2, column=4, sticky='w')




add_services_amount_entry = tk.StringVar()
add_services_amount_entry.set("")
tk.Label(add_services_addServices_frame, bg="white").grid(row=3 , column=0)



add_services_aDate_label = tk.Label(add_services_addServices_frame, text="Active Date    ",font=('Arial', 12, "bold"), bg='white')
add_services_aDate_label.grid(row=4, column=0,sticky='w')

add_services_aDate_manual_var = tk.StringVar()
add_services_aDate_manual_var.set(get_current_date())
add_services_aDate_entry = tk.Entry(add_services_addServices_frame, text = add_services_aDate_manual_var, border=2)
add_services_aDate_entry.config(width=15)
add_services_aDate_entry.grid(row=4, column=1, sticky='w')

tk.Label(add_services_addServices_frame, bg="white").grid(row=4 , column=2)

add_services_iDate_label = tk.Label(add_services_addServices_frame, text="Inactive Date    ",font=('Arial', 12, "bold"), bg='white')
add_services_iDate_label.grid(row=4, column=3,sticky='w')

add_services_iDate_manual_var = tk.StringVar()
add_services_iDate_manual_var.set(get_current_date())
add_services_iDate_entry = tk.Entry(add_services_addServices_frame, text = add_services_iDate_manual_var, border=2)
add_services_iDate_entry.config(width=15)
add_services_iDate_entry.grid(row=4, column=4, sticky='w')



frame2 = tk.Frame(add_services_container, bg='white')
frame2.grid(row=5, column=0)

add_services_add_btn = tk.Button(frame2, text="Add", bg='#007bff', command=add_service, width=5)
add_services_add_btn.grid(row=0, column=0, padx=2)

add_services_tree = ttk.Treeview(frame2, height=13, columns=("particulars", "aDate", "iDate", "unit", "qty", "rate", "amount"), show='headings')
add_services_tree.grid(row=1, column=0, sticky='ew', pady=15)

add_services_tree.heading("particulars", text="Particulars")
add_services_tree.heading("aDate", text="Active Date")
add_services_tree.heading("iDate", text="Inactive Date")
add_services_tree.heading("unit", text="Unit")
add_services_tree.heading("qty", text="Qty")
add_services_tree.heading("rate", text="Rate")
add_services_tree.heading("amount", text="Amount")

add_services_tree.column("particulars", width=300)
add_services_tree.column("aDate", width=100)
add_services_tree.column("iDate", width=100)
add_services_tree.column("unit", width=40)
add_services_tree.column("qty", width=40)
add_services_tree.column("rate", width=100)
add_services_tree.column("amount", width=100)


add_services_submit_btn = tk.Button(frame2, text="Submit", bg='green', fg='white', cursor='hand2', border=5, font=('Arial', 15, "bold"), command=add_services_submit)
add_services_submit_btn.grid(row=2, column=0, pady=5)

add_services_registrationNo_fetched = tk.StringVar()
add_services_registrationNo_fetched.set("")



# Money receipt Frame

money_receipt_frame = tk.Frame(root)

money_receipt_outer_container = tk.Frame(money_receipt_frame, bg='#fff', bd=2, relief='solid')
money_receipt_outer_container.grid(row=0, column=0)

money_receipt_header = tk.Frame(money_receipt_outer_container,  bg='grey', borderwidth=5, relief="groove")
money_receipt_header.grid(row=0, column=0, pady=10, sticky='ew')

money_receipt_header_back_btn = tk.Button(money_receipt_header, text="Back", bg="orange", fg="#fff", font=("Arial", 16), command=money_receipt_back)
money_receipt_header_back_btn.grid(row=0, column=0)

money_receipt_header_title = tk.Label(money_receipt_header, text="\t\t\t\t  Money receipt     \t\t\t\t", font=('Arial', 18), bg='grey', fg='white')
money_receipt_header_title.grid(row=0, column=1)

money_receipt_header_exit_btn = tk.Button(money_receipt_header, text="Exit", bg="red", fg="#fff", font=("Arial", 16), command=exit)
money_receipt_header_exit_btn.grid(row=0, column=3)

money_receipt_container = tk.Frame(money_receipt_outer_container, bg='#fff', relief='solid', padx=10, pady=60)
money_receipt_container.grid(row=1, column=0)

money_receipt_form = tk.Frame(money_receipt_container, bg='#fff', bd=2, relief='solid')
money_receipt_form.grid(row=1, column=0, pady=10, padx=200, sticky='')

money_receipt_registrationNo_label = tk.Label(money_receipt_form, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_registrationNo_label.grid(row=0, column=0, pady=5)

money_receipt_registrationNo_entry = tk.Entry(money_receipt_form, font=('Arial', 12), border=2)
money_receipt_registrationNo_entry.grid(row=0, column=1, pady=5)

money_receipt_find_btn = tk.Button(money_receipt_form, text="Find", bg='lightgrey', command=money_receipt_fetch_patient_details)
money_receipt_find_btn.grid(row=0, column=2, pady=2, padx=5)

money_receipt_fetched_deatils_frame = tk.Frame(money_receipt_container, bg='#fff', pady=25, padx=25)
money_receipt_fetched_deatils_frame.grid(row=2, column=0)

tk.Label(money_receipt_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=0, column=0)

money_receipt_receiptNo_label = tk.Label(money_receipt_fetched_deatils_frame, text="Receipt No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_receiptNo_label.grid(row=1, column=0, sticky='w')

money_receipt_receiptNo_entry = tk.Variable()
money_receipt_receiptNo_entry.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_receiptNo_entry ,font=('Arial', 12, "bold"), bg='#fff').grid(row=1, column=1, pady=5, sticky='w')

tk.Label(money_receipt_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=1, column=2)

money_receipt_date_label = tk.Label(money_receipt_fetched_deatils_frame, text="Date :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_date_label.grid(row=1, column=3, pady=5, sticky='w')


money_receipt_date_entry = tk.StringVar()
money_receipt_date_entry.set("")
tk.Entry(money_receipt_fetched_deatils_frame,textvariable=money_receipt_date_entry,font=('Arial', 12, "bold"), bg='#fff').grid(row=1, column=4, pady=5)

money_receipt_time_fetched = tk.StringVar()
money_receipt_time_fetched.set("")

tk.Label(money_receipt_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=2, column=0)

money_receipt_registratoinNo_label = tk.Label(money_receipt_fetched_deatils_frame, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_registratoinNo_label.grid(row=3, column=0, pady=5, sticky='w')

money_receipt_registrationNo_fetched = tk.StringVar()
money_receipt_registrationNo_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_registrationNo_fetched,font=('Arial', 12, "bold"), border=0, background='white').grid(row=3, column=1, pady=5, sticky='w')

money_receipt_patientName_label = tk.Label(money_receipt_fetched_deatils_frame, text="Patient Name :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_patientName_label.grid(row=4, column=0, pady=5, sticky='w')

money_receipt_patientName_fetched = tk.StringVar()
money_receipt_patientName_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_patientName_fetched,font=('Arial', 12, "bold"), bg='#fff', width=40, anchor='w').grid(row=4, column=1, pady=5, sticky='w')

money_receipt_address_label = tk.Label(money_receipt_fetched_deatils_frame, text="Patient Address :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_address_label.grid(row=5, column=0, pady=5, sticky='w')

money_receipt_address_fetched = tk.StringVar()
money_receipt_address_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_address_fetched,font=('Arial', 12, "bold"), bg='white', width=40, anchor='w').grid(row=5, column=1, pady=5, sticky='w')

money_receipt_age_label = tk.Label(money_receipt_fetched_deatils_frame, text="Age :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_age_label.grid(row=6, column=0, pady=5, sticky='w')

money_receipt_age_fetched = tk.StringVar()
money_receipt_age_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_age_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=6, column=1, pady=5, sticky='w')

money_receipt_gender_label = tk.Label(money_receipt_fetched_deatils_frame, text="Gender :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_gender_label.grid(row=7, column=0, pady=5, sticky='w')

money_receipt_gender_fetched = tk.StringVar()
money_receipt_gender_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_gender_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=7, column=1, pady=5, sticky='w')

money_receipt_contactNo_label = tk.Label(money_receipt_fetched_deatils_frame, text="Contact No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_contactNo_label.grid(row=8, column=0, pady=5, sticky='w')

money_receipt_contactNo_fetched = tk.StringVar()
money_receipt_contactNo_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_contactNo_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=8, column=1, pady=5, sticky='w')

money_receipt_ward_label = tk.Label(money_receipt_fetched_deatils_frame, text="Ward :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_ward_label.grid(row=9, column=0, pady=5, sticky='w')

money_receipt_ward_fetched = tk.StringVar()
money_receipt_ward_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_ward_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=9, column=1, pady=5, sticky='w')

money_receipt_bedNo_label = tk.Label(money_receipt_fetched_deatils_frame, text="Bed No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_bedNo_label.grid(row=10, column=0, pady=5, sticky='w')

money_receipt_bedNo_fetched = tk.StringVar()
money_receipt_bedNo_fetched.set("")
tk.Label(money_receipt_fetched_deatils_frame, textvariable=money_receipt_bedNo_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=10, column=1, pady=5, sticky='w')



tk.Label(money_receipt_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=11, column=0)

money_receipt_modeOfPay_label = tk.Label(money_receipt_fetched_deatils_frame, text="Mode of Pay :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_modeOfPay_label.grid(row=12, column=0, sticky='e')

money_receipt_modeOfPay_var = tk.StringVar()
money_receipt_modeOfPay_var.set("Select")
money_receipt_modeOfPay_entry = tk.OptionMenu(money_receipt_fetched_deatils_frame, money_receipt_modeOfPay_var , "Cash", "Credit Card", "Debit Card", "Online Payment", "Cheque")
money_receipt_modeOfPay_entry.config(width=14)
money_receipt_modeOfPay_entry.grid(row=12, column=1, pady=5, sticky='w')




tk.Label(money_receipt_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=12, column=2)

money_receipt_paidAmount_label = tk.Label(money_receipt_fetched_deatils_frame, text="Paid Amount :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
money_receipt_paidAmount_label.grid(row=12, column=3, sticky='e')

money_receipt_paidAmount_entry = tk.Entry(money_receipt_fetched_deatils_frame,font=('Arial', 12, "bold"), bg='#fff', validate="key", validatecommand=(validate_real_cmd))
money_receipt_paidAmount_entry.grid(row=12, column=4, pady=5, sticky='w')

tk.Label(money_receipt_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=13, column=0)

money_receipt_submit_btn = tk.Button(money_receipt_container, text="Generate receipt", bg='green', fg='white', cursor='hand2', border=5, font=('Arial', 15, "bold"), command=money_receipt_generate_receipt)
money_receipt_submit_btn.grid(row=3, column=0)


# Discharge Bill Frame

discharge_bill_frame = tk.Frame(root)
    
discharge_bill_container = tk.Frame(discharge_bill_frame, bg='#fff', bd=2, relief='solid')
discharge_bill_container.pack()

discharge_bill_header = tk.Frame(discharge_bill_container,  bg='grey', borderwidth=5, relief="groove")
discharge_bill_header.grid(row=0, column=0, pady=10, sticky='ew')

discharge_bill_header_back_btn = tk.Button(discharge_bill_header, text="Back", bg="orange", fg="#fff", font=("Arial", 16), command=discharge_bill_back)
discharge_bill_header_back_btn.grid(row=0, column=0)

discharge_bill_header_title = tk.Label(discharge_bill_header, text="\t\t\t\t      Discharge Bill      \t\t\t\t", font=('Arial', 18), bg='grey', fg='white')
discharge_bill_header_title.grid(row=0, column=1)

discharge_bill_header_exit_btn = tk.Button(discharge_bill_header, text="Exit", bg="red", fg="#fff", font=("Arial", 16), command=exit)
discharge_bill_header_exit_btn.grid(row=0, column=3)

discharge_bill_form = tk.Frame(discharge_bill_container, bg='#fff', bd=2, relief='solid')
discharge_bill_form.grid(row=1, column=0, pady=10, padx=200, sticky='')

discharge_bill_registrationNo_label = tk.Label(discharge_bill_form, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_registrationNo_label.grid(row=0, column=0, pady=5)

discharge_bill_registrationNo_entry = tk.Entry(discharge_bill_form, font=('Arial', 12), border=2)
discharge_bill_registrationNo_entry.grid(row=0, column=1, pady=5)

discharge_bill_find_btn = tk.Button(discharge_bill_form, text="Find", bg='lightgrey', command=discharge_bill_fetch_patient_details)
discharge_bill_find_btn.grid(row=0, column=2, pady=2, padx=5)

discharge_bill_fetched_deatils_frame = tk.Frame(discharge_bill_container, bg='#fff', pady=10, padx=25)
discharge_bill_fetched_deatils_frame.grid(row=2, column=0)

discharge_bill_billNo_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Bill No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_billNo_label.grid(row=0, column=0, sticky='w')

discharge_bill_billNo_entry = tk.StringVar()
discharge_bill_billNo_entry.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_billNo_entry,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=0, column=1, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=0, column=2)

discharge_bill_billDate_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Bill Date :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_billDate_label.grid(row=0, column=3, pady=5, sticky='e')

discharge_bill_billDate_entry = tk.StringVar()
discharge_bill_billDate_entry.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_billDate_entry,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=0, column=4, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=0, column=5)

discharge_bill_time_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Time :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_time_label.grid(row=0, column=6, sticky='e')

discharge_bill_time_entry = tk.StringVar()
discharge_bill_time_entry.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_time_entry, font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=0, column=7, pady=5, sticky='w')

discharge_bill_registrationNo_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_registrationNo_label.grid(row=1, column=0, sticky='w')

discharge_bill_registrationNo_fetched = tk.StringVar()
discharge_bill_registrationNo_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_registrationNo_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=1, column=1, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=1, column=2)

discharge_bill_patientName_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Patient Name :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_patientName_label.grid(row=1, column=3, sticky='e')

discharge_bill_patientName_fetched = tk.StringVar()
discharge_bill_patientName_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_patientName_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=1, column=4, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=1, column=5)

discharge_bill_contactNo_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Contact No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_contactNo_label.grid(row=1, column=6, pady=5, sticky='e')

discharge_bill_contactNo_fetched = tk.StringVar()
discharge_bill_contactNo_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_contactNo_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=1, column=7, pady=5, sticky='w')

discharge_bill_age_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Age :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_age_label.grid(row=2, column=0, sticky='w')

discharge_bill_age_fetched = tk.StringVar()
discharge_bill_age_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_age_fetched, font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=2, column=1, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=2, column=2)

discharge_bill_gender_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Gender :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_gender_label.grid(row=2, column=3, sticky='e')

discharge_bill_gender_fetched = tk.StringVar()
discharge_bill_gender_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_gender_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=2, column=4, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=2, column=5)

discharge_bill_address_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Address :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_address_label.grid(row=2, column=6, pady=5, sticky='e')

discharge_bill_address_fetched = tk.StringVar()
discharge_bill_address_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_address_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=2, column=7, pady=5, sticky='w')

discharge_bill_co_label = tk.Label(discharge_bill_fetched_deatils_frame, text="C/O :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_co_label.grid(row=3, column=0, sticky='w')

discharge_bill_co_fetched = tk.StringVar()
discharge_bill_co_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_co_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=3, column=1, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=3, column=2)


discharge_bill_so_label = tk.Label(discharge_bill_fetched_deatils_frame, text="S/O :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_so_label.grid(row=3, column=3, pady=5, sticky='e')

discharge_bill_so_fetched = tk.StringVar()
discharge_bill_so_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_so_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=3, column=4, pady=5, sticky='w')

discharge_bill_consulant_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Consultant :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_consulant_label.grid(row=4, column=0, sticky='w')

discharge_bill_consultant_fetched = tk.StringVar()
discharge_bill_consultant_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_consultant_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=4, column=1, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=4, column=2)

discharge_bill_ward_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Ward :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_ward_label.grid(row=4, column=3, sticky='e')

discharge_bill_ward_fetched = tk.StringVar()
discharge_bill_ward_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_ward_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=4, column=4, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=4, column=5)

discharge_bill_bedNo_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Bed No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_bedNo_label.grid(row=4, column=6, pady=5, sticky='e')

discharge_bill_bedNo_fetched = tk.StringVar()
discharge_bill_bedNo_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_bedNo_fetched,font=('Arial', 12, "bold",), bg='#fff', state='readonly').grid(row=4, column=7, pady=5, sticky='w')


discharge_bill_admitDate_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Admit Date :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_admitDate_label.grid(row=5, column=0, pady=5, sticky='w')

discharge_bill_admitDate_fetched = tk.StringVar()
discharge_bill_admitDate_fetched.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_admitDate_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=5, column=1, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=5, column=2)

discharge_bill_dischargeDate_label = tk.Label(discharge_bill_fetched_deatils_frame, text="Discharge Date :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_dischargeDate_label.grid(row=5, column=3, sticky='w')

discharge_bill_dischargeDate_entry = tk.StringVar()
discharge_bill_dischargeDate_entry.set("")
tk.Entry(discharge_bill_fetched_deatils_frame, text=discharge_bill_dischargeDate_entry, font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=5, column=4, pady=5, sticky='w')


discharge_bill_addServices_frame = tk.Frame(discharge_bill_container, bg='white', pady=10)
discharge_bill_addServices_frame.grid(row=3, column=0)

discharge_bill_tree = ttk.Treeview(discharge_bill_addServices_frame, height=8, columns=("sno", "particulars","aDate", "iDate", "unit", "qty", "rate", "amount"), show='headings')
discharge_bill_tree.grid(row=2, column=0, columnspan=9, sticky='ew', pady=10)

discharge_bill_tree.heading("sno", text="S.No.")
discharge_bill_tree.heading("particulars", text="Particulars")
discharge_bill_tree.heading("aDate", text="Active Date")
discharge_bill_tree.heading("iDate", text="Inactive Date")
discharge_bill_tree.heading("unit", text="Unit")
discharge_bill_tree.heading("qty", text="Qty")
discharge_bill_tree.heading("rate", text="Rate")
discharge_bill_tree.heading("amount", text="Amount")

discharge_bill_tree.column("sno", width=40)
discharge_bill_tree.column("particulars", width=200)
discharge_bill_tree.column("aDate", width=100)
discharge_bill_tree.column("iDate", width=100)
discharge_bill_tree.column("unit", width=40)
discharge_bill_tree.column("qty", width=40)
discharge_bill_tree.column("rate", width=100)
discharge_bill_tree.column("amount", width=100)




discharge_bill_subTotal_label = tk.Label(discharge_bill_addServices_frame, text="Sub Total :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_subTotal_label.grid(row=3, column=6, pady=5, sticky='e')

discharge_bill_subTotal_fetched = tk.StringVar()
discharge_bill_subTotal_fetched.set("")
tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_subTotal_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=3, column=7, pady=5, sticky='w')


##


discharge_bill_gst_label = tk.Label(discharge_bill_addServices_frame, text="G.S.T. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_gst_label.grid(row=4, column=0)

discharge_bill_gst_fetched = tk.StringVar()
discharge_bill_gst_fetched.set("")
tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_gst_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=4, column=1, pady=5)

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=4, column=2)

discharge_bill_discount_label = tk.Label(discharge_bill_addServices_frame, text="Discount :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_discount_label.grid(row=4, column=3, sticky='e')

discharge_bill_discount_entry = tk.StringVar()
discharge_bill_discount_entry.set("")
tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_discount_entry,font=('Arial', 12, "bold"), bg='#fff', validate="key", validatecommand=(validate_real_cmd)).grid(row=4, column=4, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=4, column=5)

discharge_bill_roundOff_label = tk.Label(discharge_bill_addServices_frame, text="Round Off :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_roundOff_label.grid(row=4, column=6, pady=5, sticky='e')

discharge_bill_roundOff_fetched = tk.StringVar()
discharge_bill_roundOff_fetched.set("")
tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_roundOff_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=4, column=7, pady=5, sticky='w')


##


discharge_bill_totalPaidAmount_label = tk.Label(discharge_bill_addServices_frame, text="Total Paid Amount :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_totalPaidAmount_label.grid(row=5, column=0)

discharge_bill_totalPaidAmount_fetched = tk.StringVar()
discharge_bill_totalPaidAmount_fetched.set("")
tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_totalPaidAmount_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=5, column=1, pady=5)

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=5, column=2)

discharge_bill_totalDuesAmount_label = tk.Label(discharge_bill_addServices_frame, text="Total Dues Amount :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_totalDuesAmount_label.grid(row=5, column=3, sticky='e')

discharge_bill_totalDuesAmount_fetched = tk.StringVar()
discharge_bill_totalDuesAmount_fetched.set("")
tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_totalDuesAmount_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=5, column=4, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=5, column=5)

# discharge_bill_recievedAmount_label = tk.Label(discharge_bill_addServices_frame, text="Recieved Amount :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
# discharge_bill_recievedAmount_label.grid(row=5, column=6, pady=5, sticky='e')

discharge_bill_recievedAmount_fetched = tk.StringVar()
discharge_bill_recievedAmount_fetched.set("")
# tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_recievedAmount_fetched,font=('Arial', 12, "bold"), bg='#fff', state='readonly').grid(row=5, column=7, pady=5, sticky='w')


discharge_bill_balanceAmount_label = tk.Label(discharge_bill_addServices_frame, text="Balance Amount :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
discharge_bill_balanceAmount_label.grid(row=5, column=6, pady=5, sticky='e')

discharge_bill_balanceAmount_fetched = tk.StringVar()
discharge_bill_balanceAmount_fetched.set("")
tk.Entry(discharge_bill_addServices_frame, text=discharge_bill_balanceAmount_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=5, column=7, pady=5, sticky='w')

tk.Label(discharge_bill_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=7, column=0)



discharge_bill_submit_btn_outer = tk.Frame(discharge_bill_addServices_frame, bg="white")
discharge_bill_submit_btn_outer.grid(row=8, column=0, columnspan=9, sticky='ew')

discharge_bill_submit_btn = tk.Button(discharge_bill_submit_btn_outer, text="Generate Bill", bg='green', fg='white', cursor='hand2', border=5, font=('Arial', 15, "bold"), command=discharge_bill_generate_bill)
discharge_bill_submit_btn.pack(pady=15)




# Update Patient Frame

updatePatient_frame = tk.Frame(root)
    
updatePatient_container = tk.Frame(updatePatient_frame, bg='#fff', bd=2, relief='solid')
updatePatient_container.pack()

updatePatient_header = tk.Frame(updatePatient_container,  bg='grey', borderwidth=5, relief="groove")
updatePatient_header.grid(row=0, column=0, pady=10, sticky='ew')

updatePatient_header_back_btn = tk.Button(updatePatient_header, text="Back", bg="orange", fg="#fff", font=("Arial", 16), command=updatePatient_back)
updatePatient_header_back_btn.grid(row=0, column=0)

updatePatient_header_title = tk.Label(updatePatient_header, text="\t\t\t\t      Discharge Bill      \t\t\t\t", font=('Arial', 18), bg='grey', fg='white')
updatePatient_header_title.grid(row=0, column=1)

updatePatient_header_exit_btn = tk.Button(updatePatient_header, text="Exit", bg="red", fg="#fff", font=("Arial", 16), command=exit)
updatePatient_header_exit_btn.grid(row=0, column=3)

updatePatient_form = tk.Frame(updatePatient_container, bg='#fff', bd=2, relief='solid')
updatePatient_form.grid(row=1, column=0, pady=10, padx=200, sticky='')

updatePatient_registrationNo_label = tk.Label(updatePatient_form, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_registrationNo_label.grid(row=0, column=0, pady=5)

updatePatient_registrationNo_entry = tk.Entry(updatePatient_form, font=('Arial', 12), border=2)
updatePatient_registrationNo_entry.grid(row=0, column=1, pady=5)

updatePatient_find_btn = tk.Button(updatePatient_form, text="Find", bg='lightgrey', command=updatePatient_fetch_patient_details)
updatePatient_find_btn.grid(row=0, column=2, pady=2, padx=5)

updatePatient_fetched_deatils_frame = tk.Frame(updatePatient_container, bg='#fff', pady=10, padx=25)
updatePatient_fetched_deatils_frame.grid(row=2, column=0)



updatePatient_registrationNo_label = tk.Label(updatePatient_fetched_deatils_frame, text="Registration No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_registrationNo_label.grid(row=1, column=0, sticky='w')

updatePatient_registrationNo_fetched = tk.StringVar()
updatePatient_registrationNo_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_registrationNo_fetched, state='readonly',font=('Arial', 12, "bold"), bg='#fff').grid(row=1, column=1, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=1, column=2)

updatePatient_patientName_label = tk.Label(updatePatient_fetched_deatils_frame, text="Patient Name :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_patientName_label.grid(row=1, column=3, sticky='e')

updatePatient_patientName_fetched = tk.StringVar()
updatePatient_patientName_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_patientName_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=1, column=4, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=1, column=5)

updatePatient_contactNo_label = tk.Label(updatePatient_fetched_deatils_frame, text="Contact No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_contactNo_label.grid(row=1, column=6, pady=5, sticky='e')

updatePatient_contactNo_fetched = tk.StringVar()
updatePatient_contactNo_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_contactNo_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=1, column=7, pady=5, sticky='w')

updatePatient_age_label = tk.Label(updatePatient_fetched_deatils_frame, text="Age :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_age_label.grid(row=2, column=0, sticky='w')

updatePatient_age_fetched = tk.StringVar()
updatePatient_age_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_age_fetched, font=('Arial', 12, "bold"), bg='#fff').grid(row=2, column=1, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=2, column=2)

updatePatient_gender_label = tk.Label(updatePatient_fetched_deatils_frame, text="Gender :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_gender_label.grid(row=2, column=3, sticky='e')

updatePatient_gender_fetched = tk.StringVar()
updatePatient_gender_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_gender_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=2, column=4, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=2, column=5)

updatePatient_address_label = tk.Label(updatePatient_fetched_deatils_frame, text="Address :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_address_label.grid(row=2, column=6, pady=5, sticky='e')

updatePatient_address_fetched = tk.StringVar()
updatePatient_address_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_address_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=2, column=7, pady=5, sticky='w')

updatePatient_co_label = tk.Label(updatePatient_fetched_deatils_frame, text="C/O :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_co_label.grid(row=3, column=0, sticky='w')

updatePatient_co_fetched = tk.StringVar()
updatePatient_co_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_co_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=3, column=1, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=3, column=2)


updatePatient_so_label = tk.Label(updatePatient_fetched_deatils_frame, text="S/O :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_so_label.grid(row=3, column=3, pady=5, sticky='e')

updatePatient_so_fetched = tk.StringVar()
updatePatient_so_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_so_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=3, column=4, pady=5, sticky='w')

updatePatient_consulant_label = tk.Label(updatePatient_fetched_deatils_frame, text="Consultant :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_consulant_label.grid(row=4, column=0, sticky='w')

updatePatient_consultant_fetched = tk.StringVar()
updatePatient_consultant_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_consultant_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=4, column=1, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=4, column=2)

updatePatient_ward_label = tk.Label(updatePatient_fetched_deatils_frame, text="Ward :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_ward_label.grid(row=4, column=3, sticky='e')

updatePatient_ward_fetched = tk.StringVar()
updatePatient_ward_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_ward_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=4, column=4, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=4, column=5)

updatePatient_bedNo_label = tk.Label(updatePatient_fetched_deatils_frame, text="Bed No. :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_bedNo_label.grid(row=4, column=6, pady=5, sticky='e')

updatePatient_bedNo_fetched = tk.StringVar()
updatePatient_bedNo_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_bedNo_fetched,font=('Arial', 12, "bold",), bg='#fff').grid(row=4, column=7, pady=5, sticky='w')


updatePatient_admitDate_label = tk.Label(updatePatient_fetched_deatils_frame, text="Admit Date :- ", font=('Arial', 12, "bold"), bg='#fff', anchor='w')
updatePatient_admitDate_label.grid(row=5, column=0, pady=5, sticky='w')

updatePatient_admitDate_fetched = tk.StringVar()
updatePatient_admitDate_fetched.set("")
tk.Entry(updatePatient_fetched_deatils_frame, text=updatePatient_admitDate_fetched,font=('Arial', 12, "bold"), bg='#fff').grid(row=5, column=1, pady=5, sticky='w')

tk.Label(updatePatient_fetched_deatils_frame, text='                    ', bg='#fff').grid(row=5, column=2)


updatePatient_addServices_frame = tk.Frame(updatePatient_container, bg='white', pady=10)
updatePatient_addServices_frame.grid(row=3, column=0)

updatePatient_tree = ttk.Treeview(updatePatient_addServices_frame, height=8, columns=("particulars","aDate", "iDate", "unit", "qty", "rate", "amount"), show='headings')
updatePatient_tree.configure(height=16)
updatePatient_tree.grid(row=2, column=0, columnspan=9, sticky='ew', pady=10)

updatePatient_tree.heading("particulars", text="Particulars")
updatePatient_tree.heading("aDate", text="Active Date")
updatePatient_tree.heading("iDate", text="Inactive Date")
updatePatient_tree.heading("unit", text="Unit")
updatePatient_tree.heading("qty", text="Qty")
updatePatient_tree.heading("rate", text="Rate")
updatePatient_tree.heading("amount", text="Amount")

updatePatient_tree.column("particulars", width=200)
updatePatient_tree.column("aDate", width=100)
updatePatient_tree.column("iDate", width=100)
updatePatient_tree.column("unit", width=40)
updatePatient_tree.column("qty", width=40)
updatePatient_tree.column("rate", width=100)
updatePatient_tree.column("amount", width=100)

# Function to handle double-click event on a cell
def on_double_click(event):
    # Identify the row and column under the click
    region = updatePatient_tree.identify("region", event.x, event.y)
    if region == "cell":
        row_id = updatePatient_tree.identify_row(event.y)
        column_id = updatePatient_tree.identify_column(event.x)

        # Get the item and column index
        item = updatePatient_tree.item(row_id)
        column = updatePatient_tree.column(column_id, 'id')

        # Get the current value of the cell
        cell_value = item['values'][int(column_id[1:]) - 1]

        # Place an entry widget over the cell for editing
        entry = tk.Entry(updatePatient_addServices_frame)
        entry.insert(0, cell_value)
        entry.select_range(0, 'end')

        # Function to update the cell value and remove the entry widget
        def on_focus_out(event):
            new_value = entry.get()
            updatePatient_tree.set(row_id, column=column, value=new_value)
            entry.destroy()

        entry.bind("<FocusOut>", on_focus_out)

        # Get the bounding box of the cell and place the entry widget
        x, y, width, height = updatePatient_tree.bbox(row_id, column_id)
        entry.place(x=x, y=y+10, width=width, height=height)
        entry.focus()

# Bind the double-click event to the Treeview
updatePatient_tree.bind("<Double-1>", on_double_click)


updatePatient_submit_btn_outer = tk.Frame(updatePatient_addServices_frame, bg="white")
updatePatient_submit_btn_outer.grid(row=8, column=0, columnspan=9, sticky='ew')

updatePatient_submit_btn = tk.Button(updatePatient_submit_btn_outer, text="Update", bg='green', fg='white', cursor='hand2', border=5, font=('Arial', 15, "bold"), command=updatePatient_update)
updatePatient_submit_btn.pack(pady=15)



# Run the application
root.mainloop()