<template>
  <div>
    <div class="guess-display">
      <h2>Your Guesses:</h2>
      <div v-if="highestSimilarity" class="latest-guess-container">
        <p class="latest-guess-text">
          Latest guess: {{ latestGuess }} - Similarity:
          {{ Math.floor(latestSimilarity * 1000) }}
        </p>
        <div
          class="progress-bar-container"
          v-if="Math.floor(latestSimilarity * 1000) > 599"
        >
          <div
            class="progress-bar"
            :style="{ width: getProgressBarWidth(latestSimilarity) }"
          ></div>
        </div>
      </div>
      <div v-if="isWinner && highestGuess" class="winning-word">
        <p>Congratulations, the word was {{ highestGuess.toLowerCase() }}!</p>
        <button @click="playAgain">Play Again!</button>
      </div>
    </div>

    <table>
      <thead>
        <tr class="info-row" :class="{ visible: hasGuessed }">
          <td>#</td>
          <td>Guess</td>
          <td>Similarity</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in sortedGuesses" :key="index">
          <td>{{ item.originalIndex + 1 }}.</td>
          <td>{{ item.guess.toLowerCase() }}</td>
          <td>{{ item.formattedSimilarity }}</td>

          <td>
            <div
              class="progress-far-container"
              v-if="item.formattedSimilarity <= 300"
            >
              ( Cold )
            </div>
            <div
              class="progress-far-container"
              v-if="
                item.formattedSimilarity <= 449 &&
                item.formattedSimilarity >= 301
              "
            >
              ( warm )
            </div>
            <div
              class="progress-far-container"
              v-if="
                item.formattedSimilarity <= 599 &&
                item.formattedSimilarity >= 450
              "
            >
              ( hot )
            </div>
            <div
              class="progress-bar-container"
              v-if="item.formattedSimilarity > 599"
            >
              <div
                class="progress-bar"
                :style="{ width: getProgressBarWidth(item.similarity) }"
              ></div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  guesses: Array,
  similarities: Array,
  isGameWon: Boolean,
});

// Emit event to parent to reset the game
const emit = defineEmits(["playAgain"]);

const hasGuessed = ref(false);

const highestSimilarity = computed(() => {
  return props.similarities.length ? Math.max(...props.similarities) : null;
});

const highestGuess = computed(() => {
  if (!props.similarities || props.similarities.length === 0) return null;
  const maxSimilarity = Math.max(...props.similarities);
  const index = props.similarities.indexOf(maxSimilarity);
  return index !== -1 && props.guesses && props.guesses.length > index
    ? props.guesses[index]
    : null;
});

const sortedGuesses = computed(() => {
  if (props.guesses.length > 0) {
    hasGuessed.value = true;
  }

  return props.guesses
    .map((guess, index) => ({
      guess: guess,
      similarity: props.similarities[index],
      formattedSimilarity: Math.floor(props.similarities[index] * 1000),
      originalIndex: index,
    }))
    .sort((a, b) => b.similarity - a.similarity);
});

const latestGuess = computed(() => {
  if (sortedGuesses.value.length === 0) return null;

  const latestItem = sortedGuesses.value.reduce(
    (latest, item) =>
      item.originalIndex > latest.originalIndex ? item : latest,
    sortedGuesses.value[0]
  );

  return latestItem.guess.toLowerCase();
});

const latestSimilarity = computed(() => {
  if (sortedGuesses.value.length === 0) return null;

  const latestItem = sortedGuesses.value.reduce(
    (latest, item) =>
      item.originalIndex > latest.originalIndex ? item : latest,
    sortedGuesses.value[0]
  );

  return latestItem.similarity;
});

const isWinner = computed(() => {
  return props.similarities.includes(1);
});

const playAgain = () => {
  emit("playAgain");
  hasGuessed.value = false;
};

const getProgressBarWidth = (similarity) => {
  const similarityScaled = similarity * 1000;
  if (similarityScaled < 600) return "0%";
  const widthPercentage = ((similarityScaled - 600) / 400) * 100;
  return `${widthPercentage}%`;
};
</script>

<style scoped>
.guess-display {
  margin-top: 20px;
}

td {
  padding: 10px;
}

.info-row {
  visibility: hidden;
}

.info-row.visible {
  visibility: visible;
}

.winning-word {
  color: rgb(28, 194, 28);
}

.latest-guess-container {
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 2px solid black;
  padding-bottom: 5px;
}

.latest-guess-text {
  margin: 0;
}

.progress-bar-container {
  width: 160px;
  height: 19px;
  background-color: #ddd;
  border-radius: 5px;
  overflow: hidden;
  display: inline-block;
}

.progress-bar {
  height: 100%;
  background-color: green;
  border-radius: 5px;
  transform-origin: right;
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
</style>
