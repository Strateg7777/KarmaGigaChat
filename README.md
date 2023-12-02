# Prerequisites
## Python
##### 1. (OPTIONAL) Create a python virtual environment and activate it using the following commands:
For linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
##### 2. Install the required packages using the following command:
```bash
pip install -r requirements.txt
```
## Place AUTH_DATA from credentials into a plain text file (for example, credentials.txt)

# Usage
## Run with the following command:
```bash
python main.py -i path_to_input_file -o path_to_output_file -c path_to_credentials_file
```
Where:
* path_to_input_file - path to the input file with dialogs (should include the file name and extension)
* path_to_output_file - path where excell report will be saved (should include the file name and extension)
* path_to_credentials_file - path to the file with credentials you've created on step 3 (should include the file name and extension)

Example:
```bash
python main.py -i "dialogs.txt" -o report.xlsx -c credentials.txt
```

## Dialogs file format
Dialogs file should contain at least one dialog.
Each dialog should start and end with a timestamp in the following format: `HH:MM:SS`.
Exmaple:
```
10:19:25
<Клиент>
Добрый день!
Можно заказать апельсиновый сок?
<Сотрудник>
Добрый день!
Извините, к сожалению у нас сломалась соковыжималка, поэтому апельсиновый сок сделать не сможем.
<Клиент>
Понял, ничего страшного.
Тогда сделайте мне просто латте.
<Сотрудник>
Могу вам предложить черничный латте из нашего авторского меню.
Он немного дороже обычного, но очень вкусный.
Сам его постоянно пью, вам стоит попробовать.
<Клиент>
Хорошо, давайте попробую.
<Сотрудник>
Не хотите еще дополнительно купить круассан.
Свежие, только завезли. Всегда ими завтракаю.
<Клиент>
Отлично, давайте.
10:22:08
```
