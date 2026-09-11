

from re import search
from abc import abstractmethod,ABC
from collections import Counter
from datetime import datetime

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
    
    @abstractmethod
    def view_all_members(self):
        pass


class Police(Person):

    list_of_police=[]
    def __init__(self,id,name,age,gender,phone,rank, department):
        super().__init__(id,name,age,gender,phone)
        self.rank=rank
        self.department=department
        self.assigned_cases=[]
        Police.list_of_police.append(self)

    def show_profile(self):
        return f"{self.id},{self.name},{self.rank},{self.department},{self.assigned_cases}"

    def search_profile(self,name=None,id=None):
        print(f"{name},{id}")
        for x in Police.list_of_police:
            if x.name==name:
                return f"Police officer name {name} found, whose id {x.id},rank{x.rank}"
            elif x.id==id:
                return f"Police officer name {x.name} found, whose id {id},rank {x.rank}"
        return "Not found this officer with the name or id you provided!"

    '''
    ❌❌Why the below method failing

      File , line 49, in view_all_members
            s=" ".join(x.id,x.name,x.age,x.rank)
        TypeError: str.join() takes exactly one argument (4 given)

    Reason:
     " ".join() only accepts a list of strings, but you passed individual variables (x.id, x.name, etc.) which are not in a list. Also, you were overwriting s in every loop instead of adding to it.

    Failed Code snippet:
    # def view_all_members(self):
    #     for x in Police.list_of_police:
    #         s=" ".join(x.id,x.name,x.age,x.rank)
    #     return s
    '''
    def view_all_members(self):
         for x in Police.list_of_police:
            print(x.id,x.name,x.rank)


    def assign_to_case(self,crime_obj):
        if crime_obj not in self.assigned_cases:
            self.assigned_cases.append(crime_obj)

            if self not in crime_obj.assigned_officers:
                crime_obj.assigned_officers.append(self)
            return f"Officer {self.name} assigned to Case #{crime_obj.crime_id} and type {crime_obj.crime_type}"
        return f"Officer is already assigned to the Case#{crime_obj.crime_id}"

    def view_all_my_cases(self):
        if not self.assigned_cases:
            return f"No cases assigned to the officer {self.name}"
        report=f"Cases handaled by officer {self.name} \n"
        for x in self.assigned_cases:
            report+=f"Crime id{x.crime_id} and it's type {x.crime_type} and description{x.description}\n"
        return report


