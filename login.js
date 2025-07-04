// login.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyC_sQRoRrS6XYweNkyFLlegR18vGjdFlMc",
  authDomain: "forkcast-3279d.firebaseapp.com",
  projectId: "forkcast-3279d",
  storageBucket: "forkcast-3279d.firebasestorage.app",
  messagingSenderId: "1019775482409",
  appId: "1:1019775482409:web:a62f5e842aa02292287a38"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.getElementById("login-btn");
  const emailInput = document.getElementById("email-login");
  const passwordInput = document.getElementById("password-login");

  loginBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!email || !password) {
      alert("Please enter both email and password.");
      return;
    }

    try {
      await signInWithEmailAndPassword(auth, email, password);
      // ✅ Simple redirection to home.html
      window.location.href = "home.html";
    } catch (error) {
      alert("Login failed: " + error.message);
      console.error(error);
    }
  });
});
