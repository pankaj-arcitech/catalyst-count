import csv
import time
import pandas as pd
from celery import shared_task
from myapp.models import CatalystCount, UploadedFile
from myapp.ws_client import send_message_view

@shared_task
def test_task(client_id):
    time.sleep(2)
    send_message_view(client_id,"this is msg")
    time.sleep(2)

# @shared_task
# def load_my_file(file_id, client_id):
#     new_catalyst = UploadedFile.objects.get(id=file_id)
#     dataset = new_catalyst.file.read().decode('utf-8').splitlines()
#     print("load start")
#     reader = csv.DictReader(dataset)
#     rows = list(reader)  # Convert the reader to a list to count the rows
#     total_size = len(rows)
    
#     # Calculate the chunk size
#     chunk_size = total_size // 100 if total_size > 100 else 1  # Maximum of 100 chunks

#     completed_chunks = 0
    
#     # Process the list in chunks
#     print("loop near start")
#     for i in range(0, total_size, chunk_size):
#         # Get the current chunk of data
#         chunk = rows[i:i + chunk_size]
        
#         # Update or create records for each row in the current chunk
#         try:
#             df = pd.DataFrame(chunk)
#             df.drop('', axis=1, inplace=True)
#             df.rename(columns={
#                                 'name':'name',
#                                 'domain': 'domain',
#                                 'year founded': 'year_founded',
#                                 'industry': 'industry',
#                                 'locality': 'locality',
#                                 'country': 'country',
#                                 'linkedin url': 'linkedin_url',
#                                 'current employee estimate': 'employees_from',
#                                 'total employee estimate': 'employees_to',
#                                 }, inplace=True)
#             df = df[["name", "domain", "year_founded", "industry", "locality", "country", "linkedin_url", "employees_from", "employees_to"]]
#             df.drop_duplicates(keep='first')
#             data_final = df.to_dict('records')
#             data_objs = [CatalystCount(**x) for x in data_final]
#             CatalystCount.objects.bulk_create(data_objs)
#         except Exception as ex:
#             print("oo")

#         completed_chunks += len(chunk)
        
#         # Calculate and print completion percentage
#         percentage = (completed_chunks / total_size) * 100
#         print(f"Loading... {percentage:.2f}% completed")
#         send_message_view(client_id, percentage)  
#         if new_catalyst.file:
#            new_catalyst.file.delete(save=False)
#         new_catalyst.delete()

@shared_task
def load_my_file(file_id, client_id):
    new_catalyst = UploadedFile.objects.get(id=file_id)
    file_size_bytes = new_catalyst.file.size

    # Calculate the chunk size (1% of the file size)
    chunk_size = file_size_bytes // 100  # Floor division to get integer chunk size

    # Open the file and read it in chunks
    with new_catalyst.file.open('rb') as file:
        completed_chunks = 0
        
        while completed_chunks < 100:
            # Read the next chunk of the file
            chunk = file.read(chunk_size)
            if not chunk:
                break  # Stop if no more data to read

            dataset = chunk.decode('utf-8').splitlines()
            
            # Process the chunk (example: print chunk size or perform some operation)
            print(f"Chunk {completed_chunks + 1}: Size {len(chunk)} bytes")
            print("load start")
            reader = csv.DictReader(dataset)
            rows = list(reader)  # Convert the reader to a list to count the rows
            total_size = len(rows)
            
            # Calculate the chunk size
            sm_chunk_size = total_size // 100 if total_size > 100 else 1  # Maximum of 100 chunks

            sm_completed_chunks = 0
            
            # Process the list in chunks
            print("loop near start")
            for i in range(0, total_size, sm_chunk_size):
                # Get the current chunk of data
                sm_chunk = rows[i:i + sm_chunk_size]
                
                # Update or create records for each row in the current chunk
                try:
                    df = pd.DataFrame(sm_chunk)
                    # df.drop('', axis=1, inplace=True)
                    df.rename(columns={
                                        'name':'name',
                                        'domain': 'domain',
                                        'year founded': 'year_founded',
                                        'industry': 'industry',
                                        'locality': 'locality',
                                        'country': 'country',
                                        'linkedin url': 'linkedin_url',
                                        'current employee estimate': 'employees_from',
                                        'total employee estimate': 'employees_to',
                                        }, inplace=True)
                    df = df[["name", "domain", "year_founded", "industry", "locality", "country", "linkedin_url", "employees_from", "employees_to"]]
                    df.drop_duplicates(keep='first')
                    data_final = df.to_dict('records')
                    data_objs = [CatalystCount(**x) for x in data_final]
                    CatalystCount.objects.bulk_create(data_objs)
                except Exception as ex:
                    print("ex: ", ex)
                    # break
                    # return

                sm_completed_chunks += len(sm_chunk)

            completed_chunks += 1
        
            # Calculate and print completion percentage
            percentage = (completed_chunks / 100) * 100
            send_message_view(client_id, percentage)  
        
    if new_catalyst.file:
        new_catalyst.file.delete(save=False)
    new_catalyst.delete()