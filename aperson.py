

from abc import abstractmethod,ABC

class Person(ABC):
    def __init__(self,id,name,age,gender,phone):
        self.id=id
        self.name=name 
        self.age=age 
        self.gender=gender
        self.phone=phone

    @abstractmethod
    def show_profile(self):
        pass

    @abstractmethod
    def search_profile(self):
        pass
    
class Police(Person):

    list_of_police=[]
    def __init__(self,id,name,age,gender,phone,rank, department):
        super().__init__(id,name,age,gender,phone)
        self.rank=rank
        self.department=department
        Police.list_of_police.append(self)

    def show_profile(self):
        return f"{self.id},{self.name},{self.rank},{self.department}"

    def search_profile(self,name):
        for x in Police.list_of_police:
            if x.name==name:
                return f"Police officer name {name} found, whose id {x.id},rank{x.rank}"
        return "Not found this office!"


class Criminal(Person):

    list_of_criminals=[]

    def __init__(self,id,name,age,gender,phone,address,status,aliases):
        super().__init__(id,name,age,gender,phone)
        self.address=address
        self.status=status
        self.aliases=aliases
        self.crime_records=[]
        Criminal.list_of_criminals.append(self)

    def show_profile(self):
        return f"{self.id},{self.name},{self.age},{self.gender}"

    def search_profile(self,name):
        for x in Criminal.list_of_criminals:
            if x.name==name:
                return f"Person name {name} found on the criminal list, whose id {x.id},status {x.status}"
        return "Not found this named criminal!"

    def add_crime_record(self,crime_obj):

        # record={
        #     "crime_type":crime_type,
        #     "description":description
        # }
        self.crime_records.append(crime_obj)

    
    def get_crime_record(self,name=None):

        if len(self.crime_records)==0:
            return "No crime record found"


        result=f"Crime record for {self.name}\n"

        for i,x in enumerate(self.crime_records,1):
                # result+=f"{i} id {self.id} {x['crime_type']}:{x['description']}\n"
                result += f"{i}. Crime ID: {x.crime_id} | Type: {x.crime_type} | Description: {x.description}"
        return result




class CrimeManagement: 
    list_of_all_crimes=[]

    VALID_CRIME_TYPES=[
        "Theft", "Robbery", "Fraud", "Cyber Crime", 
        "Assault", "Missing Person", "Murder", "Burglary"
    ]
    def __init__(self,crime_id,crime_type,date,location,description,severity,suspects,victims,assigned_officers,evidence,case_status):

        if crime_type not in self.VALID_CRIME_TYPES:
            raise ValueError(f"Invalid crime type. Choose from:{', '.join(self.VALID_CRIME_TYPES)}"
            )
        self.crime_id = crime_id
        self.crime_type = crime_type
        self.date = date
        self.location = location
        self.description = description
        self.severity = severity


        self.suspects = suspects
        self.victims = victims
        self.assigned_officers = assigned_officers
        self.evidence = evidence
        self.case_status = case_status
        self.crime_record = {
            "crime_id": crime_id,
            "crime_type": crime_type,
            "Date": date,
            "Location": location,
            "Description": description,
            "Severity": severity,
            "Suspects": suspects,
            "Victims": victims,
            "Assigned_officers": assigned_officers,
            "Evidence": evidence,
            "Case_status": case_status
        }
        CrimeManagement.list_of_all_crimes.append(self)

        for suspect in self.suspects:
            if isinstance(suspect,Criminal):
                suspect.add_crime_record(self)
    

    def view_details(self):
        suspect_names=", ".join([s.name for s in self.suspects])
        officer_names=", ".join([o.name for o in self.assigned_officers])

        return (f"--- Crime Report #{self.crime_id} ---\n"
                f"Type: {self.crime_type}\n"
                f"Date: {self.date}\n"
                f"Location: {self.location}\n"
                f"Severity: {self.severity}\n"
                f"Suspects: {suspect_names}\n"
                f"Assigned Officers: {officer_names}\n"
                f"Status: {self.case_status}\n"
                f"Description: {self.description}\n"
                f"Evidence: {self.evidence}\n"
                f"--------------------------")

    def modify_crime_record(self,user,**kwargs):
        if not isinstance(user,Police):
            return "Access Denied: Only Police officers can modify crime records."
        if 'case_status' in kwargs:
            self.case_status=kwargs['case_status']
        if 'description' in kwargs:
            self.description=kwargs['description']
        if 'evidence' in kwargs:
            self.evidence=kwargs['evidence']
        
        return f"Crime{self.crime_id} updated successfully by the officer  {user.name}"

    @staticmethod
    def view_all_crime_records():
        if not CrimeManagement.list_of_all_crimes:
            return "No crime records found"

        report = "--- All Recorded Crimes ---\n"
        for crime in CrimeManagement.list_of_all_crimes:
            report += f"ID: {crime.crime_id} | Type: {crime.crime_type} | Status: {crime.case_status} | Suspect: {crime.suspects[0].name if crime.suspects else 'Unknown'}\n"
        return report

