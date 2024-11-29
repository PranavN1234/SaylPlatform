
# Sayl 

A brief description of how to manage the application and the various parts of the application 

## Backend Management 




## API Reference

#### Get all items

```http
  POST /process-pdfs
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `files` | `files` |     send a list of files |

#### Get item

```http
  POST /chatbot/query
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `query`      | `string` | user query |
 `session_id`      | `string` | session id |


#### Setting up the backend 

1) Getting the backend on local system 

- Fork/Clone the repository 
- create a venv 
- install the packages from requirements.txt
- run python main.py 
- once changes are working follow the next section to deploy changes to the backend 

2) Backend deployment in Ec2 

- Check in to AWS Ec2 account and ssh into the server 
- Pull the new changes 
- Add the new required packages by installing the requirements.txt
- Restart the service 
- Test the new backend and see logs

3) Database changes 

- Login to GCP account where database is maintained 
- Connect the Cloud SQL database via sql workbench or some alternative 

#### Frontend Handling 

- Frontend for PDF extractor (Within the same repo /frontend)
- Frontend for chatbot in different repo 

1) Getting the Frontend on local 

- Frontend for pdf service comes with the Sayl Platform 
- Frontend for chatbot in different repo 

- run npm install to get the latest repos 
- npm start and test the changes on local 
- once ready run npm run build create latest build 
- sync the build with the aws s3 bucket 
- once build is synced, create a new invalidation in cloudfront and the changes will deploy to the main endpoint 