class Criminal(Person):

    list_of_criminals=[]

    def __init__(self,id,name,age,gender,phone,address,status,aliases):
        super().__init__(id,name,age,gender,phone)
        self.address=address
        self.status=status
        #self.aliases=aliases
        self.aliases = set(aliases) if isinstance(aliases, (list, tuple, set)) else {aliases}
        #Instead of forcing whoever creates the object to remember to use a set, modify:
        '''
            Then all of these work:

            Criminal(..., "DON")
            Criminal(..., ["DON", "Black Don"])
            Criminal(..., {"DON", "Black Don"})

            and internally you'll always have:

            self.aliases

            as a set.
        '''
        self.crime_records=[]
        Criminal.list_of_criminals.append(self)

    def show_profile(self):
        return f"{self.id},{self.name},{self.age},{self.gender},{self.crime_records}"

    def search_profile(self,name=None,id=None):
        for x in Criminal.list_of_criminals:
            if x.name==name:
                return f"Person name {name} found on the criminal list, whose id {x.id},status {x.status}"
            elif x.id==id:
                return f"Person name {x.name} found on the criminal list, whose id {id},status {x.status}"

        return "Not found this named criminal!"

    def view_all_members(self):
        if not Criminal.list_of_criminals:
            return "No Criminal Record found"
        
        result="------All The Criminals---------\n"
        for x in Criminal.list_of_criminals:
            # details=" ".join(str[x.id],x.name,str[x.age],x.rank) #❌Error I got: TypeError: type 'str' is not subscriptable
            '''
            The error happened because you used square brackets [] instead of parentheses ().
            str[x.id] tells Python to treat str like a list and try to find an item at index x.id. Since str is a function/type, not a list, it fails.

            Correct way: str(x.id) uses parentheses to call the function and convert the value to a string.
            Also, join() requires a list or tuple, so you must wrap them:
            " ".join([str(x.id), x.name, ...])
            '''
            details=" ".join([str(x.id),x.name,str(x.age),x.status])
            result+=details+"\n"
        return result


    def add_crime_record(self,crime_obj):

        # record={
        #     "crime_type":crime_type,
        #     "description":description
        # }
        self.crime_records.append(crime_obj)

    
    def get_crime_record(self):

        if len(self.crime_records)==0:
            return "No crime record found"


        result=f"Crime record for {self.name}\n"

        for i,x in enumerate(self.crime_records,1):
                # result+=f"{i} id {self.id} {x['crime_type']}:{x['description']}\n"
                result += f"{i}. Crime ID: {x.crime_id} | Type: {x.crime_type} | Description: {x.description}"
        return result

    def update_criminal_info(self,user,**kwargs):
        if not isinstance(user,Police):
           return "Access Denied: Only Police officers can update criminal information."

        for key,value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
            else:
                return f"Error : '{key}' is not a valid attribute of criminal"
        return f"Criminal {self.name}'s information updated by the officer {user.name}"
    
    def add_new_crime_by_police(self,user,crime_obj):
        if not isinstance(user,Police):
            return "Access Denied: Only Police officers can add crime records."

        self.crime_records.append(crime_obj)

        if self not in crime_obj.suspects:
            crime_obj.suspects.append(self)
            '''
            self.suspects = suspects লাইনটি suspects-কে ক্লাসের একটি অ্যাট্রিবিউট হিসেবে ডিক্লেয়ার করছে।
            কিন্তু আপনি যখন অবজেক্ট তৈরি করছেন (crime2 = Crime()), তখন আপনি [criminal_don] এই লিস্টটি পাস করেছেন।
            ফলে self.suspects এখন একটি লিস্ট হয়ে গেছে এবং এতে .append() ব্যবহার করা যাচ্ছে।
            '''
        
        return f"New crime record added to {self.name}"


class Crime: 
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
        # self.crime_record = {
        #     "crime_id": crime_id,
        #     "crime_type": crime_type,
        #     "Date": date,
        #     "Location": location,
        #     "Description": description,
        #     "Severity": severity,
        #     "Suspects": suspects,
        #     "Victims": victims,
        #     "Assigned_officers": assigned_officers,
        #     "Evidence": evidence,
        #     "Case_status": case_status
        # }
        Crime.list_of_all_crimes.append(self)

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

        if not kwargs:
            return "No fields provided for update"
        '''
        Without validation of kwargs-
        The problem is:
            crime1.modify_crime_record(
                officer_kamal,
                banana="something"
            )

        will say:
            updated successfully
            even though nothing was updated.
        '''
        allowed_fields={"case_status", "description", "evidence"}

        invalid_fields=set(kwargs)-allowed_fields

        if invalid_fields:
            return f"Invalid fields: {', '.join(invalid_fields)}"

        if 'case_status' in kwargs:
            self.case_status=kwargs['case_status']
        if 'description' in kwargs:
            self.description=kwargs['description']
        if 'evidence' in kwargs:
            self.evidence=kwargs['evidence']
        
        return f"Crime{self.crime_id} updated successfully by the officer  {user.name}"

    @staticmethod
    def view_all_crime_records():
        if not Crime.list_of_all_crimes:
            return "No crime records found"

        report = "--- All Recorded Crimes ---\n"
        for crime in Crime.list_of_all_crimes:
            report += f"ID: {crime.crime_id} | Type: {crime.crime_type} | Status: {crime.case_status} | Suspect: {crime.suspects[0].name if crime.suspects else 'Unknown'}\n"
        return report