# obj=Police("2004","Mr Kamal","44","Male","9878723434","Constable","CID")
# obj2=Criminal("1009","Don1","48","Male","12345667","dhaka","Wanted","DON")
# obj3=Police("20043","Mr Kamal3","443","Male","98787234343","Constable","CID")

# obj2.add_crime_record("Theft","He stole my money")
# obj2.add_crime_record("Murder","He murdered 6th january")
# # obj.show_profile()
# # obj2.show_profile()

# # for x in Police.list_of_police:
# #     print(x.show_profile())

# print(obj2.search_profile("Don2"))
# print(obj2.get_crime_record("Don1"))


# 1. Create Personnel
officer_kamal = Police("2004", "Mr Kamal", "44", "Male", "9878723434", "Constable", "CID")
officer_rahim = Police("2005", "Mr Rahim", "35", "Male", "9876543210", "Inspector", "DB")
criminal_don = Criminal("1009", "Don1", "48", "Male", "12345667", "dhaka", "Wanted", "DON")
criminal_jack = Criminal("1010", "Jack", "30", "Male", "11223344", "chittagong", "Arrested", "JACKY")

# 2. Create a Crime (Linking Suspects and Officers)
try:
    crime1 = CrimeManagement(
        crime_id="C-101",
        crime_type="Theft",
        date="2026-09-01",
        location="Green Road, Dhaka",
        description="Stole a wallet from a pedestrian.",
        severity="Medium",
        suspects=[criminal_don],       # Foreign Key: List of Criminal Objects
        victims=["Mr. X"],
        assigned_officers=[officer_kamal], # Foreign Key: List of Police Objects
        evidence="CCTV Footage",
        case_status="Investigating"
    )
    
    crime2 = CrimeManagement(
        crime_id="C-102",
        crime_type="Murder",
        date="2026-01-06",
        location="Mirpur, Dhaka",
        description="Suspected homicide.",
        severity="High",
        suspects=[criminal_don, criminal_jack],
        victims=["Mr. Y"],
        assigned_officers=[officer_rahim],
        evidence="Knife, Fingerprints",
        case_status="Open"
    )
except ValueError as e:
    print(e)

# 3. View All Crimes
print(CrimeManagement.view_all_crime_records())
print("\n")

# 4. View Specific Crime Details
print(crime1.view_details())

# 5. Check Criminal's History (Bi-directional link check)
print(criminal_don.get_crime_record())

# 6. Modify Crime (Verification Test)
# Try with a Criminal (Should Fail)
print("\n--- Modification Tests ---")
print(crime1.modify_crime_record(criminal_don, case_status="Closed")) 

# Try with a Police Officer (Should Succeed)
print(crime1.modify_crime_record(officer_kamal, case_status="Closed", evidence="New Witness Statement"))

# Verify Change
print("\n" + crime1.view_details())







