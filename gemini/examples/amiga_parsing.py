from gemini.api.parsers.amiga import AMIGAPhoneParser
import os


parser = AMIGAPhoneParser()
working_directory = '/mnt/d/Work/Data/'
os.chdir(working_directory)
data_directory = './Dataset_2024/Davis/2024-06-12/Amiga_Phone/Phone'
parser.parse(data_directory)