class Case:
    '''
    Case should not inherit from Crime just because it has a Crime ID.

    A Case is associated with a Crime; it is not a specialized type of Crime.

    So:

        Case
        ↓
        has/reference
        ↓
        Crime

    not:

        Case
        ↓
        inherits from
        ↓
        Crime
    
    '''
    list_of_all_cases=[]

    def __init__(self,case_id,crime_obj,date_opened,case_status,notes,date_closed=None):

        # Initialize Case-specific attributes
        self.case_id = case_id
        self.crime=crime_obj
        self.date_opened = date_opened
        self.case_status = case_status
        self.notes = notes
        self.date_closed = date_closed  # Optional, defaults to None
        Case.list_of_all_cases.append(self)

    @staticmethod
    def view_all_case_details():
        if not Case.list_of_all_cases:
            return f"No cases found"
        cases="----------------All the crimse converted in case----------------\n"
        for x in Case.list_of_all_cases:
            cases+=f"Case Id: {x.case_id}, Opend Date: {x.date_opened}, Case current Status: {x.case_status},  Crime id of this Case:{x.crime.crime_id}, Crime Type for this Case:{x.crime.crime_type}\n"
        return cases 


    def assigned_officers(self,officer):
        if officer in self.crime.assigned_officers:
            raise ValueError(
                f"Officer {officer.name} is already assigned to Case {self.case_id}"
            )
        self.crime.assigned_officers.append(officer)

        if self not in officer.assigned_cases:#এটার মানে হচ্ছে, এই কেইস টা যদি এই অফিসারের assigned_cases লিস্টে অলরেডি না থাকে, তবে তা ইনক্লুড করা 
            officer.assigned_cases.append(self)
        
        return f"Officer {officer.name} assigned to Case#{self.case_id}"
    '''
    changes the related Crime:

        Case
        ↓
        crime
        ↓
        assigned_officers
        ↓
        Kamal

    and also updates the officer:

        Kamal
        ↓
        assigned_cases
        ↓
        case1

    That's perfectly valid.
    '''

    def view_all_assigned_officer(self):

        all_officers=f"All the assigned officer to the case : {self.case_id}\n"

        for x in self.crime.assigned_officers:
            all_officers+=f"Officer name {x.name} rank {x.rank}"
        return all_officers


    def assign_suspects(self,criminal):
        if criminal in self.crime.suspects:
            raise ValueError(
                f"Criminal {criminal.name} already assigned as suspect on the case {self.case_id}"
            )
        self.crime.suspects.append(criminal)

        if self not in criminal.crime_records: 
            criminal.crime_records.append(self)

        return f"Criminal {criminal.name} assigned with the case {self.case_id}"
    
    def view_all_assign_suspects(self):

        all_suspects=f"All suspects of the Case {self.case_id}\n"
        for x in self.crime.suspects:
            all_suspects+=f"{x.id} {x.name}\n"
        return all_suspects


    def remove_suspects(self,criminal):
        if criminal in self.crime.suspects:
            self.crime.suspects.remove(criminal)
            return f"Criminal {criminal.name} removed from the case {self.case_id}"
        return f"Criminal {criminal.name} isn't a part of the  case {self.case_id}"


    def assign_victims(self,victim_obj):
        if victim_obj in self.crime.victims:
            raise ValueError(f"This Victim {victim_obj.name} already on that case ")
        self.crime.victims.append(victim_obj)
        return f"Victims {victim_obj.name} assigned with the case {self.case_id}"

    def view_all_victims(self):
        all_victims=f"All victims of the case {self.case_id}\n"
        for x in self.crime.victims:
            all_victims+=f"{x.name} {x.id}\n"
        return all_victims


    def remove_victim(self,victim_obj):
        if victim_obj in self.crime.victims:
            self.crime.victims.remove(victim_obj)
            return f"Victim {victim_obj.name} removed from the case {self.case_id}"
        return f"Victim {victim_obj.name} not related with the case"


    def change_case_status(self,status=None):
        self.case_status=status
        return f"Case status for the case {self.case_id} changed to {status}"


    def add_evidence(self,new_evidence=None):
        self.crime.evidence.append(new_evidence)

        all_evidence = f"All the latest evidence of the case {self.case_id}\n"

        for x in self.crime.evidence:
            all_evidence+=x +"\n"
        
        return f"Evidence added with the case {self.case_id}\n All the evidence {all_evidence}"


    '''
    -why I'm considering this two as a static method why not other method like class or object

    @staticmethod
    def global_search(query):

    @staticmethod
    def generate_statistics()


    Because these methods do not require access to a specific instance's data (self) or the class itself (cls).

    global_search: Operates on Case.list_of_all_cases, which is a shared class-level list. It doesn't need any individual case object's state.
    generate_statistics: Aggregates data from multiple global lists (Crime.list_of_all_crimes, Criminal.list_of_criminals, etc.). It is a pure utility function that produces a report independent of any single object.

    Using @staticmethod makes this explicit: "This function belongs to the Case namespace logically, but it does not depend on any Case instance." You can call it directly via Case.global_search("theft") without creating a dummy object first.
    '''

    @staticmethod
    def global_search(query):

        if not query:
            return []
        
        q = str(query).lower().strip()
        results=[]

        for case in Case.list_of_all_cases:
            # crime=case.crime \

            searchable_text=" ".join([
                str(case.case_id),
                str(case.crime.crime_id),
                case.crime.crime_type.lower(),
                case.crime.location.lower(),
                case.case_status.lower(),
                str(case.crime.date),
                *[s.name.lower() for s in case.crime.suspects],
                *[o.name.lower() for o in case.crime.assigned_officers],
                *[v.name.lower() for v in case.crime.victims]
            ])
            '''
            The * operator unpacks the list comprehension into individual arguments.
            With *: [a, b] becomes two separate items: "alice", "bob".
            Without *: [a, b] remains a single nested list object: ["alice", "bob"].
            Since you are passing these to " ".join(), which expects flat strings, omitting * would cause a TypeError because it cannot join a list inside a list. The first six items don't need * because they are already individual values, not lists.
            '''

            if q in searchable_text:
                results.append(case)
        
        return results
    
    @staticmethod
    def generate_statistics():
        '''
        stats হলো একটি Nested Dictionary (Dictionary-এর ভেতরে Dictionary)।
        stats["open_cases"] → সরাসরি Integer value (0, 1, 2...)
        stats["crime_types"] → নিজেই একটি আলাদা Dictionary/Counter ({"Theft": 5, "Murder": 2})
        তাই প্রথমটির ক্ষেত্রে সরাসরি += 1 করা যায়, কিন্তু দ্বিতীয়টির ক্ষেত্রে আগে Key সিলেক্ট করে [crime.crime_type] তারপর += 1 করতে হয়।
        
        '''
        stats ={

            "total_cases":len(Case.list_of_all_cases),
            "open_cases":0,
            "closed_cases": 0,
            "investigating_cases": 0,
            "total_criminals":len(Criminal.list_of_criminals),
            "wanted_criminals":0,
            "total_officers": len(Police.list_of_police),
            "total_victims": len(Victims.list_of_victims),
            "crime_types": Counter(),
            "locations": Counter(),
            "months": Counter(),
            "officer_assignments": Counter()
        }

        for case in Case.list_of_all_cases:
            crime=case.crime

            status=case.case_status.lower()
            if status=="open":
                stats["open_cases"]=stats["open_cases"]+1
            elif status == "closed": stats["closed_cases"] += 1
            else: stats["investigating_cases"] += 1


            stats["crime_types"][crime.crime_type]+=1
            '''
            এখানে আপনি একটু কনফিউজড হয়েছেন। stats["crime_types"] হলো একটি Dictionary (বা Counter), সাধারণ সংখ্যা নয়। তাই এখানে + 1 করলে হবে না, বরং নির্দিষ্ট Key-এর ভ্যালু বাড়াতে হবে।
            stats["crime_types"] = পুরো ডিকশনারি (যেমন: {"Theft": 5, "Murder": 2})
            stats["crime_types"]["Theft"] = শুধু Theft-এর সংখ্যা (যেমন: 5)
            '''
            stats["locations"][crime.location]+=1

            try: 
                dt=datetime.strptime(str(crime.date),"%Y-%m-%d")
                stats["months"][dt.strftime("%B %Y")]+=1
            except (ValueError,TypeError):
                pass

            for officer in crime.assigned_officers:
                stats["officer_assignments"][officer.name]+=1
        
        for criminal in Criminal.list_of_criminals:
            if getattr(criminal,'status','').lower()=='wanted':
                stats["wanted_criminals"]+=1
        
        most_common_type=stats["crime_types"].most_common(1)
        most_reported_area=stats["locations"].most_common(1)
        most_active_officer=stats["officer_assignments"].most_common(1)
        '''
         most_common(1) মেথডটি একটি List of Tuples রিটার্ন করে।

            🔍 most_common() আসলে কী?
            এটি Python-এর built-in মেথড। এটি collections.Counter ক্লাসের নিজস্ব ফাংশন, যা অটোমেটিক্যালি আইটেমগুলোকে তাদের ফ্রিকোয়েন্সি (frequency) অনুযায়ী সাজিয়ে সর্বোচ্চ N সংখ্যক আইটেম (key, count) টাপল আকারে রিটার্ন করে।
            এটি Counter ডিকশনারিকে সর্ট করে সবচেয়ে বেশি ব্যবহৃত আইটেমগুলো বের করে এবং (key, value) আকারে লিস্টে রাখে:

            [0][0] এবং [0][1] কীভাবে কাজ করে?

            যেহেতু এটি List of Tuple, তাই ইনডেক্সিং দুই ধাপে হয়:

            উদাহরণ ভ্যালু

            most_common_type[0]
            লিস্টের ১ম টাপল নেওয়া
            ("Theft", 5)

            ...[0][0]
            ওই টাপলের ১ম উপাদান (Name)
            "Theft"

            ...[0][1]
            ওই টাপলের ২য় উপাদান (Count)
            5

            ️ if most_common_type else 'N/A' কেন?
            যদি কোনো ক্রাইম বা অফিসার না থাকে, তবে most_common(1) খালি লিস্ট [] রিটার্ন করবে। তখন [0] দিলে IndexError আসবে। এই চেকটি সেই এরর প্রতিরোধ করে এবং 'N/A' দেখায়।
        
        '''
        report = f"""
===== CRIME STATISTICS REPORT =====
Total Cases          : {stats['total_cases']}
Open Cases           : {stats['open_cases']}
Closed Cases         : {stats['closed_cases']}
Investigating Cases  : {stats['investigating_cases']}
Total Criminals      : {stats['total_criminals']}
Wanted Criminals     : {stats['wanted_criminals']}
Total Officers       : {stats['total_officers']}
Total Victims        : {stats['total_victims']}


Most Common Crime: {most_common_type[0][0] if most_common_type else 'N/A'}({most_common_type[0][1] if most_common_type else 0} cases)
Most Reported Area   : {most_reported_area[0][0] if most_reported_area else 'N/A'} ({most_reported_area[0][1] if most_reported_area else 0} cases)
Most Active Officer  : {most_active_officer[0][0] if most_active_officer else 'N/A'} ({most_active_officer[0][1] if most_active_officer else 0} assignments)



--- Crimes by Month ---
"""
'''
# {most_common_type[0][1]} শুধুমাত্র সংখ্যাটা (যেমন: 5) প্রিন্ট করবে। কিন্তু ইউজার যখন দেখবে, তখন বুঝতে পারবে না এই ৫ কিসের সংখ্যা। তাই পড়ার সুবিধার্থে এবং রিপোর্টটি প্রফেশনাল দেখানোর জন্য ম্যানুয়ালি " cases" শব্দটি যোগ করা হয়েছে।
# সহজ কথায়:
# কোড আউটপুট: 5
# ফরম্যাটেড আউটপুট: 5 cases
'''

