<script setup>
import GuessingComp from "./components/GuessingComp.vue";
import { ref, onMounted } from "vue";
import moonIcon from "./assets/moonIcon.png";
import sunIcon from "./assets/sunIcon.png";

// Track the dark mode state
const isDarkMode = ref(false);

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark-mode");
    localStorage.setItem("darkMode", "enabled");
  } else {
    document.documentElement.classList.remove("dark-mode");
    localStorage.setItem("darkMode", "disabled");
  }
};

onMounted(() => {
  const storedPreference = localStorage.getItem("darkMode");
  if (
    storedPreference === "enabled" ||
    (!storedPreference &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    isDarkMode.value = true;
    document.documentElement.classList.add("dark-mode");
  }
});
</script>

<template>
  <div>
    <!-- Dark mode toggle button with image -->
    <button @click="toggleDarkMode" class="dark-mode-toggle">
      <img :src="isDarkMode ? sunIcon : moonIcon" alt="Toggle Dark Mode" />
    </button>

    <!-- Your guessing component -->
    <GuessingComp />
  </div>
</template>

<style>
:root {
  --bg-color: #ffffff;
  --text-color: #000000;
  --input-bg-color: #f0f0f0;
  --button-bg-color: green;
  --button-text-color: white;
}

.dark-mode {
  --bg-color: #181818;
  --text-color: #e0e0e0;
  --input-bg-color: #282828;
  --button-bg-color: #444;
  --button-text-color: white;
}

body {
  background-color: var(--bg-color);
  color: var(--text-color);
}

input {
  background-color: var(--input-bg-color);
  color: var(--text-color);
}

button {
  background-color: var(--button-bg-color);
  color: var(--button-text-color);
  font-family: cursive;
}

div {
  background-color: var(--bg-color);
  color: var(--text-color);
}

.dark-mode-toggle {
  margin: 20px;
  padding: 0; 
  background: none; 
  border: none; 
  border-radius: 50%; 
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dark-mode-toggle img {
  width: 24px; 
  height: 24px;
  display: block; 
}

.dark-mode-toggle:hover {
  opacity: 0.8;
}
</style>
