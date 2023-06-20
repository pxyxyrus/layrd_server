import enum
    
class RecruitmentType(enum.Enum):
    find_mentor=1
    find_mentee=2
    find_team=3

class ApplicationType(enum.Enum):
    rolling=1
    due_date=2

class WorkLocation(enum.Enum):
    on_site = 1
    remote = 2
    hybrid = 3

class ProjectStatus(enum.Enum):
    open = 1 # project is taking applicants
    withdrawn = 2 # project was withdrawn
    closed = 3 # project is no more taking applicants()
    ongoing = 4 # staking happened
    successful = 5 # project successfully finished
    unsuccessful = 6 # project aborted by someone




class ApplicationStatus(enum.Enum):
    applied = 1
    accepted = 2
    rejected = 3
    closed = 4

    

