class EncounteredCaptchaError(RuntimeError):

    def __init__(self, message:str):
        super().__init__(message)

class NoInputError(Exception):

    def __init__(self, method = 'search'):
        if method  == 'search':
            message = 'There Was No Search Term Please Enter One'

        elif method == 'account':
            message  ='There Was No Accounts list Provided To Scrape'

        elif method == 'email':
            message  = 'There Was No Email Provided Please Enter One'

        elif method  == 'password':
            message  = 'There Was No Password Provided Please Enter One'

        elif method == 'url':
            message = 'There Was No URL Provived Please Enter One'
            
        elif method == 'file_name':
            message = 'There Was No File Name Provived Please Enter One'

        elif method == 'folder_name':
            message = 'There Was No Folder Name Provived Please Enter One'

        super().__init__(message)



class AccountInvalidError(Exception):

    def __init__(self, account):
        message = 'Account {} is Invalid please Enter Unique Author Name'.format(account)
        super().__init__(message)

class AccountsNotListError(Exception):
    def __init__(self):
        message  = 'Accounts Must Be A List'
        super().__init__(message)

class UrlNotDictError(Exception):
    def __init__(self):
        message  = 'Account URLS Must Be A Dictionary'
        super().__init__(message)

class AccountDictEmptyError(Exception):
    def __init__(self):
        message  = 'Account Dictionary Is Empty'
        super().__init__(message)

class EmailNotStringError(Exception):
    def __init__(self):
        message  = 'Email Must Be A String'
        super().__init__(message)
  
class PasswordNotStringError(Exception):
    def __init__(self):
        message  = 'Password Must Be A String'
        super().__init__(message)

class SearchTermNotStringError(Exception):
    def __init__(self):
        message  = 'Search Term Must Be A String'
        super().__init__(message)

class LoginInvalidError(Exception):
    def __init__(self, message:str):
       
        super().__init__(message)

