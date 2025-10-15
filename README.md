<div align="center">

# 📚 MyBuddy – AI Study Companion

<img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
<img src="https://img.shields.io/badge/Streamlit-1.40.0-FF4B4B.svg" alt="Streamlit">
<img src="https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4.svg" alt="Gemini">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">

**Transform the way you study with AI-powered learning tools.**  
*Learning isn’t about working harder — it’s about working smarter.*

</div>

---

## 🎯 What is MyBuddy?

**MyBuddy** is your all-in-one, AI-powered study companion built to help you **learn faster, understand deeper, and remember longer**.  
It’s powered by **Google’s Gemini 2.5 Flash** — delivering lightning-fast intelligence packed into a sleek, zero-friction experience.

<div align="center">

### ⚡ Lightning Fast • 🎯 Personalized • 🎓 Study Anywhere • 🔓 Zero Friction

</div>

MyBuddy isn’t just another study tool — it’s your **personal tutor, note taker, quiz master, and memory coach**, all rolled into one.  
Whether you’re breaking down complex concepts, summarizing long notes, or testing your knowledge, MyBuddy has your back.

---
---

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🎓 **Explain Concepts**  
Break down complex topics into crystal-clear understanding.

- 🔹 Adaptive difficulty: *Basic → Intermediate → Advanced*  
- 🔹 Structured explanations with real-world examples  
- 🔹 Download explanations for offline study  
- 🔹 Perfect for understanding new subjects quickly  

</td>
<td width="50%" valign="top">

### ⚡ **Summarize Smart**  
Turn hours of reading into minutes of clarity.

- 🔹 Upload PDFs or paste any text  
- 🔹 Instantly extract key insights  
- 🔹 Adjustable summary length  
- 🔹 Save time without losing context  

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🎯 **Test Yourself**  
Transform learning into mastery through active testing.

- 🔹 AI-generated multiple-choice quizzes  
- 🔹 Instant feedback with detailed reasoning  
- 🔹 Track your performance and progress  
- 🔹 Choose quiz difficulty and length  

</td>
<td width="50%" valign="top">

### 🧠 **Remember Forever**  
Train your brain with AI-generated flashcards.

- 🔹 Smart flashcards based on active recall  
- 🔹 Self-paced review system  
- 🔹 Boost memory retention by up to 200%  
- 🔹 Perfect for exam prep and long-term learning  

</td>
</tr>
</table>

---
---

## 🚀 Quick Start

### 🧩 Prerequisites

Before you begin, make sure you have:

