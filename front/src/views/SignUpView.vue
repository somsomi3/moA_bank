<template>
  <div>
    <h1>Sign Up Page</h1>
    <form @submit.prevent="signUp">
      <label for="username">username : </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="name">username : </label>
      <input type="text" id="name" v-model.trim="name"><br>

      <label for="password1">password : </label>
      <input type="password" id="password1" v-model.trim="password1"><br>

      <label for="password2">password confirmation : </label>
      <input type="password" id="password2" v-model.trim="password2">

      <label for="age">age : </label>
      <input type="number" id="age" v-model.trim="age">

      <label for="income">income : </label>
      <input type="number" id="income" v-model.trim="income">

      <label for="job">job : </label>
      <input type="text" id="job" v-model.trim="job">

      <label for="gender">gender : </label>
      <input type="text" id="gender" v-model.trim="gender">

      <label for="grade">grade : </label>
      <input type="text" id="grade" v-model.trim="grade">

      <label for="main_bank">main_bank : </label>
      <input type="text" id="main_bank" v-model.trim="main_bank">
      
      <label for="region">region : </label>
      <input type="text" id="region" v-model.trim="region">

      <label for="consume">consume : </label>
      <input type="number" id="consume" v-model.trim="consume">

      <label for="desire_period">desire_period : </label>
      <input type="number" id="desire_period" v-model.trim="desire_period">

      <label for="financial_product">financial_product : </label>
      <input type="text" id="financial_product" v-model.trim="financial_product">
      
      <input type="submit" value="SignUp">
    </form>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import { useCounterStore } from '@/stores/counter';

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const age = ref(0)
const income = ref(0)
const job = ref(null)
const gender = ref(null)
const grade = ref(null)
const main_bank = ref(null)
const region = ref(null)
const consume = ref(0)
const desire_period = ref(0)
const financial_product = ref(0)
const name = ref(null)

const store = useCounterStore()

const signUp = function () {
  const payload = {
    username : username.value,
    password1 : password1.value,
    password2 : password2.value,
    age: age.value,
    income : income.value,
    job : job.value,
    gender: gender.value,
    grade : grade.value,
    main_bank : main_bank.value,
    region : region.value,
    consume : consume.value,
    desire_period : desire_period.value,
    financial_product : financial_product.value,
    name : name.value
  }
  store.signUp(payload)
}

</script>

<style scoped>

</style>