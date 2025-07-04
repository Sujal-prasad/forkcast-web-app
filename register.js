
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider
} from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";


const firebaseConfig = {
  apiKey: "AIzaSyC_sQRoRrS6XYweNkyFLlegR18vGjdFlMc",
  authDomain: "forkcast-3279d.firebaseapp.com",
  projectId: "forkcast-3279d",
  storageBucket: "forkcast-3279d.firebasestorage.app",
  messagingSenderId: "1019775482409",
  appId: "1:1019775482409:web:a62f5e842aa02292287a38"
};


const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.getElementById("submit");
  const emailInput = document.querySelector('input[type="email"]');
  const passwordInput = document.querySelector('input[type="password"]');
  const googleBtn = document.querySelector('button:has(img)'); // Matches your Google button

  // ✉️ Email/Password Signup
  submitBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const email = emailInput.value;
    const password = passwordInput.value;

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      alert("Signed up successfully!");
      console.log("User:", user);
      // Optional: Redirect user
      // window.location.href = "dashboard.html";
    } catch (error) {
      console.error(error);
      alert(" Error: " + error.message);
    }
  });

  // 🔐 Google Signup
  googleBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;
      alert("✅ Signed in with Google!");
      console.log("User:", user);
      // Optional: Redirect user
      // window.location.href = "dashboard.html";
    } catch (error) {
      console.error(error);
      alert(" Google Sign-In Error: " + error.message);
    }
  });
});
