import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info() # it will gave on which line of code the error occurers and in which file 
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_msg = str(error)

    error_message = "Error  in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,line_number,error_msg)

    return error_message     

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        """
        When you add the __init__() function, the child class will no longer inherit the parent's __init__() function.

        Note: The child's __init__() function overrides the inheritance of the parent's __init__() function.

        To keep the inheritance of the parent's __init__() function, add a call to the parent's __init__() function:
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)  

    def __str__(self):
        return self.error_message    
        
# if  __name__=="__main__":

#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("EXCEPTION HANDALING!!!")
#         raise CustomException(e,sys)
