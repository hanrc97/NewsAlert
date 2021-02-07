# NewsAlert
An python script for CUGB's News Alert  
中国地质大学（北京）研院和二级学院的重要新闻及通知的及时获取脚本  

## UPDATES
### **2021/02/07 - Newly launched**  
- Newly launched  
## REQUIREMENTS
pip install -r requirements.txt
## USER MANNUL (Updated on 2021/02/07)
### Modify
>iMessage.py:  
>>  
>>line 10:  ```"from": "from_which@gmail.com",```  
>>line 11:  ```"to": "to_which@gmail.com",```  
>>line 12:  ```"hostname": "smtp.gmail.com",```  
>>line 13:  ```"username": "from_which@gmail.com",```  
>>line 14:  ```"password": "from_which_password",```  
>>**For example:  
>>"from": "from_francis@gmail.com",  
>>"to": "to_han@gmail.com",  
>>"to": "to_han@gmail.com",  
>>"hostname": "smtp.gmail.com",  
>>"username": "from_francis@gmail.com",  
>>"password": "123456",**  
>>  
### Run
Linux:  ```(sudo) nohup python3 -u CUGBgraNewsAlert.py > /usr/local/src/NewsCrawl/log/CUGBgraout.log 2>&1 &```  