class Victims(Person):
    list_of_victims=[]
    def __init__(self,id,name,age,gender,phone,address,case_obj,statement):
        super().__init__(id,name,age,gender,phone)
        self.case_obj = case_obj
        self.statment=statement
        Victims.list_of_victims.append(self)

    
    def show_profile(self):
        return f"Victim Id: {self.id} His name: {self.name} The Case he's handling {self.case_obj.case_id} and his case current status : {self.case_obj.case_status}"

    def search_profile(self,name=None,id=None):
        if name: 
            print(f"Search profile for the victim , whose name {name}")
        else: 
            print(f"Search profile for the victim, whose id {id}")

        for x in Victims.list_of_victims:
            if x.name == name: 
                return f"Victims with the name {x.name} found on the victim list"
            elif x.id == id:
                return f"Victims with the id {x.id} found on the victim list"
    
    def view_all_members(self):
        victim_list="List of all the victims\n"
        for x in Victims.list_of_victims:
            victim_list+=f"Victim name {x.name}, His id {x.id} Case he's with {self.case_obj.case_id}\n" #I think on victim can have multiple case how to show it
        return victim_list

    def view_all_cases_of_victim(self):
        all_case=f"All Cases of the Victim {self.name}\n"
        for x in self.case_obj.list_of_all_cases:
            all_case+=f"{x.case_id} {x.case_status} \n"
        return all_case

    def update_victim_profile(self,user,**kwargs):
        if not isinstance(user,Police):
            raise ValueError(f"Only Police can update victims information")
        
        for key,value in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)
            else:
                raise ValueError(f"Key {key} is not any attribute of the victim profile")

        return f"Victim{self.name} profile updated by the cop {user.name}"







