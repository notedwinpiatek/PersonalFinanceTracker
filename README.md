# 💸 PersonalFinanceTracker — Find The Right Balance In Your Wallet

## 🚀 Overview
**Personal Finance Tracker** is a clean, no-nonsense Django web app that helps you actually understand where your money goes.  
Track **income**, **expenses**, and **balances** over time, visualize everything with charts, and keep your finances crystal clear — without spreadsheets from hell.

Built with simplicity in mind, so you spend less time managing money and more time… spending it wisely 😄

---

## ✨ Features
📈 **Income History** — full breakdown of all your income sources  
📉 **Expenses History** — detailed view of where your money disappears  
🏦 **Available Balance** — always know how much you really have  
📊 **Income Sources Chart** — visualize where your income comes from  
🥧 **Spending Categories** — pie chart of expenses by category  
🧾 **Transaction History** — incomes & expenses in one unified timeline  
📅 **Monthly Tracking** — compare income vs expenses month by month  
💱 **Currency Support** — not using USD? Switch currencies directly in the dashboard  

---

### 📊 Dashboard
![Dashboard](https://github.com/notedwinpiatek/PersonalFinanceTracker/blob/main/personal_finance_tracker/finance_tracker/static/finance_tracker/img/dashboard.png?raw=true)

### 💰 Income History
![Income History](https://github.com/notedwinpiatek/PersonalFinanceTracker/blob/main/personal_finance_tracker/finance_tracker/static/finance_tracker/img/income.png?raw=true)


## 🛠️ Tech Stack
<div align="center">

### 🔙 Backend
<img alt="Django" width="30px" padding-right="30" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" />
<img alt="Python" width="30px" padding-right="30" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" />
<img alt="SQLite" width="30px" padding-right="30" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" />
<br/>

### 🎨 Frontend
<img alt="HTML5" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" />
<img alt="CSS3" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" />
<img alt="JavaScript" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" />
<img alt="Chart.js" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/chartjs/chartjs-original.svg" />
<br/>

### 🎯 Design
<img alt="Figma" width="30px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg" />
</div>
<br/>

<p align="center">
📋 <a href="https://www.figma.com/design/kkRzWpZRrwnIHWqvR449Q4/Personal-Finance-Tracker?node-id=0-1&p=f"><b>View Design on Figma</b></a>
</p>

## 👥 Contributors
<p align="center">
  <a href="https://github.com/notedwinpiatek">
    <img src="https://github.com/notedwinpiatek.png" width="80" style="border-radius:50%; margin-right:8px;" />
  </a>
  <a href="https://github.com/JuliaMaxx">
    <img src="https://github.com/JuliaMaxx.png" width="80" style="border-radius:50%; margin-right:8px;" />
  </a>
</p>

---

## ⚙️ Getting Started

1. Clone the repository:
   ```sh
   git clone https://github.com/JuliaMaxx/PersonalFinanceTracker.git
2. Navigate to the project directory:
    ```sh
    cd personal_finance_tracker
    ```
3. Create virtual enviroment:
    ```sh
    python -m venv .venv
    ```
4. Run virtual enviroment: 
    #### Windows
    ```sh
    source .venv/Scripts/activate
    ```
    #### Mac/Linux
    ```sh
    source .venv/bin/activate
    ```
5. Install requirements:
    ```sh
    pip install -r requirements.txt
    ```
6. Make migrations:
    ```sh
    python manage.py migrate
    ```
7. Run the application:
    ```sh
    python manage.py runserver --insecure
    ```