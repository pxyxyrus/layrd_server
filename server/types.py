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
    applied = 'applied' # application is pending
    accepted = 'accepted' # application accepted by the project
    rejected = 'rejected' # applicant rejected the project offer
    confirmed = 'confirmed' # applicant confirmed joining the project
    withdrawn = 'withdrawn' # applicant withdrew from the project

