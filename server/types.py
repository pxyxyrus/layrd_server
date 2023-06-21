import enum
    
class RecruitmentType(enum.Enum):
    find_mentor = 'find_mentor'
    find_mentee = 'find_mentee'
    find_team = 'find_team'

class ApplicationType(enum.Enum):
    rolling ='rolling'
    due_date = 'due_date'

class WorkLocation(enum.Enum):
    on_site = 'onsite'
    remote = 'remote'
    hybrid = 'hybrid'

class ProjectStatus(enum.Enum):
    open = 'open' # project is taking applicants
    withdrawn = 'withdrawn' # project was withdrawn
    closed = 'closed' # project is no more taking applicants()
    ongoing = 'ongoing' # staking happened
    successful = 'successful' # project successfully finished
    unsuccessful = 'unsuccessful' # project aborted by someone




class ApplicationStatus(enum.Enum):
    applied = 'applied'
    accepted = 'accepted'
    rejected = 'rejected'
    closed = 'closed'

    