- 🐍 **Python 3.9+** installed  
- 🔑 A **Google Gemini API key** — [Get yours free](https://aistudio.google.com/apikey)  

---

### ⚙️ Installation


# 1️⃣ Clone the repository
```bash
git clone https://github.com/lalith-thexplorer/MyBuddy.git
cd MyBuddy
```

# 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

# 3️⃣ Add your API key
```bash
# Create .streamlit/secrets.toml and paste:
GOOGLE_API_KEY = "your-api-key-here"
```

# 4️⃣ Run the app
```bash
streamlit run app.py
```
### 🌐 Access the App

After running the command below 👇  
```bash
streamlit run app.py
```

---

## 📁 Project Structure

Here’s the organized structure of **MyBuddy**:
```
MyBuddy/
├── .streamlit/
│ ├── config.toml # App theme and layout configuration
│ └── secrets.toml # API keys (Keep this private!)
│
├── app.py # Main Streamlit application & navigation
├── utils.py # Helper functions and API utilities
│
├── explain_tab.py # "Explain Concepts" feature
├── summarize_tab.py # "Summarize Notes" feature
├── quiz_tab.py # "Test Yourself" quizzes feature
├── flashcard_tab.py # "Remember Forever" flashcards feature
│
├── requirements.txt # Python dependencies
├── README.md # Project documentation (this file)
└── .gitignore # Files and folders to ignore in Git
```
---

## 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|:----------:|:-------:|
| 🐍 **Python 3.9+** | Backend programming language |
| 🎈 **Streamlit** | Interactive web app framework |
| 🤖 **Google Gemini 2.5 Flash** | AI content generation for explanations, summaries, quizzes, flashcards |
| 📄 **pdfplumber** | Extract text from PDFs for summarization |
| 🌐 **Requests** | Make HTTP calls to APIs |

</div>

---
---

## 📖 How to Use

### 1️⃣ Explain a Topic
- Navigate to **🎓 Explain Concepts**  
- Enter your topic (e.g., *Quantum Entanglement*)  
- Select difficulty: Basic | Intermediate | Advanced  
- Click **✨ Generate Explanation**  
- Download or review your structured explanation  

---

### 2️⃣ Summarize Notes
- Go to **⚡ Summarize Smart**  
- Upload a PDF or paste text  
- Choose the desired summary length  
- Get key insights instantly  

---

### 3️⃣ Take a Quiz
- Open **🎯 Test Yourself**  
- Enter your topic and select difficulty  
- Answer AI-generated multiple-choice questions  
- Receive instant feedback with explanations  

---

### 4️⃣ Create Flashcards
- Open **🧠 Remember Forever**  
- Enter your topic or notes  
- Generate interactive flashcards  
- Review regularly to boost memory retention  

---
---

## 🌟 Why MyBuddy?

<div align="center">

| Feature | Benefit |
|---------|---------|
| ⚡ **Lightning Fast** | Instant AI-powered responses using Gemini 2.5 Flash |
| 🎯 **Personalized** | Adapts to your learning level and difficulty |
| 🎓 **Study Anywhere** | Mobile-friendly and responsive design |
| 🔓 **Zero Friction** | No login required — start learning immediately |
| 💯 **Free Forever** | Fully open-source, no hidden costs or paywalls |

</div>

---
---

## 🚢 Deployment

### Deploy to Streamlit Cloud (Free & Easy)

1. **Push your code to GitHub** ✅  
2. Go to [share.streamlit.io](https://share.streamlit.io)  
3. Click **"New app"**  
4. Select your GitHub repository: `lalith-thexplorer/MyBuddy`  
5. Set the main file path to: `app.py`  
6. Add your secrets in **Advanced settings**:
- GOOGLE_API_KEY = "your-api-key-here"
7. Click **Deploy!** 🚀  
Your app will be live at: `https://your-app-name.streamlit.app`  
*Now anyone can access your AI study companion online!*  
---
---

## 🤝 Contributing

Contributions make the open-source community amazing! Any help you provide is **greatly appreciated**.  

### How to Contribute

1. **Fork the project**  
2. **Create your feature branch**  
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes
```bash
git commit -m "Add some AmazingFeature"
```
4. Push Your Branch
```bash
git push origin feature/AmazingFeature
```
5. Open a pull Request on the original repository 
Thank you for making MyBuddy even better!

---

## 📝 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

---

## 👨‍💻 Author

<div align="center">

**Lalith - The Explorer**

[![GitHub](https://img.shields.io/badge/GitHub-lalith--thexplorer-181717?style=for-the-badge&logo=github)](https://github.com/lalith-thexplorer)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/yourprofile)

*Made with ❤️ for students who want to learn better*

</div>

---

## 💡 Pro Tips

- **Best Results**: Be specific with your topics  
- **Explain Feature**: Start with "Basic" if new to a concept  
- **Summarize**: Works best with structured text (PDFs, articles)  
- **Quiz**: Use "Intermediate" for most exam prep  
- **Flashcards**: Review regularly for best retention  

---

## 📞 Support

Having issues or suggestions? Reach out:  

- 🐛 [Report Bug](https://github.com/lalith-thexplorer/MyBuddy/issues)  
- ✨ [Request Feature](https://github.com/lalith-thexplorer/MyBuddy/issues)  
- 💬 [Ask Question](https://github.com/lalith-thexplorer/MyBuddy/discussions)  

---

<div align="center">

### ⭐ Star this repo if MyBuddy helped you study smarter!

**Happy Learning! 📚✨**  

*"The beautiful thing about learning is that no one can take it away from you."*  

**MyBuddy** © 2025 • Made with 💛 by [Lalith](https://github.com/lalith-thexplorer)

</div>


