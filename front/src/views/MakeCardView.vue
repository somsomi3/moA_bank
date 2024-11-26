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
      prompt: "", // 사용자 입력 프롬프트
      text: "", // 사용자 입력 카드 텍스트
      fontFile: null, // 업로드된 폰트 파일
      generatedCard: null, // 생성된 카드 이미지 URL
    };
  },
  methods: {
    // 폰트 파일 업로드 처리
    handleFontUpload(event) {
      this.fontFile = event.target.files[0];
    },
    // 카드 생성 API 호출
    async generateCard() {
      if (!this.prompt || !this.text || !this.fontFile) {
        alert("Please provide a prompt, text, and upload a font file.");
        return;
      }

      try {
        // FormData 생성 및 데이터 추가
        const formData = new FormData();
        formData.append("prompt", this.prompt);
        formData.append("text", this.text);
        formData.append("font", this.fontFile);
        console.log(this.text, '123')
        // API 요청
        const response = await axios.post(
          "http://127.0.0.1:8000/api/v1/card-designs/generate_card/",
          formData,
          {
            // headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob", // 이미지 데이터 처리
          }
        );

        // Blob URL 생성 및 저장
        this.generatedCard = URL.createObjectURL(response.data);
      } catch (error) {
        console.error("Error generating card:", error);
        alert("Failed to generate card. Please check your inputs and try again.");
      }
    },
  },
};
</script>

<style>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}
label {
  font-weight: bold;
}
input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
img {
  margin-top: 20px;
  max-width: 100%;
  height: auto;
  border: 2px solid #ccc;
  border-radius: 10px;
}
</style>
