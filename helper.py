# lab2_panchiwala_smp2478
# UTA ID: 1001982478
# Name: Shivani Manojkumar Panchiwala
# Completion Date: 10/31/2021


import os
import time  # import time module

class helper:
    def human_readable_size(self,size, decimal_places=2):  # Get human readable version of file size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f}{unit}"

    def getFilesWithMetadata(self, dir_name, arr):
        d = []  # list
        for file_name in arr:
            file_path = os.path.join(dir_name, file_name)  # join the file path with directory
            timestamp_str = time.strftime('%m/%d/%Y',  # last modification date of file
                                          time.gmtime(os.path.getmtime(file_path)))

            files_with_size = (os.stat(file_path).st_size)  # Get file Size in bytes

            human_size = (self.human_readable_size(files_with_size))
            data1 = (file_name, human_size, timestamp_str,dir_name)  # Get filename, human readable size, date into data
            d.append(data1)  # append all three file into d
        return d
