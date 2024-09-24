import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

export const getWordSynsets = (word) => {
  return axios.get(`${API_BASE_URL}/word/${word}`);
};

export const getSimilarity = (word1, word2) => {
  return axios.get(`${API_BASE_URL}/similarity/${word1}/${word2}`);
};
