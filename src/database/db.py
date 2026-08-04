from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(password,hashed):
    return bcrypt.checkpw(password.encode(),hashed.encode())

def check_teacher_exist(username):
    response=supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0


def create_teacher(username,password,name):
    data={"username":username,"name":name,"password":hash_pass(password)}
    response=supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username,password):
    response=supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    return None


def get_all_students():
    response=supabase.table("students").select("*").execute()
    return response.data


def create_student(name,face_embedding,voice_embedding=None):
    data={"stu_name":name,"face_embedding":face_embedding,"voice_embedding":voice_embedding}

    response=supabase.table("students").insert(data).execute()
    return response.data


def create_subject(sub_code,sub_name,teacher_id,section):
    data={"sub_code":sub_code,"sub_name":sub_name,"teacher_id":teacher_id,"section":section}
    response=supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response=supabase.table("subjects").select("*,subject_students(count),attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subjects=response.data
    for sub in subjects:
        sub["total_students"]=sub.get("subject_students",[{}])[0].get('count',0) if sub.get('subject_students')  else 0
        
        attendance=sub.get("attendance_logs",[])
        sub["total_classes"]=len(set(log["timestamp"] for log in attendance))


        sub.pop("attendance_logs",None)
        sub.pop("subject_students",None)


    return subjects


def enroll_student_to_subject(stu_id,sub_id):
    data={"student_id":stu_id,"subject_id":sub_id}
    res =supabase.table("subject_students").insert(data).execute()
    return res.data


def unenroll_student_to_subject(stu_id,sub_id):
    res=supabase.table("subject_students").delete().eq("student_id",stu_id).eq("subject_id",sub_id).execute()
    return res.data

def get_student_subjects(stu_id):
    response=supabase.table("subject_students").select("*,subjects(*)").eq("student_id",stu_id).execute()
    return response.data


def get_student_attendance(stu_id):
    res=supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",stu_id).execute()
    return res.data


def enroll_student_sub(sub_id,student_id):
    data={"subject_id":sub_id,"student_id":student_id}
    res=supabase.table("subject_students").insert(data).execute()
    return res



def save_logs(logs):
    res=supabase.table("attendance_logs").insert(logs).execute()
    return res.data



def attendance_records(teach_id):
    res=supabase.table("attendance_logs").select("*,subjects!inner(*)").eq("subjects.teacher_id",teach_id).execute()
    return res.data
