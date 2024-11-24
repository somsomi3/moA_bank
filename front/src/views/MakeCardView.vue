<template>
  <div>
    <h1>Create Your Custom Card</h1>
    <form @submit.prevent="generateCard">
      <div>
        <label for="prompt">Prompt:</label>
        <input v-model="prompt" id="prompt" placeholder="Enter prompt for the background" />
      </div>
      <div>
        <label for="text">Text:</label>
        <input v-model="text" id="text" placeholder="Enter text for the card" />
      </div>
      <div>
        <label for="font">Upload Your Font:</label>
        <input type="file" @change="handleFontUpload" accept=".ttf" />
      </div>
      <button type="submit">Generate Card</button>
    </form>

    <div v-if="generatedCard">
      <h2>Your Generated Card:</h2>
      <img :src="generatedCard" alt="Generated Card" />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      prompt: "",
      text: "",
      fontFile: null,
      generatedCard: null,
    };
  },
  methods: {
    handleFontUpload(event) {
      this.fontFile = event.target.files[0];
    },
    async generateCard() {
      if (!this.prompt || !this.text || !this.fontFile) {
        alert("Please provide a prompt, text, and upload a font file.");
        return;
      }

      try {
        const formData = new FormData();
        formData.append("prompt", this.prompt);
        formData.append("text", this.text);
        formData.append("font", this.fontFile);

        const response = await axios.post(
          "http://127.0.0.1:8000/api/v1/card-designs/generate_card/",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob", // 이미지 응답 처리
          }
        );

        this.generatedCard = URL.createObjectURL(response.data);
      } catch (error) {
        console.error("Error generating card:", error);
        alert("Failed to generate card. Please check your inputs and try again.");
      }
    },
  },
};
</script>
