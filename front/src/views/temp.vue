<template>
    <div class="container">
      <p class="message">{{ currentMessage }}</p>
      <button v-if="!isLastMessage" @click="nextMessage" class="next-button">다음으로</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // 메시지 리스트
  const messages = [
    "안녕하세요! 저는 당신의 경제 생활 매니저 모아에요!",
    "저는 당신의 경제 생활에 대한 간단한 정보를 바탕으로, 유용한 정보를 제공해 드릴거에요!",
    "지금부터 시작해볼까요?",
    "좋아요! 당신의 이름은 무엇인가요?",
    "좋아요! 성별은요?",
    "예적금을 넣고 계신가요",
    "나이를 알려주시면 좋을 것 같아요!",
    "월소득은 얼마쯤 되세요??",
    "월소비는 얼마쯤 되세요??",
    "직업이 있으신가요??",
    
  ];
  
  // 현재 메시지 인덱스 관리
  const currentIndex = ref(0);
  
  // 현재 메시지
  const currentMessage = ref(messages[currentIndex.value]);
  
  // 마지막 메시지 여부
  const isLastMessage = ref(false);
  
  // 다음 메시지로 이동
  function nextMessage() {
    if (currentIndex.value < messages.length - 1) {
      currentIndex.value++;
      currentMessage.value = messages[currentIndex.value];
  
      // 마지막 메시지인지 확인
      if (currentIndex.value === messages.length - 1) {
        isLastMessage.value = true;
      }
    }
  }
  </script>
  
  <style scoped>
  .container {
    text-align: center;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .message {
    font-size: 18px;
    margin-bottom: 20px;
    line-height: 1.6;
  }
  
  .next-button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
  }
  
  .next-button:hover {
    background-color: #0056b3;
  }
  </style>
