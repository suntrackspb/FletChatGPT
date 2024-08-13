# Flet Kandinsky and ChatGpt PWA

### Click here to [live demo](https://den.sntrk.ru/home)

You can specify all the settings yourself in .env or fill them out in the application settings as a client. The client settings override the server settings for the client.


## Run local
1. ```shell 
   git clone https://github.com/suntrackspb/FletChatGPT.git
   ```
2. ```shell 
   cd FletChatGPT
   ```
3. ```shell 
   source venv\bin\activate
   ```
4. ```shell 
   pip install -r requirements.txt
   ```
5. ```shell 
   python main.py
   ```
6. Open http://your_ip:8009

## Run in docker

1. Clone repository
2. ```shell
   cd FletChatGPT
   ```

3. ```shell
   docker compose up -d
   ```
4. Open http://your_ip:8009