#------------------------------------------------------------------------------------
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
criminal_don = Criminal("1009", "Don1", "48", "Male", "12345667", "dhaka", "Wanted", {"DON", "Black Don", "DON"})
criminal_jack = Criminal("1010", "Jack", "30", "Male", "11223344", "chittagong", "Arrested", {"JACKY"})

# 2. Create a Crime (Linking Suspects and Officers)
try:
    crime1 = Crime(
        crime_id="C-101",
        crime_type="Theft",
        date="2026-09-01",
        location="Green Road, Dhaka",
        description="Stole a wallet from a pedestrian.",
        severity="Medium",
        suspects=[criminal_don],       # Foreign Key: List of Criminal Objects
        victims=[],
        assigned_officers=[officer_kamal], # Foreign Key: List of Police Objects
        evidence=["CCTV fotage"],
        case_status="Investigating"
    )
    
    crime2 = Crime(
        crime_id="C-102",
        crime_type="Murder",
        date="2026-01-06",
        location="Mirpur, Dhaka",
        description="Suspected homicide.",
        severity="High",
        suspects=[criminal_don, criminal_jack],
        victims=[],#Initialize the crime with an empty list first, then add the victim later using your existing assign_victims method:
        assigned_officers=[officer_rahim],
        evidence=[],
        case_status="Open"
    )
