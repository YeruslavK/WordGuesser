<template>
  <div class="my-component">
    <h1>{{ title }}</h1>
    <div class="input-container">
      <input
        v-model="userInput"
        @keydown.enter="handleEnterGuess"
        placeholder="Enter a word"
        :disabled="isGameWon"
      />
    </div>
    <div class="button-container">
      <button @click="handleEnterGuess" class="enter-guess">Guess</button>
      <button @click="toggleRules" class="show-rules">?</button>
    </div>

    <div v-if="wordError" class="word-error">
      <p>Sorry, this word does not exist or contains inappropriate language.</p>
    </div>

    <!-- Game Rules Overlay -->
    <div v-if="showRules" class="rules-overlay">
      <div class="rules-content">
        <button @click="toggleRules" class="close-rules">X</button>
        <h1 class="rules-heading">Game Rules:</h1>
        <ol>
          <li>Objective: Guess the winning word by entering guesses.</li>
          <li>
            Gameplay:
            <ul>
              <li>Input: Type a word into the input field and press Enter.</li>
              <li>
                Guesses: Each guess is checked for its similarity to the winning
                word (from 0 to 1000).
              </li>
            </ul>
          </li>
          <li>
            Winning: You win if a guess matches the target word exactly or if
            the similarity score reaches 1000.
          </li>
          <li>
            Reset: After winning or choosing to play again, the game resets with
            a new random winning word.
          </li>
        </ol>
      </div>
    </div>

    <GuessDisplay
      :guesses="guesses"
      :similarities="similarities"
      @playAgain="resetGame"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { getWordSynsets, getSimilarity } from "../api";
import { commonWordsArr } from "../resources/commonWordsArr";
import GuessDisplay from "./GuessDisplay.vue";
import { Filter } from "bad-words";

const userInput = ref("");
const targetWord = ref("");
const guesses = ref([]);
const similarities = ref([]);
const title = "WordGuesser";
const wordError = ref(false);
const showRules = ref(false);
const filter = new Filter();

// Checks if the similarity equals to 1 then the game is won.
const isGameWon = computed(() => {
  return similarities.value.some((similarity) => similarity === 1);
});

// Randomises The common words array and returns a random word based on a random index of the length of the array.
const getRandomCommonWord = () => {
  const randomIndex = Math.floor(Math.random() * commonWordsArr.length);
  return commonWordsArr[randomIndex];
};

// A function to fetch the synsets (words that are similar the winning word).
const fetchSynsets = async () => {
  if (userInput.value) {
    wordError.value = false;
    // Checks if the inputed word by the user is Profane.
    if (filter.isProfane(userInput.value)) {
      wordError.value = true;
      userInput.value = "";
      return;
    }

    try {
      const response = await getWordSynsets(userInput.value);
      const synsets = response.data;

      if (synsets.length === 0) {
        wordError.value = true;
        userInput.value = "";
        return;
      }

      // If the word is not in the guesses list
      if (!guesses.value.includes(userInput.value)) {
        guesses.value.push(userInput.value);

        // Check for exact match
        if (userInput.value.toLowerCase() === targetWord.value.toLowerCase()) {
          similarities.value.push(1);
        } else {
          // If not an exact match, check the similarity score
          const simResponse = await getSimilarity(
            userInput.value,
            targetWord.value
          );
          similarities.value.push(simResponse.data.similarity);
        }
      }
    } catch (error) {
      console.error("Error fetching synsets:", error);
      wordError.value = true;
      userInput.value = "";
    }
  }
};

// Fetches a random winning word.
const fetchRandomWord = async () => {
  try {
    targetWord.value = getRandomCommonWord();
  } catch (error) {
    console.error("Error fetching random word:", error);
  }
};

// Fetches a random word right after the render happens and the DOM is constructed.
onMounted(async () => {
  await fetchRandomWord();
});

// When enter is pressed pushes the user input to the guesses array and checks for similarities adn resets the input.
const handleEnterGuess = async () => {
  if (userInput.value.toLowerCase() === targetWord.value.toLowerCase()) {
    guesses.value.push(userInput.value);
    similarities.value.push(1);
    wordError.value = false;
  } else {
    await fetchSynsets();
    userInput.value = "";
  }
};

const toggleRules = () => {
  showRules.value = !showRules.value;
};

// Resets the everything in the project to play another round.
const resetGame = async () => {
  userInput.value = "";
  guesses.value = [];
  similarities.value = [];
  wordError.value = false;
  await fetchRandomWord();
};
</script>

<style scoped>
.my-component {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: cursive;
}

.input-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
}

input {
  height: 60px;
  font-size: 24px;
  padding: 0 15px;
  text-align: center;
  border: 2px solid #ccc;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  box-sizing: border-box;
  border: 2px solid #ccc;
  transition: border-color 0.3s;
}

input:focus {
  border-color: var(--primary-color);
  outline: none;
}

.enter-guess,
.show-rules {
  background-color: green;
  color: white;
  font-size: 24px;
  cursor: pointer;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
}
input::placeholder {
  font-size: 24px;
  color: #aaa;
}

.show-rules {
  background-color: green;
  color: white;
  font-size: 24px;
  cursor: pointer;
  border: none;
  border-radius: 8px;
}

.enter-guess {
  background-color: green;
  color: white;
  font-size: 24px;
  cursor: pointer;
  border: none;
  border-radius: 8px;
}

.word-error {
  color: red;
}

.rules-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.5s;
}

.dark-mode .rules-content {
  background-color: #333;
  color: #e0e0e0;
}

.rules-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  color: black;
}

button {
  background-color: green;
  color: white;
  padding: 5px 15px;
  font-size: 17px;
  font-family: cursive;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 20px;
}

button:hover {
  background-color: darkgreen;
}

button:focus {
  outline: none;
}

button:disabled {
  background-color: gray;
  cursor: not-allowed;
}

.close-rules {
  cursor: pointer;
  transition: color 0.3s ease;
  float: right;
}

@media (max-width: 600px) {
  input {
    width: 90%;
  }

  .button-container {
    flex-direction: column;
  }

  .enter-guess,
  .show-rules {
    width: 100%;
    margin: 5px 0;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
