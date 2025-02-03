#Overview
# PortfolioPro Backened

PortfolioPro is a **full-stack portfolio management application** that allows users to create, update, and showcase their projects while associating skills and adding bookmarks and comments.

##Author
**PortfolioPro** was created by **[Perpetual Akinyi](https://github.com/Perpe2024

## 🚀 Features
- **User Details** – Users can see their profile details.
- **Project Management** – Users can create, edit, and delete projects.
- **Skills Association** – Assign skills to projects from a dropdown list.
- **Bookmarks & Comments** – Public bookmarking and commenting system.
- **Responsive UI** – Clean and user-friendly interface built with React.

## 🛠️ Tech Stack
- **Frontend:** React, React Router, Formik
- **Styling:** CSS, Tailwind (if used later)
- **Deployment:** Vercel (Frontend) & Render (Backend)

## 📂 Project Structure
```
PortfolioPro/
│── client
│   ├── instance/
│   ├── migration/
│   ├── models.py/
│   ├── app.py
│   ├── seed.py
│── pipfilelock/
│── validations.py
│── README.md
```

## ⚡ Installation & Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-username/PortfolioPro.git
   cd PortfolioPro
   ```
2. **Install Dependencies**
   ```sh
   npm install
   ```
3. **Start the Development Server**
   ```sh
   npm start
   ```

## 🔗 Backend API Configuration
Make sure your **PortfolioPro backend** is running and update the API URLs in your frontend code.
Example API Base URL:
```sh
http://127.0.0.1:5555
```
Or with gunicorn :
```sh
http://127.0.0.1:8000
```

## 🚀 Deployment on Vercel
1. **Build the Project**
   ```sh
   npm run build
   ```
2. **Deploy with Vercel**
   - Install Vercel CLI if not installed:
     ```sh
     npm install -g vercel
     ```
   - Run the deployment command:
     ```sh
     vercel
     ```
   - Follow the instructions to complete deployment.
   - Your frontend will be live on Vercel.
   -The deployment for this application is ```sh https://portfolio-pro-frontend.vercel.app/```

## 📌 Roadmap
- [ ] Improve UI with CSS
- [ ] Add Search & Filter for Projects

## 🛠️ Contributing
Contributions are welcome! Feel free to fork the repo and submit a PR.

## 📝 License
This project is licensed under the **MIT License**.

---
### 🎯 Stay Updated
For updates and improvements, keep checking back!

🔥 Happy Coding!