except ValueError as e:
    print(e)

#search profile by name or id
# print(officer_kamal.search_profile(id="2004"))
# print(criminal_jack.search_profile(id="1009"))

# print(officer_kamal.view_all_members())
# print(criminal_don.view_all_members())


# # 3. View All Crimes
# print(Crime.view_all_crime_records())
# print("\n")

# # 4. View Specific Crime Details
# print(crime1.view_details())

# # 5. Check Criminal's History (Bi-directional link check)
# print(criminal_don.get_crime_record())

# # 6. Modify Crime (Verification Test)
# # Try with a Criminal (Should Fail)
# print("\n--- Modification Tests ---")
# print(crime1.modify_crime_record(criminal_don, case_status="Closed")) 

# # Try with a Police Officer (Should Succeed)
# print(crime1.modify_crime_record(officer_kamal, case_status="Closed", evidence="New Witness Statement"))

# # Verify Change
# print("\n" + crime1.view_details())


print(officer_kamal.assign_to_case(crime1))
print(officer_kamal.assign_to_case(crime2))

print(officer_kamal.view_all_my_cases())


print(criminal_don.add_crime_record(crime1))
print(crime1.modify_crime_record(
    officer_kamal,
    banana="something"
))

case1=Case("2000",crime1,"23-5-26","Open","This is a running Case")
print(case1.view_all_case_details())

# case1.assigned_officers(officer_kamal)

print(case1.view_all_assigned_officer())

case1.assign_suspects(criminal_jack)

print(case1.remove_suspects(criminal_jack))
print(case1.view_all_assign_suspects())

#id,name,age,gender,phone,address,case_obj,statement
victim1=Victims(id="999",name="Mr Vicky",age=44,gender="male",phone=834343,address="Dhaka",case_obj=case1,statement="I want the result soon")


print(victim1.show_profile())

print(case1.assign_victims(victim1))
print(case1.view_all_victims())



print(case1.change_case_status(status="Closed"))

print(case1.add_evidence(new_evidence="Finger Print"))


print(victim1.view_all_cases_of_victim())
print(victim1.update_victim_profile(officer_kamal,name="zamal"))#Argument Order: user is the first positional parameter, so officer_kamal must come before name="zamal".



search_results=Case.global_search("theFT")
print(f"Found {len(search_results)} cases for 'theft' ")

for c in search_results:
    print(f" >Case #{c.case_id} | {c.crime.crime_type} | {c.crime.location}")